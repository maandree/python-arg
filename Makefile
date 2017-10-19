.POSIX:

PREFIX = /usr/local

PYTHON_MAJOR = $$(python --version 2>&1 | cut -d . -f 1 | cut -d ' ' -f 2)
PYTHON_MINOR = $$(python$(PYTHON_MAJOR) --version 2>&1 | cut -d . -f 2)

all:
	@true

check:
	python$(PYTHON_MAJOR) ./test.py

install:
	mkdir -p -- "$(DESTDIR)$(PREFIX)/lib/python$(PYTHON_MAJOR).$(PYTHON_MINOR)/site-packages"
	cp -- arg.py "$(DESTDIR)$(PREFIX)/lib/python$(PYTHON_MAJOR).$(PYTHON_MINOR)/site-packages/"

uninstall:
	-rm -f -- "$(DESTDIR)$(PREFIX)/lib/python$(PYTHON_MAJOR).$(PYTHON_MINOR)/site-packages/arg.py"

clean:
	-rm -rf -- *.pyc *.pyo __pycache__

.SUFFIXES:

.PHONY: all check install uninstall clean
