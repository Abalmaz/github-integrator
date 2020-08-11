# GitHub  integration

GitHub integration API is a service to connect to the GitHub with personal token or GitHub app.

## Workflow

1. `/oauth/access_token` identifying using the personal access token
2. `/oauth` authenticate on behalf of the app installation.


## Deployment

### Localhost

#### PostgreSQL
This should be done automatically for you if you run the setup script. But basically what it does is to:

1. Create a database user.
2. Create a development database.
3. Create a test database.

#### run 
1. Set correct path to the project on your machine in `env.sh` file.
2. Run `env.sh`
3. Install requirements
3. Run the application locally: `flask run`.

### Environment variables

Before you start reading the paragraph, please, have a look at [env.templates.sh] (.deploy/) folder.
