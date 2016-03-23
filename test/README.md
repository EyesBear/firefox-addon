#Search Addon
For Development:
- Easiest way is to install jpm using npm with the command ```npm install jpm --global``` (see [https://developer.mozilla.org/en-US/Add-ons/SDK/Tools/jpm#Installation](url) for more.)
- Then ```cd``` into the *addon* directory and use the command ```jpm run```, this will open a new Firefox window with the addon installed, including any changes you've made.

How to use:
- Open firefox and type about:config.
- Search for "xpinstall.signatures.required" and toggle it to false.
- Press Ctrl(Cmd) + O and select @addon-0.0.1.xpi to install the addon.
- Highlight any word/phrase on a web page, a popup with a list of products from Amazon.ca would appear.
- Click a product image to visit its product page on Amazon.
- Example:
![example](http://i.imgur.com/Q9iI5ir.png?1)
