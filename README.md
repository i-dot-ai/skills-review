# Skills review

This app suggests skills for a given job title (using OpenAI), and allows users to identify which of the suggested skills are incorrect. The data on job title, correct and incorrect skill suggestions are saved to the database.

## Local setup

1. Clone the repository: `git clone git@github.com:i-dot-ai/skills-review.git`
2. Create a copy of the `.env.sample` file and rename it to `.env`
3. Obtain an OpenAI API key by visiting the [OpenAI website](https://beta.openai.com/signup/)
4. Add the key to the `.env` file as the value for the `OPENAI_KEY` environment variable
5. Run the project locally: `docker-compose up`
6. Visit http://localhost:8008/

To access the admin:

1. Create a superuser: `docker-compose run web python manage.py createsuperuser`
2. Go to http://localhost:8008/admin/

To access the Django shell (eg to query database):

`docker-compose run web python manage.py shell`

## Note

Make sure to keep the `.env` file in the .gitignore file if you are planning on pushing this to a remote repository.
