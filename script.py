import requests
import xml.etree.ElementTree as ET

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

root = ET.fromstring(searchResponse.text)

for id in root.findall('.//{http://www.orcid.org/ns/common}path'):
	searchRecord = "https://pub.orcid.org/v3.0/" + id.text + "/personal-details"
	recordResponse = requests.get(url = searchRecord, data = searchData)
	
	recordRoot = ET.fromstring(recordResponse.text)
	firstName = recordRoot.find(".//{http://www.orcid.org/ns/personal-details}given-names").text
	lastName = recordRoot.find(".//{http://www.orcid.org/ns/personal-details}family-name").text
	print(firstName + " " + lastName)