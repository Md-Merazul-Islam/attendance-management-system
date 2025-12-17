# ===================================================================
# Makefile - Docker & Django Commands
# Location: project_root/Makefile
# ===================================================================

.PHONY: help build up down restart logs shell migrate test clean

# Colors
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help:
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)Django Docker Management Commands$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)🚀 Docker Commands:$(NC)"
	@echo "  make build           - Build Docker images"
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make restart         - Restart all services"
	@echo "  make ps              - Show running containers"
	@echo "  make clean           - Remove containers and volumes"
	@echo ""
	@echo "$(YELLOW)📋 Logs:$(NC)"
	@echo "  make logs            - View all logs"
	@echo "  make logs-web        - View web logs"
	@echo "  make logs-celery     - View celery logs"
	@echo "  make logs-beat       - View celery beat logs"
	@echo "  make logs-db         - View database logs"
	@echo ""
	@echo "$(YELLOW)🗄️  Database:$(NC)"
	@echo "  make migrate         - Run migrations"
	@echo "  make makemigrations  - Create migrations"
	@echo "  make dbshell         - Open database shell"
	@echo "  make backup          - Backup database"
	@echo "  make restore         - Restore database"
	@echo ""
	@echo "$(YELLOW)🐍 Django:$(NC)"
	@echo "  make shell           - Open Django shell"
	@echo "  make superuser       - Create superuser"
	@echo "  make collectstatic   - Collect static files"
	@echo "  make test            - Run tests"
	@echo ""
	@echo "$(YELLOW)🔧 Development:$(NC)"
	@echo "  make exec-web        - Execute bash in web container"
	@echo "  make exec-celery     - Execute bash in celery container"

# ===================================================================
# Docker Commands
# ===================================================================

build:
	@echo "$(GREEN)🔨 Building Docker images...$(NC)"
	docker-compose build --no-cache

up:
	@echo "$(GREEN)🚀 Starting services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started!$(NC)"
	@echo "$(YELLOW)Web: http://localhost:8000$(NC)"

down:
	@echo "$(RED)⏹️  Stopping services...$(NC)"
	docker-compose down

restart:
	@echo "$(YELLOW)🔄 Restarting services...$(NC)"
	docker-compose restart

ps:
	@echo "$(GREEN)📦 Running containers:$(NC)"
	docker-compose ps

stop:
	@echo "$(RED)⏸️  Stopping services...$(NC)"
	docker-compose stop

# ===================================================================
# Logs
# ===================================================================

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-celery:
	docker-compose logs -f celery

logs-beat:
	docker-compose logs -f celery-beat

logs-db:
	docker-compose logs -f db

logs-redis:
	docker-compose logs -f redis


# ===================================================================
# Database Commands
# ===================================================================

migrate:
	@echo "$(GREEN)🗄️  Running migrations...$(NC)"
	docker-compose exec web python manage.py migrate

makemigrations:
	@echo "$(GREEN)📝 Creating migrations...$(NC)"
	docker-compose exec web python manage.py makemigrations

showmigrations:
	docker-compose exec web python manage.py showmigrations

dbshell:
	@echo "$(GREEN)🗄️  Opening database shell...$(NC)"
	docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

backup:
	@echo "$(GREEN)💾 Backing up database...$(NC)"
	docker-compose exec -T db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Backup created!$(NC)"

restore:
	@echo "$(YELLOW)⚠️  Restoring database from backup.sql...$(NC)"
	docker-compose exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql
	@echo "$(GREEN)✅ Database restored!$(NC)"

reset-db:
	@echo "$(RED)⚠️  WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d db redis; \
		sleep 5; \
		docker-compose up -d web; \
		docker-compose exec web python manage.py migrate; \
		echo "$(GREEN)✅ Database reset complete!$(NC)"; \
	fi

# ===================================================================
# Django Commands
# ===================================================================

shell:
	@echo "$(GREEN)🐍 Opening Django shell...$(NC)"
	docker-compose exec web python manage.py shell

