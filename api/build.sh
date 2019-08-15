#!/bin/bash

pip freeze > ./api/requirements.txt

docker build ./api --tag=hvz-api
