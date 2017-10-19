#!/usr/bin/env python
# See LICENSE file for copyright and license details.
# -*- coding: utf-8 -*-

import sys
import arg


parser = arg.Parser()
assert parser.argv == sys.argv[1:]


parser = arg.Parser(argv = ['-a', '-aa', '-aaa'])
n = 0
for c in parser.flags:
    assert c == 'a'
    n += 1
assert n == 6
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


parser = arg.Parser(argv = ['-abc', '-xyz'])
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
assert parser.symbol == '-'
assert next(flags) == 'b'
assert parser.flag == '-b'
assert next(flags) == 'c'
assert parser.flag == '-c'
assert next(flags) == 'x'
assert parser.flag == '-x'
assert parser.lflag == '-xyz'
assert next(flags) == 'y'
assert parser.flag == '-y'
assert parser.lflag is None
assert next(flags) == 'z'
assert parser.flag == '-z'
assert parser.symbol == '-'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


for mid in ('', '-', 'x'):
    parser = arg.Parser(argv = ['-abc', mid, '-xyz'])
    flags = parser.flags
    assert next(flags) == 'a'
    assert parser.flag == '-a'
    assert parser.symbol == '-'
    assert next(flags) == 'b'
    assert parser.flag == '-b'
    assert next(flags) == 'c'
    assert parser.flag == '-c'
    try:
        next(flags)
        assert False
    except StopIteration:
        pass
    assert type(parser.argv) is list
    assert len(parser.argv) == 2
    assert type(parser.argc) is int
    assert parser.argc == 2
    assert parser.argv == [mid, '-xyz']


parser = arg.Parser(argv = ['-abc', '--', '-xyz'])
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
assert parser.symbol == '-'
assert next(flags) == 'b'
assert parser.flag == '-b'
assert next(flags) == 'c'
assert parser.flag == '-c'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 1
assert type(parser.argc) is int
assert parser.argc == 1
assert parser.argv == ['-xyz']


parser = arg.Parser(argv = ['-abc', '--', '-xyz'], keep_dashdash = True)
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
assert parser.symbol == '-'
assert next(flags) == 'b'
assert parser.flag == '-b'
assert next(flags) == 'c'
assert parser.flag == '-c'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 2
assert type(parser.argc) is int
assert parser.argc == 2
assert parser.argv == ['--', '-xyz']


parser = arg.Parser(argv = ['a', '--', 'b'], keep_dashdash = True, store_nonflags = True)
flags = parser.flags
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 3
assert type(parser.argc) is int
assert parser.argc == 3
assert parser.argv == ['a', '--', 'b']


parser = arg.Parser(argv = ['a', '--', 'b'], keep_dashdash = False, store_nonflags = True)
flags = parser.flags
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 2
assert type(parser.argc) is int
assert parser.argc == 2
assert parser.argv == ['a', 'b']


parser = arg.Parser(argv = ['-a-b'])
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
try:
    next(flags)
    assert False
except arg.UsageError:
    pass


parser = arg.Parser(argv = ['-123', '-xyz'])
flags = parser.flags
assert next(flags) == '1'
assert parser.flag == '-1'
assert next(flags) == '2'
assert parser.flag == '-2'
assert next(flags) == '3'
assert parser.flag == '-3'
assert next(flags) == 'x'
assert parser.flag == '-x'
assert next(flags) == 'y'
assert parser.flag == '-y'
assert next(flags) == 'z'
assert parser.flag == '-z'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


parser = arg.Parser(argv = ['-123', '-xyz'])
flags = parser.flags
assert next(flags) == '1'
assert parser.flag == '-1'
assert parser.arghere == '123'
assert parser.isargnum
assert parser.argnum == 123
assert next(flags) == 'x'
assert parser.flag == '-x'
assert next(flags) == 'y'
assert parser.flag == '-y'
assert next(flags) == 'z'
assert parser.flag == '-z'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


parser = arg.Parser(argv = ['-1', '-xyz'])
flags = parser.flags
assert next(flags) == '1'
assert parser.flag == '-1'
assert parser.arghere == '1'
assert parser.isargnum
assert parser.argnum == 1
assert next(flags) == 'x'
assert parser.flag == '-x'
assert next(flags) == 'y'
assert parser.flag == '-y'
assert next(flags) == 'z'
assert parser.flag == '-z'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


parser = arg.Parser(argv = ['-ab', '--', '-xyz'], store_nonflags = True)
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
assert next(flags) == 'b'
assert parser.flag == '-b'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 1
assert type(parser.argc) is int
assert parser.argc == 1
assert parser.argv == ['-xyz']


parser = arg.Parser(argv = ['-ab', '--', '-xyz'], keep_dashdash = True, store_nonflags = True)
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
assert next(flags) == 'b'
assert parser.flag == '-b'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 2
assert type(parser.argc) is int
assert parser.argc == 2
assert parser.argv == ['--', '-xyz']


for mid in ('o', 'oo'):
    parser = arg.Parser(argv = ['-ab', mid, '-xyz'], store_nonflags = True)
    flags = parser.flags
    assert next(flags) == 'a'
    assert parser.flag == '-a'
    assert next(flags) == 'b'
    assert parser.flag == '-b'
    assert next(flags) == 'x'
    assert parser.flag == '-x'
    assert next(flags) == 'y'
    assert parser.flag == '-y'
    assert next(flags) == 'z'
    assert parser.flag == '-z'
    try:
        next(flags)
        assert False
    except StopIteration:
        pass
    assert type(parser.argv) is list
    assert len(parser.argv) == 1
    assert type(parser.argc) is int
    assert parser.argc == 1
    assert parser.argv == [mid]


