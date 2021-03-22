

# store API credentials
with open('api_credentials.json', 'r') as f:
    api_credentials = json.load(f)
    client_id = api_credentials['client_id']
    client_secret = api_credentials['client_secret']
    refresh_token = api_credentials['refresh_token']

# make POST request to Strava API
req = requests.post("https://www.strava.com/oauth/token?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token".format(client_id, client_secret, refresh_token)).json()

# update API credentials file
api_credentials['access_token'] = req['access_token']
api_credentials['refresh_token'] = req['refresh_token']
with open('api_credentials.json', 'w') as f:
    json.dump(api_credentials, f)

# store new access token
access_token = api_credentials['access_token']


# Extract most recent date from the request log file
with open('request_log.csv', 'r') as f:
    
    # read file line-by-line     
    lines = f.read().splitlines()
    
    # store last line as a dictionary
    first_line = lines[0].split(',')
    last_line = lines[-1].split(',')
    last_line_dict = dict(list(zip(first_line, last_line)))

    # extract timestamp from last line
    start_date = last_line_dict['timestamp']
# convert timestamp from ISO-8601 to UNIX format
start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
start_date_tuple = start_date_dt.timetuple()
start_date_unix = int(time.mktime(start_date_tuple))



# store URL for activities endpoint
base_url = "https://www.strava.com/api/v3/"
endpoint = "athlete/activities"
url = base_url + endpoint

# define headers and parameters for request
headers = {"Authorization": "Bearer {}".format(access_token)}
params = {"after": start_date_unix}

# make GET request to Strava API
req = requests.get(url, headers = headers, params = params).json()