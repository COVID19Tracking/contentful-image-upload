#!/bin/bash
docker build -t contentful-upload .
docker run -d -p 56733:80 --name=contentful-upload -v $PWD:/app contentful-upload
