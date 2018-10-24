import logging

def configure_logger(filename, verbose):
    logging.basicConfig(filename=filename,
                        level=_get_logging_level(verbose),
                        format=_get_format(filename is None))
    logging.getLogger('selenium').setLevel(logging.WARNING)

def _get_logging_level(verbose):
    if not verbose:
        return logging.WARNING
    elif verbose == 1:
        return logging.INFO
    else:
        return logging.DEBUG

def _get_format(with_color=False):
    name = _ColoredString('%(name)s')
    level = _ColoredString('%(levelname)s')
    format = '%(asctime)s'
    format += '|' + (name.to_blue() if with_color else name)
    format += '|' + (level.to_bold_gray() if with_color else level)
    format += '|%(message)s'
    return format

class _ColoredString(unicode):
    """Implementation of string with additional methods allowing to wrap string
    content with given color.
    Example:
    >>> ColoredString('foo').to_red()
    '\033[0;31mfoo\033[0m'
    """
    C_RED = '\033[0;31m%s\033[0m'
    C_BLUE = '\033[0;34m%s\033[0m'
    C_GREEN = '\033[0;32m%s\033[0m'
    C_WHITE = '\033[0;37m%s\033[0m'
    C_BOLD_RED = '\033[1;31m%s\033[0m'
    C_BOLD_GREEN = '\033[1;32m%s\033[0m'
    C_BOLD_WHITE = '\033[1;37m%s\033[0m'
    C_BOLD_GRAY = '\033[1;30m%s\033[0m'

    def __getattr__(self, name):
        if not name.startswith('to_'):
            return super(_ColoredString, self).__getattribute__(name)
        else:
            def colorize():
                return getattr(self.__class__, 'C_%s' % name[3:].upper()) % self

            return colorize
