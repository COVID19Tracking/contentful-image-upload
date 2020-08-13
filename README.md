## Installation

### Credentials

You will need a [Contentful OAuth Application](https://app.contentful.com/account/profile/developers/applications) to run this program. ([Docs here](https://www.contentful.com/developers/docs/extensibility/oauth/))

Credentials live in `app/config.json`, which should be structured like:

```
{
  "contentful-space-id": "<contentful-space-id>",
  "directory-path": "imgs",
  "contentful-environment": "<contentful-environment>",
  "contentful-client-id": "<contentful-client-id>",
  "redirect-uri": "<redirect-uri>"
}
```

## Getting Started

### Dependencies

Python requirements live in `requirements.txt`.
Install them with `pip3 install -r requirements.txt`

### Development
Run the development server with:
* `export FLASK_APP=app/app/app.py`
* `python3 -m flask run`
* Visit http://localhost:5000

#### HTTPS Tunneling
Because Contentful requires HTTPS for its URI redirects, you'll need to be use a service like [ngrok](https://ngrok.com/) to run the development server. The development server runs on port 5000: you'll need to forward 5000 over http.

Keep in mind that you'll need to update the URI redirect in [your OAuth application](https://app.contentful.com/account/profile/developers/applications) to the HTTPS proxy in order for the authentication workflow to work.

### Deployment
This project uses `docker-compose` for containerization. There are three services:
1. `nginx`, which runs on ports 80 and 443.
2. `flask_app`, the actual Flask application, runs on port 5000. (`nginx` reverse proxies to `0.0.0.0:5000` via uswgi.)
3. `certbot`, which handles HTTPS certificates.

(This configuration is based on [wmnnd's boilerplate](https://github.com/wmnnd/nginx-certbot).)

#### OK, but how does it run?

`docker-compose up` should do the trick.

### todos
Todo items are marked with `todo` in the comments. Try `grep -r "todo"` to find outstanding items.

### Code formatting

Code is formatted using [yapf](https://github.com/google/yapf).
To format all files, try `yapf . -i --recursive` from the root directory.
