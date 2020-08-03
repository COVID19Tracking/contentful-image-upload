#!/bin/bash
docker build -t contentful-upload .
docker run -d -p 80:80 contentful-upload
