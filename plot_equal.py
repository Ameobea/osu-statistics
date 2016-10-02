import sys
from datetime import datetime
import matplotlib.pyplot as plt
from pprint import pprint

times = []
ranks = []

with open("equal.csv") as f:
    for line in f:
        # timestamp, rank
        vals = line.split(",")
        times.append(datetime.strptime(vals[0], "\"%Y-%m-%d %H:%M:%S\""))
        ranks.append(vals[1].replace("\"", ""))

plt.figure(figsize=(22,10))
plt.plot(times, ranks, color="g")
plt.grid(color="#505030")
ax = plt.gca()
# Make this work with our blog's color scheme
ax.set_axis_bgcolor("#101010")
plt.show()
plt.savefig("equal.png", transparent=True)
