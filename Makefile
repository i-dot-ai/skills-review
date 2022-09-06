include .envs/web

define _update_requirements
	docker-compose run requirements bash -c "pip install -U pip setuptools && pip install -U -r /app/$(1).txt && pip freeze > /app/$(1).lock"
endef

.PHONY: update-api-requirements
update-api-requirements:
	$(call _update_requirements,requirements)
	$(call _update_requirements,requirements-dev)

.PHONY: reset-db
reset-db:
	docker-compose up --detach ${POSTGRES_HOST}
	docker-compose run ${POSTGRES_HOST} dropdb -U ${POSTGRES_USER} -h ${POSTGRES_HOST} ${POSTGRES_DB}
	docker-compose run ${POSTGRES_HOST} createdb -U ${POSTGRES_USER} -h ${POSTGRES_HOST} ${POSTGRES_DB}
	docker-compose kill
