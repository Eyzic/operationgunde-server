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

#### API for forms

| HTTP Method | URI | Payload | Returns | Action | 
| --- | --- | --- | --- | --- |
| GET | http://[hostname]/api/form/stats | {'user_id': String, 'date': String [YYYY-MM-DD]} | {'user_id', 'date', 'hrv', 'sleeping_hours', 'stress_level', 'muscle_ache', 'mood_level', 'injury_level', 'energy_level'} or {'error'} | Get a stats document based on user_id and date |
| POST | http://[hostname]/api/form/stats | {'user_id': String, 'date': String [YYYY-MM-DD], 'hrv': Integer, 'sleeping_hours': Integer, 'stress_level': Integer, 'muscle_ache': Integer, 'mood_level': Integer, 'injury_level' : Integer, 'energy_level': Integer} | {'error'} or {'message'} | Post the stats form (HRV form) to database |
| DELETE | http://[hostname]/api/form/stats | {'user_id': String, 'date': String [YYYY-MM-DD]} | {'error'} or {'message'} | Delete a stats document based on user_id and date |
| GET | http://[hostname]/api/form/stats/hrv | {'user_id': String, 'date': String [YYYY-MM-DD]} | Integer | Get HRV data from user_id and date |
| GET | http://[hostname]/api/form/training | {'user_id': String, 'date': String [YYYY-MM-DD]} | {'user_id', 'date', 'training_intensity', 'training_type', 'elapsed_time', 'energy_level'} | Get a training form from the database, based on user_id and date |
| POST | http://[hostname]/api/form/training | {'user_id': String, 'date': String [YYYY-MM-DD], 'training_intensity': Integer, 'training_type': String, 'training_duration': Integer, 'energy_level': Integer} | {'error'} or {'message'} | Post the training form (after training form) to database |


#### API for activities

| HTTP Method | URI | Payload | Returns | Action |
| --- | --- | --- | --- | --- |
| GET | http://[hostname]/api/activities | {'user_id': String, 'nb_activities': Integer} | [{'activity_id', 'title', 'average_heartrate', 'start_date_local', 'distance', 'moving_time', 'elapsed_time', 'type'}] | Returns a list of all stored activities from user_id |
| POST | http://[hostname]/api/activity | {'user_id': String, 'title': String, 'average_heartrate': Integer, 'start_date_local': String, 'distance': Integer, 'moving_time': Integer, 'elapsed_time': Integer, 'type': String} | {'error'} or {'message'} | Post an activity to database |
#### API for groups and organisations

| HTTP Method | URI | Payload | Returns | Action |
| --- | --- | --- | --- | --- |
| POST | http://[hostname]/api/group | {'group': String, 'logo':String[cat/dog/lion/fox/owl]} | {'message'} or {'error'} | Create a group with a group logo |
| GET | http://[hostname]/api/group | {'group': String} | [{'name'}] or {'error'} | Get all the members of a specific group |
| POST | http://[hostname]/api/user/group | {'user_id': String, 'group': String} | {'message'} | Adds an user to a group |
| GET | http://[hostname]/api/user/group | {'user_id': String} | [{'group', 'nb_members', 'logo'}] or {'error'} | Get all the groups that an user is member of |
| GET | http://[hostname]/api/group/png | {'logo': String[cat/dog/lion/fox/owl]} | logo.png | Get a group logo in PNG format |

<!-- | POST | http://[hostname]/api/user/organisation | {'user_id': String, 'organisation': String} | {'message'} | Adds an organisation to an user |
| GET | http://[hostname]/api/user/organisation | {'user_id': String} | [organisations] or {'error'} | Get all the organisations that an user is member of |
| GET | http://[hostname]/api/organisation | {'organisation': String} | [{'user_id', 'name'}] or {'error'} | Get all the members of a specific organisation | -->



## Connecting to the Strava API and retrieving data to MongoDB

To access the Strava data the user first needs to call `http://[hostname]/strava/authorize` and authorize data collection. The authorization needs to take place at the local server since we're running on `port 5000`. Once the authorization is done, the server will initially store the data locally at `os.path.expanduser('~'), '.stravadata'` and then push the data to MongoDB.

| HTTP Method | URI | Payload | Returns | Action | 
| --- | --- | --- | --- | --- |
| GET | http://[hostname]/strava/authorize | empty | {URL to strava authorization} | Authorize the server to get data from the Strava API |
| POST | http://[hostname]/strava/connect/name | {'user_id': String} | {'error'} or {'message'} | If FIRSTNAME and LASTNAME matches in both user['name'] and strava['name'], it automatically connects the two activity data |
| POST | http://[hostname]/strava/connect/id | {'user_id': String, 'strava_id': String} | {'error'} or {'message'} | Manually connect an user_id with a strava_id to be able to GET Strava activites |
| GET | http://[hostname]/strava/athlete | {'strava_id': String} | {'firstname', 'lastname'} | Gets athlete data from strava_id |
| GET | http://[hostname]/strava/athlete_all | empty | {'firstname', 'lastname', 'strava_id'} | Returns all stored athletes in MongoDB |

## Using the log-in system and authentication

Initially, users are authenticated by using their unique ID:s (e.g. '093715d842774acf896eb182c181a729'). This is received by using the /signup or /login call. If you want, you can call the /signout to generate a new random user-ID that's received when you log in again.

By not using the /signout, you can keep the pre-set user-ID between different user calls.

| HTTP Method | URI | Payload | Returns | Action | 
| --- | --- | --- | --- | --- |
| POST | http://[hostname]/signup | {'name': String, 'email': String, 'password': String} | {'user_id'} or {'error'} | Stores an user in the database with a hashed password and a random unique ID |
| POST | http://[hostname]/login | {'email': String, 'password': String} | {'user_id'} or {'error'} | Compares 'email' and 'password' with existing users in the database |
| POST | http://[hostname]/signout | {'user_id': String} | {'error'} or {'message'} | Sign out by changing the user_id in the database to a new random unique ID |
