# aacps-bus-notifications

## AACPS bus notifications effing suck.  This makes them better--for me, at least.

### General Info
Easy scripts to run with or without containerization.  To run, you need:
    - Two environment variables TWILIO_SID and TWILIO_AUTH that contain the SID and auth token for Twilio access.

    - User information added to a .psv file

To run in a docker container, ensure your docker client is started and run the `docker_run.sh` script.  This will build the docker container and start it.

To run with no container, run the `run.sh` script.  This will create and activate a Python venv, install dependencies, and run the scheduler program.

### To-Do
Still in development:
    - Need to write unit tests.

    - Update to save user information in a MySQL DB instead of pipe-separate values (.psv) file