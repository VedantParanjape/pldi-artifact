import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import argparse

def confidence_error(data, confidence=0.95):
    dist = st.NormalDist.from_samples(data)
    z = st.NormalDist().inv_cdf((1 + confidence) / 2.)
    h = dist.stdev * z / ((len(data) - 1) ** .5)
    return h

parser = argparse.ArgumentParser(description="Generate normalized runtime plots from benchmark results.")
parser.add_argument("filepath", type=str, help="Path to the input CSV file (semicolon-separated).")
args = parser.parse_args()

file = open(args.filepath, mode ='r')
filew = open('results/runtime-speedup-table1.csv', mode='w+')

results = []
header = []
data = []
vals = []
speedup = []

for line in file.readlines():
    results.append(line.strip().split(";"))

header = results[0]
for result in results[1:]:
    result.pop()
    temp = []
    temp.append(result[0])
    for value in result[1:]:
        temp.append(int(value))
    data.append(temp)

for i in data:
    vals.append([i[0], st.median(i[1:])])

for i in range(0, len(vals), 2):
    speedup.append([vals[i][0].split(".")[0], vals[i][1]/vals[i+1][1]])

labels = [i[0] for i in speedup]
speedup_values = [i[1] for i in speedup]
confidence = [confidence_error(i[1:]) for i in data]
# print(speedup)
# print(labels)
# print(speedup_values)
# print(confidence)

buffer = []
buffer.append("benchmark,speedup,avgunoptruntime,avgoptruntime\n")

for i in range(0, len(vals), 2):
    buffer.append(f"{labels[int(i/2)]},{round(speedup_values[int(i/2)],2)},{round(vals[i][1],2)},{round(vals[i+1][1],2)}\n")

for i in buffer:
    filew.write(i)
