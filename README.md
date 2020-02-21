# Bakisha

<br/>

#### Content:

- [Project Setup](#project-setup)
- [pgAdmin Server](##pgadmin-server)

<br/>

### <a name="#project-setup">Project Setup</a>

1. Install [Docker](https://docs.docker.com/install/) (and if you're on Linux, install [Docker Compose](https://docs.docker.com/compose/install/) as well)
2. Copy `example.env` file from the root directory, paste it under the same directory and rename it to `.env`. 
3. Uncomment `DB_USERNAME` and `DB_PASSWORD` in `.env` and set their values to any of your choice.
4. Setup pgAdmin: Uncomment `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` in `.env` and set their values to any  of your choice.
5. Go to projects root directory and run:

   `docker-compose up` or `docker-compose up -d` (detach mode)

6. Site is now available at [localhost:8000](http://localhost:8000/) and pgAdmin at [localhost:8888](http://localhost:8888/) 

<br/>

### <a name="#pgadmin-server">pgAdmin Server</a>

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
