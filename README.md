# mpc-scryfall
Simple tool to retrieve Scryfall scans of MTG cards, perform some light processing on them, and prepare them for printing with MPC. This tool will throw Scryfall scans through waifu2x (courtesy of deepAI), lightly filter the image, then remove the holographic stamp and copyright info. There is an expectation that some post-image processing will need to be done in GIMP or Photoshop or a similar image editing tool. Depending on the Scryfall scan, the outer bleed edge and the inner card border can be differing shades of black. My tool will add a full black (0,0,0) outer border (or full white if choosing a white bordered set). This can differ from the black color from the scan, so you will want to bucket fill similar colors on the inner black border to match the full black outer border. Similarly, the holostamp (if removed) will leave the stamp area black. You can use content aware filling (photoshop) or heal selection (GIMP) to flatten the stamp area and text box. See an example below of a fully processed card taken from a scryfall scan with the stamp area flattened/filled.

![img1](https://i.imgur.com/aQdaYQ7.png)

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
* Update the 'cards' text files and put the card names, URLs, or paths to local card images you want to scan in it, one on each line.
* To scan each card in `cards.txt`, run `scryfall_formatter.py`
* To scan each card in `cards_local.txt`, run `scryfall_formatter_local.py`
* To scan each card in `cards_url.txt`, run `scryfall_formatter_url.py`
* To do entire sets at a time, run `scryfall_format_set.py` and type in the three-character set code for the set you want when prompted
* To process a single url, run `scryfall_format_url.py` and follow the prompts.
* To download all art crops for a set, run `scryfall_image_crop_set.py` and follow the prompts (this is useful for the mtg-autoproxy tool: https://github.com/ndepaola/mtg-autoproxy).
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