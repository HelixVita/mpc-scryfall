from scryfall_formatter_allow_dups import *
from scryfall_formatter import *

# Scan every card in a set
page = 1
cardnames = []
cardnumbers = []
totalcards = 0
more = True
expansion = input("Type the three-character set code for the set you want to scan: ")
advanced = input("Enter advanced scryfall criteria here. (e.g. frame:showcase color:red) Leave blank for no extra criteria: ")
holo = input("Enter Yes to remove the holostamp from the scan. Leave blank to keep the holostamp: ")
copyright = input("Enter Yes to remove the copyright from the scan. Leave blank to keep the copyright: ")
allowdups = input("Enter Yes to allow duplicate filenames. This will work for cards with different art, assuming unique:prints is used in the advanced parameter. Leave blank to skip duplicate filenames: ")

# ensure we get every card from the set (multiple search result pages)
while more:
	time.sleep(0.1)
	cardset = scrython.cards.Search(q="set:" + expansion + " " + advanced, page=page)
	more = cardset.has_more()
	totalcards = cardset.total_cards()
	cardnames = cardnames + [cardset.data()[x]["name"] for x in range(len(cardset.data()))]
	cardnumbers = cardnumbers + [cardset.data()[x]["collector_number"] for x in range(len(cardset.data()))]
	page += 1

print("Collected search results for set: " + expansion)
print("Total number of cards:")
print(totalcards)


if allowdups:
	for idx, cardnumber in enumerate(cardnumbers):
		cardname = cardnames[idx]
		process_card_dups(cardname, cardnumber, expansion=expansion, advanced=advanced, holo=holo, copyright=copyright)
else:
	for cardname in sorted(set(cardnames)):
		process_card(cardname, expansion=expansion, advanced=advanced, holo=holo, copyright=copyright)
