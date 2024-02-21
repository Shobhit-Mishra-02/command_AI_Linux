#! /bin/bash

CURR_LOCATION=$(pwd) # this will hold the current location of the user

FOLDER_NAME="commandAIPackages"

# cd into the commandAIPackages folder
cd "$HOME/bin/$FOLDER_NAME"

source env/bin/activate # activating the virtual env
python commAI.py # running the python script
deactivate # deactivatin the env

cd $CURR_LOCATION # comming back to the user's initial location