#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import time

if __name__ == '__main__':
    lab = raw_input('Select laboratory:\n')
    tur = raw_input('Select Group:\n')

    target_dir = 'data/turmas/' + lab + '/'
    tm = []
    correct   = []
    allsub    = []
    students  = []
    
    for subdir, dirs, files in os.walk(target_dir, followlinks=False):
        for f in files:
            if f.endswith('.json'):
                tgtf = target_dir + f
                print "Loading", tgtf 
                try:
                    with open(tgtf, 'r') as fp:
                        js = json.load(fp)
                        
                    timev = f.strip('.json')
                    tm.append(timev)
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
                    
    tm = [int(x) for x in tm]                
    correct  = [x for (y,x) in sorted(zip(tm,correct), 
                                      key=lambda pair: pair[0])]
    allsub   = [x for (y,x) in sorted(zip(tm,allsub),   
                                      key=lambda pair: pair[0])]
    students = [x for (y,x) in sorted(zip(tm,students), 
                                      key=lambda pair: pair[0])]
    
    tm.sort()
    yday = time.localtime(tm[0]).tm_yday
    xgraph_str = []
    xgraph_x = []
    for i in range(1, len(tm)):
        if time.localtime(tm[i]).tm_yday > yday:
            xgraph_x.append(i)
            xgraph_str.append(time.strftime("%a\n%d/%m\n00:00", 
                                            time.localtime(tm[i])))
            yday = time.localtime(tm[i]).tm_yday
    
    ind = np.arange(len(correct))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    p1 = ax.bar(ind, allsub, color='#b0c4de', width=1)
    p2 = ax.bar(ind, students, color='#3f5d7d', width=1)
    p3 = ax.bar(ind, correct, color='#deb0b0', width=1)
    
    plt.legend((p1[0], p2[0], p3[0]), (u"Submissões", "Alunos", "Sub. Finais Corretas"), 
               loc='upper left')
    
    print xgraph_x
    print xgraph_str
    print "LENcorr", len(correct)
    plt.xticks(xgraph_x, xgraph_str)
    
    plt.tight_layout()
    str_turma = "Turma " + tur
    if tur == "all":
        str_turma = "Todas as turmas"
    plt.title(u"Laboratório " + lab + " - "+ str_turma) 
    plt.savefig("graph"+tur+lab+".png")
    try:
        plt.show()
    except:
        print "Unable to draw"


def px(p):
    print
