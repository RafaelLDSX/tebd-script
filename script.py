from settings import *
import requests
from xml.dom import minidom

def obter_record_xml(orcId):
	request_data = {'Content-type':'application/vnd.orcid+xml',
					'Authorization type':'Bearer',
					'Access token':loginInfo["access_token"] }
	request_url = "https://pub.orcid.org/v3.0/" + str(orcId) + "/record"
	request_response = requests.get(url = request_url, data = request_data)
	return request_response.text

loginUrl = "https://pub.orcid.org/oauth/token"

loginData = {'client_id':client_id,
		'client_secret':client_secret,
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

f = open("test2.xml", "w+")

xml_record = obter_record_xml(IDs[0].firstChild.data)

f.write(obter_nome(xml_record))
f.close()

def xml_para_dom(xml):
	return minidom.parseString(str(xml))

def obter_nome(xml_dom):
	primeiro_nome = xml_dom.getElementsByTagName("personal-details:given-names")
	nome_de_familia = xml_dom.getLementsByTagName("personal-details:family-name")
	