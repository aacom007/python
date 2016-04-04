import mysql.connector
from mysql.connector import errorcode
import json
import urllib
import mechanize
from readability.readability import Document
from readability.readability import Document

browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Firefox')]

def fetchDataForKey(search):
    hits = []
    query = urllib.urlencode({'q': search})
    for x in range(0, 5):
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&start='+`4*x`+'&%s' % query 
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

            
          
          for key in hits:              
              urls = [] 
              urls.append(key['url'])
              search_url = urllib.urlopen(key['url'])              
              url_results = search_url.read()
              html = browser.open(url).read()
              article = Document(html).summary()
              data_query = (key['url'], article[0:480])
              cursor.execute(sqlQuery, data_query)
              cnx.commit()
              print key['url']

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Your user name or password is incorrect")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            cursor.close()

        cnx.close() 
        print urls
fetchDataForKey('wiki')



