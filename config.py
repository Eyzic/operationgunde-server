import urllib

mongodb = {
    "URI": "mongodb+srv://" 
    + urllib.parse.quote_plus("dbUser")
    + ":"
    + urllib.parse.quote_plus("Hejsan123") 
    + "@cluster0.en8to.mongodb.net/Cluster0?retryWrites=true&w=majority",
    "key": "TEST123"
}

strava = {
    "STRAVA_CLIENT_ID" : "62111" ,
    "STRAVA_CLIENT_SECRET" : "00295152a762be432ee05b08bdd7367e570bd972" ,
    "STRAVA_ACCESS_TOKEN" : "a7db3e02cea9b734c810eaf0a615596ad827ff05" ,
    "STRAVA_REFRESH_TOKEN" : "06cbd0a56c10357d40846272b02fbab263b0791a",
    "STRAVA_FETCH_DATA_DATE": "2021-04-01"
}