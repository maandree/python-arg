PREFIX       = /usr
PYTHONDIR    = $(PREFIX)/lib/python$(PYTHON_VERSION)
PYTHONPKGDIR = $(PYTHONDIR)/site-packages

PYTHON_MAJOR   = $$(python --version 2>&1 | cut -d . -f 1 | cut -d ' ' -f 2)
PYTHON_MINOR   = $$(python$(PYTHON_MAJOR) --version 2>&1 | cut -d . -f 2)
PYTHON_VERSION = $(PYTHON_MAJOR).$(PYTHON_MINOR)

PYTHON = python$(PYTHON_VERSION)
