.PHONY: help install migrate test lint format clean docker-up docker-down docker-logs

help:
	@echo "Healthcare SaaS Platform - Available Commands"
	@echo "=============================================="
	@echo "install       - Install dependencies"
	@echo "migrate       - Run database migrations"
	@echo "test          - Run tests"
	@echo "lint          - Run linting checks"
	@echo "format        - Format code with black and isort"
	@echo "clean         - Remove Python cache files"
	@echo "docker-up     - Start Docker containers"
	@echo "docker-down   - Stop Docker containers"
	@echo "docker-logs   - View Docker logs"
	@echo "superuser     - Create Django superuser"
	@echo "shell         - Open Django shell"

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

test:
	pytest --cov=. --cov-report=html --cov-report=term

lint:
	flake8 . --exclude=migrations,venv,env --max-line-length=120
	black --check .
	isort --check-only .

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

dev:
	python manage.py runserver

.DEFAULT_GOAL := help
