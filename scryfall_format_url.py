from scryfall_formatter_url import *

# grab URL to use
url = input("Enter the URL to the card you want processed: ")
cardname = input("Enter the name of the card you want processed: ")

process_card(url, cardname)