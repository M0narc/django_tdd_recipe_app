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
            REWATCH
        
    urls:
        base > 127.0.0.1:8000