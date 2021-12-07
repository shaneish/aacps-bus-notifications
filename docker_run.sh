#!/bin/bash

service docker start
docker build aacps-bus-notifications .
docker run -t -i -p 80:80 aacps-bus-notifications