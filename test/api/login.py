
from pymongo import Connection

server="localhost"
port = 27017
#Establish a connection with mongo instance.
conn = Connection(server,port)

poll = conn.events.polls_post.find_one({},{"title" : 1}) #first parameter is the query, second one is the projection.
print "Title : ", poll['title']
