# md.python.dict

md.python.dict component defines contracts to perform operations over
native python `dict` type, and provides few useful tools out from box.

## Architecture overview

[![Architecture overview][architecture-overview]][architecture-overview]

## Component overview

```python3
def flat(dict_: dict, initial_key: tuple = ()) -> dict: ...

def inline_index(
    dict_: typing.Dict[typing.Union[typing.Hashable, typing.Sequence], typing.Any],
    glue: str = '.'
) -> typing.Dict[str, typing.Any]:  ...

def merge(left: dict, right: dict, merge_value_types: typing.Tuple[type] = None) -> dict: ...
```

## Install

```sh
pip install md.python.dict --index-url https://source.md.land/python/  
```

## [Documentation](docs/index.md)

Read documentation with examples: https://development.md.land/python/md.python.dict/

## [Changelog](changelog.md)
## [License (MIT)](license.md)

[architecture-overview]: docs/_static/architecture-overview.class-diagram.svg
