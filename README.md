## Installation

### Dependencies

Python requirements live in `requirements.txt`.

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

Run the script with

```
export FLASK_APP=app.py
flask run
```

## Development

Set `export FLASK_ENV=development` to enable auto-updating as files change.

### Deployment
1. Build the Docker container: `docker build -t image-upload .`
2. Run the Docker container: `docker run -d --name image-upload-container -p 80:80 image-upload`

### todos
Todo items are marked with `todo` in the comments. Try `grep -r "todo"` to find outstanding items.

### Code formatting

Code is formatted using [yapf](https://github.com/google/yapf).
To format all files, try `yapf . -i --recursive` from the root directory.
