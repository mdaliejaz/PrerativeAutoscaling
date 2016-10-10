import argparse
import time
import math
import sys
import datetime
import time
import subprocess
import re
import time
import os

from Queue_10 import *
from random import *

from exponential_average import *
from arima import *
from weighted_average import *

machine_on_list	 	= []
machine_off_list	= []
machine_index		= 0
machine_size		= 0
machine_cap		= 100
#noOfVM			= []
#count 			= 0
fileHandle		= 0

def scale(no_vms_earlier, pred_load, scaling_flag):

	global machine_on_list
	global machine_off_list
	global machine_index
	global machine_size
	global machine_cap
	global count
	#global noOfVM
	#global fileHandle

	no_vms_pred = int(pred_load/machine_cap) + 1;
	#noOfVM.append(no_vms_pred)
	'''
	count += 1
	if scaling_flag == 1:
		fileHandle.write(str(count*10) + "," + str(no_vms_pred) + ", Predictive" + "\n");
	else:
		fileHandle.write(str(count*10) + "," + str(no_vms_pred) + ", Reactive" + "\n");
	'''


	print ("Num vm predicted ", no_vms_pred)
	print ("last_allocated_vms ", no_vms_earlier)

	#now = time.time()
	now = datetime.datetime.now()
	if (no_vms_earlier < no_vms_pred):
		diff = no_vms_pred - no_vms_earlier
		
		if (diff > (machine_size - machine_index)):
			print("Got a spike, turning on all machines")
			diff = machine_size - machine_index
			no_vms_pred = machine_size

		i = 0
		while (i < diff):
			print ("turning on")
			#print (machine_on_list[machine_index])
			cmd = "curl --data \""
			cmd = cmd + machine_on_list[machine_index]
			cmd = cmd + "\" http://52.39.125.23/balancer-manager"
			#print ("Firing curl ", cmd)
			os.popen(cmd)
			#on_status = subprocess.Popen([cmd])
			i += 1
			machine_index += 1		
			#output, err = on_status.communicate()
	elif (no_vms_earlier > no_vms_pred):
		diff = no_vms_earlier - no_vms_pred 
		i = 0
		while (i < diff):
			print ("turning off")
			machine_index -= 1	
			cmd = "curl --data \""
			#print ("index", machine_index)
			cmd = cmd + machine_off_list[machine_index]
			cmd = cmd + "\" http://52.39.125.23/balancer-manager"
			#on_status = subprocess.Popen([cmd])
			#print ("Firing curl ", cmd)
			os.popen(cmd)
			i += 1
			#output, err = on_status.communicate()
	else:
		print("No auto-scaling required")
		return	no_vms_earlier

	#later = time.time()
	later = datetime.datetime.now()
	#difference = int(later - now)
	t = later - now
	print ("Time to scale: ", t.microseconds)

	return no_vms_pred


def get_num_requests(duration):

	logFile = "/var/log/apache2/access.log"

	old_p1 = subprocess.Popen(["wc", "-l", logFile], stdout=subprocess.PIPE)
	old_p2 = subprocess.Popen(["awk", "{print $1}"], stdin=old_p1.stdout, stdout=subprocess.PIPE)
	old_p1.stdout.close()
	old_output, old_err = old_p2.communicate()
	old_output = re.findall(r'\d+', str(old_output))
	old_p2.stdout.close()

	time.sleep(duration)

	new_p1 = subprocess.Popen(["wc", "-l", logFile], stdout=subprocess.PIPE)
	new_p2 = subprocess.Popen(["awk", "{print $1}"], stdin=new_p1.stdout, stdout=subprocess.PIPE)
	new_p1.stdout.close()

	new_output, new_err = new_p2.communicate()
	new_output = re.findall(r'\d+', str(new_output))
	new_p2.stdout.close()

	diff = int(new_output[0]) - int(old_output[0])
	return diff

def read_machines(on_file, off_file):

	global machine_on_list
	global machine_off_list
	global machine_size

	with open(on_file) as f:
			machine_on_list = f.read().splitlines()

	with open(off_file) as f:
			machine_off_list = f.read().splitlines()


	machine_size = len(machine_on_list)

	print ("Machine size ", machine_size)


def read_initial_data():
	# read from file pending ... low priority task
	input_data = [Queue_10() for j in range(180)]
	#print("reading initial data ...");

	with open("trace_files/trace_mix") as f:
		trace = f.read().splitlines()
	
	for j in range(180):
		noise = np.random.normal(0, 100, 10)
		for k in range(10):
			(input_data[j]).enqueue(int(int(trace[j]) + noise[k]))

	return input_data

