#!/usr/bin/env python
import json
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

csvfile = "services_iag.csv"
with open(csvfile, "a") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow( ['service_name', 'service_id', 'update_code', 'iag'])
	

API_ACCESS_KEY=''
BASE_URL = 'https://api.pagerduty.com'
HEADERS = {
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Authorization': 'Token token={token}'.format(token=API_ACCESS_KEY),
		'Content-type': 'application/json'
	}
	
count = 0

def get_services_count():
	global count
	count = requests.get(BASE_URL + '/services?total=true' , headers=HEADERS)
	#print(count.json())
	count = count.json()['total']
	print(count)
	
	
def get_services(offset):
	print('Getting services')
	params = {
		'offset':offset
	}
	all_services = requests.get(BASE_URL + '/services', headers=HEADERS, params=params)
	for service in all_services.json()['services']:
		payload = {
			"service": {
				"alert_creation": "create_alerts_and_incidents",
    			"alert_grouping": "intelligent"
    			}
			}
		service_iag = requests.put(BASE_URL + '/services/' + service['id'], headers=HEADERS, data=json.dumps(payload))
		#print(service_iag.json())
		with open(csvfile, 'a') as output:
			writer = csv.writer(output, lineterminator='\n')
			row = [service['name'], service['id'], service_iag, service_iag.json()['service']['alert_grouping']]
			#print(row)
			writer.writerow(row)
	
		
	    	
def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	get_services_count()

	for offset in xrange(0,count):
		if offset % 25 == 0:
			get_services(offset)
	

if __name__=='__main__':
	sys.exit(main())
