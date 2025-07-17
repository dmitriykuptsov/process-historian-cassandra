import numpy as np
from scipy import stats
from sys import argv

d = []
f = open(argv[1])
l = f.readlines()
for i in l:
	if i.strip() == "":
		continue
	d.append(float(i.strip()))

data = np.array(d)

confidence_level = 0.95  # For a 95% confidence interval
degrees_of_freedom = len(data) - 1
sample_mean = np.mean(data)
standard_error_of_mean = stats.sem(data)

confidence_interval = stats.t.interval(
	confidence_level,
	df=degrees_of_freedom,
	loc=sample_mean,
	scale=standard_error_of_mean
)

print(str(sample_mean) + " " + str(confidence_interval[0]) + " " + str(confidence_interval[1]))
