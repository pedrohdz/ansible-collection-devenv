from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from itertools import filterfalse
from jinja2 import contextfilter


def process_items(context, state_test, items):
    filtered_items = filterfalse(is_ignore(context), items)
    filtered_items = filter(state_test, filtered_items)
    filtered_items = filterfalse(has_macport_variants(context), filtered_items)
    return sum(map(item_processor(context), filtered_items), start=[])


def item_processor(context):
    def _item_processor(item):
        return process_item(context, item)
    return _item_processor


def process_item(context, item):
    if isinstance(item, str):
        return [item]

    try:
        sub_item = item[context['ansible_pkg_mgr']]
        if isinstance(sub_item, str):
            return [sub_item]
        return sub_item['packages']
    except KeyError:
        pass

    try:
        return item['packages']
    except KeyError:
        return [item['name']]


def process_macport_variants(context, items):
    filtered_items = filterfalse(is_ignore(context), items)
    filtered_items = filter(is_present, filtered_items)
    filtered_items = filter(has_macport_variants(context), filtered_items)
    return map(process_macport_variant_item, filtered_items)


def process_macport_variant_item(item):
    return (item['macports']['variant_name'], item['macports']['variant'])


def process_alternatives(context, items):
    filtered_items = filterfalse(is_ignore(context), items)
    filtered_items = filter(is_present, filtered_items)
    filtered_items = filter(has_alternatives(context), filtered_items)
    return sum(map(
        process_alternatives_item(context), filtered_items), start=[])


def process_alternatives_item(context):
    def _func(item):
        pkg_mgr = context['ansible_pkg_mgr']
        return [(_k, _v) for _k, _v in item[pkg_mgr]['alternatives'].items()]
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


def is_ignore(context):
    def _ignore_filter(item):
        pkg_mgr = context['ansible_pkg_mgr']
        try:
            return item[pkg_mgr]['ignore']
        except (TypeError, KeyError):
            return False
    return _ignore_filter


def has_macport_variants(context):
    def _filter(item):
        if context['ansible_pkg_mgr'] != 'macports':
            return False
        try:
            return ('variant' in item['macports']
                    or 'variant_name' in item['macports'])
        except (KeyError, TypeError):
            return False
    return _filter


def has_alternatives(context):
    def _filter(item):
        pkg_mgr = context['ansible_pkg_mgr']
        try:
            return 'alternatives' in item[pkg_mgr]
        except (TypeError, KeyError):
            return False
    return _filter


# -----------------------------------------------------------------------------
# Register filters
# -----------------------------------------------------------------------------
@contextfilter
def absent_packages(context, items):
    return process_items(context, is_absent, items)


@contextfilter
def present_packages(context, items):
    return process_items(context, is_present, items)


@contextfilter
def present_macport_variants(context, items):
    return process_macport_variants(context, items)


@contextfilter
def alternatives(context, items):
    return process_alternatives(context, items)


class FilterModule(object):
    def filters(self):
        return {
            'absent_packages': absent_packages,
            'alternatives': alternatives,
            'present_macport_variants': present_macport_variants,
            'present_packages': present_packages,
        }
