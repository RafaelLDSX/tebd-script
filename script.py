import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

loginUrl = "https://pub.orcid.org/oauth/token"

loginData = {'client_id':'APP-FVIDJFTXXIGC984E',
		'client_secret':'acde52e3-3b0a-41fa-b89f-e5ecb7828438',
		'grant_type':'client_credentials',
		'scope':'/read-public'} 

loginResponse = requests.post(url = loginUrl, data = loginData)
loginInfo = loginResponse.json()

searchUrl = "https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:(%22Universidade%20\Federal%20Rural%20Do%20Rio%20De%20Janeiro%22+OR+UFRRJ)"
searchData = {	'Content-type':'application/vnd.orcid+xml',
			  	'Authorization type':'Bearer',
			  	'Access token':loginInfo["access_token"] }

searchResponse = requests.get(url = searchUrl, data = searchData)

IDsXML = minidom.parseString(searchResponse.text);

IDs = IDsXML.getElementsByTagName("common:path")

f = open("test.xml", "w+")

searchRecord = "https://pub.orcid.org/v3.0/" + IDs[0].firstChild.data + "/activities"
recordResponse = requests.get(url = searchRecord, data = searchData)

f.write(recordResponse.text)
f.close()
