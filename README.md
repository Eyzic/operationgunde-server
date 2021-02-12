# operationgunde-server

The api is written in Python 3.

## Dependencies and installing

* Flask
* Flask_restful


First navigate to the folder containing the repo on your local machine in a termianl and create a virtual environment using `python -m venv env`. Then activate it by typing `env/Scripts/activate` for windows and `source env/bin/activate` on linux and mac.

To install the dependencies, simply write `pip install -r requirements.txt` on windows or `pip3 install -r requirements.txt` on mac and linux.

## Running the application

Navigate to the folder in a terminal and type `python main.py` to start the API-server (running on localhost:5000) and type `python test.py` to run a test file which issues a get-request to the server.
