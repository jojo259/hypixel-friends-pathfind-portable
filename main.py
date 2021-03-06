import requests
import time

def getApi(url):
	while True:
		try:
			apiCalled = requests.get(url, timeout = 10).json()
			if apiCalled['success']:
				return apiCalled
			else:
				print('api error, probably throttled, retrying')
				time.sleep(1)
		except:
			print('api error, probably timeout, retrying')
			time.sleep(1)

def readApiKey():
	global apiKey
	try:
		apiKey = open('apiKey.txt').read()
	except:
		print('\nerror, create text file "apiKey" with your hypixel api key\nexiting')
		exit()

def testApiKey():
	global apiKey
	apiUrl = f'https://api.hypixel.net/friends?key={apiKey}&uuid=1f2e58ced9164d55bd3fa7f4a81dd09f'
	dataReceived = getApi(apiUrl)
	print()
	if dataReceived != None:
		print('	api key works')
	else:
		print('	invalid api key, exiting')
		exit()

def getUuid(username):
	returned = False
	while not returned:
		try:
			apiUrl = f'https://api.mojang.com/users/profiles/minecraft/{username}'
			dataReceived = getApi(apiUrl)
			uuid = dataReceived['id']
			returned = True
			return uuid
		except:
			pass

def getFriends(getUuid):
	gotFriends = False
	apiUrl = f'https://api.hypixel.net/friends?key={apiKey}&uuid={getUuid}'
	while True:
		dataReceived = getApi(apiUrl)
		friendsList = []
		if dataReceived != None:
			if 'records' not in dataReceived:
				print('failed, probably rate limited, retrying')
				time.sleep(1)
				continue
			for friendsEntry in dataReceived['records']:
				uuidSender = friendsEntry['uuidSender']
				uuidReceiver = friendsEntry['uuidReceiver']

				diffUuid = None
				if getUuid == uuidSender:
					friendsList.append(uuidReceiver)
				else:
					friendsList.append(uuidSender)
			return friendsList
	return []

def getUsernameFromUuid(uuid):
	returned = False
	while not returned:
		try:
			apiUrl = f'https://api.mojang.com/user/profiles/{uuid}/names'
			dataReceived = getApi(apiUrl)
			dataReceivedLen = len(dataReceived)
			lastUsername = dataReceived[dataReceivedLen - 1]['name']
			returned = True
			return lastUsername
		except:
			pass

def uuidListToUsernames(uuidList):
	for i, uuid in enumerate(uuidList):
		uuidList[i] = getUsernameFromUuid(uuid)
	return uuidList

def pathfindFriends(pfFrom, pfTo):
	checkQueue = [pfFrom]
	alrCheckedOrQueued = {}
	nodePrev = {}
	while len(checkQueue) > 0:
		curCheck = checkQueue[0]
		curFriends = getFriends(curCheck)
		alrCheckedOrQueued[curCheck] = True
		checkQueue.pop(0)
		print(f'checking {curCheck}, checked {len(alrCheckedOrQueued) - len(checkQueue)}, to potentially check {len(checkQueue)}')
		for friend in curFriends:
			if friend == pfTo:
				print('found path')
				nodePrev[pfTo] = curCheck
				break
			if friend not in alrCheckedOrQueued:
				checkQueue.append(friend)
				alrCheckedOrQueued[friend] = True
				nodePrev[friend] = curCheck
		else:
			continue
		break
	else:
		print('not found')
		return [] #no path found
	path = [pfTo]
	while path[len(path) - 1] != pfFrom:
		path.append(nodePrev[path[len(path) - 1]])
	return list(reversed(path))

global apiKey
readApiKey()
print('testing api key')
testApiKey()

global pathfindFrom
global pathfindTo
print()
print('pathfinding targets (not case-sensitive):')
print()
pathfindFrom = input('	pathfind from:	')
pathfindTo = input('	pathfind to:	')
print()

pathfindFrom = getUuid(pathfindFrom)
pathfindTo = getUuid(pathfindTo)

timerStart = time.time()
pathFound = pathfindFriends(pathfindFrom, pathfindTo)
timerDone = time.time()
print()
print(f'Time: {int(((timerDone - timerStart)/60)*100)/100}mins = {int(timerDone - timerStart)}s = {int((timerDone - timerStart)*1000)}ms')
pathFoundUsernames = uuidListToUsernames(pathFound)
pathFoundUsernamesPretty = ' --> '.join(pathFoundUsernames)

print()
print(pathFoundUsernamesPretty)

while True: time.sleep(1) #indefinitely pause