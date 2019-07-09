import os
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import time
from subprocess import Popen, PIPE
import numpy as np
import pickle

N = 20

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
        output, _ = p.communicate()
        #fail_if_error(error)
        results.append(extract_runtime(output))

    print('Got the following runtimes:', results)
    results = remove_min_max(results)
    re = 1000 * np.array(results)
    return np.mean(re), np.std(re)


def fuse_cmd(command, cid, dim):
    cmd = command + [str(x) for x in dim]
    print('Running command: ', cmd)
    return cmd


def run_benchmark_all_dims(command, cid, dims):
    return [run_benchmark(fuse_cmd(command, cid, dim)) for dim in dims]

# The benchmarks.
benchmarks = {
    'gd1': [],
    'gd2': []
}

results = benchmarks.copy()

name = ['base-native', 'base-byte', 'mirage-base', 
    'owl-native', 'owl-byte', 'mirage-owl', 'js']

# Commands for running the benchmarks.
for b in benchmarks.keys():
    benchmarks[b].append(([b + '/' + 'gd_base.exe'], 0))
    benchmarks[b].append(([b + '/' + 'gd_base.bc'], 1))
    benchmarks[b].append(([b + '_mirage/' + 'gd_base.native'], 2))
    benchmarks[b].append(([b + '/' + 'gd_owl.exe'], 3))
    benchmarks[b].append(([b + '/' + 'gd_owl.bc'],  4))
    benchmarks[b].append(([b + '_mirage/' + 'gd_owl.native'], 5))
    benchmarks[b].append((['node', b + '/' + 'gd_base.js'],  6))
    


for fig_id, b in enumerate(benchmarks.keys()):
    re = [(0, 0)] * len(name)
    for command, colour_id in benchmarks[b]:
        re[colour_id] = run_benchmark(command)
    results[b] = zip(*re)


re_str = "Results:\n"
for b in benchmarks.keys():
    mu, std = results[b]
    re_str += (b + '\n')
    re_str += '\t'.join(name)
    re_str += '\n'
    re_str += '\t\t'.join(('%.2f' % x) for x in mu)
    re_str += '\n'
    re_str += '\t\t'.join(('%.2f' % x) for x in std)
    re_str += '\n'

results_dir = 'results/' + time.strftime('%d-%m-%Y--%H:%M:%S') + '/'
os.makedirs(results_dir)

pickle.dump(results, open(results_dir + "/results.p", "wb"))

#with open(results_dir + 'results.txt', 'w+') as f:
#    f.write(re_str)

font=18
params = {'legend.fontsize': font,
          'figure.figsize': (10, 6),
         'axes.labelsize': font-2,
         'axes.titlesize': font,
         'xtick.labelsize':font,
         'ytick.labelsize':font}
pylab.rcParams.update(params)

bar_mu  = [([0],[0])]*(len(name))
bar_std = [([0],[0])]*(len(name))

blen = len(benchmarks.keys())
mus  = [0] * blen
stds = [0] * blen

for i, b in enumerate(benchmarks.keys()):
    mus[i], stds[i] = results[b]

bar_mu = zip(*mus)
bar_std = zip(*stds)

n_groups = 2

bar_width = 0.11
fig, ax = plt.subplots()
index = np.arange(n_groups)
opacity = 0.9
error_config = {'ecolor': '0.3'}


for i, n in enumerate(name):
    ax.bar(index + i * bar_width, bar_mu[i], bar_width,
        alpha=opacity,
        yerr=bar_std[i], error_kw=error_config,
        label=name[i])

ax.set_xlabel('Use Gradient Descent to find $argmin(f)$')
ax.set_ylabel('Time (ms)')
ax.set_xticks(index + bar_width * 2.3)
ax.set_xticklabels(('$f(x) = sin(x)$', '$f(x)=x^3 - 2x^2 +2$'))
ax.legend()

fig.tight_layout()
plt.savefig(results_dir + 'numcmp.pdf', format='pdf')
plt.close()