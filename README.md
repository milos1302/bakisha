# Bakisha

## Project Setup

1. Install [Docker](https://docs.docker.com/install/) (and if you're on Linux, install [Docker Compose](https://docs.docker.com/compose/install/) as well)
2. Copy `example.env` file from the root directory, paste it under the same directory and rename it to `.env`. 
3. Uncomment `DB_USERNAME` and `DB_PASSWORD` in `.env` and set their values to any of your choice.
4. **[Optional]** Setup pgAdmin:
    - Uncomment `pgadmin` service configuration in `docker-compose.yml`
    - Uncomment `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` in `.env` and set their values to any  of your choice.
    - pgAdmin will be available at [localhost:8888](http://localhost:8888/) once you finish with the entire project setup
5. Go to projects root directory and run:

   `docker-compose up` or `docker-compose up -d` (detach mode)

6. Site is now available at [localhost:8000](http://localhost:8000/)

### pgAdmin
If you skipped the optional setup of pgAdmin in **Project Setup**, you can still do it afterwards.

If the containers are running, just stop them with `docker-compose stop` (if you're not running them in detach mode, just press `CTRL + C`).
Now, complete **4th** and **5th** step in **Project Setup**, and after you finish, pgAdmin will be available at [localhost:8888](http://localhost:8888/).

In order to connect to the database server, you will have to add a new server:
- Go to [localhost:8888](http://localhost:8888/)
- Click on **Add New Server** (under ***Quick Links***)
- Choose a name fot the server (General > Name)
- Go to Connection tab and provide the necessary information:
    - Host name/address: `postgres`
    - Port: `5432`
    - Username: `DB_USERNAME` value defined in `.env`
    - Password: `DB_PASSWORD` value defined in `.env`     
- Click on **Save** and the server should now appear under the **Servers** on the left
