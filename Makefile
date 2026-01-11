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

fresh-install:
	@echo "Stopping and removing all containers and volumes..."
	docker-compose down -v
	@echo "Rebuilding Docker images..."
	docker-compose build
	@echo "Starting containers..."
	docker-compose up -d
	@echo "Waiting for database to be ready..."
	@timeout /t 5 /nobreak > nul
	@echo "Running migrations..."
	docker-compose exec backend python manage.py migrate
	@echo "Loading test fixtures..."
	docker-compose exec backend python seed_data.py
	@echo "Creating superuser (admin/admin)..."
	docker-compose exec backend python create_superuser.py
	@echo "Fresh start complete! Login at http://localhost:3000/login"

reset-db:
	@echo "Dropping database..."
	docker-compose exec db psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'superpayment' AND pid <> pg_backend_pid();"
	docker-compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS superpayment;"
	@echo "Creating fresh database..."
	docker-compose exec db psql -U postgres -c "CREATE DATABASE superpayment;"
	@echo "Running migrations..."
	docker-compose exec backend python manage.py migrate
	@echo "Loading test fixtures..."
	docker-compose exec backend python seed_data.py
	@echo "Creating superuser (admin/admin)..."
	docker-compose exec backend python create_superuser.py
	@echo "Database reset complete!"
