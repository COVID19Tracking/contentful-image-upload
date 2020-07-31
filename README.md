## Installation

### Dependencies

Python requirements live in `requirements.txt`.

### Credentials

~~You will need a [Contentful Personal Access Token](https://www.contentful.com/help/personal-access-tokens/) to run this script.~~

You will need a [Contentful OAuth Application](https://app.contentful.com/account/profile/developers/applications) to run this program. ([Docs here](https://www.contentful.com/developers/docs/extensibility/oauth/))

Credentials live in `config.json`, which should be structured like:

```
{
  "contentful-access-token": "<contentful-access-token>",
  "contentful-space-id": "<contentful-space-id>",
  "directory-path": "imgs",
  "contentful-client-id": "<contentful-client-id>",
  "redirect-uri": "<redirect-uri>"
}
```

Run the script with

```
export FLASK_APP=web.py
flask run
```

## Development

Set `export FLASK_ENV=development` to enable auto-updating as files change.

### Code formatting

Code is formatted using [yapf](https://github.com/google/yapf).
To format all files, try `yapf . -i --recursive` from the root directory.
