create_config_project: 
	django-admin startproject config .

create_todo_app:
	python manage.py startapp todos

create_user_app:
	python manage.py startapp users

dev:
	python manage.py runserver

make_migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

create_superuser:
	python manage.py createsuperuser

freeze_requirements:
	pip freeze > requirements.txt
