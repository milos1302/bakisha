# Bakisha

<br/>

#### Content:

- [Project Setup](#project-setup)
- [pgAdmin Server](#pgadmin-server)
- [Docker Containers](#docker-containers)

<br/>

### <a name="#project-setup">Project Setup</a>

1. Install [Docker](https://docs.docker.com/install/) (and if you're on Linux, install 
[Docker Compose](https://docs.docker.com/compose/install/) as well).
2. Copy `example.env` file from the root directory, paste it under the same directory and rename it to `.env`. 
3. Uncomment `DB_USERNAME` and `DB_PASSWORD` in `.env` and set their values to any of your choices.
4. Setup pgAdmin: Uncomment `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` in `.env` and set their 
values to any  of your choices.
5. Go to projects root directory and run:

   `docker-compose up` or `docker-compose up -d` (detach mode)

6. Site is now available at [localhost:8000](http://localhost:8000/) and pgAdmin at 
[localhost:8888](http://localhost:8888/).
7. [**Optional**] You may wanna [create a superuser](#create-superuser) to have an access to admin dashboard.  


<br/>


### <a name="#create-superuser">Create Superuser</a>

In order to access admin dashboard you'll need to create a superuser. Open you terminal and make sure that 
***django*** and ***postgres*** containers are running. Now, do the following steps:
 1. SSH into ***djanog*** container: `docker exec -it django bash`
 2. Create a superuser: `python manage.py createsuperuser`
 3. Fill up all the information
 4. Exit the container: `exit`  


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


<br/>


### <a name="#docker-containers">Docker Containers</a>

Docker containers are configured in [docker-composer.yml](/docker-compose.yml) file and all custom Dockerfile(s)
are located in [docker folder](/docker) under the same name as their service (`container_name`) in 
[docker-composer.yml](/docker-compose.yml).
Docker services (containers) used in this project:
- **django** - This docker container is being built with a custom [Dockerfile](/docker/django/Dockerfile) where 
[python:3](https://hub.docker.com/_/python) image is being extended.
This Dockerfile will create django project with the provided [requirements.txt](/app/requirements.txt) file
and it will make and run migrations at the end of the build.
Each start of the django container will start the django server, and django application will be available at 
[localhost:8000](http://localhost:8000/).

- **postgres** ([postgres](https://hub.docker.com/_/postgres) image)
- **pgadmin** ([dpage/pgadmin4](https://hub.docker.com/r/dpage/pgadmin4) image)
