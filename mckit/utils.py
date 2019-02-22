import numpy as np


MAX_DIGITS = np.finfo(float).precision


def significant_digits(value, reltol=1.e-12, resolution=None):
    """The minimum number of significant digits to provide relative tolerance.

    Parameters
    ----------
    value : float
        The value to be checked.
    reltol : float
        Relative tolerance needed to represent the value.
    resolution : float
        The threshold value, below which numbers are believed to be zero.
        Default: None - not applied.

    Returns
    -------
    digits : int
        The number of digits.
    """
    if resolution and abs(value) < resolution:
        return 0
    low = 0
    high = MAX_DIGITS
    while high - low > 1:
        p = round(0.5 * (high + low))
        v = np.round(value, p)
        d = max(abs(value), abs(v))
        if d != 0 and abs(value - v) / d > reltol:
            low = p
        else:
            high = p
    return high


def significant_array(array, reltol=1.e-12, resolution=None):
    """The minimum number of significant digits to provide relative tolerance.
    """
    result = np.empty_like(array, dtype=int)
    for index in zip(*map(np.ravel, np.indices(array.shape))):
        result[index] = significant_digits(array[index], reltol, resolution)
    return result


def round_scalar(value, digits):
    """Rounds scalar value to represent the value in minimal form.

    Parameters
    ----------
    value : float
        The value to be rounded.
    digits : int
        The number of significant digits.

    Returns
    -------
    result : float
        Rounded value.
    """
    return round(value, digits)


def round_array(array, digarr):
    """Rounds array to desired precision.

    Parameters
    ----------
    array : numpy.ndarray
        Array of values.
    digarr : arraylike[int]
        Array of corresponding significant digits.

    Returns
    -------
    result : numpy.ndarray
        Rounded array.
    """
    result = np.empty_like(array)
    for index in zip(*map(np.ravel, np.indices(array.shape))):
        result[index] = round_scalar(array[index], digarr[index])
    return result
