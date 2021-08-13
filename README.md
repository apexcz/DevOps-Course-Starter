# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. 

You also need to create a Trello [account](https://trello.com/signup) and get an [API_KEY and TOKEN](https://trello.com/app-key).Add your Trello key and token in the `.env` file as shown in the `.env.template`
* TRELLO_API_KEY 
* TRELLO_TOKEN

The ToDo App uses the Trello credentials provided to create a Board on Trello called "Tasky_1_2_3_". This is the board used to save the lists of tasks. Please ensure that you have not exhausted your limits of creating new boards.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the tests

To run the unit and integration tests, use the command ``poetry run pytest tests``. This will run any test defined in a function
matching the pattern ``test_*`` or ``*_test``, in any file matching the same patterns, in the ``tests`` directory.

To run the selenium, please ensure to add the selenium chromedriver on your $PATH. Then run, ``poetry run pytest tests_e2e``. Remember, that you must have Chrome web browser installed.

Note that the selenium tests creates a ``DummyBoard`` on Trello which gets deleted after test completion.

## Running on Docker

There are two environments that can be run on docker: development and production. The simplest way to launch the app is by running:
```bash
# To run both development and production
docker-compose up 

# To run only development
docker-compose up todo-development

# To run only production
docker-compose up todo-production
```

Alternatively, you may run the app this way:
### Follow the following steps to run the app in ``development``.

1. cd to the base directory containing the Dockerfile
2. Build an image from the ``development`` stage
```bash
docker build --target development --tag todo-app:dev .
```
3. Create a container from the image created above.
```bash
docker run --env-file .env -p 5001:5000 --mount type=bind,source="$(pwd)",target=/app/ todo-app:dev
```
**Note:** You have to specify the location of your .env file.

### Follow the following steps to run the app in ``production``.

1. cd to the base directory containing the Dockerfile
2. Build an image from the ``production`` stage
```bash
docker build --target production --tag todo-app:prod .
```
3. Launch a container from the image created above.
```bash
docker run --env-file .env -p 5000:5000 todo-app:prod
```