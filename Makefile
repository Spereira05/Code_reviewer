# Start the development environment
up:
	docker-compose up -d

# Start with logs displayed
run:
	docker-compose up

# Build or rebuild services
build:
	docker-compose build

# Stop containers
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Format code (requires black to be installed)
format:
	uv pip install black
	black app/

# Install dependencies
install:
	uv pip install -e .

# Install development dependencies
dev-deps:
	uv pip install black pytest

# Run tests (requires pytest to be installed)
test:
	pytest

# Enter the web container shell
shell:
	docker-compose exec web /bin/bash

