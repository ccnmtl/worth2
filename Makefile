APP=worth2
JS_FILES=media/js/src/
REQUIREJS=$(NODE_MODULES)/.bin/r.js
PY_DIRS=$(APP) features

all: jenkins

include *.mk

behave: check
	$(MANAGE) behave

media/main-built.js: $(JS_SENTINAL) build.js media/js/src
	$(REQUIREJS) -o build.js