parser = arg.Parser(argv = ['-abc'], symbols = '+')
flags = parser.flags
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 1
assert type(parser.argc) is int
assert parser.argc == 1
assert parser.argv == ['-abc']


parser = arg.Parser(argv = ['+xyz', '-abc'], symbols = '+')
flags = parser.flags
assert next(flags) == 'x'
assert parser.flag == '+x'
assert parser.symbol == '+'
assert next(flags) == 'y'
assert parser.flag == '+y'
assert next(flags) == 'z'
assert parser.flag == '+z'
assert parser.symbol == '+'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 1
assert type(parser.argc) is int
assert parser.argc == 1
assert parser.argv == ['-abc']


parser = arg.Parser(argv = ['+xyz', '-abc'], symbols = '-+')
flags = parser.flags
assert next(flags) == 'x'
assert parser.flag == '+x'
assert parser.symbol == '+'
assert next(flags) == 'y'
assert parser.flag == '+y'
assert next(flags) == 'z'
assert parser.flag == '+z'
assert parser.symbol == '+'
assert next(flags) == 'a'
assert parser.flag == '-a'
assert parser.symbol == '-'
assert next(flags) == 'b'
assert parser.flag == '-b'
assert next(flags) == 'c'
assert parser.flag == '-c'
assert parser.symbol == '-'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


parser = arg.Parser(argv = ['+xyz', '++', '-abc'], symbols = '-+')
flags = parser.flags
assert next(flags) == 'x'
assert parser.flag == '+x'
assert parser.symbol == '+'
assert next(flags) == 'y'
assert parser.flag == '+y'
assert next(flags) == 'z'
assert parser.flag == '+z'
assert parser.symbol == '+'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 2
assert type(parser.argc) is int
assert parser.argc == 2
assert parser.argv == ['++', '-abc']


parser = arg.Parser(argv = ['-123', '-xyz'])
flags = parser.flags
assert next(flags) == '1'
assert parser.arg == '23'
assert next(flags) == 'x'
assert parser.flag == '-x'
assert parser.arg == 'yz'
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


for a in ('', '-x'):
    parser = arg.Parser(argv = ['-1', a])
    flags = parser.flags
    assert next(flags) == '1'
    assert parser.arg == a
    try:
        next(flags)
        assert False
    except StopIteration:
        pass
    assert type(parser.argv) is list
    assert len(parser.argv) == 0
    assert type(parser.argc) is int
    assert parser.argc == 0


parser = arg.Parser(argv = ['-123', '-xyz'])
flags = parser.flags
assert next(flags) == '1'
parser.consume()
assert next(flags) == 'x'
parser.consume()
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 0
assert type(parser.argc) is int
assert parser.argc == 0


parser = arg.Parser(argv = ['--123', 'x'])
flags = parser.flags
assert next(flags) == '-'
assert not parser.testlong('--abc')
assert parser.testlong('--123', arg.NEED_NO_ARGUMENT)
try:
    next(flags)
    assert False
except StopIteration:
    pass
assert type(parser.argv) is list
assert len(parser.argv) == 1
assert type(parser.argc) is int
assert parser.argc == 1
assert parser.argv == ['x']


for check_arg in (True, False):
    for arg_need in (arg.NEED_ARGUMENT, arg.NEED_DETACHED_ARGUMENT):
        parser = arg.Parser(argv = ['--123', 'x'])
        flags = parser.flags
        assert next(flags) == '-'
        assert not parser.testlong('--abc')
        assert parser.testlong('--123', arg_need)
        if check_arg:
            assert parser.arg == 'x'
        try:
            next(flags)
            assert False
        except StopIteration:
            pass
        assert type(parser.argv) is list
        assert len(parser.argv) == 0
        assert type(parser.argc) is int
        assert parser.argc == 0


for check_arg in (True, False):
    parser = arg.Parser(argv = ['--123=x'])
    flags = parser.flags
    assert next(flags) == '-'
    assert not parser.testlong('--abc')
    assert parser.testlong('--123', arg.NEED_ATTACHED_ARGUMENT)
    if check_arg:
        assert parser.arg == 'x'
    try:
        next(flags)
        assert False
    except StopIteration:
        pass
    assert type(parser.argv) is list
    assert len(parser.argv) == 0
    assert type(parser.argc) is int
    assert parser.argc == 0


parser = arg.Parser(argv = ['--123', 'x'])
flags = parser.flags
assert next(flags) == '-'
assert not parser.testlong('--abc')
try:
    parser.testlong('--123', arg.NEED_ATTACHED_ARGUMENT)
    assert False
except arg.UsageError:
    pass


for a in ('x', ''):
    parser = arg.Parser(argv = ['--123=' + a])
    flags = parser.flags
    assert next(flags) == '-'
    assert not parser.testlong('--abc')
    assert parser.testlong('--123', arg.MAY_HAVE_ATTACHED_ARGUMENT)
    assert parser.arg == a
    try:
        next(flags)
        assert False
    except StopIteration:
        pass
    assert type(parser.argv) is list
    assert len(parser.argv) == 0
    assert type(parser.argc) is int
    assert parser.argc == 0

    parser = arg.Parser(argv = ['--123', a])
    flags = parser.flags
    assert next(flags) == '-'
    assert not parser.testlong('--abc')
    assert parser.testlong('--123', arg.MAY_HAVE_ATTACHED_ARGUMENT)
    assert parser.arg == None
    try:
        next(flags)
        assert False
    except StopIteration:
        pass
    assert type(parser.argv) is list
    assert len(parser.argv) == 1
    assert type(parser.argc) is int
    assert parser.argc == 1
    assert parser.argv == [a]


parser = arg.Parser(argv = ['-a-'], usage = lambda : sys.exit(0))
flags = parser.flags
assert next(flags) == 'a'
assert parser.flag == '-a'
next(flags)
assert False
