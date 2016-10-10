import SimpleHTTPServer
import SocketServer
import random
import time
import datetime

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
#httpd.serve_forever()
while (1):
    start_time = time.time()
    #print start_time
    array =  []
    
    for x in range(1, 2000):
        array.append(random.randint(0,9))

    for x in range(1, 1999):
	#print x
	if array[x] % 2 == 0:
	    array[x] += 1

    for x in range(1, 1999):
	if array[x]%2 == 1:
            array[x] -= 1
 
    httpd.handle_request()
    end_time = time.time()
    #print end_time
    uptime = end_time - start_time
    #human_uptime = str(datetime.timedelta(seconds=int(uptime)))
    #print uptime
    #print human_uptime
    #break
#    i = i + 1
