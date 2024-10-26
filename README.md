# Freelance Service Marketplace

# Table of Contents

1. [Project Overview](#project-overview)
2. [Purpose](#purpose)
3. [Technologies](#technologies)
   - [Requirements](#requirements)
   - [Production](#production)
   - [Development](#development)
4. [Environment Variables](#environment-variables)
   - [Required Variables](#required-variables)
   - [Configuration File](#configuration-file)
5. [Project Structure](#project-structure-)
   - [Core Directories](#core-directories)
   - [Django Settings](#django-settings)
6. [Authentication](#authentication)
7. [APIs](#apis)
   - [Authentication](#authentication-1)
   - [User Management](#user-management)
   - [Categorization](#categorization)
   - [Consultation](#consultation)
   - [API Documentation](#api-documentation)
8. [Deployment](#deployment)
   - [Deployment Script](#deployment-script)
   - [Docker Compose Configuration](#docker-compose-configuration)
   - [Nginx Configuration](#nginx-configuration)
   - [Gunicorn Configuration](#gunicorn-configuration)
   - [Django Settings Configuration](#django-settings-configuration)
9. [Integrations](#integrations)
   - [Emails](#emails)
   - [Storage](#storage)
   - [Zoom](#zoom)
10. [Code Quality](#code-quality)
    - [Formatting](#formatting)
    - [Linter](#linter)
    - [Pre-Commits](#pre-commits)
    - [VSC Configuration](#vsc-configuration)
11. [CI/CD](#cicd)
12. [Setup](#setup)
    - [Clone the Repository](#clone-the-repository)
    - [Set Up a Virtual Environment](#set-up-a-virtual-environment)
    - [Install Pre-Commit Hooks](#install-pre-commit-hooks)
    - [Build and Run the Docker Containers](#build-and-run-the-docker-containers)
    - [Enter the Webapp Container](#enter-the-webapp-container)
    - [Run Migrations](#run-migrations)
    - [Collect Static Files](#collect-static-files)
13. [Tests](#tests)
    - [Fixtures](#fixtures)
    - [Run](#run)
    - [Coverage](#coverage)
14. [Sources](#sources)


## Project Overview

This project is a Django-based service marketplace where freelancers can list their services, and clients can search for and hire them. It features functionalities such as service booking, user management, and search capabilities, demonstrating how Django can be used to build a comprehensive e-commerce platform. The application provides a practical example of integrating various components to create a fully operational web service.

## What is it for?
The primary purpose of this project was to enhance my skills in organizing code effectively within a web application. By working on this project, I aimed to learn and apply best practices for structuring and maintaining Django applications. Additionally, I focused on deploying the application and preparing it for production environments, which included configuring Docker for containerization and using Docker Compose for managing services. The project also involved integrating with external APIs and services to enrich functionality 

This experience has been invaluable in understanding how to manage code efficiently, ensuring better scalability, maintainability, and successful deployment in real-world scenarios.


## Technologies

This project leverages a variety of tools and libraries to ensure both development and production environments are optimized and maintainable. Dependencies are managed with Pipenv, which simplifies the installation and management of packages, and ensures a consistent development environment.

### Requirements

All dependencies for this project, including both production and development packages, are managed using Pipenv. Pipenv simplifies the process of installing and managing dependencies, as well as creating a virtual environment for the project.

This project is configured to use **Python 3.12**, as specified in the **Pipfile**. Ensure you have this version installed on your system to avoid any compatibility issues. **Pipfile.lock** file ensures that all dependencies are installed in their exact versions

### Production

In a production environment, the following packages and tools are used:

- **Django REST Framework SimpleJWT**: Provides JSON Web Token authentication for Django REST Framework.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX that serves the Django application.
- **WhiteNoise**: Helps serve static files directly from the application, reducing dependency on a separate web server.
- **psycopg2**: PostgreSQL adapter for Python, used to interact with PostgreSQL databases.
- **django-filter**: Adds filtering capabilities to Django REST Framework.
- **httpx**: A fully featured HTTP client for Python 3, used for making HTTP requests.
- **boto3**: Amazon Web Services (AWS) SDK for Python, used for interacting with AWS services.
- **drf-spectacular**: Generates OpenAPI 3.0 schemas for Django REST Framework.

### Development

For development, the following tools and libraries are included:

- **flake8**: A linting tool for Python that checks for style violations.
- **flake8-bugbear**: A plugin for flake8 that adds additional checks for common mistakes and code quality issues.
- **black**: An automatic code formatter for Python to enforce consistent code style.
- **pre-commit**: A framework for managing and maintaining multi-language pre-commit hooks.
- **pytest-django**: A plugin for pytest that provides Django-specific testing utilities.
- **factory-boy**: A flexible and easy-to-use library for creating test fixtures.
- **coverage**: A tool for measuring code coverage of Python programs.

## Environment variables

To properly configure and run the application, you need to provide certain environment variables. These variables are essential for integrating with various components and ensuring the application operates correctly. 

### Required Variables

At a minimum, you must define the following variables:
- **DJANGO_DEBUG**: Indicates whether Django should run in debug mode.
- **DOMAIN**: Specifies the domain name for the application.

### Configuration File

You can find a complete list of required environment variables in the `.env.example`file. To set up your environment, follow these steps:

- Create a `.env` file: This file should contain the necessary environment variables for your application. 

- Copy and Edit: Start by copying the `.env.example` file to a new file named `.env`. Then, edit this `.env` file to include your actual environment variables, use command:
    ```
    cp .env.example .env
    ```

- Update with Real Values: Ensure that you replace placeholder values with the real values specific to your environment.


## Structure

There are two core directories in this project:
 - **apps/** - consists of all separated django applications:
    - **api**: handles the creation and management of RESTful API endpoints for the project.
    - **authentication**: manages user authentication, registration, and login processes.
    - **categorization**: handles the organization and categorization of content within the application.
    - **common**: provides shared utilities, models, and functions used across multiple apps.
    - **consultations**: manages the scheduling, booking, and management of consultations or appointments.
    - **core**: contains the central configurations and settings for the entire project.
    - **emails**: manages the creation, sending, and tracking of email communications.
    - **integrations**: handles integrations with third-party services and APIs.
    - **storages**: manages file storage and media handling within the application.
    - **users**: manages user profiles, permissions, and related functionality.

 - **config/** - contains core Django project settings:
    - **django/** - separated configurations for running django in production or testing environment:
        - **base.py**: contains the common settings and configurations that are shared across all environments
        - **production.py**: includes settings specifically tailored for running the Django application in a production environment, such as security settings and database configurations.
        - **test.py**: defines settings optimized for running tests, often including configurations for in-memory databases and other testing tools to ensure fast and isolated test runs.
    - **settings/** - setting file for each additional configuration:
        - **email_sending.py** - contains settings and configurations related to sending emails, such as SMTP server details, email templates, and other related options.
        - **storages.py** - manages configurations for file storage, including settings for media and static files, as well as any integration with external storage services like AWS S3 or Google Cloud Storage.
        - **zoom_meetings.py** - handles settings and. API integrations necessary for managing Zoom meetings, including authentication credentials and meeting-related configurations.

## Auth
This project uses JWT for authentication, facilitated by the rest_framework_simplejwt library. The authentication endpoints are configured to handle user login and token refresh operations:

```python
auth_patterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]
```

To access protected resources, include the access token in the Authorization header of your HTTP requests as a Bearer token in this format:

```
Bearer <your-access-token>
```

## APIs

This Django project provides several API endpoints organized into different categories and documentation tools to facilitate development and testing.

**Authentication**

- `/auth/`: Includes endpoints for user authentication, such as login and token management. This is configured in the `apps.authentication.urls` module.

**User Management**

- `/users/`: Manages user-related operations, such as user profiles and account details. This is configured in the `apps.users.urls` module.

**Categorization**

- `/categorization/`: Handles operations related to categorizing services or items. This is configured in the `apps.categorization.urls` module.

**Consultation**

- `/consultations/`: Manages consultations and related operations. This is configured in the `apps.consultations.urls` module.

**API Documentation**

The project includes automatic API documentation via `drf-spectacular`:

- **Schema Endpoint** (`/schema/`): Provides the OpenAPI schema for the project.
- **Swagger UI** (`/schema/swagger-ui/`): Offers an interactive Swagger UI interface for exploring and testing the API endpoints.
- **ReDoc** (`/schema/redoc/`): Provides an alternative ReDoc interface for viewing the API documentation.

These documentation endpoints are configured to help developers easily explore and understand the API structure and available endpoints.

## Deployment

Deploying this application involves a series of automated steps designed to streamline the process. The deployment setup includes a script, Docker Compose configuration, and various configuration files to ensure the application runs smoothly in a production environment.

### Deployment Script

The `deploy_script.sh` script automates the deployment process. It performs the following steps:

- Pulls the latest code from the repository.
- Builds Docker images using `docker-compose`.
- Stops and removes any existing containers.
- Starts new containers.
- Runs database migrations.

### Docker Compose Configuration

**`docker-compose.yml`**:

This file defines services for `postgres`, `app`, and `proxy`. Ensure to set the following environment variables for your production environment:

- `POSTGRES_DB`: The name of your PostgreSQL database.
- `POSTGRES_USER`: The PostgreSQL user.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL user.
- `DJANGO_SECRET_KEY`: The secret key for Django.
- `DJANGO_ALLOWED_HOSTS`: The list of allowed hosts for Django.
- `DOMAIN`: The domain name for your application.

### Nginx Configuration

`default.conf.tpl`:

This file configures Nginx as a reverse proxy. Ensure to:

- Set the `DOMAIN` variable to your domain name.
- Uncomment the SSL configuration if you require HTTPS.

### Gunicorn Configuration

`gunicorn.conf.py`:

This file configures Gunicorn to serve the Django application. Adjust the settings as needed for your production environment.

### Django Settings Configuration

The production settings file utilizes several environment variables to configure Django:

- `SECRET_KEY`: Retrieved from `DJANGO_SECRET_KEY`. This is a critical setting for Django's cryptographic signing.
- `ALLOWED_HOSTS`: Defined by the `DJANGO_ALLOWED_HOSTS` environment variable. This specifies the list of host/domain names that this Django site can serve.
- `CORS_ALLOW_ALL_ORIGINS`: Set to `False` to prevent allowing all origins by default.
- `CORS_ORIGIN_WHITELIST`: Defined by `DJANGO_CORS_ORIGIN_WHITELIST`, which is a list of allowed origins for CORS requests.

Additionally, you can configure additional security settings (commented out in the code):

- `SECURE_PROXY_SSL_HEADER`: If using HTTPS, set to enforce HTTPS redirection.
- `SECURE_SSL_REDIRECT`: Redirect HTTP to HTTPS.
- `SECURE_CONTENT_TYPE_NOSNIFF`: Enforce content-type sniffing.

Ensure these environment variables are set appropriately in your production environment to maintain security and proper functionality.

## Integrations

This project integrates with several services to enhance its functionality and performance. These integrations include email delivery options, media storage solutions, and Zoom API connectivity. Each integration is configured through environment variables and provides flexibility for different deployment environments.

### Emails

This project includes configurable email backend settings that allow for flexible email delivery options based on the environment. The email backend can be configured to use different strategies depending on the environment variables set.

#### Email Sending Strategies

The email sending strategy is determined by the `EMAIL_SENDING_STRATEGY` environment variable. It can be set to either `"console"` or `"smtp"`, which affects how emails are handled:

- **Console Email Backend**  
  If `EMAIL_SENDING_STRATEGY` is set to `"console"`, the application uses Django's built-in console email backend (`django.core.mail.backends.console.EmailBackend`). This backend outputs email content to the console, which is useful for development and debugging purposes.

- **SMTP Email Backend**  
  If `EMAIL_SENDING_STRATEGY` is set to `"smtp"`, the application uses Django's SMTP email backend (`django.core.mail.backends.smtp.EmailBackend`). This backend sends emails using an SMTP server. The following SMTP settings are configured via environment variables:

  - `EMAIL_HOST`: The SMTP server host.
  - `EMAIL_USE_TLS`: A boolean indicating whether to use TLS (default is `False`).
  - `EMAIL_USE_SSL`: A boolean indicating whether to use SSL (default is `True`).
  - `EMAIL_PORT`: The port used for the SMTP server.
  - `EMAIL_HOST_USER`: The username for the SMTP server.
  - `EMAIL_HOST_PASSWORD`: The password for the SMTP server.

### Environment Variable Configuration

The settings are dynamically loaded from environment variables using utility functions (`env_to_enum` and `env_to_bool`) to convert and validate the configuration values. Ensure that the relevant environment variables are set according to your deployment environment to properly configure the email backend.

This setup allows for easy switching between different email delivery methods, facilitating development, testing, and production deployments.

### Storage

This project supports media storage using AWS S3, allowing for scalable and reliable file management. The integration is configurable through environment variables to switch between local storage and S3 storage based on the deployment requirements.

#### Storage Strategies

The application can be configured to use either local storage or AWS S3 for handling media files. The storage type is determined by the `STORAGE_TYPE` environment variable:

- **Local Storage**  
  If `STORAGE_TYPE` is set to `"local"`, media files are stored locally on the server. The media files are saved in a directory named `"media"` located at the project's base directory. The `MEDIA_ROOT` and `MEDIA_URL` settings are configured to serve the media files from this local directory.

- **S3 Storage**  
  If `STORAGE_TYPE` is set to `"s3"`, the application uses AWS S3 for storing media files. The necessary AWS credentials and bucket information are configured through the following environment variables:
  - `AWS_S3_ACCESS_KEY_ID`: The access key ID for AWS.
  - `AWS_S3_SECRET_ACCESS_KEY`: The secret access key for AWS.
  - `AWS_S3_BUCKET_NAME`: The name of the S3 bucket where media files will be stored.

#### Development Mode

For development purposes, the project supports local file operations. This can be useful for testing and debugging without requiring AWS S3 integration. The following functions handle file operations in a local development environment:

- `file_name_generate(extension: str = ".txt") -> str`  
  Generates a unique file name with a specified extension using UUIDs. This ensures that each file name is unique.

- `text_to_file_local_upload(*, file_name: str, content: str) -> None`  
  Saves text content to a local file. If a file with the same name already exists, it will be deleted before saving the new content.

- `local_file_get_content(*, file_name: str) -> str`  
  Reads and returns the content of a local file. This function opens the file and decodes its content to a string.

When handling file operations, the application checks the `STORAGE_TYPE_STRATEGY` setting to determine the appropriate storage method:

- **S3 Storage**  
  If `STORAGE_TYPE_STRATEGY` is set to `StorageType.S3`, files are uploaded to and retrieved from AWS S3 using the functions `text_to_file_upload` and `file_get_content`.

- **Local Storage**  
  If `STORAGE_TYPE_STRATEGY` is set to `StorageType.LOCAL`, files are handled locally using the functions `text_to_file_local_upload` and `local_file_get_content`.

#### Example Usage

Here is an example of how the application decides between local and S3 storage based on the storage type configuration:

```python
if settings.STORAGE_TYPE_STRATEGY == StorageType.S3:
    text_to_file_upload(file_name=file_name, content=content)
else:
    text_to_file_local_upload(file_name=file_name, content=content)
```

### Zoom

This project integrates with the Zoom API to manage Zoom meetings programmatically. It uses Zoom's OAuth 2.0 authentication and the Zoom REST API to create and manage meetings.

#### Configuration

The integration is configured using environment variables. Ensure the following environment variables are set:

- `ZOOM_ACCOUNT_ID`: Your Zoom account ID.
- `ZOOM_CLIENT_ID`: Your Zoom OAuth client ID.
- `ZOOM_CLIENT_SECRET`: Your Zoom OAuth client secret.

#### Zoom Credentials

The `ZoomCredentials` class is used to store and manage Zoom API credentials. These credentials are loaded from environment variables and are used to authenticate API requests.

#### OAuth Token

The `_get_oauth_token` function retrieves an OAuth token required for making authorized API requests to Zoom. It uses the client credentials (client ID and client secret) to obtain the token via Zoom's OAuth endpoint. The token is then used in subsequent API requests to authenticate.

#### Meeting Management

- **Create a Meeting**  
  The `create_meeting` function schedules a new Zoom meeting. It requires the following parameters:
  - `topic`: The topic of the meeting.
  - `start_time`: The start time of the meeting in UTC.
  - `duration`: The duration of the meeting in minutes.

  This function sends a request to Zoom's API to create a scheduled meeting. It returns a `MeetingDetails` object containing information about the newly created meeting, such as the meeting ID, join URL, and start URL.

## Code Quality

Maintaining high code quality is crucial for a reliable and maintainable project. We utilize several tools and configurations to ensure our code meets quality standards.

### Formatting

For automatic code formatting we use **Black**. It helps in maintaining consistent code style across the project. To format your code, ensure that Black is configured in your development environment to format code automatically upon saving. This can be set up through editor settings.

```
pipenv run black .
```

### Linter

Perform static code analysis with **Flake8**  to enforce coding standards and identify style violations. To check your code, run Flake8 which will analyze your codebase based on the configuration defined in the `.flake8` file. This configuration allows you to customize which errors and warnings to show, as well as specify which files and directories to ignore.

```
pipenv run flake8
```

### Pre-Commits

**Pre-commit** hooks are used to enforce code quality before commits are made. Install these hooks to automatically run code formatting and linting checks before changes are committed. This helps in maintaining code quality throughout the development process. The behavior of these hooks is defined in the `.pre-commit-config.yaml` file, where you can specify which tools (e.g., Black, Flake8) are used and their respective versions.

```
pipenv run pre-commit install
```

### VSC Configuration

For a seamless development experience, configure Visual Studio Code to automatically format code on save. This configuration ensures that all code adheres to the project's formatting rules and helps in maintaining consistency across the codebase. Adjust the settings in the `settings.json` file to integrate with Black, ensuring that code formatting is handled automatically as you write.

By following these guidelines and configurations, you ensure that the codebase remains clean, readable, and maintainable, thereby facilitating a smoother development process.

## CI /CD

The deployment process is automated using GitHub Actions. The workflow is defined in the `.github/workflows/django.yml` file and consists of the following jobs:

- **Build**: 
  - Runs on `ubuntu-latest`.
  - Sets up Python 3.12.
  - Installs dependencies using `pipenv`.
  - Runs code formatter (`black`).
  - Runs linter (`flake8`).
  - Executes tests (`pytest`).

- **Check Secrets**:
  - Runs on `ubuntu-latest`.
  - Verifies the presence of required secrets for deployment:
    - `AWS_HOST_USER`
    - `AWS_EC2_IP_ADDRESS`
    - `EC2_SSH_KEY`
  - Ensures all required secrets are set before proceeding.

- **Deploy**:
  - Runs on `ubuntu-latest`.
  - Depends on the successful completion of the **Check Secrets** job.
  - Checks out the code.
  - Creates an SSH key file from the `EC2_SSH_KEY` secret.
  - Executes the `deploy_script.sh` on the EC2 instance to perform deployment tasks.
  - Cleans up the SSH key file after deployment.

## Setup

- **Clone the Repository**

Start by cloning the repository and navigating to the project directory:

```bash
git clone https://github.com/WojciechKubak/Freelance-Service-Marketplace
cd Freelance-Service-Marketplace
```
- **Set Up a Virtual Environment**

Install the required Python packages and create a virtual environment using pipenv:

```bash
pipenv install
```
- **Install Pre-Commit Hooks**

To ensure code quality and consistency, install the pre-commit hooks:

```bash
pipenv run pre-commit install
```
- **Build and Run the Docker Containers**

Build and start the Docker containers in detached mode:

```bash
docker-compose up -d --build
```
- **Enter the Webapp Container**

To access the web application container for any necessary tasks or debugging, use the following command:

```bash
docker exec -it <container-name> bash
```
- **Run Migrations**

Apply database migrations to set up or update the database schema:


```bash
python manage.py migrate
```
- **Collect Static Files**

Gather all static files into a single location for serving:


```bash
python manage.py collectstatic
```

## Tests

This project primarily uses **pytest** and **pytest-django** for running tests. The testing setup is configured to use an SQLite database, which facilitates running tests both from within a container and locally, without additional GitHub Actions configuration.

**pytest** is configured via the `pytest.ini` file. This configuration includes:

- Logging settings
- Test file identifiers
- The Django settings module used for testing

Key configurations in `pytest.ini` include:
- **Logging**: Provides log output with timestamps and file information.
- **Test File Identifiers**: Specifies which files to consider as test files.
- **Django Settings Module**: Points to `config.django.test` for test-specific settings.

### Fixtures

The `conftest.py` file contains essential fixtures used across tests. Notable fixtures include:

- **Database Access Fixture**: Ensures all tests have database access without explicitly using `pytest.mark.django_db`.

```python
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db) -> None:
    pass
```

 **Authentication Request Fixture**: Facilitates API tests that require authentication by providing a method to create authenticated requests.
```python
 @pytest.fixture(scope="session")
def auth_request() -> Callable[[User, str, str, dict[str, Any] | None], APIRequestFactory]:
    def _make_request(
        user: User, method: str, url: str, data: dict[str, Any] | None = None
    ) -> APIRequestFactory:
        refresh = RefreshToken.for_user(user)
        factory = APIRequestFactory()
        request = getattr(factory, method.lower())(
            url, data, HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )
        return request

    return _make_request
```

### Run
To run the tests, ensure your virtual environment is properly set up and execute:

```bash
pipenv run pytest
```
### Coverage
The project includes a .coverage file for tracking test coverage. To generate a coverage report, use:

```bash
pipenv run coverage run -m pytest
```
For a more detailed, navigable HTML report, generate it with:

```bash
pipenv run coverage html
```

## Resources

- **Django Styleguide** [[ hacksoft-django-styleguide](https://github.com/HackSoftware/Django-Styleguide)]
- **Deployment:** [[deploying-a-django-application-with-docker-nginx-and-certbot](https://medium.com/@akshatgadodia/deploying-a-django-application-with-docker-nginx-and-certbot-eaf576463f19)]
- **Celery with emails** [[ending-django-email-using-celery](https://anshu-dev.medium.com/sending-django-email-using-celery-bf20e07ce04f)]
