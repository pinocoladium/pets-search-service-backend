TAIL=100

# Переменные, которые используются в скриптах, для использование нужно указать ее при запуске
# Например make logs c=celery

# Переменная "c", для указания с каким контейнером взаимодействовать. По дефолту - django
define set-default-container
	ifndef c
	c = django
	else ifeq (${c},all)
	override c=
	endif
endef


set-container:
	$(eval $(call set-default-container))


build:
	docker compose -f docker-compose.yml build
up:
	docker compose -f docker-compose.yml up --remove-orphans  -d $(c)
down:
	docker compose -f docker-compose.yml down
logs: set-container
	docker compose -f docker-compose.yml logs --tail=$(TAIL) -f $(c)
restart: set-container
	docker compose -f docker-compose.yml restart $(c)
exec: set-container
	docker compose -f docker-compose.yml exec $(c) /bin/bash
remove: set-container
	docker compose -f docker-compose.yml rm -fs $(c)


migrate: set-container
	docker compose -f docker-compose.yml run --rm $(c) bash -c './manage.py migrate'
migrations: set-container
	docker compose -f docker-compose.yml run --rm $(c) bash -c './manage.py makemigrations'
shell: set-container
	docker compose -f docker-compose.yml exec $(c) /bin/bash -c './manage.py shell'

pre-commit: set-container
	docker compose -f docker-compose.yml run --rm $(c) bash -c 'PRE_COMMIT_HOME=.precomcache pre-commit run --all-files'