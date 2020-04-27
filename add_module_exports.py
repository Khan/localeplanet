#! /usr/bin/python
"""Modify each icu.{{lang}}.js file in this directory to export icu.

This script must be run after each time you run update the files using
download.sh in order to not break our build system.

Instructions:
Open your server terminal and navaigate to the webapp directory.
In your server terminal, run the following command to gain write permissions:

    sudo chmod +x add_module_exports.py

Enter your password for the computer you're using. Then run:

    ./add_module_exports.py
"""
from __future__ import absolute_import

import os
import logging

def main():
    files = os.listdir(".")
    files_updated = []
    files_not_updated = []

    for file in files:
        if file.endswith(".js") and not file.endswith("__language__.js"):
            file_path = "./" + file
            module_exports_string = 'module.exports = icu;'
            needs_modification = True

            # We assume that if our exports line is not present, then our code
            # needs to be added.
            with open(file_path, "r") as myFile:
                for num, line in enumerate(myFile, 1):
                    if module_exports_string in line:
                        needs_modification = False
                        break

            if needs_modification:
                # Track the file that we updated.
                files_updated.append(file)

                # Read the file contents so we can edit them.
                f = open(file_path, "r")
                contents = f.readlines()
                f.close()

                # Process the contents to make our modifications.
                # First we want to locate where we are inserting our new
                # icu var declaration and delete the old one.
                #
                # The bit we're removing always looks like:
                #      window.icu = window.icu || new Object();
                #      var icu = window.icu;
                del_start = contents.index(
                    '\twindow.icu = window.icu || new Object();\n')
                del contents[del_start]
                del contents[del_start]

                # Now we can insert our new lines.
                contents.insert(del_start, '\tvar icu = {};\n')
                contents.insert(
                    del_start + 1, '\tif (typeof window !== "undefined") {\n')
                contents.insert(
                    del_start + 2, '\t\ticu = window.icu = window.icu || {};\n')
                contents.insert(del_start + 3, '\t}\n')

                # Finally, we want to add the export.
                # This goes just inside the end of the IIFE.
                iife_end = contents.index('})();')
                contents.insert(iife_end, '\t' + module_exports_string + '\n')

                # Write out the updated file.
                f = open(file_path, "w")
                f.write("".join(contents))
                f.close()
            else:
                files_not_updated.append(file)

    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logging.info("These files were updated:")
    logging.info(files_updated)
    logging.info("These files were not updated:")
    logging.info(files_not_updated)
    logging.info("done! :)\n")

if __name__ == "__main__":
    main()
