# BACKEND DJANGO QA
The aim of this repository is to put into practice some best practices regarding code Quality Assurance, like testing and static analysis.

A few things regarding Django specifically will also be addressed, like overriding the default User model and using this new model as default User validation model.

The creation of abstract models as a base model will also be addressed in this repository.

As for the API, its structure will be created with the help of Django Rest Framework.

## Creating pre-commit hook
A git pre-commit hook can be created by running the following command on terminal
```bash
make create-pre-commit
```

This hook will run tests and linting before the commit.

## Testing

## Static Analysis

Linting will be executed by using ```pylint```. Run the following command on terminal.
```bash
pylint --rcfile=.pylintrc --django-settings-module=core.settings */ 
```

Or alternativally, execute the following.
```bash
make lint
```

## API