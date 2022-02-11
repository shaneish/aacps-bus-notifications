# aacps-bus-notifications

## AACPS bus notifications effing suck.  This makes them better--for me, at least.

### General Info
Easy scripts to run with or without containerization.  To run, you need:

    - Two env vars TWILIO_SID and TWILIO_AUTH which contain SID and auth token for Twilio client.

    - User information added to a .psv file

To run in a docker container, ensure your docker client is started and run the `docker_run.sh` script.  This will build the docker container and start it.

To run with no container, run the `run.sh` script.  This will create and activate a Python venv, install dependencies, and run the scheduler program.  This requires a system install of Python 3.7 aliased as `python3.7`.

### To-Do
Still in development:
    
   - ~~Need to write unit tests~~
    
   - ~~Update to store user information in DB instead of pipe separated values (.psv) file~~

   - Create an API with Flask that allows DB updates
