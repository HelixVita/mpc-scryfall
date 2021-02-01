# mpc-scryfall
Simple tool to retrieve Scryfall scans of MTG cards, perform some light processing on them, and prepare them for printing with MPC. This tool will throw Scryfall scans through waifu2x (courtesy of deepAI), lightly filter the image, then remove the holographic stamp.

![img1](https://i.imgur.com/gLBAYFL.png)

# Requirements
* An internet connection while the tool is running
* A deepAI.org account (free) 
* Python 3
* The Python 3 packages:
   * Scrython
   * imageio
   * requests
   * numpy
   * scikit-image

# Install / Usage Guide
* Download the script and filter image somewhere on your computer
* Update the file called `config.py` with the API token from deepai.org. It should be one line with the following contents `TOKEN = '<your token from deepAI.org>'`, excluding the <>'s.
* Create a folder called `formatted` in the same location
* Update the 'cards' text files and put the card names, URLs, or paths to lcoal card images you want to scan in it, one on each line.
* To scan each card in `cards.txt`, run `scryfall_formatter.py`
* To scan each card in `cards_local.txt`, run `scryfall_formatter_local.py`
* To scan each card in `cards_url.txt`, run `scryfall_formatter_url.py`
* To do entire sets at a time, run `scryfall_format_set.py` and type in the three-character set code for the set you want when prompted
* To process a single url, run `scryfall_format_url.py` and follow the prompts.
* If you're on a Mac and get an error talking about certificate verification failing, go to Applications -> Python 3.X and run `Install Certificates.command`, and that should fix it!
* If you get an error that looks something like `KeyError: 'output_url'`, double check that you've received and confirmed your deepAI account by email

# Limitations / Other Notes
This can work on any magic card scan, but it'll only attempt to do post-filtering cleanup on planeswalkers and any cards printed in the M15 onwards frame. I also haven't tried printing any cards yet with this, but I placed some of the resulting images into MPC and the crops looked fine.
