## KU Polls: Online Survey Questions 
[![Unit Tests](https://github.com/Qosanglesz/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/Qosanglesz/ku-polls/actions/workflows/django.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

1. Git clone repository
    ```
    git clone https://github.com/yourusername/your-project.git
    ```
2. Navigate to the project directory
    ```
    cd ku-polls
    ```
3.  Create a virtual environment (optional)
    ```
    virtualenv venv
    ```
4.  Activate the virtual environment
    ```
    .\venv\Scripts\Activate
    ```
5.  Install requirement
    ```
    pip install -r requirements.txt
    ```
6.  Mygrate and loading data
    ```
    # Step 1 migrate.
    python manage.py migrate

    # Step 2 load user data.
    python manage.py loaddata data/users.json

    # Step 3 load polls data.
    python manage.py loaddata data/polls.json
    ```
7.  Runserver
    ```
    python manage.py runserver
    ```
## Demo User

| Username  | Password        |
|-----------|-----------------|
|   Peach   | @As123456za     |
|   Vader   | @Iamyourfater   |
## Demo superuser

|Username|Password|
|:--:|:--:|
|admin|admin|

## Project Documents


All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Domain Model](https://github.com/Qosanglesz/ku-polls/wiki/Domain-Model)
- [Development plan](https://github.com/Qosanglesz/ku-polls/wiki/Development-Plan)
- [Iteration 1](https://github.com/Qosanglesz/ku-polls/wiki/Iteration-1-Plan)
- [Iteration 2](https://github.com/Qosanglesz/ku-polls/wiki/Iteration-2-Plan)
- [Iteration 3](https://github.com/Qosanglesz/ku-polls/wiki/Iteration-3-Plan)
- [Task](https://github.com/users/Qosanglesz/projects/1/views/2)

[django-tutorial]: TODO-write-the-django-tutorial-URL-here
