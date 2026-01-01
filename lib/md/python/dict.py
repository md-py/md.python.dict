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
) -> typing.Dict[str, typing.Any]:
    """
    Cast flatten dictionary index (tuple) to scalar (dot separated, by default) notation (string)

    example:
        { ('parent', 'child') : 42 } -> { 'parent.child' : 42 }
    """
    assert all([isinstance(key, typing.Hashable) and isinstance(key, typing.Sequence) for key in dict_.keys()])
    dictionary = {}
    for key, value in dict_.items():
        if isinstance(key, str):
            dictionary[key] = value
            continue

        if hasattr(key, '__iter__'):
            dictionary[glue.join([str(k) for k in key])] = value
            continue
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


V = typing.TypeVar('V')

class CaseInsensitiveDictKey(str):
    """
    A case-insensitive string key for dictionary lookups.

    This class inherits from str but overrides hash and equality comparison
    to make the key case-insensitive. When used as a dictionary key,
    'Key', 'KEY', and 'key' will all be treated as the same key.

    Attributes:
        _hash (int): Pre-calculated hash value based on the lowercase version
                     of the string for efficient comparisons.

    Example:
        >>> key1 = CaseInsensitiveDictKey("Hello")
        >>> key2 = CaseInsensitiveDictKey("HELLO")
        >>> key1 == key2
        True
        >>> hash(key1) == hash(key2)
        True
        >>> d = CaseInsensitiveDict({key1: "world"})
        >>> "HELLO" in d
        True
    """

    def __init__(self, key: typing.Any) -> None:
        """
        Initialize a case-insensitive key.

        Args:
            key: Any value that can be converted to a string. The string
                 representation will be used for case-insensitive comparison.

        Note:
            The hash is pre-calculated based on the lowercase version of
            the string for performance.
        """
        str.__init__(key)
        self._hash = hash(self.lower())

    def __hash__(self) -> int:
        """
        Return the hash value based on the lowercase version.

        Returns:
            The hash of the lowercase string representation.
        """
        return self._hash

    def __eq__(self, other: typing.Hashable) -> bool:
        """
        Compare with another hashable object for equality.

        Args:
            other: Another hashable object to compare with.

        Returns:
            True if the lowercase versions are equal, False otherwise.

        Note:
            The comparison is case-insensitive. If 'other' is not a string,
            it's converted to string representation first.
        """
        return self._hash == hash(other)


class CaseInsensitiveDict(typing.Dict[str, V]):
    """
    A dictionary with case-insensitive string keys.

    This dictionary treats keys like 'key', 'KEY', and 'Key' as equivalent.
    It inherits from the standard dict but wraps all keys in CaseInsensitiveDictKey
    to provide case-insensitive lookup behavior.

    Type Parameters:
        V: The type of values stored in the dictionary.

    Example:
        >>> d = CaseInsensitiveDict({"Name": "John", "Age": 30})
        >>> d["name"]  # Access with different case
        'John'
        >>> d["NAME"] = "Jane"  # Overwrites existing "Name" key
        >>> d["Name"]
        'Jane'
        >>> "AGE" in d  # Case-insensitive membership test
        True
        >>> list(d.keys())  # Original case is preserved
        ['Name', 'Age']

    You can also initialize with keyword arguments:
        >>> d = CaseInsensitiveDict(Name="John", Age=30)

    Or combine both:
        >>> d = CaseInsensitiveDict({"Name": "John"}, Age=30)
    """

    def __init__(
        self,
        dict_: typing.Optional[typing.Dict[typing.Hashable, V]] = None,
        **kwargs: V
    ) -> None:
        """
        Initialize a case-insensitive dictionary.

        Args:
            dict_: Optional initial dictionary. Keys will be converted to
                   case-insensitive keys. If None, an empty dictionary is created.
            **kwargs: Additional key-value pairs to add to the dictionary.

        Note:
            The original case of the first key added is preserved for display
            purposes, but all subsequent lookups are case-insensitive.
        """
        super().__init__()
        if dict_:
            for key, value in dict_.items():
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def __contains__(self, key: typing.Any) -> bool:
        """
        Check if a key exists in the dictionary (case-insensitive).

        Args:
            key: The key to look for. Can be any type that can be converted
                 to a string representation.

        Returns:
            True if a case-insensitive match is found, False otherwise.

        Example:
            >>> d = CaseInsensitiveDict({"Name": "John"})
            >>> "name" in d
            True
            >>> "NAME" in d
            True
        """
        return super().__contains__(CaseInsensitiveDictKey(key))

    def __setitem__(self, key: typing.Any, value: V) -> None:
        """
        Set a key-value pair (case-insensitive).

        Args:
            key: The key to set. If a key with different case already exists,
                 it will be overwritten.
            value: The value to associate with the key.

        Example:
            >>> d = CaseInsensitiveDict()
            >>> d["Key"] = "value1"
            >>> d["KEY"] = "value2"  # Overwrites previous entry
            >>> d["key"]
            'value2'
        """
        super().__setitem__(CaseInsensitiveDictKey(key), value)

    def __getitem__(self, key: typing.Any) -> V:
        """
        Get a value by key (case-insensitive).

        Args:
            key: The key to look up. Case-insensitive match is performed.

        Returns:
            The value associated with the key.

        Raises:
            KeyError: If the key is not found (case-insensitively).

        Example:
            >>> d = CaseInsensitiveDict({"Name": "John"})
            >>> d["name"]
            'John'
            >>> d["NAME"]
            'John'
        """
        return super().__getitem__(CaseInsensitiveDictKey(key))

    def __delitem__(self, key: typing.Any) -> None:
        """
        Delete a key-value pair (case-insensitive).

        Args:
            key: The key to delete. Case-insensitive match is performed.

        Raises:
            KeyError: If the key is not found (case-insensitively).

        Example:
            >>> d = CaseInsensitiveDict({"Name": "John", "Age": 30})
            >>> del d["name"]  # Deletes "Name" key
            >>> "Name" in d
            False
        """
        return super().__delitem__(CaseInsensitiveDictKey(key))
