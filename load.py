#!/usr/bin/python
import requests
import time
import random
import arrow

baseurl = 'http://admin:admin@localhost:5984/testdb'

# Create the db
requests.put(baseurl)

doc = {
    "subject":"I like Plankton",
    "author":"Rusty",
    "date":arrow.utcnow().format(),
    "tags":["plankton", "baseball", "decisions"],
    "body":"I decided today that I don't like baseball. I like plankton."
}

while(True):
    time.sleep(random.randint(1, 15))
    # insert doc(s)
    for i in range(0, random.randint(1,6)):
        response = requests.post(baseurl, json=doc)
    print(response.json())

    # maybe delete one?
    if(random.randint(1, 15) > 6):
        requests.post(baseurl + "/{}?{}".format(response.json()['id'], response.json()['rev']))