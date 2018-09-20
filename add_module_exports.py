#! /usr/bin/python
"""Adds a module.exports line to the end of each icu.{{lang}}.js file in this
directory.

This script must be run after each time you run update the files using
download.sh in order to not break our build system.


Instructions:
Open your server terminal and navaigate to the webapp directory.
In your server terminal, run the following command to gain write permissions:

    sudo chmod +x add_module_exports.py

Enter your password for the computer you're using. Then run:

    third_party/javascript-khansrc/localeplanet/add_module_exports.py
"""
from __future__ import absolute_import

import os
import logging

def main():
    files = os.listdir("third_party/javascript-khansrc/localeplanet/")
    files_updated = []
    files_not_updated = []

    for file in files:
        if file.endswith(".js"):
            file_path = "third_party/javascript-khansrc/localeplanet/" + file
            module_exports_string = 'module.exports = icu;'
            needs_module_exports_string = True

            with open(file_path) as myFile:
                for num, line in enumerate(myFile, 1):
                    if module_exports_string in line:
                        needs_module_exports_string = False
                        break

            if needs_module_exports_string:
                files_updated.append(file)
                f = open(file_path, "a")
                f.write("\n\n")
                f.write(module_exports_string)
                f.write("\n")
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
