import matplotlib.pyplot as plt
import numpy as np
import statistics as st
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

results = []
header = []
data = []
unopt_median_time = []
unopt_normalised_time = []
opt_normalised_time = []
opt_normalised_median_time = []
speedup = []
unopt_times = []
opt_times = []

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
    if "unopt" in result[0]:
        unopt_times.append(temp)
    elif "opt" in result[0]:
        opt_times.append(temp)

for i in unopt_times:
    unopt_median_time.append([i[0], st.median(i[1:])])

for i in range(0, len(unopt_median_time)):
    times_u = [round(t / unopt_median_time[i][1], 2) for t in unopt_times[i][1:]]
    unopt_normalised_time.append(times_u)

    times_on = [round(t / unopt_median_time[i][1], 2) for t in opt_times[i][1:]]
    opt_normalised_time.append(times_on)

    times_o = [round(t / unopt_median_time[i][1], 2) for t in opt_times[i][1:]]
    opt_normalised_median_time.append([opt_times[i][0], st.median(times_o)])

# print(unopt_times)
# print(opt_times)
# print(unopt_median_time)
# print(opt_normalised_median_time)

labels = [i[0].split(".")[0] for i in opt_times]
unopt_normalised = [1]*len(unopt_times)
opt_normalised = [i[1] for i in opt_normalised_median_time]

confidence_unopt = [round(confidence_error(i), 3) for i in unopt_normalised_time]
confidence_opt = [round(confidence_error(i), 3) for i in opt_normalised_time]
# print(confidence_unopt)
# print(confidence_opt)

f = plt.figure()
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

width=1
x=np.array([3*i for i in range(0, len(labels))])

bar_unopt = plt.bar(x, unopt_normalised, width, label="Unoptimized (baseline)", yerr=confidence_unopt)
bar_opt = plt.bar(x+width, opt_normalised, width, label="Optimized (COATL)", yerr=confidence_opt)

plt.ylabel("Runtime (Normalized)", fontsize=20)
plt.ylim(0, 1.3)
plt.xlabel("Benchmarks", fontsize=20)
plt.xticks(x+0.5, labels)
plt.legend(loc='upper left', ncols=3)

plt.tight_layout()
plt.show()

f.savefig("results/runtime-speedup-fig11.pdf", bbox_inches='tight')
