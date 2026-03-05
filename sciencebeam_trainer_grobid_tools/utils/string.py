from functools import partial
from typing import Callable, Dict, List, Optional, Set, Tuple


class PlusMinus:
    PLUS = '+'
    MINUS = '-'


PLUS_OR_MINUS = {PlusMinus.PLUS, PlusMinus.MINUS}


def is_blank(text: str) -> bool:
    return not text or not text.strip()


def comma_separated_str_to_list(s):
    s = s.strip()
    if not s:
        return []
    return [item.strip() for item in s.split(',')]


def plus_minus_comma_separated_str_to_list(s: str, default_value: List[str]) -> List[str]:
    user_list = comma_separated_str_to_list(s)
    if not user_list or not user_list[0] or user_list[0][0] not in PLUS_OR_MINUS:
        return user_list
    result = default_value.copy()
    mode = None
    for user_item in user_list:
        if not user_item:
            continue
        if user_item[0] in PLUS_OR_MINUS:
            mode = user_item[0]
            value = user_item[1:]
        else:
            value = user_item
        if mode == PlusMinus.PLUS:
            result.append(value)
        if mode == PlusMinus.MINUS:
            result.remove(value)
    return result


def plus_minus_comma_separated_str_to_set(s: str, default_value: Optional[Set[str]]) -> Set[str]:
    return set(
        plus_minus_comma_separated_str_to_list(s, list(default_value or set()))
    )


def get_plus_minus_comma_separated_str_to_list_fn(
    default_value: List[str]
) -> Callable[[str], List[str]]:
    return partial(plus_minus_comma_separated_str_to_list, default_value=default_value)


def get_plus_minus_comma_separated_str_to_set_fn(
    default_value: Set[str]
) -> Callable[[str], Set[str]]:
    return partial(plus_minus_comma_separated_str_to_set, default_value=default_value)


def parse_key_value(expr: str) -> Tuple[str, str]:
    key, value = expr.split('=', maxsplit=1)
    return key.strip(), value.strip()


def parse_dict(expr: str, delimiter: str = '|') -> Dict[str, str]:
    if not expr:
        return {}
    d = {}
    for fragment in expr.split(delimiter):
        key, value = parse_key_value(fragment)
        d[key] = value
    return d


# copied from distutils.util.strtobool
def strtobool(val: str) -> int:
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))
