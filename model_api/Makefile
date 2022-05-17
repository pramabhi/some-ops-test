BUILDDIR=$(shell pwd)
ENV ?= local

build:
	docker-compose -f docker-compose.yml build

build-debug: ## builds debug service image
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up

app-debug: build-debug		## Build and run in debug mode
	docker-compose -f docker-compose.yml up  --abort-on-container-exit &

down:
	docker-compose -f docker-compose.yml down

restart: down up
