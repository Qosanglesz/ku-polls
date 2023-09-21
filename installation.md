## Installation Guideline

1. Git clone repository
    ```
    git clone https://github.com/Qosanglesz/ku-polls.git
    ```
2. Navigate to the project directory
    ```
    cd ku-polls
    ```
3.  Create a virtual environment
    ```
    python -m venv venv
    ```
4.  Activate the virtual environment
    ```
    # activate virtual environment on MAC, LINUX
    source venv/bin/activate

    # activate virtual environment on WINDOW
    venv\Scripts\activate
    ```
5.  Install requirement
    ```
    pip install -r requirements.txt
    ```
5. Setting Environment Variables
    ```
    # coppy sample.env as .env on MAC, LINUX
    cp sample.env .env

    # coppy sample.env as .env on WINDOW
    copy sample.env .env
    ```
6. Set Values for Externalized Variables
    ```
    # edit .env file in BASE directory
    SECRET_KEY=your_secret_key
    DEBUG=True
    ```
7.  Mygrate and loading data
    ```
    # Step 1 migrate.
    python manage.py migrate

    # Step 2 load user data.
    python manage.py loaddata data/users.json

    # Step 3 load polls data.
    python manage.py loaddata data/polls.json
    ```
8. Run test
    ```
    python manage.py test polls
    ```
9.  Runserver
    ```
    python manage.py runserver
    ```