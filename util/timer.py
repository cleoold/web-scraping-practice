
def func_timer(f):
    'Traces the time consumed in the function.'
    from functools import wraps
    from time import time
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        res = f(*args, **kwargs)
        timeDiff = time() - start
        print(f'-DEBUG: {f.__name__}{args} used {timeDiff:.4f} s.')
        return res
    return wrapper


class sec_timer:
	'''Traces the time consumed of a with block.
	eg:   from sys import _getframe
	      with timer(_getframe().f_lineno) as _:'''
    def __init__(self, line=0):
        self.line = line
    def __enter__(self):
        from time import time
        self.t0 = time()
    def __exit__(self, exc_type, exc_val, exc_tb):
        from time import time
        timeDiff = time() - self.t0
        print(f'-DEBUG: section line {self.line} used {timeDiff:.4f} s.')
