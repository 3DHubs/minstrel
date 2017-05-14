from .types import HandlerDict, T, Number


def number_handler(value: Number) -> Number:
    if value == 0:
        return 0

    out = 1

    if value != int(value):
        out = 1.5

    if value < 0:
        out = -1 * out

    return out


def string_handler(value: str) -> str:
    if len(value) == 0:
        return ''

    return 'foo'


def noop_handler(value: T) -> T:
    return value


handler_map: HandlerDict = {
    (type(None),): noop_handler,
    (bool,): noop_handler,
    (int, float): number_handler,
    (str,): string_handler,
}
