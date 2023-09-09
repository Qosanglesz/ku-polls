## KU Polls: Online Survey Questions 

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
    python manage.py migrate
    python manage.py loaddata data/polls-v1.json
    ```
7.  Runserver
    ```
    python manage.py runserver
    ```

## Demo superuser

|Username|Password|
|:--:|:--:|
|admin|admin|

## Project Documents


All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development plan](https://github.com/Qosanglesz/ku-polls/wiki/Development-Plan)
- [Iteration 1](https://github.com/Qosanglesz/ku-polls/wiki/Iteration-1-Plan)
- [Iteration 2](https://github.com/Qosanglesz/ku-polls/wiki/Iteration-2-Plan)
- [Task](https://github.com/users/Qosanglesz/projects/1/views/2)

[django-tutorial]: TODO-write-the-django-tutorial-URL-here
