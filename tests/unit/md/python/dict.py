import unittest.mock

import md.python.dict


# Implementation
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
    def test_merge_dictionaries_without_key_intersection(self) -> None:
        # arrange
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'c': 3}

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert {'a': 1, 'b': 2, 'c': 3} == dict3

    def test_merge_dictionaries_second_value_overrides(self) -> None:
        # arrange
        dict1 = {'a': 1}
        dict2 = {'a': 2}

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert {'a': 2} == dict3

    def test_merge_dictionaries_second_value_overrides_sequence(self) -> None:
        # arrange
        dict1 = {'a': [1]}
        dict2 = {'a': [2]}

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert {'a': [2]} == dict3

    def test_merge_dictionaries_with_common_keys(self) -> None:
        # arrange
        dict1 = {'a': {'a': 1}}
        dict2 = {'a': {'b': 2}}

        # act
        dict3 = md.python.dict.merge(left=dict1, right=dict2)

        # assert
        assert {'a': {'a': 1, 'b': 2}} == dict3
