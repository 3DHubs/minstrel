# Minstrel

> It's like... a jester mocks things, and jesters are a subclass of minstrels?

Minstrel is a CLI utility and Python module that combines a bunch of different
strategies to make mocking as simple as possible. The goal here was to create
mocks for our applications that developers would want to use.

To avoid the mocks from going stale, we're implementing a simple pattern. Each
Minstrel file consists of several pars:

* **Base:** the base object, which you'll be able to diff off of with patches.
* **Transports:** objects containing configuration hints for different ways to
  persist the mocks. Currently supported:
  * _SQL_
    * table: the name of the table.
  * _AMQP_
    * exchange: the exchange to publish to.
    * routing\_key: the routing key to publish with.
* **Derivatives:** these are definitions for the derived objects, or for how to
  derive them.
    * _patches_: a list of [JSON Patches][jsonpatch] to derive an object.

Which means it could look like this, right now:

    {
        "transports": {
            "sql": {
                "table": "foobar"
            }
        },
        "base": {
            "a": 1,
            "b": "foo"
        },
        "derivatives": [
            {
                "patches": [
                    { "op": "replace", "path": "/a", "value": -1 }
                ],
            },
            {
                "patches": [
                    { "op": "replace", "path": "/a", "value": 0 },
                    { "op": "add", "path": "/c", "value": true }
                ],
            },
        ]
    }

## Development

I've been using [Pipenv][pipenv] for this, so big props to Kenneth for this:

```
pipenv --three install
```

## Installation

Running `python setupy.py install` will do, for now.


[jsonpatch]: http://jsonpatch.com
[pipenv]: http://pipenv.org "✨🍰✨"
