#!/bin/bash

service docker start
docker build -t aacps-bus-notifications .
docker run -d -rm aacps-bus-notifications