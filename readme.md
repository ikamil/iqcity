# iqcity
---
A monitoring and data analysis system for the "SMART CITY" project, designed for automated collection of IQ index data. It enables collecting and analyzing data to calculate the IQ score of a territorial unit both in automatic mode and in operator mode with manual data upload.

To run PostgreSQL on a non-standard port (54321 in the example), first comment out the relevant line in docker-compose, run it once to initialize the directory, then stop it with `docker-compose down`, uncomment the PostgreSQL config file line, and start it again with `docker-compose up -d`.

After installation, you need to create connections for `s3_default` (AWS secret and key) and `pg_default` (PostgreSQL login and password) on the container running on port 8080, via the Admin -> Connections menu.
