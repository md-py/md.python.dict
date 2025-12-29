import unittest.mock
import typing

import pytest

import md.python.dict


# internal utility:
def drown_dictionary(dictionary: dict, depth: int, key: typing.Hashable = 'key') -> dict:
    for _ in range(depth):
        dictionary = {key: dictionary}
    return dictionary


def dataset(data_set: typing.Dict[str, typing.Dict[str, typing.Any]]) -> pytest.mark.parametrize:
    argnames = []
    argvalues = []
    ids = []
    for id_, argument_map in data_set.items():
        if not argnames:
            argnames = list(argument_map.keys())
        argvalues.append([argument_map[argument_value] for argument_value in argnames])
        ids.append(id_)
    return pytest.mark.parametrize(argnames=argnames, argvalues=argvalues, ids=ids)


# Tests:
class TestDefaultMergeDictionary:
    def test_merge(self) -> None:
        # arrange
        left = {'foo': 'bar'}
        right = {'bar': 'baz'}

        # act
        default_merge_dictionary = md.python.dict.DefaultMergeDictionary()
        with unittest.mock.patch('md.python.dict.merge') as merge_mock:
            merge_mock.return_value = {'foo': 'bar', 'bar': 'baz'}
            merged_dict = default_merge_dictionary.merge(left=left, right=right)

        # assert
        merge_mock.assert_called_once_with(left=left, right=right)
        assert merged_dict == {'foo': 'bar', 'bar': 'baz'}


class TestFlat:
    def test_flat(self) -> None:
        # arrange
        dict_ = {
            'foo': {
                'bar': {
                    'baz': 42
                }
            }
        }

        # act
        flatted_dict = md.python.dict.flat(dict_=dict_)

        # assert
        assert ('foo', 'bar', 'baz') in flatted_dict
        assert flatted_dict[('foo', 'bar', 'baz')] == 42

    def test_flat_with_initial_key(self) -> None:
        # arrange
        initial_key = ('root',)
        dict_ = {
            'foo': {
                'bar': {
                    'baz': 42
                }
            }
        }

        # act
        flatted_dict = md.python.dict.flat(dict_=dict_, initial_key=initial_key)

        # assert
        assert ('root', 'foo', 'bar', 'baz') in flatted_dict
        assert flatted_dict[('root', 'foo', 'bar', 'baz')] == 42


class TestInlineIndex:
    def test_inline_index(self) -> None:
        # act
        inlined_index_dict = md.python.dict.inline_index(dict_={
            ('foo', 'bar'): 'baz',
            ('foo', 'bar', 'baz'): 42
        })

        # assert
        assert 'foo.bar' in inlined_index_dict
        assert inlined_index_dict['foo.bar'] == 'baz'

        assert 'foo.bar.baz' in inlined_index_dict
        assert inlined_index_dict['foo.bar.baz'] == 42

    def test_inline_index_with_custom_glue(self) -> None:
        # act
        inlined_index_dict = md.python.dict.inline_index(dict_={
            ('foo', 'bar'): 'baz',
            ('foo', 'bar', 'baz'): 42
        }, glue='-')

        # assert
        assert 'foo-bar' in inlined_index_dict
        assert inlined_index_dict['foo-bar'] == 'baz'

        assert 'foo-bar-baz' in inlined_index_dict
        assert inlined_index_dict['foo-bar-baz'] == 42


class TestMergeDictionaries:
    @dataset({
        'no deep': dict(depth=0),
        'very deep': dict(depth=600),
    })
    def test_merge_dictionaries_without_key_intersection(self, depth: int) -> None:
        # arrange
        dict1 = drown_dictionary(dictionary={'a': 1, 'b': 2}, depth=depth)
        dict2 = drown_dictionary(dictionary={'c': 3}, depth=depth)
        expected_result = drown_dictionary(dictionary={'a': 1, 'b': 2, 'c': 3}, depth=depth)

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert expected_result == dict3

    @dataset({
        'no deep': dict(depth=0),
        'very deep': dict(depth=600),
    })
    def test_merge_dictionaries_second_value_overrides(self, depth: int) -> None:
        # arrange
        dict1 = drown_dictionary(dictionary={'a': 1}, depth=depth)
        dict2 = drown_dictionary(dictionary={'a': 2}, depth=depth)
        expected_result = drown_dictionary(dictionary={'a': 2}, depth=depth)

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert expected_result == dict3

    @dataset({
        'no deep': dict(depth=0),
        'very deep': dict(depth=600),
    })
    def test_merge_dictionaries_second_value_overrides_sequence(self, depth: int) -> None:
        # arrange
        dict1 = drown_dictionary(dictionary={'a': [1]}, depth=depth)
        dict2 = drown_dictionary(dictionary={'a': [2]}, depth=depth)
        expected_result = drown_dictionary(dictionary={'a': [2]}, depth=depth)

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert expected_result == dict3

    @dataset({
        'no deep': dict(depth=0),
        'very deep': dict(depth=600),
    })
    def test_merge_dictionaries_with_common_keys(self, depth: int) -> None:
        # arrange
        dict1 = drown_dictionary(dictionary={'a': {'a': 1}}, depth=depth)
        dict2 = drown_dictionary(dictionary={'a': {'b': 2}}, depth=depth)
        expected_result = drown_dictionary(dictionary={'a': {'a': 1, 'b': 2}}, depth=depth)

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert expected_result == dict3
