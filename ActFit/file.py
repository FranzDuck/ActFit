from io import BytesIO
from typing import Tuple, Dict, Callable, Union

import dill

__all__ = ("dump", "dumps", "load", "loads")


def dump(
    func: Callable, params: Dict[str, float], file: BytesIO, *args, **kwargs
) -> None:
    """Dump a fit to file
    
    :param func: fitted function
    :param params: fitted parameters
    :param file: file object to dump into
    """
    dill.dump((func, params), file, *args, **kwargs)


def dumps(func: Callable, params: Dict[str, float], *args, **kwargs) -> bytes:
    """Dump a fit to bytes/str
    
    :param func: fitted function
    :param params: fitted parameters
    """
    file = BytesIO()
    dump(func, params, file, *args, **kwargs)
    return file.getvalue()


def load(file: BytesIO, *args, **kwargs) -> Tuple[Callable, Dict[str, float]]:
    """Load a fit from file
    
    :param file: file to load from
    """
    return dill.load(file, *args, **kwargs)


def loads(s: Union[str, bytes], *args, **kwargs) -> Tuple[Callable, Dict[str, float]]:
    """Load a fit from str/bytes
    
    :param s: byte-/string to load from
    """
    file = BytesIO(s)
    return load(file, *args, **kwargs)
