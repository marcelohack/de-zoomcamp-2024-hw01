## Question 1. Docker tags

```console
❯ docker run --help | grep "Automatically remove the container when it exits"
      --rm                             Automatically remove the container when it exits
```

## Question 2. Docker run: version of wheel

```console
❯ docker run --rm -it python:3.9 /bin/bash
root@a51a4451d6b9:/#
root@a51a4451d6b9:/#
root@a51a4451d6b9:/# pip list
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0

[notice] A new release of pip is available: 23.0.1 -> 23.3.2
[notice] To update, run: pip install --upgrade pip
root@a51a4451d6b9:/#
root@a51a4451d6b9:/#
root@a51a4451d6b9:/# exit
exit
```

## Question 3. Count records

How many taxi trips were totally made on September 18th 2019?

```console
SELECT
    COUNT(*)
FROM
    green_taxi_trips g
WHERE 
    -- CAST(g.lpep_pickup_datetime AS DATE) = '2019-09-18'
    CAST(g.lpep_pickup_datetime AS DATE) = '2019-09-18 00:00:00'
    -- DATE_TRUNC('DAY', g.lpep_pickup_datetime) = '2019-09-18'
    AND CAST(g.lpep_dropoff_datetime AS DATE) = '2019-09-18'

// 15612
```

## Question 4. Largest trip for each day
Which was the pick up day with the largest trip distance Use the pick up time for your calculations.

```console
SELECT
    DATE_TRUNC('DAY', g.lpep_pickup_datetime) AS day,
    SUM(g.trip_distance) AS total_distance
FROM
    green_taxi_trips g 
GROUP BY
    1
ORDER BY total_distance DESC
LIMIT 1

// 2019-09-26 00:00:00	58759.9400000002
```

## Question 5. Three biggest pickups
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

```console
SELECT
    SUM(g.total_amount),
    z."Borough" AS location
FROM
    green_taxi_trips g 
    INNER JOIN zones z ON (g."PULocationID" = z."LocationID")
WHERE
    CAST(g.lpep_pickup_datetime AS DATE) = '2019-09-18'
    AND z."Borough" != 'Unknown'
GROUP BY
    location
HAVING
    SUM(g.total_amount) > 50000
ORDER BY 1 DESC
LIMIT 3

//
96333.2399999993	Brooklyn
92271.29999999847	Manhattan
78671.70999999887	Queens
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

Note: it's not a typo, it's tip , not trip

```
SELECT
    MAX(g.tip_amount),
    zdo."Zone" AS dropoff_zone
FROM
    green_taxi_trips g 
    INNER JOIN zones zpu ON (g."PULocationID" = zpu."LocationID")
    INNER JOIN zones zdo ON (g."DOLocationID" = zdo."LocationID")
WHERE
    (EXTRACT('month' FROM CAST(g.lpep_pickup_datetime AS DATE)),
    EXTRACT('year' FROM CAST(g.lpep_pickup_datetime AS DATE)))=(9,2019)
    AND LOWER(zpu."Zone") = 'astoria'
GROUP BY
    dropoff_zone
ORDER BY 1 DESC
LIMIT 1

// 62.31	JFK Airport
```

## Question 7. Terraform
After updating the main.tf and variable.tf files run:

```console
terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "australia-southeast1"
      + max_time_travel_hours      = (known after apply)
      + project                    = "de-zoomcamp-365521"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "AUSTRALIA-SOUTHEAST1"
      + name                        = "de-zoomcamp-365521-data-lake"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_storage_bucket.demo-bucket: Creation complete after 2s [id=de-zoomcamp-365521-data-lake]
google_bigquery_dataset.demo_dataset: Creation complete after 3s [id=projects/de-zoomcamp-365521/datasets/trips_dataset]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```