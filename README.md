# django_tdd_recipe_app
Django recipe app using tdd, github actions and docker compose.

# Technologies
Python web framework
Handles
    URL Mappings
    Object Relational Rapper
    Admin site
Django REST framework
    Django add-on
    Build REST API's
PostgreSQL
    Database (my favorite DB)
Docker
    This is going to be a dockerised environment
    Development and Deployment
Swagger
    Documentation (automated Docs)
    Browsable API (TESTING)
GitHub Actions
    Automation
        Testing and linting
        Similar to Travis-CI, Jenkins, GitLab CI/CD
        Run jobs when code changes
        Automating tasks
        Common uses:
            Deployment
            Code linting
            Unit test


Apps
    * in order to create apps the right way to do it is
      docker-compose run --rm app sh -c "python manage.py startapp appName"
    * app/ - Django project
    * app/core/ - Code shared between multiple apps
    * app/user/ - User related code (user registration or AuthTokens)
    * app/recipe/ - recipe related code

Unit Tests
    Code which tests code
        Sets up conditions / inputs
        runs a piece of code
        checks outputs with "assertions"
    Benefits
        Ensures code runs as expected
        Catches bugs before prod
        Improves reliability
    Steps should be
        Write Test
        Run test expected to fail
        Add feature
        Run test expected to pass
        re-factor if needed and run tests again


