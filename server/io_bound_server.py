import SimpleHTTPServer
import SocketServer
#import random
import time
import datetime
import os

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
#httpd.serve_forever()
while (1):
    start_time = time.time()
    #print start_time
    
    #for x in range(1, 10):
    fileHandle = open("io_file.txt", 'w')
    	#rawState = fileHandle.readline().split(',')
    	#N = int(rawState[0]) + 1;
    	#M = int(rawState[1]) + 2; 
    	#K = int(rawState[2]) + 3;
    fileHandle.write("12,45,64")
    	#op = str(N)
    	#fileHandle.write(str(N) + "," + str(M) + "," + str(K) + ",")
    os.fsync(fileHandle)
    fileHandle.close()
	
    #print N
    httpd.handle_request()
    end_time = time.time()
    #print end_time
    uptime = end_time - start_time
    #human_uptime = str(datetime.timedelta(seconds=int(uptime)))
    print uptime
    #print human_uptime
    #break
#    i = i + 1
