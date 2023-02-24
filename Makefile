clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f .coverage
	rm -f coverage.xml

lint:
	pylint --rcfile=.pylintrc --django-settings-module=core.settings */

test:
	python manage.py test