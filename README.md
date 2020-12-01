# iqcity

The system for monitoring and analyzing data of the "SMART CITY" project for automated processing of the cities IQ index.
Allows ingesting and analyzing data to calculate the IQ index of a territorial unit both in automatic mode and in operator mode using cloud data uploading xlsx files with any structure and key columns.

To be able to run postgresql on a non-standard port (54321 in the example), you must first comment out this conf file's volume mapping line in docker-compose, run first time to initialize the PostgreSQL directory, then stop docker-compose down, uncomment this line with the PostgreSQL config file, and run docker-compose up -d again.

After installation, you need to create connections to S3, named s3_default (AWS secret and key) and PostgreSQL named pg_default (logins and passwords for postgres).
This must be done on the container with port http:://localhost:8080 Airflow web admin pane, in the Admin -> Connections menu.



Система мониторинга и анализа данных проекта «УМНЫЙ ГОРОД» для автоматизированного сбора данных индекса IQ позволяет собирать и анализировать данные для расчета IQ территориальной единицы как в автоматическом режиме так и в режиме оператора и загрузки данных

Для возможности запустить postgresql на нестандартном порту (54321 в примере) нужно сначала закомментировать эту строку в docker-compose, запустить 1 раз для инициализации директории, затем остановить docker-compose down, раскомментировать строку с конфиг-файлом PostgreSQL, и запустить docker-compose up -d

После установки, необходимо создать подключения к s3_default (AWS секрет и ключ) и pg_default (логины и пароли на постгрес) на контейнере с портом 8080, в меню Admin -> Connections
