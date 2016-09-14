#!/usr/bin/env python
'''Slim down localeplanet to just the things we need

On mobile native, we only need a small bit of what localeplanet provides, so
to cut down on size (localeplanet is 2.1 megs), we extract what we need into a
small js file.

On the web, pages only load what we need, so it's not a problem; but on
native, we have to download everything.
'''

import subprocess
import json
import os


def get_git_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


def get_decimal_format(lines):
    '''Get the json blob representing the decimal_format'''

    for line in lines:
        line = line.strip()
        if line.startswith('var nfs = '):
            return line[len('var nfs = '):-1]  # remove trailing semicolon
    raise Exception('No `var nfs` line found')


def is_same_format(a, b):
    for k in a:
        if a[k] != b[k]:
            return False
    return True


def is_locale_file(name):
    return name.startswith('icu.') and name.endswith('.js')


def process_all_locales():
    '''Extract the info we care about from the files in this directory'''

    configs = [{
        'decimal_separator':'.',
        'grouping_separator':',',
        'minus':'-'
    }]
    locales = {}
    for name in filter(is_locale_file, os.listdir('.')):
        locale = name.split('.')[1]
        text = open(name).read()
        decimal_format = json.loads(get_decimal_format(text.split('\n')))
        index = 0
        for i, config in enumerate(configs):
            if is_same_format(config, decimal_format):
                index = i
                break
        else:
            configs.append(decimal_format)
            index = len(configs) - 1

        locales[locale] = index

    return {'configs': configs, 'locales': locales}


def write_results(results, destination):
    open(destination, 'w').write('''
;(function() {
// This file was automatically generated by Khan/localeplanet/slim.py
// We only use one function from `localeplanet` on mobile native, so we
// cut the weight dramatically by generating this slim version.
// [git hash: %s]

var data = %s;
var locale = 'en-US';

window.icu = {
    getLocale: function() {
        return locale;
    },
    getLanguage: function() {
        return locale.split("-")[0];
    },
    setLocale: function(newLocale) {
        locale = newLocale;
    },
    getDecimalFormatSymbols: function() {
        return data.configs[data.locales[locale]] || data.configs[0];
    }
};
})();
''' % (get_git_hash(), json.dumps(results)))

    print '''Wrote to %s

Now copy it into ~/khan/mobile-client-webview-resources/\
ThirdParty/javascript-khansrc/localeplanet/
''' % destination

if __name__ == '__main__':
    if not os.path.exists('./build'):
        os.mkdir('./build')
    write_results(process_all_locales(), './build/icu-slim.js')