def dummy_new_val(data):
	time.sleep(5)

	if (data % 10 == 0):
		return data * 10000
	else:
		return 2000

def read_initial_data_10():
	input_data = []

	for j in range(10):
		input_data.insert(0, randint(40,50))

	return input_data

def predict_current_val_lastweek(input_data):
	last_allocated_vms = machine_size
	load_delta 		   = 0
	call_pred		   = True
	threshold		   = 50 
	new_input		   = 0
	global fileHandle

	for j in range(185):
		to_allocate = (input_data[j]).val();
		predict_val = exponential_moving_average(to_allocate)
		#predict_val = arima(to_allocate)
		time = j*10
		print ("To predict array ", to_allocate)
		print ("Predicted value ", predict_val)

		predict_val	= predict_val / 10;
		if (call_pred == True):
			print ("Predictive auto-scaling")
			last_allocated_vms = scale(last_allocated_vms, predict_val, 1)
			

		#new_input = apache_new_val(3600)
		#new_input = dummy_new_val(j)
		new_input = get_num_requests(10)
		new_input = new_input/10
		
		print ("Actual load value ", new_input)

		load_delta	= abs(new_input - predict_val)

		if (load_delta > threshold):
			print ("Reactive auto-scaling")
			last_allocated_vms = scale(last_allocated_vms, new_input, 0)
			call_pred = False
			#fileHandle.write(str(time) + "," + str(last_allocated_vms) + ",Reactive" + "\n");
		else:
			call_pred = True
			#fileHandle.write(str(time) + "," + str(last_allocated_vms) + ",         " + "\n");
			
			(input_data[j]).enqueue(new_input)
		
		if (load_delta > threshold):
			fileHandle.write(str(time) + "," + str(last_allocated_vms) + ",Reactive" + "\n");
		else:
			fileHandle.write(str(time) + "," + str(last_allocated_vms) + ",Predictive" + "\n");

def predict_current_val_last10(input_data):
	last_allocated_vms = 0
	load_delta 		   = 0
	call_pred		   = True
	threshold		   = 50 
	new_input		   = 0

	while (True):

		predict_val = exponential_moving_average(input_data, 10)

		print ("Predicted value ", predict_val)

		if (call_pred == True):
			print ("Predictive auto-scaling")
			last_allocated_vms = scale(last_allocated_vms, predict_val)

		#new_input = apache_new_val(3600)
		#new_input = dummy_new_val(j)
		new_input = get_num_requests(10)
		new_input = new_input/10
		
		print ("Actual load value ", new_input)

		load_delta	= new_input - predict_val

		if (load_delta > threshold):
			print ("Reactive auto-scaling")
			last_allocated_vms = scale(last_allocated_vms, new_input)
			call_pred = False
		else:
			call_pred = True


		input_data.insert(0, new_input)

def predict_current_val_combined(input_data_week, input_data_10):
	last_allocated_vms 	   = 0 
	load_delta 		   = 0
	call_pred		   = True
	threshold		   = 50 
	new_input		   = 0

	for j in range(185):
		to_allocate = (input_data_week[j]).val();
		to_allocate.extend(input_data_10)
		predict_val = exponential_moving_average(to_allocate, 10)

		print ("Predicted value ", predict_val)

		if (call_pred == True):
			print ("Predictive auto-scaling")
			last_allocated_vms = scale(last_allocated_vms, predict_val)

		#new_input = apache_new_val(3600)
		new_input = get_num_requests(10)
		new_input = new_input/10
		#new_input = dummy_new_val(j)
		
		print ("Actual load value ", new_input)

		load_delta	= abs(new_input - predict_val)

		if (load_delta > threshold):
			print ("Reactive auto-scaling")
			last_allocated_vms = scale(last_allocated_vms, new_input)
			call_pred = False
		else:
			call_pred = True

		(input_data_week[j]).enqueue(new_input)
		input_data_10.insert(0, new_input)


def test1():
	global machine_index
	
	read_machines("on_file", "off_file")
	input_data = read_initial_data()
	
	#scale(0, 1000, True)
	predict_current_val_lastweek(input_data)

def test2():
	global machine_index
	
	read_machines("on_file", "off_file")
	input_data = read_initial_data_10()
	
	predict_current_val_last10(input_data)

def test3():
	global machine_index
	
	read_machines("on_file", "off_file")
	input_data_week = read_initial_data()
	input_data_10 	= read_initial_data_10()
	
	predict_current_val_combined(input_data_week, input_data_10)

def main():
	global fileHandle
	fileHandle = open("noOfVM.txt", 'w+');
	test1()
	#test2()
	#test3()

if __name__ == "__main__":
	main()
