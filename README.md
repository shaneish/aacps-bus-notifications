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

    - N̶e̶e̶d̶ ̶t̶o̶ ̶w̶r̶i̶t̶e̶ ̶u̶n̶i̶t̶ ̶t̶e̶s̶t̶s̶

    - U̶p̶d̶a̶t̶e̶ ̶t̶o̶ ̶s̶a̶v̶e̶ ̶u̶s̶e̶r̶ ̶i̶n̶f̶o̶r̶m̶a̶t̶i̶o̶n̶ ̶i̶n̶ ̶a̶ ̶D̶B̶ ̶i̶n̶s̶t̶e̶a̶d̶ ̶o̶f̶ ̶p̶i̶p̶e̶-̶s̶e̶p̶a̶r̶a̶t̶e̶ ̶v̶a̶l̶u̶e̶s̶ ̶(̶.̶p̶s̶v̶)̶ ̶f̶i̶l̶e̶
