import os
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import time
from subprocess import Popen, PIPE
import numpy as np
import pickle

N = 40 #repeat number, should > 2

def fail_if_error(error):
    if error:
        print(error)
        raise AssertionError()

def remove_min_max(x):
    trimmed = x[:]
    trimmed.remove(max(trimmed))
    trimmed.remove(min(trimmed))
    return trimmed

def extract_runtime(output):
    ind = output.find(b'Execution time: ')
    stop_ind = output.find(b' seconds', ind)
    return float(output[ind + 16:stop_ind])


def run_benchmark(cmd):
    results = []
    for _ in range(N):
        p = Popen(cmd, stdin=None, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        fail_if_error(error)
        results.append(extract_runtime(output))

    print('Got the following runtimes:', results)
    results = remove_min_max(results)
    re = 1000 * np.array(results)
    return np.mean(re), np.std(re)


def fuse_cmd(command, cid, dim):
    if cid < 5: # Non Mirage command
        cmd = command + [str(x) for x in dim]
        print('Running command: ', cmd)
    else:
        dim = ' '.join(str(x) for x in dim)
        cmd = command + ['--params=' + dim]
        print('Running command: ', cmd)
    return cmd


def run_benchmark_all_dims(command, cid, dims):
    return [run_benchmark(fuse_cmd(command, cid, dim)) for dim in dims]

# The benchmarks.
benchmarks = {
    'map': [],
    'fold': []
}

# Commands for running the benchmarks.
for b in benchmarks.keys():
    benchmarks[b].append(([b + '/' + b + '_eval.exe'], 0))
    benchmarks[b].append(([b + '/' + b + '_eval.bc'], 1))
    benchmarks[b].append(([b + '/' + b + '_eval_owl.exe'], 2))
    benchmarks[b].append(([b + '/' + b + '_eval_owl.bc'],  3))
    benchmarks[b].append((['node', b + '/' + b + '_eval.js'],  4))
    benchmarks[b].append(([b + '_mirage/' + b + '_mirage_base.native'],  5))
    benchmarks[b].append(([b + '_mirage/' + b + '_mirage_owl.native'],  6))


# The shapes of the Ndarrays.
"""
dims = [[100],
        [300],
        [600],
        [33, 33],
        [50, 50],
        [70, 70],
        [100, 100],
        [150, 150],
        [200, 200],
        [250, 250],
        [300, 300],
        [350, 350],
        [400, 400],
        [450, 450],
        [500, 500],
        [600, 600],
        [700, 700],
        [800, 800],
        [900, 900],
        [100, 100, 100],
        [120, 120, 120],
        [140, 140, 140],
        [160, 160, 160],
        [180, 180, 180],
        [200, 200, 200],
        [220, 220, 220],
        [240, 240, 240],
        [260, 260, 260],
        [280, 280, 280],
        [300, 300, 300]]  # TODO: change here the dimensions
"""

dims = [[100],
        [200],
        [300],
        [450],
        [600],
        [800],
        [33, 33],
        [40, 40],
        [50, 50],
        [60, 60],
        [70, 70],
        [80, 80],
        [100, 100],
        [120, 120],
        [150, 150],
        [200, 200],
        [250, 250],
        [300, 300],
        [350, 350],
        [400, 400],
        [500, 500],
        [600, 600],
        [700, 700],
        [800, 800]]

x_labels = ['10^{:.1f}'.format(np.log10(np.prod(np.array(dim)))) for dim in dims]

x = [np.prod(np.array(dim)) for dim in dims]

ls = ['-', '-', '--', '--', ':', '-.', '-.']
marker = ['o', '^', 'o', '^', '.', 's', '*']
color = ['orchid', '#008744', '#d62d20', 'coral', '#0057e7', '#ffa700', '#77428d']
legend = ['native-owl', 'bytecode-owl','native-base','bytecode-base', 
    'javascript', 'mirage-base', 'mirage-owl']

font=18
params = {'legend.fontsize': font,
          'figure.figsize': (19, 7.5),
         'axes.labelsize': font-2,
         'axes.titlesize': font,
         'xtick.labelsize':font,
         'ytick.labelsize':font}
pylab.rcParams.update(params)


results = benchmarks.copy()
for fig_id, b in enumerate(benchmarks.keys()):
    re = [0] * len(legend)
    for command, colour_id in benchmarks[b]:
        re[colour_id] = run_benchmark_all_dims(command, colour_id, dims)
    results[b] = re


# The dir where we save the results.
results_dir = 'results/' + time.strftime('%d-%m-%Y--%H:%M:%S') + '/'
os.makedirs(results_dir)


pickle.dump(results, open(results_dir + "/results.p", "wb"))
#results = pickle.load(open("results.p", "rb"))

for fig_id, b in enumerate(benchmarks.keys()):
    print('Running the ' + b + ' benchmark!')

    plt.subplot(1,2, fig_id+1)
    #plt.figure(fig_id + 1)
    plt.title(b)
    plt.xscale("log", nonposx='clip')
    plt.yscale("log", nonposx='clip')

    plot_handlers = [None for _ in range(len(legend))]
    #for command, colour_id in benchmarks[b]:
    #    results = run_benchmark_all_dims(command, colour_id, dims)
    #    mu, std = zip(*results)
    #    plot_handlers[colour_id] = plt.errorbar(x, mu, std, linestyle=ls[colour_id], marker=marker[colour_id])
    for command, colour_id in benchmarks[b]:
        mu, std = zip(*results[b][colour_id])
        plot_handlers[colour_id] = plt.errorbar(x, mu, std, 
            linestyle=ls[colour_id], 
            marker=marker[colour_id],
            color=color[colour_id])

    plt.xlabel('Ndarray size')
    plt.ylabel('Time (ms)')

    plt.legend(plot_handlers, legend)

plt.savefig(results_dir + b + '.pdf', format='pdf')
plt.close()
