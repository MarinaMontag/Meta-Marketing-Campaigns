# Makefile для управління міграціями та docker-compose

migrate:
	docker compose exec app alembic revision --autogenerate -m "$(m)"

upgrade:
	docker compose exec app alembic upgrade head

current:
	docker compose exec app alembic current

downgrade:
	docker compose exec app alembic downgrade -1

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f app

bash:
	docker compose exec app bash

reset-db:
	docker compose exec mysql mysql -udb_user -pdb_password db_name \
		-e "SET FOREIGN_KEY_CHECKS = 0; \
		TRUNCATE TABLE fact_insights_daily; \
		TRUNCATE TABLE dim_ad; \
		TRUNCATE TABLE dim_adset; \
		TRUNCATE TABLE dim_campaign; \
		SET FOREIGN_KEY_CHECKS = 1;"

initial-upload: reset-db
	docker compose exec app python src/scripts/initial_upload.py