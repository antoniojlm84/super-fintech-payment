.PHONY: up down build logs backend-shell migrate

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

backend-shell:
	docker-compose exec backend bash

migrate:
	docker-compose exec backend python manage.py migrate

maketigrations:
	docker-compose exec backend python manage.py makemigrations

superuser:
	docker-compose exec backend python manage.py createsuperuser
