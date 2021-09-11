# dlensExporter
Python GUI program to convert .dlens files from Delver Lens N mobile application into .csv format to allow importing into various sites and platforms. 

<p align="center">
  <img src="demo.gif" alt="Demo" />
</p>

## Usage

You need three files:

    - data.db from the Delver Lens N APK, you can obtain this by extracting the APK downloadable for example from https://apps.evozi.com/apk-downloader/?id=delverlab.delverlens.
    - .json file with card data from Scryfall, downloadable from https://scryfall.com/docs/api/bulk-data, Default Cards should suffice.
    - .dlens file from Delver Lens N through it's backup or export deck option.
    
## Notes

Currently only supports Deckbox .csv format. There are some differences between what Scryfall API provides as card or set names, and these need to be manually changed. I have added some I've come across myself, but it's not all-inclusive.
