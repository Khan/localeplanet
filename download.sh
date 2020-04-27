#!/bin/sh

# Download the latest icu.js files from localeplanet.com.  We take the
# list of locales from babel, since we are the javascript version of
# babel.py.  (Though, sadly, with a different API.)
#
# NOTE: if we ask localeplanet for a locale it doesn't have
# information about, it will return English data, though possibly with
# the correct language-name.  For instance, 'tg' is correctly "Tajik",
# but the days of teh week are in English.  This is actually desirable
# behavior, since when we don't have data for a country we just fall
# back to English anyway.  This way, we don't have to worry about
# having a 404 because we are missing a locale that babel has.
#
# You can specify the babel/localedata directory on the commandline.
# If you don't, we take it relative to the download.sh script, so
# you should run this script like './download.sh'.

BABEL_DIR=${1-../webapp/third_party/babel/localedata}

locales=`ls "$BABEL_DIR"/*.dat | tr _ - | xargs -n1 basename | sed s/.dat$//`
for locale in $locales; do
   url="http://www.localeplanet.com/api/$locale/icu.js"
   echo "Fetching $url"
   curl -s $url > icu.$locale.js
done

# Also add the __language__ symlink which is the scheme we use to
# select the right js file to include in our javascript package
# system.
# NOTE(somewhatabstract): Pretty sure this isn't used since it was symlinking
# to icu-en.js but we use icu.en.js. Likely this is outdated but I fixed it
# anyway.
ln -snf icu.en.js icu.__language__.js

echo "DONE"
