#! /bin/bash

CURR_LOCATION=$(pwd) # this will hold the current location of the user

# Check if the user's home directory has a bin folder, if not, create it
if [ ! -d "$HOME/bin" ] 
then
    mkdir "$HOME/bin"
    echo "Creating bin directory in $HOME"
fi

# Take input for the REPLICATE_API_TOKEN
read -p "Enter REPLICATE_API_TOKEN: " REPLICATE_API_TOKEN


# name of the package folder, which will be placed inside the /bin folder of user's home directory
FOLDER_NAME="commandAIPackages"

# Check if the commandAIPackages folder is already present,
# then remove it and create a new one
if [ -d "$HOME/bin/$FOLDER_NAME" ] 
then 
    rm -rf "$HOME/bin/$FOLDER_NAME"
    echo "Removed the $HOME/bin/$FOLDER_NAME (old folder)"
fi 

# creating commandAIPackages folder
mkdir "$HOME/bin/$FOLDER_NAME"
echo "Created the new $HOME/bin/$FOLDER_NAME (new folder !!)"

# move commandAI.py and requirements.txt into commandAIPackages folder
cp commAI.py "$HOME/bin/$FOLDER_NAME/commAI.py"
cp requirements.txt "$HOME/bin/$FOLDER_NAME/requirements.txt"
echo "Copy commandAI.py and requirements.txt files to the $HOME/bin/$FOLDER_NAME/commAI.py"

# then create a virtual env for python, inside commandAIPackages folder
cd "$HOME/bin/$FOLDER_NAME"

echo "Creating the virtual env"
python -m venv env

source env/bin/activate # this will activate the virtual env

echo "Starting the installation..."
pip install -r requirements.txt # starting the installation of packages

deactivate # deactivating the virtual env

# now, creating a .env file which contains the REPLICATE_API_TOKEN
touch .env
.env<"REPLICATE_API_TOKEN=$REPLICATE_API_TOKEN"

# comming back to the initial location
cd $CURR_LOCATION 

# copy the askCommAI.sh script to inside the bin folder
cp askCommAI.sh "$HOME/bin/askCommAI.sh"
chmod +x "$HOME/bin/askCommAI.sh"

echo "Finally, placed the askCommAI.sh file inside the bin"
echo "RUN: askCommAI.sh"
echo "BEST OF LUCK !!"
