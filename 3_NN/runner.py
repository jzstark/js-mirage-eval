import os
import matplotlib.pyplot as plt
import time
from subprocess import Popen, PIPE
import numpy as np

N = 5

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
    cmd = command + [str(x) for x in dim]
    print('Running command: ', cmd)
    return cmd


def run_benchmark_all_dims(command, cid, dims):
    return [run_benchmark(fuse_cmd(command, cid, dim)) for dim in dims]

# The benchmarks.
benchmarks = {
    'sqnet': [],
    'vgg': []
}

results = benchmarks

name = ['base-native', 'base-byte', 'owl-native', 'owl-byte', 
    'js', 'mirage-base', 'mirage-owl']

# Commands for running the benchmarks.
for b in benchmarks.keys():
    benchmarks[b].append(([b + '/' + b + '_base.exe'], 0))
    benchmarks[b].append(([b + '/' + b + '_base.bc'], 1))
    benchmarks[b].append(([b + '/' + b + '_owl.exe'], 2))
    benchmarks[b].append(([b + '/' + b + '_owl.bc'],  3))
    benchmarks[b].append((['node', b + '/' + b + '.js'],  4))
    benchmarks[b].append(([b + '_mirage/' + b + '_mirage_base.native'],  5))
    benchmarks[b].append(([b + '_mirage/' + b + '_mirage_owl.native'],  6))


for fig_id, b in enumerate(benchmarks.keys()):
    re = [(0, 0)] * (len(name))
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

with open(results_dir + 'results.txt', 'w+') as f:
    f.write(re_str)