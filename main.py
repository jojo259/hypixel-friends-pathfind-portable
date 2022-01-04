import requests

apiKey = None

def readApiKey():
	try:
		apiKey = open('apiKey.txt').read()
	except:
		print('cant read api key, exiting')
		exit()

def testApiKey():
	apiUrl = f'https://api.hypixel.net/friends?key={apiKey}&uuid=1f2e58ced9164d55bd3fa7f4a81dd09f'
	print(apiUrl)

readApiKey()
print('testing api key')
testApiKey()

def getApi(url):
	#print(url)
	try:
		receivedApi = requests.get(url,timeout=1)
		receivedApi = receivedApi.json()

		return receivedApi
	except:
		return None

while notFound:
	apiUrl = f'https://api.hypixel.net/friends?key={apiKey}&uuid={toCheckUuid}'