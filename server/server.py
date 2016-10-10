import SimpleHTTPServer
import SocketServer
#import random
#import time
#import datetime

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
#httpd.serve_forever()
while (1):
#    start_time = time.time()
#    print start_time
    product = 1
    for x in range(1, 100):
        product = product * x
#    product = 1
#    for x in range(1, 100):
#        product = product * x
#    product = 1
#    for x in range(1, 100):
#        product = product * x
#    print product
    httpd.handle_request()
#    end_time = time.time()
#    print end_time
#    uptime = end_time - start_time
#    human_uptime = str(datetime.timedelta(seconds=int(uptime)))
#    print uptime
#    print human_uptime
#    i = i + 1
