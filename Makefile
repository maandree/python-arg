.POSIX:

CONFIGFILE = config.mk
include $(CONFIGFILE)


all:
	@true

check:
	$(PYTHON) ./test.py

install:
	mkdir -p -- "$(DESTDIR)$(PYTHONPKGDIR)"
	cp -- arg.py "$(DESTDIR)$(PYTHONPKGDIR)/"

uninstall:
	-rm -f -- "$(DESTDIR)$(PYTHONPKGDIR)/arg.py"

clean:
	-rm -rf -- *.pyc *.pyo __pycache__

.SUFFIXES:

.PHONY: all check install uninstall clean
