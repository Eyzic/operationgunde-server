# operationgunde-server

The api is written in Python 3.

## Dependencies and installing

* Flask
* Flask_restful


First navigate to the folder containing the repo on your local machine in a terminal and create a virtual environment using `python -m venv env`. Then activate it by typing `env/Scripts/activate` for windows and `source env/bin/activate` on linux and mac.

To install the dependencies, simply write `pip install -r requirements.txt` on windows or `pip3 install -r requirements.txt` on mac and linux.

## Running the application

Navigate to the folder in a terminal and type `python main.py` to start the API-server (running on localhost:5000) and type `python test.py` to run a test file which issues a get-request to the server.

## Reaching the API

The following is a quick guide on how to communicate with the database. Packages should be sent and received as JSON.

| HTTP Method | URI | Payload | Returns | Action | 
| --- | --- | --- | --- | --- |
| GET | http://[hostname]/api/stats | {'user': Integer, 'date': String [YYYY-MM-DD]} | {'user', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'} or error | Get a stats document based on user and date |
| POST | http://[hostname]/api/stats | {'user': Integer, 'date': String [YYYY-MM-DD], 'hrv': Integer, 'sleeping_hours': Integer, 'stress_level': Integer, 'muscle_ache': Integer, 'mood_level': Integer, 'injury_level' : Integer, 'energy_level': Integer} | {error} or {messages} | Post the stats form (HRV form) to database |
| DELETE | http://[hostname]/api/stats | {'user': Integer, 'date': String [YYYY-MM-DD]} | {error} or {messages} | Delete a stats document based on user and date |
| GET | http://[hostname]/api/stats/hrv | {'user': Integer, 'date': String [YYYY-MM-DD]} | Integer | Get HRV data from user and date |
| POST | http://[hostname]/api/training | {'user': Integer, 'activity_id': Integer, 'training_intensity': Integer, 'training_type': String, 'training_duration': Integer, 'energy_level': Integer} | {error} or {messages} | Post the training form (after training form) to database |