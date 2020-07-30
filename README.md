## Installation

There are two required API tokens to run this script.

1. A [Contentful Personal Access Token](https://www.contentful.com/help/personal-access-tokens/) to upload content
2. A [Tinify API Key](https://tinypng.com/developers) for image optimization

These credentials live in `config.json`, which should be structured like:

```
{
  "contentful-access-token": "<contentful-access-token>",
  "tinify-api-key": <tinify-api-key>""
}

```

Run the script with `python process_images.py`

## Development

## Code formatting

Code is formatted using [yapf](https://github.com/google/yapf).
To format all files, try `yapf . -i --recursive` from the root directory.
