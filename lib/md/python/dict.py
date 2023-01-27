import copy
import typing

import md.python


# Metadata
__version__ = '1.0.0'
__author__ = 'https://md.land/md'

__all__ = (
    # Metadata
    '__version__',
    '__author__',
    # Contract
    'MergeDictionaryInterface',
    # Implementation:
    'CaseInsensitiveDict',
    'CaseInsensitiveDictKey',
    'DefaultMergeDictionary',
    'flat',
    'inline_index',
    'merge',
)


# Exception
class DictExceptionInterface:
    pass


# Contract
class MergeDictionaryInterface(md.python.PythonExceptionInterface):
    def merge(self, left: dict, right: dict) -> dict:
        raise NotImplementedError


# Implementation:
class DefaultMergeDictionary(MergeDictionaryInterface):
    def merge(self, left: dict, right: dict) -> dict:
        return merge(left=left, right=right)


def flat(dict_: dict, initial_key: tuple = ()) -> dict:
    """
    Performs flatting dictionary object

    example:
        {'parent': {'child' : 42} } -> { ('parent', 'child') : 42 }
    """

    flatten_dict = {}

    for key, value in dict_.items():
        flatten_key = initial_key + (key,)

        if isinstance(value, dict):
            value = flat(value, flatten_key)

            for nested_dict_key, nested_dict_value in value.items():
                flatten_dict[nested_dict_key] = nested_dict_value
        else:
            flatten_dict[flatten_key] = value

    return flatten_dict


def inline_index(
    dict_: typing.Dict[typing.Union[typing.Hashable, typing.Sequence], typing.Any],
    glue: str = '.'
) -> typing.Dict[str, typing.Any]:  # todo rename param
    """
    Cast flatten dictionary index (tuple) to scalar (dot separated, by default) notation (string)

    example:
        { ('parent', 'child') : 42 } -> { 'parent.child' : 42 }
    """
    assert all([isinstance(key, typing.Hashable) and isinstance(key, typing.Sequence) for key in dict_.keys()])
    dictionary = {}
    for key, value in dict_.items():
        dictionary[glue.join(key)] = value
    return dictionary


def merge(left: dict, right: dict) -> dict:
    """ Merges two dictionaries into one and returns it """
    merged_dict = copy.copy(left)
    for key, value in right.items():
        if key in merged_dict:
            if isinstance(merged_dict[key], dict) and isinstance(value, dict):
                merged_dict[key] = merge(merged_dict[key], value)
                continue
            merged_dict[key] = right[key]  # warning: override
            continue
        merged_dict[key] = value  # just copy by key from second dict, which not exists in first
    return merged_dict


class CaseInsensitiveDictKey(str):
    def __init__(self, key) -> None:
        str.__init__(key)
        self._hash = hash(self.lower())

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other: typing.Hashable) -> bool:
        return self._hash == hash(other)


class CaseInsensitiveDict(dict):
    def __init__(self, dict_: dict = None, **kwargs) -> None:
        super().__init__()
        if dict_:
            for key, value in dict_.items():
                self[key] = value
        for key, value in kwargs:
            self[key] = value

    def __contains__(self, key: typing.Hashable) -> bool:
        return super().__contains__(CaseInsensitiveDictKey(key))

    def __setitem__(self, key: typing.Hashable, value: typing.Any) -> None:
        super().__setitem__(CaseInsensitiveDictKey(key), value)

    def __getitem__(self, key: typing.Hashable) -> typing.Any:
        return super().__getitem__(CaseInsensitiveDictKey(key))
