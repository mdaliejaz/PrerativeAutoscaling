import sys
# import getopt
import os
# from subprocess import PIPE, run
import subprocess
import re
import time


# try:
#     opts, args = getopt.getopt(sys.argv[1:], ':l:f:h', ['logFile=', 'frequency=', 'help'])
# except getopt.GetoptError:
#     # usage()
#     print("error in input")
#     sys.exit(2)

# logFile = "/var/log/apache2/access.log"
logFile = "sampleLog"
# frequency = None

# for opt, arg in opts:
#     if opt in ('-h', '--help'):
#         print("help")
#         sys.exit(2)
#     elif opt in ('-l', '--logFile'):
#         logFile = arg
#     elif opt in ('-f', '--frequency'):
#         frequency = arg
#     else:
#         print("unknown")
#         sys.exit(2)

# if logFile == None:
#     print("error: logFile not provided")
#     sys.exit(2)

# if frequency == None:
#     frequency = 60

# if type(frequency) is not int:
#     print("error: frequency should be integer")
#     sys.exit(2)

# if os.path.exists(logFile):
#     print "error: logFile does not exist."
#     sys.exit(2)

# lastCount = "wc -l "+ logFile + " | sed 's/\\([0-9]*\\).*/\\1/'"
# subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read()
# process = subprocess.Popen(..)   # pass command and arguments to the function
# stdout, stderr = process.communicate()

# command = ['echo', 'hello']
# result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
# print(result.returncode, result.stdout, result.stderr)

old_p1 = subprocess.Popen(["wc", "-l", logFile], stdout=subprocess.PIPE)
# old_p2 = subprocess.Popen(["sed", "s/\\([0-9]*\\).*/\\1/"], stdin=old_p1.stdout, stdout=subprocess.PIPE)
old_p2 = subprocess.Popen(["awk", "{print $1}"], stdin=old_p1.stdout, stdout=subprocess.PIPE)
old_p1.stdout.close()

output, err = old_p2.communicate()
output = re.findall(r'\d+', str(output))
# print(output[0])
old_p2.stdout.close()

time.sleep(5)

new_p1 = subprocess.Popen(["wc", "-l", logFile], stdout=subprocess.PIPE)
# old_p2 = subprocess.Popen(["sed", "s/\\([0-9]*\\).*/\\1/"], stdin=old_p1.stdout, stdout=subprocess.PIPE)
new_p2 = subprocess.Popen(["awk", "{print $1}"], stdin=new_p1.stdout, stdout=subprocess.PIPE)
new_p1.stdout.close()

new_output, new_err = new_p2.communicate()
new_output = re.findall(r'\d+', str(new_output))
# print(output[0])
new_p2.stdout.close()

diff = int(new_output[0]) - int(output[0])
print(diff)
# print(err)
# lastCount = ["ls", "-l"]
# workingDir = "."
# result = subprocess.Popen(lastCount,cwd=workingDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
# result = subprocess.check_output(lastCount)
# result = run(lastCount, stdout=PIPE, stderr=PIPE, universal_newlines=True)
# print(result.returncode, result.stdout, result.stderr)
# print(result)

# while(1):
#     newCount = "wc -l "+ logFile + " | sed 's/\\([0-9]*\\).*/\\1/'"
    # diff = newCount - lastCount










