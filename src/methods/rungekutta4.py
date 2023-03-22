
def rk4(func, tk, _yk, _dt=0.01, **kwargs):

    f1 = func(tk, _yk, **kwargs)
    f2 = func(tk + _dt / 2, _yk + (f1 * (_dt / 2)), **kwargs)
    f3 = func(tk + _dt / 2, _yk + (f2 * (_dt / 2)), **kwargs)
    f4 = func(tk + _dt, _yk + (f3 * _dt), **kwargs)

    return _yk + (_dt / 6) * (f1 + (2 * f2) + (2 * f3) + f4)
