<h1 align="center">
JobBlazer - We do the hard work so you don't have to.
  </h1>

## Tracking Project Status - JobBlazer (BackEnd)

## Getting Started

### Prerequisites:

Be sure, you have installed following dependenices installed on your development machine:

- python >= 3.7
- git
- pip
- postgresql

### Installation:

To install Octagon on your local machine, follow these steps:

#### 1. Clone the Octagon BE repository:

    git clone https://github.com/Devsinc-Org/Octagon-BE

#### 2. Familiarize yourself with the following files and directories:

- `requirements.txt`: contains all the dependencies required to run the Django project
- `.env.example`: contains all environment variables required to run the Django project

- `settings/` directory: contains all settings required to run the project on local, development, production, and staging environments

- `base.py`: contains the main settings for Django
- `local.py`: contains the settings for the local database
- `development.py`: contains the settings for the development database
- `production.py`: contains the settings for the production database
- `staging.py`: contains the settings for the staging database

### Usage

To use Octagon, follow these steps:

#### 1. Create and activate virtual environment

##### For linux or macOS

    python3 -m venv venv
    source venv/bin/activate

##### For Windows

    python -m venv venv
    venv/Scripts/activate

#### 2. Install dependencies for django using pip:

    pip install -r requirements.txt

#### 3. Configuration

Rename the `.env.example` file to .env and update the values with your own configuration.

#### 4. Set the environment variable in .env:

    ENVIRONMENT=development

- e.g: ('local', 'development', 'production', 'stagging')

#### 5. Run migrations

    python manage.py makemigrations

Above command will create database migrations

#### 6. Migrate DB Migrations

    python manage.py migrate

Above command will update db schema according to migrations.

#### 7. Running the application

    python manage.py runserver

The application will be available at http://127.0.0.1:8000/

#### Note:

- We need to use the PostgreSQL database because the project has dependencies on it.
