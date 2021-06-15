# mpc-scryfall
Simple tool to retrieve Scryfall scans of MTG cards, perform some light processing on them, and prepare them for printing with MPC. This tool will throw Scryfall scans through waifu2x (courtesy of deepAI), lightly filter the image, then remove the holographic stamp and copyright info. There is an expectation that some post-image processing will need to be done in GIMP or Photoshop or a similar image editing tool. Depending on the Scryfall scan, the outer bleed edge and the inner card border can be differing shades of black. My tool will add a full black (0,0,0) outer border (or full white if choosing a white bordered set). This can differ from the black color from the scan, so you will want to bucket fill similar colors on the inner black border to match the full black outer border. Similarly, the holostamp (if removed) will leave the stamp area black. You can use content aware filling (photoshop) or heal selection (GIMP) to flatten the stamp area and text box. See an example below of a fully processed card taken from a scryfall scan with the stamp area flattened/filled.

![img1](https://i.imgur.com/bqGvQdi.png)

# Requirements
* An internet connection while the tool is running
* A deepAI.org account (free) 
* Python 3
* The Python 3 packages (use pip to install the following packages, e.g. pip install Scrython):
   * Scrython
   * imageio
   * requests
   * numpy
   * scikit-image

# Install / Usage Guide
* Download the script and filter image somewhere on your computer
* Update the file called `config.py` with the API token from deepai.org. It should be one line with the following contents `TOKEN = '<your token from deepAI.org>'`, excluding the <>'s.
* Create a folder called `formatted` in the same location
* To download and process specific cards from Scryfall:
   * Add each card to `cards.txt`, one card on each line.
   * Run `scryfall_formatter.py`
* To process cards/images that you have stored locally:
   * Add each card/image filepath to `cards_local.txt`, one card/image filepath on each line.
   * Run `scryfall_formatter_local.py`
* To process cards/images that you have a URL for:
   * Add each card/image URL to `cards_url.txt`, one card/image URL on each line.
   * Run `scryfall_formatter_url.py`
* To download and process entire sets from Scryfall:
   * Run `scryfall_format_set.py`
   * Type in the three-character set code for the set you want when prompted
* To process a single card/image that you have a URL for:
   * Run `scryfall_format_url.py`
   * Follow the prompts.
* To download all art crops for a set from Scryfall:
   * Create a folder called `artcrop`
   * Run `scryfall_image_crop_set.py`
   * Follow the prompts (this is useful for the mtg-autoproxy tool: https://github.com/ndepaola/mtg-autoproxy).
* If you're on a Mac and get an error talking about certificate verification failing, go to Applications -> Python 3.X and run `Install Certificates.command`, and that should fix it!
* If you get an error that looks something like `KeyError: 'output_url'`, double check that you've received and confirmed your deepAI account by email

# Limitations / Other Notes
* This can work on any magic card scan, but it'll only attempt to do post-filtering cleanup on planeswalkers and any cards printed in the M15 onwards frame. Pre M-15 cards will need to have the copyright info manually removed. Content Aware Fill (photoshop) or Heal Selection (GIMP) are the most efficient ways to do this.
* If you have a folder full of images you want to process with the local card formatter, you can generate the cards_local.txt file very easily by doing the following (assuming you are using Windows):
   * Open a command prompt and cd to the directory where the images live.
   * Run the following command: dir /b /s >cards_local.txt
   * This will create a file called cards_local.txt in the directory with the images, with all the filepaths to the images populated.
   * Then all you have to do is add the pipe | and the name you want the card saved as, so for example: C:\MPC-Images\Demonic Tutor.png|Demonic Tutor

# Tip Jar
* https://paypal.me/BootlegMTG
* Tips are never expected, but always appreciated.