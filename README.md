# Bakisha

<br/>

#### CONTENT:

- [Project Setup](#project-setup)
- [Create Superuser](#create-superuser)
- [Docker Containers](#docker-containers)
- [How To Database](#how-to-database)
- [pgAdmin Server](#pgadmin-server)

#### Additional Documentation:
- [PyCharm Configuration](README.pycharm.md)

<br/>

### <a name="#project-setup">Project Setup</a>

1. Install [Docker](https://docs.docker.com/install/) (and if you're on Linux, install 
[Docker Compose](https://docs.docker.com/compose/install/) as well).
2. Copy `example.env` file from the root directory, paste it under the same directory and rename it to `.env`. 
3. Uncomment `DB_USERNAME` and `DB_PASSWORD` in `.env` and set their values to any of your choices.
4. [**Optional**] You can put one or more database dumps in [/docker/postgres/init_db](/docker/postgres/init_db)
and they will be executed in alphabetical order. Keep in mind that you won't be able to do this after the volumes 
for `postgres` container are created. 
5. Setup pgAdmin: Uncomment `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` in `.env` and set their 
values to any of your choices.
6. Go to projects root directory and run:

   `docker-compose up` or `docker-compose up -d` (detach mode)

7. Site is now available at [localhost:8000](http://localhost:8000/) and pgAdmin at 
[localhost:8888](http://localhost:8888/) 
    - refer to [pgAdmin Server](#pgadmin-server) on how to setup the database server at pgAdmin.
8. [**Optional**] You may wanna [create a superuser](#create-superuser) to have an access to admin dashboard
if you didn't provide any initial db dumps that contain this kind of user.  

<br/>


### <a name="#create-superuser">Create Superuser</a>

In order to access admin dashboard we need a **superuser**. If we didn't provide any initial db dumps that 
contain this kind of user, we will need to create it. Open your terminal and make sure that `django` and 
`postgres` containers are running (`docker ps` or `docker container ls` will display all running containers). 
Now, do the following steps:
 1. SSH into `django` container: `docker exec -it django bash`
 2. Create a superuser: `python manage.py createsuperuser`
 3. Fill up all the information
 4. Exit the container: `exit`  

<br/>


### <a name="#docker-containers">Docker Containers</a>

Docker containers are configured in [docker-composer.yml](/docker-compose.yml) file and all custom Dockerfile(s)
are located in [docker folder](/docker) under the same name as their service (`container_name`) in 
[docker-composer.yml](/docker-compose.yml).
Docker services (containers) used in this project:
1. **django** - This docker container is being built with a custom [Dockerfile](/docker/django/Dockerfile) where 
[python:3](https://hub.docker.com/_/python) image is being extended.
This Dockerfile will create the django project with the provided [requirements.txt](/app/requirements.txt) file
and it will make and run migrations at the end of the build.
Each start of the django container will start the django server, and the site will be available at 
[localhost:8000](http://localhost:8000/).

    - Aliases that you can use inside the container:
        - `django` - alias for `python manage.py` 
        - `ll` - alias for `ls -la`

2. **postgres** ([postgres](https://hub.docker.com/_/postgres) image)
3. **pgadmin** ([dpage/pgadmin4](https://hub.docker.com/r/dpage/pgadmin4) image)

<br/>


### <a name="#how-to-database">How to Database</a>

If you put sql script(s) in [/docker/postgres/init_db](/docker/postgres/init_db) directory before running `docker-compose up`
(before the volumes for `postgres` container are created), those sql scripts will execute in alphabetical order.
 After the volumes for `postgres` are created, execution of these scripts will be skipped.
 
 However, if you want to **import** some data after the `postgres` volumes have been created, you can use 
 something like this:
 
    `docker exec -i <postgres_container_name> psql -U postgres -d <database_name> < backup.sql`
 
 Example: `docker exec -i postgres psql -U bakisha_user -d bakisha_db < bakisha.sql`
 
 In this example, `bakisha.sql` script is located in the directory on our local machine from which we
 are executing this command. This script will be executed inside the `postgres` on `bakisha_db` database by 
 the `bakisha` database user. Note that `bakisha_db` needs to exist in order for this command to work.
 
 
 In order to **export** a database, you can something like this:
 
    `docker exec <postgres_container_name> pg_dump -U postgres <database_name> > backup.sql`
 
 Example: `docker exec postgres pg_dump -U postgres bakisha > bakisha.sql`
 
 In the example above, we are creating `bakisha.sql` database dump of `bakisha` database located in
 `postgres` container, and this dump will be located in the directory on our local machine from which we 
 executed this command.
  
<br/>


### <a name="#pgadmin-server">pgAdmin Server</a>

In order to connect to the database server, you will have to add a new server:
- Go to [localhost:8888](http://localhost:8888/)
- Click on **Add New Server** (under ***Quick Links***)
- Choose a name for the server (General > Name)
- Go to Connection tab and provide the necessary information:
    - Host name/address: `postgres`
    - Port: `5432`
    - Username: `DB_USERNAME` value defined in `.env`
    - Password: `DB_PASSWORD` value defined in `.env`     
- Click on **Save** and the server should now appear under the **Servers** on the left

<br/>
    
    
