import sys
from datetime import datetime
import matplotlib.pyplot as plt
from pprint import pprint

# Assumes that this script was called with `python plot.py xxxx.csv`
filename = sys.argv[1]

times = []
ranks = []

with open(filename) as f:
    for line in f:
        # start, end, min, max
        vals = line.split(", ")
        if vals[2] != "0" and vals[3] != "0":
            times.append(datetime.strptime(vals[1], "%Y-%m-%d %H:%M:%S"))
            ranks.append(vals[3])

plt.figure(figsize=(22,10))
plt.plot(times, ranks, color="g")
plt.grid(color="#505030")
ax = plt.gca()
# Make this work with our blog's color scheme
ax.set_axis_bgcolor("#101010")
ax.tick_params(axis="x", colors="#dddddd")
ax.tick_params(axis="y", colors="#dddddd")
# plt.show()
fn = filename.split("-")[0]
plt.savefig(fn, transparent=True)
