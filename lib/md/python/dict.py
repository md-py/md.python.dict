import typing

import md.python


# Metadata
__version__ = '1.0.0'
__author__ = 'https://md.land/md'
__all__ = (
    # Metadata
    '__version__',
    '__author__',
    # Exception
    'DictExceptionInterface',
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
class DictExceptionInterface(md.python.PythonExceptionInterface):
    pass


# Contract
class MergeDictionaryInterface:
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
    stack = [(dict_, initial_key)]

    while stack:
        current_dict, current_path = stack.pop()

        for key, value in current_dict.items():
            new_path = current_path + (key,)

            if isinstance(value, dict):
                stack.append((value, new_path))
                continue

            flatten_dict[new_path] = value
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
    merged_dict = {}
    for key, value in left.items():
        merged_dict[key] = value

    stack = []  # current_merged_dict, key, right_value

    for key, value in right.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            stack.append((merged_dict, key, value))
        else:
            merged_dict[key] = value

    while stack:
        current_merged_dict, key, right_value = stack.pop()
        current_merged_value = current_merged_dict[key]

        for key, value in right_value.items():
            if key in current_merged_value and isinstance(current_merged_value[key], dict) and isinstance(value, dict):
                stack.append((current_merged_value, key, value))
            else:
                current_merged_value[key] = value

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
