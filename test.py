import mysql.connector
from mysql.connector import errorcode
import json
import urllib

def fetchDataForKey():
    search = 'network'
    query = urllib.urlencode({'q': search})
    for x in range(0, 5):
        number = 4*x
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0%s' % query + '&start=0&rsz=20'
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        print data

fetchDataForKey()
