import sys,requests,json,pathlib,time
username = "" #Specify your username here
password = "" #Specify your password here
if(username=="" or password==""):
	print('Looks like you haven\'t specified the username and password yet. Please edit line 2 and 3 of this script')
	exit(0)
try:
	qid = sys.argv[1]
	file = sys.argv[2]
except:
	print("Failed to start web scrapping. Please give a valid set of arguments.")
	print("Format: python spoj-submitter.py <problemcode> <filename>")
	print("Sample use: python spoj-submitter.py FOXLINGS myfile.cpp")
	exit(0)

#Code to check is the file exists
pfile = pathlib.Path(file)
if not pfile.is_file():
	print('\nNo such file \''+file+'\' found. Please check for the location')
	exit(0)
#End code for file exists

print("Specified File: "+file)

#Common headers for all requests
header = {'Host':'www.spoj.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','Referer':'http://www.spoj.com/'}
#End common headers

#Check is the problem exists
url = 'http://www.spoj.com/submit/'+qid+'/'
try:
	r=requests.get(url,headers=header,allow_redirects=False)
except:
	print("Connection error. Make sure you are connected to Internet")
	exit(0)
if(r.status_code==404):
	print('\nNo such problem was found on the server.')
	exit(0)

print("Specified problem: "+qid)
#End check for problem

#Send login data
login_data = {'next_raw':'','autologin':'1','login_user':username,'password':password}
try:
	r=requests.post('http://www.spoj.com/login/',data=login_data,headers=header,allow_redirects=False)
except:
	print("\nConnection error. Falied to login")
	exit(0)
header['Cookie'] = r.headers['Set-Cookie'].split('; ')[0]
#Login data sent and session ID captured

#Check if login successful
if(len(r.headers['Set-Cookie'].split('autologin_hash'))<2):
	print('\nLogin failed')
	exit(0)
else:
	print('\nLogin successful')
#End code to check login

#Check the language code
url = 'http://www.spoj.com/submit/'+qid+'/'
try:
	r=requests.get(url,headers=header,allow_redirects=False)
except:
	print("Connection error. Make sure you are connected to Internet")
r=str(r.content).split('<option value="')
for i in range(1,len(r)):
	r[i] = r[i].split('" >')
	lcodes[int(r[i][0])] = r[i][1].split('</option>')[0]
print(lcodes)
while(1==1):
	lang = input("\nEnter the language code (-1 to list all): ")
	lang = int(lang)
	if(lang==-1):
		print()
		for key in lcodes:
			print(str(key)+ "\t:\t" +lcodes[key])
		print()
	else:
		if(lang in lcodes):
			break
		else:
			print("\nInvalid code. Try again..")
			continue
#End language check

#All checks have passed now. Upload the file
file = {'subm_file': open(file,'rb')}
upload_data = {'lang': lang, 'problemcode': qid, 'file': '', 'submit':'Submit!'}
try:
	r = requests.post('http://www.spoj.com/submit/complete/', headers=header,files=file,data=upload_data)
except:
	print("\nConnection error. Problem couldn't be submitted")
	exit(0)
print("\nSolution submitted..")
#File upload complete

def clean(s):
	s = s.replace("\\n", "")
	s = s.replace("\\t", "")
	s = s.replace(" ","")
	s = s.strip()
	return s

#Check for the the result
print("\nRunning Judge..\n")
url = 'http://www.spoj.com/status/'+qid+','+username+'/'
while(1==1):
	try:
		r=str(requests.get(url,headers=header).content)
	except:
		print("Connection error. Failed to fetch status")
		exit(0)
	status=int(clean((r.split('" status="'))[1].split('"')[0]))
	if(status<10):
		time.sleep(3)
		continue
	s=""
	if(status==15):
		s="Accepted"
	elif(status==14):
		s="Wrong Answer"
	elif(status==13):
		s="Time Limit Exceeded"
	elif(status==12):
		s="Runtime Error"
	elif(status==11):
		s="Compilation Error"
	elif(status==10):
		s="Disqualified"
	else:
		s="Unknown status"
	t=clean((r.split('best solutions">'))[1].split('<')[0])
	m=clean((r.split('id="statusmem_'))[1].split('>')[1].split('<')[0])
	print("Status : "+s)
	print("Time : "+t)
	print("Memory : "+m)
	break
