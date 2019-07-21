__all__ = ("MONOSPACE_FONT", "event_wrapper", "chain_call")


MONOSPACE_FONT = ("consolas", 10)


def event_wrapper(func):
    def inner(*args):
        return func()

    return inner


def chain_call(*funcs):
    def inner():
        return [func() for func in funcs]

    return inner
