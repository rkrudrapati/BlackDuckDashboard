import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from xml.etree import ElementTree as et


datafile = r"C:/Users/Desktop/NewIssue.xml"

months_in_words = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
url = "https://fortify.philips.com/ssc/api/v1/projectVersions/11900/artifacts"
querystring = {"fields":"lastScanDate","limit":"1"}
headers = {
    'host': "fortify.philips.com/ssc:443",
    'accept': "application/json",
    'authorization': "FortifyToken MDE2ZjU2MjgtNzMxNy00NjQzLWJlMjQtMTUyYjNkYzA2OWY0",
    'content-type': "application/json;charset=UTF-8",
    'cache-control': "no-cache"
    }
lastScanDate = ''
response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
print(response.text)
for each_item in response.json()['data']:
    lastScanDate = each_item['lastScanDate']

print(lastScanDate)
lastScanDate_List = lastScanDate.split("-")
year = lastScanDate_List[0]
month = lastScanDate_List[1]
date = lastScanDate_List[2].split('T')[0]

month = months_in_words[int(month)+1]

updated_lastScanDate = "%s %s, %s" %(month, date, year)
replace_text = "[issue age]:&quot;issue new\: %s&quot;" %updated_lastScanDate

print(replace_text)
tree = et.parse(datafile)

root = tree.getroot()

for elem in root.getiterator():
    # print(elem.tag)
    if(elem.tag == 'Refinement'):
        elem.text = elem.text.replace(elem.text, replace_text)
        break

tree.write(datafile, xml_declaration=True, method='xml', encoding="utf8")