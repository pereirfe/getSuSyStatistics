#!/usr/bin/python

import turmas
import time
import json

if __name__ == '__main__':
    interval = int(raw_input('Select time interval in seconds:\n'))
    lab = raw_input('Select laboratory:\n')
    
    print 'Kill this program with Ctrl-D'

    while True:
        try:
            print 'Coletando dados de', time.ctime()
            filename = './data/turmas/' + lab + '/' + str(int(time.time())) + '.json'
            with open(filename, 'w') as f:
                js = turmas.getConsolidateJson(lab)
                json.dump(js,f)
            print ""
            time.sleep(interval)

        except:
            pass

