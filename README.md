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