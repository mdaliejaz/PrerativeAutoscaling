import random

with open("trace_files/trace_new") as f:
	trace = f.read().splitlines()

new_file = open("trace_files/trace_new_noise", "w")
for j in range(180):
	#noise = np.random.normal(0, 100, 10)
	noise = random.randint(-300, 300)
	new_file.write(str(int(trace[j]) + noise) + "\n")
