import sys


def get_func_args(func):
    def inner():
        func_code = func.__code__
        arg_obj = func.__code__.co_varnames[:func_code.co_argcount + func_code.co_kwonlyargcount]
        return arg_obj

    return inner


def get_current_func():
    return sys._getframe(0).f_code