APP=worth2
JS_FILES=media/js/src/
REQUIREJS=$(NODE_MODULES)/.bin/r.js
PY_DIRS=$(APP) features
MAX_COMPLEXITY=9

all: jenkins

include *.mk

behave: check
	$(MANAGE) behave

media/main-built.js: $(JS_SENTINAL) build.js media/js
	$(REQUIREJS) -o build.js
