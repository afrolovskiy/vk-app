.PHONY: initdev migrate run

initdev:
	python3 -m venv venv
	venv/bin/pip install -r requirements/development.txt

migrate:
	venv/bin/python manage.py migrate

run:
	venv/bin/python manage.py runserver
