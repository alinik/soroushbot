import functools
import logging
logger = logging.getLogger(__name__)

def ignore_exception(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            value = None
            logging.exception("Silent ignore")
        return value

    return wrapper_decorator


