"""Helpers and utils."""

import time


def multi_choice_prompt(prompt, choices, default=None):
    ans = None
    while ans not in choices.keys():
        try:
            ans = raw_input(prompt + ' ').lower()
            if not ans:  # response was an empty string
                ans = default
        except KeyboardInterrupt:
            pass
        except EOFError:
            if default in choices.keys():
                ans = default
                print()
            else:
                raise

    return choices[ans]


class timer(object):
    """Timer Context Manager.

    Usage:
        with(timer("doing something")):
            time.sleep(10)
    """
    def __init__(self, name='timer', log=None):
        self.name = name
        self.log = log

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, ty, val, tb):
        end = time.time()
        msg = "%s : %0.3f ms" % (self.name, (end - self.start) * 1000)
        if self.log and hasattr(self.log, 'debug'):
            self.log.debug(msg)
        else:
            print(msg)
        return False


def termsize():
    """Try to figure out the size of the current terminal.

    Returns:
        Size of the terminal as a tuple: (height, width).
    """
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])