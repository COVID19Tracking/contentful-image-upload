## Installation

### Dependencies

Python requirements live in `requirements.txt`.

### Credentials

You will need a [Contentful Personal Access Token](https://www.contentful.com/help/personal-access-tokens/) to run this script.

Credentials live in `config.json`, which should be structured like:

```
{
  "contentful-access-token": "<contentful-access-token>",
  "contentful-space-id": "<contentful-space-id>",
  "directory-path": "imgs"
}
```

Run the script with

```
export FLASK_APP=web.py
flask run
```

## Development

### Code formatting

Code is formatted using [yapf](https://github.com/google/yapf).
To format all files, try `yapf . -i --recursive` from the root directory.
