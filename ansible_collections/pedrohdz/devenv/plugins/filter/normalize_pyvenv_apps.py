from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from copy import deepcopy


def normalize_pyvenv_apps(items):
    result = map(convert_string, items)
    return map(normalize, result)


def convert_string(item):
    if isinstance(item, str):
        return {'name': item}
    elif isinstance(item, dict):
        return item
    raise TypeError('Unknown type for: {0}'.format(item))


def normalize(item):
    if 'bin_files' not in item:
        item['bin_files'] = [item['name']]
    if 'packages' not in item:
        item['packages'] = [item['name']]
    if 'state' not in item:
        item['state'] = 'present'
    return item


class FilterModule(object):
    def filters(self):
        return {
            'normalize_pyvenv_apps': normalize_pyvenv_apps,
        }
