# Add iso code for any locales you want to support here (space separated)
# default is no locales
# LOCALES = af
LOCALES = af

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
LRELEASE ?= lrelease-qt5

# QGIS3 default
QGISDIR=.local/share/QGIS/QGIS3/profiles/default


# translation
SOURCES = \
	project_colors_dock/__init__.py \
	project_colors_dock/project_colors_dock.py \
	project_colors_dock/gui/colors_dock.py \
	project_colors_dock/gui/gui_utils.py

PLUGINNAME = project-colors-dock

PY_FILES = \
	project_colors_dock/__init__.py \
	project_colors_dock/project_colors_dock.py \
	project_colors_dock/gui/colors_dock.py \
	project_colors_dock/gui/gui_utils.py

EXTRAS = metadata.txt icon.png

EXTRA_DIRS =

PEP8EXCLUDE=pydev,conf.py,third_party,ui

default:

%.qm : %.ts
	$(LRELEASE) $<

test: transcompile
	@echo
	@echo "----------------------"
	@echo "Regression Test Suite"
	@echo "----------------------"

	@# Preceding dash means that make will continue in case of errors
	@-export PYTHONPATH=`pwd`:$(PYTHONPATH); \
		export QGIS_DEBUG=0; \
		export QGIS_LOG_FILE=/dev/null; \
		nosetests3 -v -s --with-id --with-coverage --cover-package=. project_colors_dock.test \
		3>&1 1>&2 2>&3 3>&- || true
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core error, try sourcing"
	@echo "the helper script we have provided first then run make test."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make test"
	@echo "----------------------"


deploy:
	@echo
	@echo "------------------------------------------"
	@echo "Deploying (symlinking) plugin to your qgis3 directory."
	@echo "------------------------------------------"
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $HOME/$(QGISDIR)/python/plugins
	ln -s `pwd`/project_colors_dock $(HOME)/$(QGISDIR)/python/plugins/${PWD##*/}


transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	@chmod +x scripts/compile-strings.sh
	@scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f i18n/*.qm

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --reports=n --rcfile=pylintrc project_colors_dock
	@echo
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core' error, try sourcing"
	@echo "the helper script we have provided first then run make pylint."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make pylint"
	@echo "----------------------"


# Run pep8/pycodestyle style checking
#http://pypi.python.org/pypi/pep8
pycodestyle:
	@echo
	@echo "-----------"
	@echo "pycodestyle PEP8 issues"
	@echo "-----------"
	@pycodestyle --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128,E402,E501,W504 --exclude $(PEP8EXCLUDE) project_colors_dock
	@echo "-----------"
	@echo "Ignored in PEP8 check:"
	@echo $(PEP8EXCLUDE)
