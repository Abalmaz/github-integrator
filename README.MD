# GitHub  integration

GitHub integration API is a service to connect to the GitHub with personal token or GitHub app.

## Workflow

1. `/oauth/access_token` identifying using the personal access token. If token is valid and has right scopes('read:discussion',
                   'read:org',
                   'read:user',
                   'repo',
                   'user:email'), he will be authenticate. To Github will be sent a request to get data 
                   about the user, and if a user with this github id is not in the database, 
                   then it will be added.
2. `/oauth` authenticate on behalf of the GitHub app. Users are redirected to request their GitHub identity, 
and If the user accepts your request, GitHub redirects back to '/oauth/github-callback' url

| Methods | URI | Action |
|---------|-----|--------|
|POST| /oauth/access_token|Parameters: in json format like {"personal_token": "github_user_personal_token"}. Identifying using the personal access token. If token is valid and has right scopes('read:discussion','read:org','read:user','repo','user:email'), he will be redirecting to '/oauth/github-callback' url|
|GET| /oauth| Identifying with GitHub app. Users are redirected to request their GitHub identity, and if the user accepts request, GitHub redirects back to '/oauth/github-callback' url.|
|GET| /oauth/github-callback| To Github will be sent a request to get data about the user, and if a user with this github id is not in the database, then it will be added, with GitHub ID, GitHub Login, GitHub email and GitHub access token fields. Access tiken will be encrypt before save.|
|GET| /docs| Swagger documentation|

## Deployment

### Localhost

#### run 
1. Set correct parameters in `env.sh` file.
2. Run `env.sh`
3. Install requirements
3. Run the application locally: `flask run`.

### Environment variables

Before you start reading the paragraph, please, have a look at [env.templates.sh] (.deploy/) folder.
