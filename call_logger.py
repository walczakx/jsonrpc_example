import logging
from functools import wraps
from inspect import getcallargs

def log_function_call(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('rpc.call_log.function')
        logger.info('Request to call [{0}] with args {1} {2}'.format(f.__name__, args, kwargs))
        try:
            logger.debug('Enter {0}{1}'.format(f.__name__, getcallargs(f, *args, **kwargs)))
            ret_value = f(*args, **kwargs)
        except Exception:
            logger.exception('Function [{0}] raised exception'.format(f.__name__))
            raise
        else:
            logger.info('Function [{0}] returned {1}'.format(f.__name__, ret_value))
        return ret_value

    return wrapper

def log_method_call(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('rpc.call_log.method')
        logger.info('Request to call [{0}] with args {1} {2}'.format(f.__name__, args[1:], kwargs))
        try:
            print_args = getcallargs(f, *args, **kwargs)
            if 'self' in print_args:
                del print_args['self']
                logger.debug('Enter {0}{1}'.format(f.__name__, print_args))

            ret_value = f(*args, **kwargs)
        except Exception:
            logger.exception('Method [{0}] raised exception'.format(f.__name__))
            raise
        else:
            logger.info('Method [{0}] returned {1}'.format(f.__name__, ret_value))
        return ret_value

    return wrapper
