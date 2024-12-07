docker-start: sudo docker run -d --name my_db_postgres -e POSTGRES_PASSWORD=083Hdwd3 -e POSTGRES_USER=admin -e POSTGRES_DB=my_first_db -p 5432:5432 postgres
Where:
my_db_postgres - container_name;
POSTGRES_PASSWORD - password for DB;
POSTGRES_USER - username;
POSTGRES_DB - DB's name.
Change everything in config.py
