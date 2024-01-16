# RPG NPC Generator

The RPG NPC Generator is a web application for generating [non-player characters (NPCs)](https://en.wikipedia.org/wiki/Non-player_character) for tabletop role-playing games. The current logic of the app is based on the [Pathfinder 2e](https://en.wikipedia.org/wiki/Pathfinder_Roleplaying_Game) ruleset.

This is a project developed for University of Helsinki [databases & web programming course](https://hy-tsoha.github.io/materiaali/). The main goal of the project was to create a character creator tool without relying on heavy client-side UI frameworks. Instead, the focus was on keeping the technology stack minimal and exploring the capabilities of large language model APIs, such as the ChatGPT API, while leveraging database concepts.

## How it works

The RPG NPC Generator utilizes character templates defined under the `data/character_templates.json` file. These templates serve as the basis for generating characters. When the app is initialized, these templates are inserted into the Postgres database.

When generating a character, the template is cloned, and the character's stats are generated based on the template's stats. This ensures that each character has unique attributes and abilities. In addition to the stats, the generator also leverages AI-generated content to enhance the character's details. AI generated content is powered by [ChatGPT API](https://platform.openai.com/docs/api-reference).

The app also has a character gallery feature that allows users to view and browse the generated characters.

## Stack

### Core technologies:

- [Flask](https://flask.palletsprojects.com/): Lightweight web framework for Python.
- [PostgreSQL](https://www.postgresql.org/): Powerful open-source relational database.
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy): Python SQL toolkit and ORM library.
- [Alembic](https://alembic.sqlalchemy.org/): Database migration tool for SQLAlchemy.
- [Celery](https://docs.celeryq.dev/en/stable/): Distributed task queue framework for Python.
- [Redis](https://redis.io/): In-memory data structure store.
- [Bulma](https://bulma.io/): Modern CSS framework for building user interfaces.

### Linting, formatting and testing:

- [flake8](https://github.com/PyCQA/flake8): Python code linter.
- [isort](https://github.com/PyCQA/isort): Python import sorter.
- [black](https://github.com/psf/black): Python code formatter.
- [djLint](https://www.djlint.com/): Linter and formatter for Jinja2 templates.
- [pytest](https://github.com/pytest-dev/pytest): Testing framework for Python.
- [pytest-cov](https://github.com/pytest-dev/pytest-cov): Plugin for pytest that generates coverage reports.

### Note about Flask

The course this app was developed for required the use of Flask, which is the reason it was chosen. Because the app is very IO heavy and ChatGPT calls can sometimes be quite slow, I'd normally choose a framework that better supports async operations, such as [node.js](https://nodejs.org/en) or [Quart](https://quart.palletsprojects.com/en/latest/).

To solve the issue of slow IO operations and improve the performance of the app, the project utilizes Celery, a distributed task queue framework for Python.

Celery allows for the asynchronous execution of tasks, which is particularly useful for handling time-consuming operations such as making API calls to ChatGPT. By offloading these tasks to Celery workers, the main application can continue processing other requests without waiting for the slow tasks to complete.

## Project structure

The project follows a typical structure for a Flask web application. Here is an overview of the main directories and files:

```
├── npcgen           # Main application directory
│   ├── auth         # Authentication related files
│   ├── characters   # Character generation and management files
│   ├── static       # Static files (CSS, JS, images)
│   └── templates    # HTML templates
├── data             # Data directory (character templates, etc.)
├── tests            # Test directory
├── .env.example     # Example environment variable file
├── compose.yml      # Docker Compose configuration file
└── requirements.txt # Python dependencies
```

## Local setup

> **_NOTE:_** Please note that the setup steps provided below have not been tested on Windows. It is recommended to run these steps using Windows Subsystem for Linux (WSL) or a similar environment.

To run the app locally using Docker, follow these steps:

1. Make sure you have [Docker installed](https://docs.docker.com/get-docker/) on your machine.
2. Clone the repository:

   ```shell
   git clone https://github.com/jrauha/rpg-npc-generator.git
   ```

3. Navigate to the project directory:

   ```shell
   cd rpg-character-generator
   ```

4. Copy the `.env.example` file and rename it to `.env`:

   ```shell
   cp .env.example .env
   ```

5. Configure the OpenAI API key:

   Open the `.env` file and set the value of `OPENAI_API_KEY` to your OpenAI API key.

6. Start the Docker containers:

   ```shell
   docker compose up -d
   ```

7. Init database:

   ```shell
   ./run flask db reset --with-testdb
   ./run flask db migrate
   ```

   If you're not planning to run tests locally you can leave out the `--with-testdb` option.

8. Create admin user:

   ```shell
   ./run cmd flask auth create-user --superuser
   # follow the prompts
   ```

9. Init character templates:

   ```
   ./run cmd flask characters init-templates
   ```

10. Open your web browser and visit `http://localhost:8000` to access the app.

## Running tests

To run the tests, follow these steps:

1. Make sure you have the project set up locally as described in the "Local setup" section.

2. Run linters and formatters:

   ```shell
   ./run quality
   ```

3. Run the tests:

   ```shell
   ./run test
   ```

   This command will execute all the tests in the project and provide you with the test results.

   Alternatively you can run only unit tests with following command:

   ```shell
   ./run test:unit
   ```

### Continuous integration (CI)

The project includes support for continuous integration (CI) to automate the build and testing process. `.github/workflows/ci.yml` file defines the steps that will be executed whenever a new commit is pushed to the repository.

## References

- NPC templates are based on [Pathfinder NPC Gallery](https://2e.aonprd.com/Rules.aspx?ID=1396)
- The Docker support in this project is based on the [Docker Flask example](https://github.com/nickjj/docker-flask-example/tree/main).
