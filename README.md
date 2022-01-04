# hypixel-friends-pathfind-portable
finds a path between two players on hypixel using friends lists. first checks friends, then mutual friends, then mutual mutual friends etc. until it finds a path.

limited by the hypixel api ratelimit to 120 friends lists checked per minute.

setup:
* pip install requests (used to make requests to hypixel api)

* put your api key in apiKey.txt

* set your players to pathfind from and to in the two text files

* run main.py

if it is a long path it will take a long time to find.

works for any players as long as there is a path (there probably will be...)
