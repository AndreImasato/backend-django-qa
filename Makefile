clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f .coverage
	rm -f coverage.xml

create-pre-commit:
	@echo "Creating pre-commit hook..."
	bash create_precommit.sh

lint:
	pylint --rcfile=.pylintrc --django-settings-module=core.settings */

test:
	python manage.py test

commit-test:
	python manage.py test --exclude-tag=exclude_git_commit