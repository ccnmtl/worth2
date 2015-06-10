MANAGE=./manage.py
APP=worth2
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python check jshint jscs test flake8

travis: ./ve/bin/python check jshint jscs flake8
	$(MANAGE) test

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	chmod +x manage.py bootstrap.py
	./bootstrap.py

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint media/js/src/

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs media/js/src/

js: node_modules/.bin/r.js
	./node_modules/.bin/r.js -o build.js

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .

node_modules/.bin/r.js:
	npm install requirejs --prefix .

test: ./ve/bin/python
	npm install
	$(MANAGE) jenkins --pep8-exclude=migrations

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) features --max-complexity=10 --exclude=migrations

behave: ./ve/bin/python check
	$(MANAGE) behave

runserver: ./ve/bin/python check
	$(MANAGE) runserver

migrate: ./ve/bin/python check jenkins
	$(MANAGE) migrate --fake-initial

check: ./ve/bin/python
	$(MANAGE) check

shell: ./ve/bin/python
	$(MANAGE) shell_plus

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm -f celerybeat-schedule .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make check
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make check
	make test
	make migrate
	make flake8

collectstatic: ./ve/bin/python check
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python check jenkins
	createdb $(APP)
	make migrate