shell-plus:
	@echo "$(GREEN)🐍 Opening Django shell_plus...$(NC)"
	docker-compose exec web python manage.py shell_plus

superuser:
	@echo "$(GREEN)👤 Creating superuser...$(NC)"
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	@echo "$(GREEN)📦 Collecting static files...$(NC)"
	docker-compose exec web python manage.py collectstatic --noinput

test:
	@echo "$(GREEN)🧪 Running tests...$(NC)"
	docker-compose exec web pytest

test-cov:
	@echo "$(GREEN)🧪 Running tests with coverage...$(NC)"
	docker-compose exec web pytest --cov=apps --cov-report=html

# ===================================================================
# Celery Commands
# ===================================================================

celery-purge:
	@echo "$(YELLOW)🗑️  Purging Celery tasks...$(NC)"
	docker-compose exec celery celery -A config purge -f

celery-inspect:
	@echo "$(GREEN)🔍 Inspecting Celery workers...$(NC)"
	docker-compose exec celery celery -A config inspect active

celery-stats:
	@echo "$(GREEN)📊 Celery statistics...$(NC)"
	docker-compose exec celery celery -A config inspect stats

# ===================================================================
# Development Commands
# ===================================================================

exec-web:
	@echo "$(GREEN)🐳 Entering web container...$(NC)"
	docker-compose exec web bash

exec-celery:
	@echo "$(GREEN)🐳 Entering celery container...$(NC)"
	docker-compose exec celery bash

exec-db:
	@echo "$(GREEN)🐳 Entering database container...$(NC)"
	docker-compose exec db sh

# ===================================================================
# Cleanup Commands
# ===================================================================

clean:
	@echo "$(RED)🧹 Cleaning up...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

clean-all:
	@echo "$(RED)⚠️  Removing ALL containers, images, and volumes!$(NC)"
	docker-compose down -v --rmi all
	docker system prune -af --volumes
	@echo "$(GREEN)✅ Full cleanup complete!$(NC)"

prune:
	@echo "$(YELLOW)🧹 Pruning Docker system...$(NC)"
	docker system prune -f

# ===================================================================
# Production Commands
# ===================================================================

deploy:
	@echo "$(GREEN)🚀 Deploying to production...$(NC)"
	git pull origin main
	docker-compose down
	docker-compose build
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "$(GREEN)✅ Deployment complete!$(NC)"

health:
	@echo "$(GREEN)🏥 Checking service health...$(NC)"
	@echo "Web: $$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/admin/login/)"
	@echo "Redis: $$(docker-compose exec redis redis-cli ping)"
	@echo "Database: $$(docker-compose exec db pg_isready)"

# ===================================================================
# Monitoring
# ===================================================================

stats:
	@echo "$(GREEN)📊 Container statistics:$(NC)"
	docker stats --no-stream

top:
	@echo "$(GREEN)⬆️  Top processes:$(NC)"
	docker-compose top

# ===================================================================
# Logs Management
# ===================================================================

clear-logs:
	@echo "$(YELLOW)🗑️  Clearing application logs...$(NC)"
	rm -rf logs/*.log
	rm -rf logs/celery/*.log
	rm -rf logs/django/*.log
	@echo "$(GREEN)✅ Logs cleared!$(NC)"

logs-size:
	@echo "$(GREEN)📊 Log file sizes:$(NC)"
	du -sh logs/*

# ===================================================================
# Quick Start
# ===================================================================

init:
	@echo "$(GREEN)🚀 Initializing project...$(NC)"
	cp .env.example .env
	@echo "$(YELLOW)⚠️  Please edit .env file with your configuration$(NC)"
	@echo "$(GREEN)Then run: make setup$(NC)"

setup:
	@echo "$(GREEN)🔧 Setting up project...$(NC)"
	mkdir -p logs/celery logs/django
	docker-compose build
	docker-compose up -d
	@echo "$(YELLOW)⏳ Waiting for services to start...$(NC)"
	sleep 10
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "$(YELLOW)Create superuser: make superuser$(NC)"