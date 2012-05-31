# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:44:26 2012

@author: Laurnet Trembloy
"""

import socket

class Prologix(object):

    name='Prologix'

    def __init__(self,ip,addr=1):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sock.settimeout(5)
        self.sock.connect((ip, 1234))
        self.config='eoi 1'
        self.config='eos 2'
        self._batch=[]
        return

    def __repr__(self):
        return self.name

    def write(self,message):
        print message
        self.sock.send(message+'\n')
        return

    def writeOPC(self,message):
        self.sock.send(message+';*OPC?\n')
        result=self.read()
        while result !='1':
            result=self.read()
            print 'waiting OPC',result
        return

    def read(self):
        try:
            answer=self.sock.recv(10000000)
        except:
            answer=' '
        return self.format(answer)

    def raw(self):
        try:
            answer=self.sock.recv(10000000)
        except:
            answer=' '
        return answer

    def batch(self,message):
        self._batch.append(message)
        return

    def askBin(self,message):
        t= time()
        self.write('FRMT PACKED')
        self.write(message+';*OPC?')
        answer=self.raw()
        while ( (answer[-9:-1]!='#5000011')):
            answer+=self.raw()

        self.write('frmt ASCII')
        liste=answer.split('#5')
        result=[0,]
        for i in liste[1:-1]:
           length=int(i[:5])/4
           result.extend( unpack('%df'%length,i[5:]))

        return result

    def ask(self,message):
        self.write(message+';*OPC?')
        answer=self.raw().strip()
        while not answer:
            answer=self.raw().strip()

        while (answer.split(';')[-1][0]!='1'):
            answer+=self.raw().strip()
        try:
            return map(float,answer.split(';')[:-1])
        except:
             return answer.split(';')[:-1]

    def ask_wt130(self,message):
        self.write(message)
        answer=self.raw().strip()
        while not answer:
            answer=self.raw().strip()
        try:
            return map(float,answer.split(','))
        except:
             return answer.split(',')

    @property
    def config(self):
        pass
    @config.setter
    def config(self,message):
        self.sock.send('++'+message+'\n')
        return

