import os
import sys
import subprocess
import re

lines = open("trace_files/trace_new").read().split('\n')
numConns=0; listLines =[]

for line in lines:
	# print line;
   	listLines.append(line.strip())
   	numConns = numConns + int(line)
  
output_filename = ""

count = 0	
for line in listLines:
	count += 1
	output_filename = "output/output_" + line
	#strCommand = "grep RT:" + output_filename + " | awk '{ if($4 >= 6) print $4}' | wc -l" + " >> " + "result.txt"
	p1 = subprocess.Popen(["grep", "RT:", output_filename], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["awk", "{if($4 >= 6) print $4}"], stdin=p1.stdout, stdout=subprocess.PIPE)
	cmd = 'wc -l >> result.txt'
	#p3 = subprocess.Popen(["wc", "-l", ">>", "result.txt"], stdin=p2.stdout, stdout=subprocess.PIPE)
	p3 = subprocess.Popen(cmd, shell=True, stdin=p2.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	p2.stdout.close()
	#output, err = p2.communicate()
	#output = re.findall(r'\d+', str(output))
	p3.stdout.close()
	#if count == 14:
		#break
	#print strCommand
	#os.system(strCommand)
	#print "\n\n\n"
	#grep "RT:" dump | awk '{ if($4 >= 6) print $4}' | wc -l
	
lines2 = open("result.txt").read().split('\n')
listLines2 =[]
for line in lines2:
   	listLines2.append(line.strip())
   
length = len(listLines2)
fileHandle = open("final_result.txt", 'w+');
for x in xrange(0,length):
	fileHandle.write(listLines2[x] + "\n");
	#fileHandle.write(listLines[x]/10 + "," + listLines2[x] + "\n");
	
