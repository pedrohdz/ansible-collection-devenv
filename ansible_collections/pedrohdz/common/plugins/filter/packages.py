from itertools import filterfalse
from jinja2 import contextfilter


def process_items(context, state_test, items):
    filtered_items = filterfalse(ignore_test(context), items)
    filtered_items = filter(state_test, filtered_items)
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


# -----------------------------------------------------------------------------
# Filter tests
# -----------------------------------------------------------------------------
def absent_test(item):
    try:
        return item['state'] == 'absent'
    except (TypeError, KeyError):
        return False


def present_test(item):
    try:
        return item['state'] == 'present'
    except (TypeError, KeyError):
        return True


def ignore_test(context):
    def _ignore_filter(item):
        pkg_mgr = context['ansible_pkg_mgr']
        try:
            return item[pkg_mgr]['ignore']
        except (TypeError, KeyError):
            return False
    return _ignore_filter


# -----------------------------------------------------------------------------
# Register filters
# -----------------------------------------------------------------------------
@contextfilter
def absent_packages(context, items):
    return process_items(context, absent_test, items)


@contextfilter
def present_packages(context, items):
    return process_items(context, present_test, items)


class FilterModule(object):
    def filters(self):
        return {
            'absent_packages': absent_packages,
            'present_packages': present_packages,
        }
