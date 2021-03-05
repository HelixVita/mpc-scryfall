import scrython
import requests
import time
import pathlib
import os
import urllib.request

def process_card(cardname, expansion=None):
	time.sleep(0.05)
	path = pathlib.Path(__file__).parent.absolute()

	# try/except in case the search doesn't return anything
	try:
		# If the card specifies which set to retrieve the scan from, do that
		if expansion:
			# Set specified from set formatter
			query = "!\"" + cardname + "\" set=" + expansion
			print("Processing: " + cardname + ", set: " + expansion)
		else:
			query = "!\"" + cardname + "\""
			print("Processing: " + cardname)
		card = scrython.cards.Search(q=query).data()[0]

	except scrython.foundation.ScryfallError:
		print("Couldn't find card: " + cardname)
		return

	# Handle cards with multiple faces
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
		image_url = card_obj["image_uris"]["art_crop"]
		artist = card_obj["artist"]
		fullpath = os.path.join(path, "artcrop\\" + expansion + "\\" + name + " (" + artist + ").png")
		try:
			os.mkdir("./artcrop/" + expansion)
			urllib.request.urlretrieve(image_url, fullpath)
		except FileExistsError:
			urllib.request.urlretrieve(image_url, fullpath)