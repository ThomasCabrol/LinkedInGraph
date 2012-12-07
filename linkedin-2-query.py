#!/usr/bin/env python
# encoding: utf-8
"""
linkedin-2-query.py

Created by Thomas Cabrol on 2012-12-03.
Copyright (c) 2012 dataiku. All rights reserved.

Building the LinkedIn Graph
"""

import oauth2 as oauth
import urlparse
import simplejson
import codecs

CONSUMER_KEY = "your-consumer-key-here"
CONSUMER_SECRET = "your-consumer-secret-here"
OAUTH_TOKEN = "your-oauth-token-here"
OAUTH_TOKEN_SECRET = "your-oauth-token-secret-here"

OUTPUT = "linked.csv"

def linkedin_connections():
    # Use your credentials to build the oauth client
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    # Fetch first degree connections
    resp, content = client.request('http://api.linkedin.com/v1/people/~/connections?format=json')
    results = simplejson.loads(content)    
    # File that will store the results
    output = codecs.open(OUTPUT, 'w', 'utf-8')
    # Loop thru the 1st degree connection and see how they connect to each other
    for result in results["values"]:
        con = "%s %s" % (result["firstName"].replace(",", " "), result["lastName"].replace(",", " "))
        print >>output, "%s,%s" % ("Thomas Cabrol",  con)
        # This is the trick, use the search API to get related connections
        u = "https://api.linkedin.com/v1/people/%s:(relation-to-viewer:(related-connections))?format=json" % result["id"]
        resp, content = client.request(u)
        rels = simplejson.loads(content)
        try:
            for rel in rels['relationToViewer']['relatedConnections']['values']:
                sec = "%s %s" % (rel["firstName"].replace(",", " "), rel["lastName"].replace(",", " "))
                print >>output, "%s,%s" % (con, sec)
        except:
            pass
    

if __name__ == '__main__':
	linkedin_connections()
