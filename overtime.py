#!/usr/bin/python

import turmas
import time
import json
import sys

def main():
    try:
        interval = int(sys.argv[1])
        #int(raw_input('Select time interval in seconds:\n'))
        lab = sys.argv[2] #raw_input('Select laboratory:\n')
    except IndexError:  
        print "Use: overtime TIMEINSECONDS LAB"
        return 0

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
            print "Unable to get data.. waiting.."
            time.sleep(interval/5)
            pass


if __name__ == '__main__':
    main()
