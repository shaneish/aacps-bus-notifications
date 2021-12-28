#!/bin/bash

docker build -t aacps-bus-notifications .
docker run --env TWILIO_SID --env TWILIO_AUTH -d --rm aacps-bus-notifications