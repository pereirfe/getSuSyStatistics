#!/usr/bin/python

import json
import matplotlib.pyplot as plt
import numpy as np
from subprocess import call
import sys
import os

target_dir = 'data/turmas/'

if __name__ == '__main__':
    lab = raw_input('Select laboratory:\n')
    tur = raw_input('Select Group:\n')

    tm = []
    correct   = []
    allsub    = []
    students  = []
    
    for subdir, dirs, files in os.walk(target_dir, followlinks=False):
        for f in files:
            if f.endswith('.json'):
                tgtf = target_dir + lab + '/'+ f
                print "Loading", tgtf 
                try:
                    with open(tgtf, 'r') as fp:
                        js = json.load(fp)

                    time = f.strip('.json')
                    tm.append(time)
                    if tur != 'all':
                        correct.append(js[tur]['finais_corretas'])
                        allsub.append(js[tur]['total'])
                        students.append(js[tur]['alunos'])
                    else:
                        correct.append(0)
                        allsub.append(0)
                        students.append(0)
                        for key, s in js.iteritems():
                            correct[-1] += (s['finais_corretas'])
                            allsub[-1] += (s['total'])
                            students[-1] += (s['alunos'])
                        
                except:
                    print "Not ready"
                    pass

    correct = [x for (y,x) in sorted(zip(tm,correct), key=lambda pair: pair[0])]
    allsub  = [x for (y,x) in sorted(zip(tm,allsub), key=lambda pair: pair[0])]
    students = [x for (y,x) in sorted(zip(tm,students), key=lambda pair: pair[0])]
    
    ind = np.arange(len(correct))*0.8
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(ind, allsub, color='#b0c4de')
    ax.bar(ind, students)
    ax.bar(ind, correct, color='#deb0b0')


    plt.tight_layout()
    plt.show()


def px(p):
    print p
