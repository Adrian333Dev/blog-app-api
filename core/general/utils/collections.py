# Collection of helper functions.

import collections


def deep_update(d, u):
    # Recursively update a dict.
    # Subdict's won't be overwritten but also updated.

    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
