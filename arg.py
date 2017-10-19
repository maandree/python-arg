# See LICENSE file for copyright and license details.
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys as _sys
import os as _os
import errno as _errno

MAY_HAVE_ATTACHED_ARGUMENT = 0
NEED_ARGUMENT = 1
NEED_ATTACHED_ARGUMENT = 2
NEED_DETACHED_ARGUMENT = 3
NEED_NO_ARGUMENT = 4

class UsageError(Exception):
    pass

class Parser(object):
    '''
    Command line parser

    Example usage:
        import sys
        import arg
        
        def usage():
            print('usage: %s [-v value] [-xy]' % sys.argv[0], file = sys.stderr)
            sys.exit(1)
        
        xflag = False
        yflag = False
        vflag = None
        
        parser = arg.Parser(usage = usage)
        for c in parser.flags:
            if c == 'x':
                xflag = True
            elif c == 'y':
                yflag = True
            elif c == 'v':
                vflag = parser.arg
            else:
                usage()
    '''

    def __init__(self, argv = None, symbols = '-', keep_dashdash = False, store_nonflags = False, usage = None):
        '''
        @param  argv           A list with the arguments to parse, if `None`, `sys.argv[1:]` is used
        @param  symbols        A string or list contain the characters that will cause an argument
                               to be parsed as being a flag, multicharacter strings will be ignored
        @param  keep_dashdash  If `True`, `--` will be returned in `self.argv`
        @param  keep_nonflags  During parsing, non-flag arguments are ignored, and after the last
                               flag has been parsed, `self.argv` will have the ignored arguments at
                               the beginning
        @param  usage          Function (without arguments) that is to be called if parsing fails
                               due to usage error, if `None`, `UsageError` will be raised instead
                               on usage error
        '''
        if argv is None:
            argv = _sys.argv[1:]
        self._argv = list(argv)
        self._usage_func = usage
        self._symbols = symbols
        self._keep_ddash = keep_dashdash
        self._stored = [] if store_nonflags else None

    def _usage(self):
        if self._usage_func is None:
            raise UsageError()
        else:
            self._usage_func()

    @property
    def flags(self):
        '''
        Return a generator that returns the flags in the command line
        
        Properties and functions in `self` can be used to after each
        time a flag is returned
        
        Each returned value is a single character
        '''
        self._brk = False
        self._accept_none_arg = False
        while len(self._argv):
            if len(self._argv[0]) < 2:
                if self._stored is not None:
                    self._stored.append(self._argv[0])
                    self._argv = self._argv[1:]
                    continue
                break
            self._symbol = self._argv[0][0]
            self._lflag = self._argv[0]
            if self._symbol not in self._symbols:
                if self._stored is not None:
                    self._stored.append(self._argv[0])
                    self._argv = self._argv[1:]
                    continue
                break
            if self._argv[0] == 2 * self._symbol:
                if self._symbol == '-':
                    if not self._keep_ddash:
                        self._argv = self._argv[1:]
                elif self._stored is not None:
                    self._stored.append(self._argv[0])
                    self._argv = self._argv[1:]
                    continue
                break
            self._i = 1
            n = len(self._argv[0])
            while self._i < n:
                self._flag = self._argv[0][self._i]
                if self._flag == self._symbol and self._i != 1:
                    self._usage()
                if self._i + 1 < n:
                    self._arg = self._argv[0][self._i + 1:]
                elif len(self._argv) > 1:
                    self._arg = self._argv[1]
                else:
                    self._arg = None
                yield self._flag
                self._lflag = None
                self._accept_none_arg = False
                if self._brk:
                    if len(self._argv) > 1 and self._arg is self._argv[1]:
                        self._argv = self._argv[1:]
                    self._brk = False
                    break
                self._i += 1
            self._argv = self._argv[1:]
        if self._stored:
            self._argv = self._stored + self._argv
        self._stored = None

    @property
    def flag(self):
        '''
        Return the current short flag, for example '-a',
        this string is always two characters long
        '''
        return self._symbol + self._flag

    @property
    def symbol(self):
        '''
        Get the first character in the flag, normally '-'
        '''
        return self._symbol

    @property
    def lflag(self):
        '''
        Get the entire current argument, for example
        '--mode=755', `None` not at the beginning
        '''
        return self._lflag

    @property
    def argv(self):
        '''
        Return a list of all remaining arguments
        '''
        return self._argv

    @property
    def argc(self):
        '''
        Return the number of remaining arguments
        '''
        return len(self._argv)

    @property
    def arg(self):
        '''
        Get the argument specified for the flag, can only be
        `None` (no argument) if `self.testlong` has returned
        `True` with `MAY_HAVE_ATTACHED_ARGUMENT` as the second
        argument for the currnet flag
        
        Reading this property will cause the parser to assume
        that the flag should have an argument, if these is
        no argument UsageError will be raised (or the specified
        usage function will be called) unless `self.testlong`
        has returned `True` with `MAY_HAVE_ATTACHED_ARGUMENT`
        as the second argument for the currnet flag
        '''
        if self._arg is None and not self._accept_none_arg:
            self._usage()
        self._brk = True
        return self._arg

    @property
    def arghere(self):
        '''
        Return the current argument with an offset such that the
        first character is the character associated with the
        current flag, for example, if the current argument is
        '-123' and the current flag is '1', '123' is returned
        
        Reading this property will cause the parser to continue
        with the next argument when getting the next flag
        '''
        self._brk = True
        self._arg = None
        return self._argv[0][self._i:]

    @property
    def isargnum(self):
        '''
        Check whether the value returned by `arghere` will be a number
        
        Calling this function does not affect the parser
        '''
        return self._argv[0][self._i:].isdigit()

    @property
    def argnum(self):
        '''
        Identical to `arghere`, except the returned value will
        be converted to an integer
        
        If the value returned by `self.arghere` is not a
        number, UsageError will be raised (or the specified
        usage function will be called)
        '''
        if not self.isargnum:
            self._usage()
        return int(self.arghere)

    def consume(self):
        '''
        Cause the parser to skip the rest of current argument
        and continue with the next argument
        
        If `self.arg` has been read and returned the next argument,
        the parser will still read that argument
        '''
        self._arg = None
        self._brk = True

    def testlong(self, flag, argument = 0):
        '''
        Check whether the current flag is specific long flag
        
        It is important to use this function, because it will
        set the parser's state appropriately whe it finds a match
        
        If the flag is the specified long flag, but its argument
        status does not match `argument`, UsageError will be raised
        (or the specified usage function will be called)
        
        @param  flag      The long flag, should start with its symbol prefix (usually '--')
        @param  argument  arg.MAY_HAVE_ATTACHED_ARGUMENT (default):
                                  The flag may have an argument attached to the flag
                                  separated by a '=', for example '--value=2', but
                                  it is not necessary, so just '--value' is also accepted,
                                  but the next argument may not be parsed as a value
                                  associated with the flag
                          arg.NEED_ARGUMENT:
                                  The flag must have an attached argument or a detached
                                  argument, for example '--value=2' is accepted, but
                                  '--value' is only accepted if it is not the last argument,
                                  if the current argument does not contain a '='
                          arg.NEED_ATTACHED_ARGUMENT:
                                  The flag must have an attached argument, for example
                                  '--value=2' is accepted but '--value' is not
                          arg.NEED_DETACHED_ARGUMENT:
                                  The flag must have a detached argument, for example
                                  '--value' is accepted, but only if it is not the last
                                  argument, but '--value=2' is not accepted
                          arg.NEED_NO_ARGUMENT:
                                  The flag must not have an argument, for example
                                  '--value' is accepted but '--value=2' is not
        '''
        if self._lflag is None:
            return False
        attached = self._lflag.startswith(flag + '=')
        if attached:
            arg = self._lflag[self._lflag.index('=') + 1:]
            lflag = self._lflag[:self._lflag.index('=')]
        else:
            arg = self._argv[1] if len(self._argv) > 1 else None
            lflag = self._lflag
        if lflag != flag:
            return False
        elif argument == MAY_HAVE_ATTACHED_ARGUMENT:
            if not attached:
                arg = None
                self._accept_none_arg = True
        elif argument == NEED_ARGUMENT:
            if arg is None:
                self._usage()
        elif argument == NEED_ATTACHED_ARGUMENT:
            if not attached:
                self._usage()
        elif argument == NEED_DETACHED_ARGUMENT:
            if attached or arg is None:
                self._usage()
        elif argument == NEED_NO_ARGUMENT:
            arg = None
            if attached:
                self._usage()
        else:
            raise OSError(_os.strerror(_errno.EINVAL), _errno.EINVAL)
        self._arg = arg
        self._brk = True
        return True
