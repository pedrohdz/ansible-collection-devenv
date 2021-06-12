from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from itertools import filterfalse
from jinja2 import contextfilter


def process_items(package_mgr, state_test, items):
    filtered_items = filterfalse(is_ignore(package_mgr), items)
    filtered_items = filter(state_test, filtered_items)
    filtered_items = filterfalse(has_macport_variants(package_mgr), filtered_items)
    return sum(map(item_processor(package_mgr), filtered_items), start=[])


def item_processor(package_mgr):
    def _item_processor(item):
        return process_item(package_mgr, item)
    return _item_processor


def process_item(package_mgr, item):
    if isinstance(item, str):
        return [item]

    try:
        sub_item = item[package_mgr]
        if isinstance(sub_item, str):
            return [sub_item]
        return sub_item['packages']
    except KeyError:
        pass

    try:
        return item['packages']
    except KeyError:
        return [item['name']]


def process_macport_variants(package_mgr, items):
    filtered_items = filterfalse(is_ignore(package_mgr), items)
    filtered_items = filter(is_present, filtered_items)
    filtered_items = filter(has_macport_variants(package_mgr), filtered_items)
    return map(process_macport_variant_item, filtered_items)


def process_macport_variant_item(item):
    return (item['macports']['variant_name'], item['macports']['variant'])


def process_alternatives(package_mgr, items):
    filtered_items = filterfalse(is_ignore(package_mgr), items)
    filtered_items = filter(is_present, filtered_items)
    filtered_items = filter(has_alternatives(package_mgr), filtered_items)
    return sum(map(
        process_alternatives_item(package_mgr), filtered_items), start=[])


def process_alternatives_item(package_mgr):
    def _func(item):
        return [(_k, _v) for _k, _v
                in item[package_mgr]['alternatives'].items()]
    return _func


# -----------------------------------------------------------------------------
# Filter tests
# -----------------------------------------------------------------------------
def is_absent(item):
    try:
        return item['state'] == 'absent'
    except (TypeError, KeyError):
        return False


def is_present(item):
    try:
        return item['state'] == 'present'
    except (TypeError, KeyError):
        return True


def is_ignore(package_mgr):
    def _ignore_filter(item):
        try:
            return item[package_mgr]['ignore']
        except (TypeError, KeyError):
            return False
    return _ignore_filter


def has_macport_variants(package_mgr):
    def _filter(item):
        if package_mgr != 'macports':
            return False
        try:
            return ('variant' in item['macports']
                    or 'variant_name' in item['macports'])
        except (KeyError, TypeError):
            return False
    return _filter


def has_alternatives(package_mgr):
    def _filter(item):
        try:
            return 'alternatives' in item[package_mgr]
        except (TypeError, KeyError):
            return False
    return _filter


# -----------------------------------------------------------------------------
# Register filters
# -----------------------------------------------------------------------------
def absent_packages(items, package_mgr):
    return process_items(package_mgr, is_absent, items)


def present_packages(items, package_mgr):
    return process_items(package_mgr, is_present, items)


def present_macport_variants(items, package_mgr):
    return process_macport_variants(package_mgr, items)


def alternatives(items, package_mgr):
    return process_alternatives(package_mgr, items)


class FilterModule(object):
    def filters(self):
        return {
            'absent_packages': absent_packages,
            'alternatives': alternatives,
            'present_macport_variants': present_macport_variants,
            'present_packages': present_packages,
        }
