import pytest

import md.python.dict


class TestCaseInsensitiveDict:
    @pytest.mark.parametrize('key', ['key', 'keY', 'kEy', 'kEY', 'Key', 'KeY', 'KEy', 'KEY'])
    def test_case_insensitive_dict_access_after_init(self, key: str) -> None:
        # act
        case_insensitive_dict = md.python.dict.CaseInsensitiveDict()
        case_insensitive_dict['key'] = 42

        # assert
        assert case_insensitive_dict[key] == 42

    @pytest.mark.parametrize('key', ['key', 'keY', 'kEy', 'kEY', 'Key', 'KeY', 'KEy', 'KEY'])
    def test_case_insensitive_dict_access_after_init_from_dict(self, key: str) -> None:
        # act
        case_insensitive_dict = md.python.dict.CaseInsensitiveDict(dict_={'key': 42})

        # assert
        assert case_insensitive_dict[key] == 42

    @pytest.mark.parametrize('key', ['key', 'keY', 'kEy', 'kEY', 'Key', 'KeY', 'KEy', 'KEY'])
    def test_case_insensitive_dict_delete_key(self, key: str) -> None:
        # act
        case_insensitive_dict = md.python.dict.CaseInsensitiveDict(dict_={'key': 42})
        del case_insensitive_dict['key']

        # assert
        assert key not in case_insensitive_dict

