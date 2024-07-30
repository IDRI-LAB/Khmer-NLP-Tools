import functools
import re
import sys

from khnlp.util.file import make_dirs, get_dir_path


class Logger(object):
    def __init__(self, output_file):
        self.terminal = sys.stdout
        self.log = open(output_file, "a")

    def __getattr__(self, attr):
        return getattr(self.terminal, attr)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass

    def close(self):
        self.log.close()


def write_log(path):
    def real_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            new_path = path
            params = re.findall(r'{.*}', new_path)
            for param in params:
                param_ = param[1:-1]
                if kwargs.get(param_) is not None:
                    new_path = new_path.replace(param, kwargs.get(param_))

            make_dirs(get_dir_path(new_path))
            sys.stdout = Logger(new_path)

            value = function(*args, **kwargs)

            # sys.stdout.close() - currently disable

            return value

        return wrapper

    return real_decorator
