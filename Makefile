APP=worth2
JS_FILES=media/js/src/
PY_DIRS=$(APP) features

all: jenkins

include *.mk

behave: check
	$(MANAGE) behave
