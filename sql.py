import mysql.connector
from mysql.connector import errorcode
import json
import urllib

def showsome(search):
    query = urllib.urlencode({'q': search})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']

    try:
      cnx = mysql.connector.connect(user='akshay', password='abc123456', database='nbc1')
      cursor = cnx.cursor()

      sqlQuery = ("INSERT INTO nbcdemo"
           "(keyName, description)"
           "VALUES (%s, %s)")
      for h in hits:
          print ' ', h['url'], ' ', h['content']
          data_query = (h['url'], h['content'])
          cursor.execute(sqlQuery, data_query)
          cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Your user name or password is incorrect")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        cursor.close()

    cnx.close() 

showsome('steve jobs')

