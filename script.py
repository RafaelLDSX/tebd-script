from settings import *
import requests
from xml.dom import minidom

def obter_record_xml(orcId):
	request_data = {'Content-type':'application/vnd.orcid+xml',
					'Authorization type':'Bearer',
					'Access token':loginInfo["access_token"] }
	request_url = "https://pub.orcid.org/v3.0/" + str(orcId) + "/record"
	request_response = requests.get(url = request_url, data = request_data)
	return request_response.text.encode('utf-8')

loginUrl = "https://pub.orcid.org/oauth/token"

loginData = {'client_id':client_id,
		'client_secret':client_secret,
		'grant_type':'client_credentials',
		'scope':'/read-public'} 

loginResponse = requests.post(url = loginUrl, data = loginData)
loginInfo = loginResponse.json()

searchUrl = "https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:(%22Universidade%20\Federal%20Rural%20Do%20Rio%20De%20Janeiro%22+OR+UFRRJ)&start=0&rows=200"
searchData = {	'Content-type':'application/vnd.orcid+xml',
			  	'Authorization type':'Bearer',
			  	'Access token':loginInfo["access_token"] }

searchResponse = requests.get(url = searchUrl, data = searchData)



start = 0

while(len(IDs) > 0):
	
	for id in IDs:
		print(id.firstChild.data)
		f.write(obter_record_xml(id.firstChild.data))

	start += 200

	searchUrl = "https://pub.orcid.org/v3.0/search/?q=affiliation-org-name:(%22Universidade%20\Federal%20Rural%20Do%20Rio%20De%20Janeiro%22+OR+UFRRJ)&start=" + start + "&rows=200"

	searchResponse = requests.get(url = searchUrl, data = searchData)

	xml_dom = minidom.parseString(searchResponse.text);

	IDs = xml_dom.getElementsByTagName("common:path")

f.close()


	