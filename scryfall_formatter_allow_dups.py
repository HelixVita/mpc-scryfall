import scrython
import imageio
import requests
import time
import config
import numpy as np
import os
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from skimage.transform import resize
from skimage.filters import unsharp_mask


def process_card_dups(cardname, cardnumber, expansion=None, advanced=None, holo=None, copyright=None, dups=None):
	time.sleep(0.05)

	# try/except in case the search doesn't return anything
	try:
		# If the card specifies which set to retrieve the scan from, do that
		if advanced:
			# advanced specified from advanced formatter
			query = "cn:" + cardnumber + " set:" + expansion + " " + advanced
			print("Processing: " + cardname + ", set: " + expansion + ", advanced: " + advanced)        
		elif expansion:
			# Set specified from set formatter
			query = "!\"" + cardname + "\" set:" + expansion
			print("Processing: " + cardname + ", set: " + expansion)
		else:
			query = "!\"" + cardname + "\""
			print("Processing: " + cardname)
		card = scrython.cards.Search(q=query).data()[0]

	except scrython.foundation.ScryfallError:
		print("Couldn't find card: " + cardname)
		return

	# Handle cards with multiple faces
	collectornumber = card["collector_number"]
	if card["layout"] == "transform":
		cards = [x for x in card["card_faces"]]
	elif card["layout"] == "modal_dfc":
		cards = [x for x in card["card_faces"]]
	elif card["layout"] == "double_faced_token":
		cards = [x for x in card["card_faces"]]
	else:
		cards = [card, ]

	for card_obj in cards:
		name = card_obj["name"].replace("//", "&")  # should work on macOS & windows now
		name = name.replace(":", "")  # case for Circle of Protection: X
		name = name.replace("?", "")
		name = name.replace("\"", "")

		if expansion is None:
			expansion = card_obj["set"]

		# Process with waifu2x
		r = requests.post(
			"https://api.deepai.org/api/waifu2x",
			data={
				'image': card_obj["image_uris"]["large"],
			},
			headers={'api-key': config.TOKEN}
		)
		output_url = r.json()['output_url']
		im = imageio.imread(output_url)

		# Read in filter image
		filterimage = np.copy(imageio.imread("./filterimagenew.png"))

		# Resize filter to shape of input image
		filterimage = resize(filterimage, [im.shape[0], im.shape[1]], anti_aliasing=True, mode="edge")

		# Initialise arrays
		im_filtered = np.zeros(im.shape, dtype=np.complex_)
		im_recon = np.zeros(im.shape, dtype=np.float_)

		# Apply filter to each RGB channel individually
		for i in range(0, 3):
			im_filtered[:, :, i] = np.multiply(fftshift(fft2(im[:, :, i])), filterimage)
			im_recon[:, :, i] = ifft2(ifftshift(im_filtered[:, :, i])).real

		# Scale between 0 and 255 for uint8
		minval = np.min(im_recon)
		maxval = np.max(im_recon)
		im_recon_sc = (255 * ((im_recon - minval) / (maxval - minval))).astype(np.uint8)

		# TODO: pre-m15, post-8ed cards
		# TODO: pre-8ed cards (?)

		# Borderify image
		pad = 57  # Pad image by 1/8th of inch on each edge
		bordertol = 16  # Overfill onto existing border by 16px to remove white corners
		im_padded = np.zeros([im.shape[0] + 2 * pad, im.shape[1] + 2 * pad, 3])

		# Set border colour depending on set
		if card["border_color"] == "black":
			bordercolour = [0,0,0]
		elif card["border_color"] == "white":
			bordercolour = [255,255,255]
		else:
			bordercolour = [0,0,0]
	
		# Pad image
		for i in range(0, 3):
			im_padded[pad:im.shape[0] + pad, pad:im.shape[1] + pad, i] = im_recon_sc[:, :, i]

		# Overfill onto existing border to remove white corners
		# Left
		im_padded[0:im_padded.shape[0],
				  0:pad + bordertol, :] = bordercolour

		# Right
		im_padded[0:im_padded.shape[0],
				  im_padded.shape[1] - (pad + bordertol):im_padded.shape[1], :] = bordercolour

		# Top
		im_padded[0:pad + bordertol,
				  0:im_padded.shape[1], :] = bordercolour

		# Bottom
		im_padded[im_padded.shape[0] - (pad + bordertol):im_padded.shape[0],
				  0:im_padded.shape[1], :] = bordercolour

		# Remove copyright line
		if copyright:
			if card["frame"] == "2015":
				# Modern frame
				leftPix = 735
				rightPix = 1140
				topPix = 1550
				bottomPix = 1585

				# story spotlights have a shifted legal line
				try:
					if card_obj["story_spotlight"] is True:
						topPix = 1585
						bottomPix = 1625
						# spotlight card
				except KeyError:
					pass

				# creatures have a shifted legal line
				try:
					power = card_obj["power"]
					toughness = card_obj["toughness"]
					topPix = 1575
					bottomPix = 1615
					# Creature card
				except KeyError:
					pass

				# planeswalkers have a shifted legal line too
				try:
					loyalty = card_obj["loyalty"]
					topPix = 1575
					bottomPix = 1615
				except KeyError:
					pass

				im_padded[topPix:bottomPix, leftPix:rightPix, :] = bordercolour

			elif card["frame"] == "2003":
				# 8ED frame
				try:
					loyalty = card_obj["loyalty"]
					leftPix = 300
					rightPix = 960
					topPix = 1570
					bottomPix = 1600
					im_padded[topPix:bottomPix, leftPix:rightPix, :] = bordercolour
				except KeyError:
					# TODO: Content aware fill?
					pass

		# Remove holostamp
		if holo:
			if card["frame"] == "2015" and (card["rarity"] == "rare" or card["rarity"] == "mythic") \
					and "/large/front/" in card_obj["image_uris"]["large"]:
				# Need to remove holostamp
				# Define bounds of ellipse to fill with border colour
				leftE = 575
				rightE = 690
				topE = 1520
				bottomE = 1575

				cx = (leftE + rightE) / 2
				cy = (topE + bottomE) / 2

				h = (bottomE - topE) / 2
				w = (rightE - leftE) / 2

				for x in range(leftE, rightE + 1):
					for y in range(topE, bottomE + 1):
						# determine if point is in the holostamp area
						if pow(x - cx, 2) / pow(w, 2) + pow(y - cy, 2) / pow(h, 2) <= 1:
							# point is inside ellipse
							im_padded[y, x, :] = bordercolour

		im_sharp = unsharp_mask(im_padded.astype(np.uint8), radius=3, amount=0.3)
		im_sharp = im_sharp * 255
		
		# Write image to disk
		if expansion:
			try:
				os.mkdir("./formatted/" + expansion)
				if os.path.isfile("./formatted/" + expansion + "/" + name + ".png"):
					imageio.imwrite("formatted/" + expansion + "/" + name + " - " + collectornumber + ".png", im_sharp.astype(np.uint8))
				else:
					imageio.imwrite("formatted/" + expansion + "/" + name + ".png", im_sharp.astype(np.uint8))
			except FileExistsError:
				if os.path.isfile("./formatted/" + expansion + "/" + name + ".png"):
					imageio.imwrite("formatted/" + expansion + "/" + name + " - " + collectornumber + ".png", im_sharp.astype(np.uint8))
				else:
					imageio.imwrite("formatted/" + expansion + "/" + name + ".png", im_sharp.astype(np.uint8))
		else:
			imageio.imwrite("formatted/" + name + " - " + collectornumber + ".png", im_sharp.astype(np.uint8))


if __name__ == "__main__":
	# Loop through each card in cards.txt and scan em all
	with open('cards.txt', 'r') as fp:
		for cardname in fp:
			cardname = cardname.rstrip()
			cardname = cardname.replace("\"", "")
			try:
				pipe_idx = cardname.index("|")
				process_card_dups(cardname[0:pipe_idx], "", cardname[pipe_idx+1:],"","yes","yes")
			except ValueError:
				process_card_dups(cardname)
