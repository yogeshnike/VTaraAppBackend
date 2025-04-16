# VTaraAppBackend
Backend for VTara - Automotive Threat Analysis and Risk Assessment Tool


# Docker COmmand

docker run --name vtara-db -e POSTGRES_USER=vtara_user -e POSTGRES_PASSWORD=securepass -e POSTGRES_DB=vtara_db -p 5432:5432 -v ~/vtara_pgdata:/var/lib/postgresql/data -d postgres:latest

# For the first time

poetry run flask db init
poetry run flask db migrate -m "Add Project model"
poetry run flask db upgrade