# VTaraAppBackend
Backend for VTara - Automotive Threat Analysis and Risk Assessment Tool


# Docker COmmand

docker run --name vtara-db -e POSTGRES_USER=vtara_user -e POSTGRES_PASSWORD=securepass -e POSTGRES_DB=vtara_db -p 5432:5432 -v ~/vtara_pgdata:/var/lib/postgresql/data -d postgres:latest

# For the first time

poetry run flask db init
poetry run flask db migrate -m "Add Project model"
poetry run flask db upgrade

poetry install
poetry run python run.py


poetry run flask db revision -m "Clean all tables"



TRUNCATE TABLE edge RESTART IDENTITY CASCADE;
TRUNCATE TABLE node RESTART IDENTITY CASCADE;
TRUNCATE TABLE "group" RESTART IDENTITY CASCADE;
TRUNCATE TABLE project RESTART IDENTITY CASCADE;