
# Data Engineering Zoomcamp 2024 - Homework 1

## Instructions

1. Create Docker/Postgres data folder:

```console
mkdir -p data/postgres
```
2. Start Docker:

```console
docker compose -f docker/docker-compose.yaml up -d
```

3. Data Ingestion

```console

// Using Python command line

python src/ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --csv="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

python src/ingest_zones.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --csv="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

// Using Docker

docker build -f docker/Dockerfile -t de-zoomcamp-ingest-data .

docker run --network ny_taxi_hw01 --rm de-zoomcamp-ingest-data ingest_data.py \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --csv="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

docker run --network ny_taxi_hw01 --rm de-zoomcamp-ingest-data ingest_zones.py \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --csv="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

```

4. Questions  
Please check the [Homework Execution](./homework_execution.md) document.

5. Terraform  
Please check the **gcp_stack** folder.

6. Stop Docker

```console
docker compose -f docker/docker-compose.yaml down -v
```
