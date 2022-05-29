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


# Additional Notes on Post-Filtering Methods
FelixVita's notes to self how (in detail) to best perform post-filtering cleanup in photoshop.

## Copyright Removal (for Cards with Modern frame)
My preferred method is to use the Content Aware Fill, using the following workflowØ
* Open all cards in photoshop (as separate tabs)
* Find the card that has the largest (i.e. widest) copyright out of all the cards AND has a power/toughness box
* Use the lasso tool to draw a selection around the copyright of that card
* Explanation: The reason I don't use a simple rectangular selection here is because I've found that the irregular edge caused by the slightly unsteady hand actually makes the result better.
* Right click the selection and choose "Content Aware Fill"
* Enable the "Mirrored" option in the right side-panel
* Done.

## Bucket Fill
When you're doing this it's a bit hard to tell whether you've managed to successfully replace the pale black color of the border with the same true black as the bleed edge.
Unfortunately though, the solution isn't as easy as setting the tolerance high and the opacity to 100%, because that's not gonna work with the black border cards. Instead I've adopted a slightly different workflow:
* Bucket fill tool, with the following settings:
   * color = true black (#000000),
   * mode = normal,
   * opacity 50%,
   * tolerance = 20,
   * contiguous = enabled (to avoid stuff in the middle of the card to get filled)
* Then, for every non-black card, I click about 6-7 times around various places of the border
   * For black cards, you'll just want to be a bit more careful where and how many times you click
* Then I bring up levels (Ctrl+L) and drag the middle slider all the way to the left
   * This will reveal whether the border is true black or not
* Close the levels window and click a few more times if needed
* Done.

## Holofoil stamp removal
* I'm not as obsessive about this one, and I'm sure there's a better way, but as of right now here's my (not particularly complex) workflow:
* I use a rectangular selection over the holofoil 'cavity' and right-click and select Context Aware Fill and use the default settings.
* Then I usually have to repeat this 2-3 times on a smaller and smaller area each time until it becomes perfectly straight.
* Note: I prefer not to do this on dual-colored cards as it ends up looking quite ugly imho.