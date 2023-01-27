# Documentation

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

def merge(left: dict, right: dict) -> dict: ...
```

## Install

```sh
pip install md.python.dict --index-url https://source.md.land/python/  
```

## Usage
### Operations over dictionary
#### Flat dictionary

```python3
def flat(dict_: dict, initial_key: tuple = ()) -> dict: ...
```

`md.python.dict.flat` function flats structured dictionary object, and returns
new dictionary with flatten key of `tuple` type, for example:

```python3
import md.python.dict

md.python.dict.flat({
    'foo': {
        'bar': {
            'baz': 42
        }
    }
})
```

will return: 

```python3
{
    ('foo', 'bar', 'baz'): 42
}
```

When `initial_key: tuple` argument is provided, it's value used 
as prefix for resulting dictionary key by prepending it, for example:

```python3
import md.python.dict

md.python.dict.flat({
    'foo': {
        'bar': {
            'baz': 42
        }
    }
}, initial_key=('4', '8'))
```

will return:

```python3
{
    ('4', '8', 'foo', 'bar', 'baz'): 42
}
```

#### Inline dictionary index

```python3
def inline_index(
    dict_: typing.Dict[typing.Union[typing.Hashable, typing.Sequence], typing.Any],
    glue: str = '.'
) -> typing.Dict[str, typing.Any]:  ...
```


`md.python.dict.inline_index` function inlines iterable dictionary key into
scalar key (string), by joining its parts with `glue: str = '.'` argument, for example:

```python3
import md.python.dict

md.python.dict.inline_index(dict_={
    ('foo', 'bar'): 'baz',
    ('foo', 'bar', 'baz'): 42
})
```

will retutn:

```python3
{
    'foo.bar': 'baz',
    'foo.bar.baz': 42
}
```

and 

```python3
import md.python.dict

md.python.dict.inline_index(
    dict_={
        ('foo', 'bar'): 'baz',
        ('foo', 'bar', 'baz'): 42
    },
    glue='-'
)
```

will return:

```python3
{
  'foo-bar': 'baz', 
  'foo-bar-baz': 42
}
```

#### Merge dictionaries

```python3
def merge(left: dict, right: dict) -> dict: ...
```

`md.python.dict.merge` function merges two dictionaries and returns new dictionary,
for example:

```python3
import md.python.dict

md.python.dict.merge(left={'a': 1, 'b': 2}, right={'c': 3})
```

will return:

```python3
{
    'a': 1,
    'b': 2, 
    'c': 3
}
```

!!! warning

    In some cases `merge` operation leads to data overwrite, for example:

    ```python3
    import md.python.dict

    md.python.dict.merge(left={'a': ['some', 'useful', 'data']}, right={'a': None})
    ```

    will return:

    ```python3
    {'a': None}
    ```

!!! notice

    `merge` operation does not merges types different from `dict` type, for example:

    ```python3
    import md.python.dict

    md.python.dict.merge(
        left={'a': ['some', 'useful', 'data']}, 
        right={'a': ['here', 'no']}
    )
    ```

    will return:

    ```python3
    {'a': ['here', 'no']}
    ```

### Case-insensitive dictionary

`md.python.dict.CaseInsensitiveDict` provides extension of standard `dict` type,
that allows to access to the same value by a key not depending on it case.

```python3
import md.python.dict

case_insensitive_dict = md.python.dict.CaseInsensitiveDict({
    'key': 42
})
assert case_insensitive_dict['KEY'] == 42  # ok 

case_insensitive_dict['Key'] = 4  # ok 
assert case_insensitive_dict['KeY'] == 4  # ok

# etc ...
```

[architecture-overview]: _static/architecture-overview.class-diagram.svg
