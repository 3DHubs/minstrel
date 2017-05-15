# Minstrel

> It's like... a jester mocks things, and jesters are a subclass of minstrels?

Minstrel is a CLI utility and Python module that combines a bunch of different
strategies to make mocking as simple as possible. The goal here was to create
mocks for our applications that developers would want to use.

To avoid the mocks from going stale, we're implementing a simple pattern. Each
Mintrel file consists of two parts: the original object or base, and
patch-based derivatives. Looks somewhat like this:

    {
        "base": {
            "a": 1,
            "b": "foo"
        },
        "derivatives": [
            [
                { "op": "replace", "path": "/a", "value": -1 }
            ],
            [
                { "op": "replace", "path": "/a", "value": 0 },
                { "op": "add", "path": "/c", "value": true }
            ]
        ]
    }

## Installation

TBD.

## Todo

* [ ] Applying mocks.
* [ ] Revert simplified values back to original values for more valid data.
* [ ] More intelligently inspect nested objects for picking an optimal base.
* [ ] Path-based matching on nested objects to avoid duplication.
