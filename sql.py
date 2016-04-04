import mysql.connector
from mysql.connector import errorcode
import json
import urllib

def fetchDataForKey(search):
    query = urllib.urlencode({'q': search})
    for x in range(0, 5):
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&start='+`4*x`+'&%s' % query 
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        print data
        hits = data['results']

        try:
          cnx = mysql.connector.connect(user='akshay', password='abc123456', database='nbc1')
          cursor = cnx.cursor()

          sqlQuery = ("INSERT INTO nbcdemo"
               "(keyName, description)"
               "VALUES (%s, %s)")
          for key in hits:
              print ' ', key['url'], ' ', key['content']
              data_query = (key['url'], key['content'])
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

fetchDataForKey('nbc')



