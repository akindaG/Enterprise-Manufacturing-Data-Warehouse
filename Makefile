install:
	python -m pip install -r requirements.txt

test:
	python -m pytest

run-1:
	python -m etl_pipeline.run_etl --source-dir source_data/run_1 --run-date 2026-08-01

run-2:
	python -m etl_pipeline.run_etl --source-dir source_data/run_2 --run-date 2026-08-15

dashboard:
	streamlit run dashboard/app.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-reset:
	docker compose down -v
