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
    "client_id" : "62111" ,
    "client_secret" : "00295152a762be432ee05b08bdd7367e570bd972" ,
    "access_token" : "a7db3e02cea9b734c810eaf0a615596ad827ff05" ,
    "refresh_token" : "06cbd0a56c10357d40846272b02fbab263b0791a" 
}