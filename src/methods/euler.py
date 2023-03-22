
def euler(func, tk, _yk, _dt=0.01, **kwargs):
    return _yk + func(tk, _yk, **kwargs) *_dt
