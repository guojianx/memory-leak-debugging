#!/usr/bin/python3
import sys
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
from matplotlib.offsetbox import (TextArea, AnnotationBbox)

def get_rss(filename):
    with open(filename) as f:
        for line in f:
            if "VmRSS" in line:
                try:
                    rss = re.search("VmRSS:(.+?)kB", line).group(1)
                except AttributeError:
                    print("couldn't find VmRSS in \"" + line +"\"")
                    exit(1)

                return int(rss)
                

if (len(sys.argv) != 2):
    print(sys.argv[0] + " <pid>")
    exit(1)

proc_file = '/proc/' + sys.argv[1] + '/status'

#rss_hist = [10, 100, 200, 300]
#date_array = ['2019-10-20', '2019-10-21', '2019-10-22', '2019-10-23']
rss_hist = []
date_array = []
fig, ax = plt.subplots(figsize=(20,10))

def draw(i):
    while (len(rss_hist) >= 1800) :
        del rss_hist[0]
        del date_array[0]

    rss_hist.append(get_rss(proc_file))
    date_array.append(str(datetime.datetime.now()))

    max_y = max(rss_hist)
    max_x = rss_hist.index(max_y)
    max_str = date_array[max_x]
    min_y = min(rss_hist)
    min_x = rss_hist.index(min_y)
    min_str = date_array[min_x]

    max_offsetbox = TextArea(max_str, minimumdescent=False)
    min_offsetbox = TextArea(min_str, minimumdescent=False)
    note_str = 'max:  ' + str(max_y) + ' kB\n' + \
               'min:  ' + str(min_y) + ' kB\n' + \
               'diff: ' + str(max_y - min_y) + ' kB'

    max_ab = AnnotationBbox(max_offsetbox, (max_x, max_y),
            xybox=(1.02, 1.02),
            xycoords = 'data',
            boxcoords = "axes fraction",
            box_alignment = (0.5, 0.5),
            arrowprops=dict(arrowstyle="-|>", color="red"))
    min_ab = AnnotationBbox(min_offsetbox, (min_x, min_y),
            xybox=(1.02, 0.96),
            xycoords = 'data',
            boxcoords = "axes fraction",
            box_alignment = (0.5, 0.5),
            arrowprops=dict(arrowstyle="-|>", color="green"))

    period_str = date_array[0] + ' --- ' + date_array[-1]
    ax.clear()
    plt.title(period_str)
    ax.add_artist(max_ab)
    ax.add_artist(min_ab)
    ax.text(.05, .95, note_str,
            transform=ax.transAxes, ha="left", va="top")
    ax.plot(max_x, max_y, 'or')
    ax.plot(min_x, min_y, 'ob')
    ax.plot(rss_hist, linewidth=2)

ani = animation.FuncAnimation(fig, draw, interval = 1000)
plt.show()