Why user Docker?
    Consistent dev and prod environment
    Easier collaboration (really man, this works wonders in Mac for some reason, I've had issues in linux)
    You can have Different versions of
        Python
        Database
        SDK
    Capture all dependencies as code
        Python requirements
        Operating system dependencies
    Easier cleanup

How we'll use Docker
    Define Dockerfile
        Contains all the operating system level dependencies that our project needs
    Create Docker Compose configuration
        Tells Docker how to run the images that are created from our docker file configuration
    Run all commands via Docker compose

Docker on GitHub Actions
    Docker hub introduced rate limit
        100pulls/6h for unauthenticated users

Using Docker Compose
    Run all commands through Docker Compose
        - docker-compose run --rm app sh -c "python manage.py collectstatic"
        - docker-compose Runs a docker compose command
        run WILL start a specific container defined in config
        "--rm" removes the container (optional, removes container after it finish running)
        "app" is the ame of the service
        "sh -c" passes in a shell command

Stuff:
    Docker Access token is in secrets

    hub.docker.com has all the base images, for example
    python, with all the image tags
    3.9-alpine3.13
    is the name of the tag
    alpine is the lightweight version of linux, it's striped of
    everything you don't need

    docker:
        docker build .
    docker-compose:
        docker-compose build
        docker-compose up (to create our container and get our app up and running)


    django and compose:
        docker-compose run --rm app sh -c "flake8"
        docker-compose run --rm app sh -c "python manage.py test"
        docker-compose run --rm app sh -c "python manage.py startapp appName"
        docker-compose run --rm app sh -c "python manage.py createsuperuser"
        docker-compose run --rm app sh -c "django-admin startproject app ."
        the little "." at the end is telling it to create the files
        inside our alredy created "app" folder, otherwise it will create anotherone and we'll have conflicts.
        the way it was able to sinc is through the volumen inside our docker-compose.yml
        everything we create inside our project gets inside our conteiner and everything we create inside our container gets created in our local env


    GitHub Actions:
        Trigger > our trigger will be a push to GitHub
        Job > Run unit tests > Results
        Create a config file at .github/workflows/checks.yml
            Set trigger
            Add steps for running testing and linting
        Configure Docker hub auth


    Testing:
        Import test class:
            SimpleTestCase: No DB
            TestCase: testing with DB
        Import obj to test
        Define Test Class
        Add test_ method
        Setup inputs
        Execute code to be tested
        Check output
        To Run:
            docker-compose run --rm app sh -c "python manage.py test"
        Public tests:
            Unauthenticated requests(Registering a new user for example)
        Private tests:
            Authenticated requests(Update an existing user)
        
    Mocking:
        Override or change behaviour of dependencies
        Avoid unintended side effects
        Isolate code being tested
        REWATCH FROM MOCKING PART
    Testing APIs:
        REWATCH TESTING WEB APPS

    DATABASE:
        PostgreSQL
            Popular open source DB
            Integrates well with Django
            It's supported by Django
        Set a depends_on:
            in the docker compose
        db:
            image:postgress:13-alpine
        Volumes
            This is how we store persistent data
            maps directory in container to local machine until we clear it if we want to
            THIS NEEDS IT'S OWN BLOCK in docker-compose
                dev-db-data: is populated automatically
            the data inside db  dev-db-data:/var etc.
            is in the documentation
        You need to configure Django
            telling it how to connect
        Install DB adaptor dependencies
            install the tools django uses to connect
            required inside our docker conteiner
        Update Python requirements
            with the Postgres adapter
        Django needs to know...
            Engine(type of db) - > Postgres
            Hostname(IP or domain name for database)
            Port(default port for postgres == 5432)
            DB Name (it can have multiple DB's inside)
            Username
            Password
            all this we do in the DABASES inside settings.py, we're gonna be pulling this info from environment variables
            Environment variables
                Pull config values from environment variables
                Easily passed to Docker
                Used in local, dev or prod
                Single place to configure project
                Easy to do with python
                ej. os.environ.get('DB_HOST')
        Psycopg2
            the package that we need in order for Django to connect to our DB
            Most popular PostgreSQL adaptor for python
            Supported by Django oficially
            psycopg2-binary
                OK for development
                not good for prod
                since it's optimized for the OS that is running on.
            psycopg2
                Compiles from source (code)
                you need certain dependencies for it to work, we're using this one.
        Installing Psycopg2
            List of package dependencies in docs
                C compiler
                python3-dev
                libpq-dev
            Equivalent package for Alpine
                postgresql-client
                build-base
                postgresql-dev
                musl-dev
            Found by searching and trial and error FML
            Docker best practice
                Clean up build dependencies
                That means we're gonna customize our docker file so that we clean up the packages after using them to keep up Alpine lightweight.
            In order to install Psycopg2
            first you need to update the requirements if needed with
            psycopg2>=2.8.6,<2.9
            then>
            docker-compose down
            to clear the containers there
            docker-compose build
            and now it's installed

        Fixing Database race condition
            Problem with docker-compose is that it
                It's using depends_on ensures services starts
                    but it DOESN'T ensure the application is running

            The race condition comes up when our app starts before our db therefore crashing the app, we need to create a command that specifies django to wait_for_db to be up
            This is a custom management command
            Make Django "wait_for_db"
                Check for db availability
                Continue when db ready
            Create a custom Django management command
                Docker-compose makes sure the db starts first and then make the app wait for the db to be ready instead of straigth up crashing
            When is this an issue?
                When we're running docker-compose locally
                Running on deployed environment

            Time to create the core app if it's not there:
            docker-compose run --rm app sh -c "python manage.py startapp core"
            delete:
                tests
                views
            create:
                tests directory with __init__.py
                add it in installed_apps
                management directory with __init__.py
                    commands directory with __init__.py
                        and here we create wait_for_db.py
                        there are docs for creating commands

    Django ORM
        Object relational mapper (ORM)
        Abstraction layer of data
            Django handles database structure and changes the db for you

    Api Documentation:
        What to document?
            Everything needed to use the API
            Available endpoints (paths)
                /api/recipes
            Supported methods
             GET, POST, PUT, PATCH, DELETE
            Format of payloads(inputs)
                Parameters
                Post JSON format
            Format of responses(outputs)
                Response Json format
            Authentication process

        Option for docs
            Manual
                Word doc
                Markdown
            Automated
                Use metadata from code (comments)
                Generate documentation pages

        Docs in drf
            Auto generate docs(with third party library)
                drf-spectacular
            Generates schema
            Brosable web interface
                Make test requests
                Handle auth
            How it works!!
                Generate "schema" file
                Parse schema into GUI
            OpenAPI Schema
                Standard for describing APIs
                Popular in industry
                Supported by most API docs tools (we're using swagger)
                Uses popular formats: Yaml/json
            Using a Schema
                Download and run in local Swagger instance
                Serve Swagger with API

        Option for docs
            Manual
                Word doc
                Markdown
            Automated
                Use metadata from code (comments)
                Generate documentation pages

        Docs in drf
            Auto generate docs(with third party library)
                drf-spectacular
            Generates schema
            Brosable web interface
                Make test requests
                Handle auth
            How it works!!
                Generate "schema" file
                Parse schema into GUI
            OpenAPI Schema
                Standard for describing APIs
                Popular in industry
                Supported by most API docs tools (we're using swagger)
                Uses popular formats: Yaml/json
            Using a Schema
                Download and run in local Swagger instance
                Serve Swagger with API
        Add it to settings.py
        Resources
            https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation

    User API
        User registration
        Creating auth token (login system)
        Viewing/updating profile

        # admin for this will be in the core app, just like the migrations

        Endpoints
            user/create/
                post - Register a new user
            user/token/
                post - Create new token
            user/me/
                put/patch - Update profile
                get - View profile
        Serializers with some special **kwargs

        Authentication
            Type of Auth
                Basic
                    Send username and password with each request (http basic)
                    for every request you make.
                Token
                    Use a token in the http header, you generate a token from the users email
                    and password, including that token for every request.
                Json Web Token(JWT)
                    Same as above but different (?), Use an access and refresh token, this is an advance type of auth, requires external libraries to get it runnin'
                Session
                    Use cookies, it's the common way to auth websites, django uses it, to my knowledge
                
                This app uses Token auth, since it has some kind of balance of simplicity and security, not the most secure, but it's good enough, it's supported by DRF so we don't have to install anything else, and it's supported by most clients

                How it works?
                    start by creating a token providing an endpoint that accepts -> post username/password and then that creates a token in our DB returning it to our client, saving it for later use(most likely in the local storage, session storage, cookies), and then every request that the client makes to the api's that needs to be authenticated will include this token in the http headers of the requests.
                    Pros
                        Supported out of the box
                        Simple to use
                        Supported by most
                        Avoid sending username/password each time
                    Cons
                        Token needs to be secured
                        Requires DB requests, almost never a problem... unless you are working for a million dollar company, you might want to use JWT
                
                    Loggin out
                        Happens on the client side
                        Delete token


    Requirements.txt something new
        Run a > docker-compose build
    urls:
        base > 127.0.0.1:8000/admin
        swagger > api/docs/