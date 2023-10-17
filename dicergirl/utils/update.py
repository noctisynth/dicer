import re


def require_update(old_version: str, new_version: str):
    regex = r"^(\d+)\.(\d+)\.(\d+)(.*?)?(\d+?)?$"

    old_tuple = re.match(regex, old_version)
    new_tuple = re.match(regex, new_version)

    old_tuple_main = tuple(map(int, filter(None, old_tuple.group(1, 2, 3))))
    new_tuple_main = tuple(map(int, filter(None, new_tuple.group(1, 2, 3))))

    new_length = len(list(filter(None, new_tuple.groups())))
    old_length = len(list(filter(None, old_tuple.groups())))

    if old_length == 5:
        old_pre_release = old_tuple.group(4)[0]
        old_pre_version = int(old_tuple.group(5))
    elif old_length == 3:
        old_pre_release = "s"
        old_pre_version = 1
    else:
        return False

    if new_length == 5:
        new_pre_release = new_tuple.group(4)[0]
        new_pre_version = int(new_tuple.group(5))
    elif new_length == 3:
        new_pre_release = "s"
        new_pre_version = 1
    else:
        return False

    if old_tuple_main < new_tuple_main:
        return True
    elif old_tuple_main > new_tuple_main:
        return False
    elif old_tuple_main == new_tuple_main:
        if old_pre_release < new_pre_release:
            return True
        elif old_pre_release > new_pre_release:
            return False
        elif old_pre_release == new_pre_release:
            if old_pre_version < new_pre_version:
                return True
            elif old_pre_version > new_pre_version:
                return False
            elif old_pre_version == new_pre_version:
                return False
