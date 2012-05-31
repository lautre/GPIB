# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 11:28:28 2012

@author: Laurent Trembloy
"""

from time import *
from collections import *
from struct import *

from Generic import *
from GpibHeader import Header

class Device(object):

    def __init__(self,instrument):
        print 'Initialization',self.name
        print instrument

        for header in self.headers:
            print header
            self.makeHeader(header)
        self._queue=[]
        self._batch=[]
        self.gpib=instrument

        self.initconfig()
        return

    def initconfig(self):
        pass

    def makeHeader(self,name):
        setattr(self,name.lower(),Header(name, instrument=self))
        return

    def __setitem__(self,item,value):
        setattr(self,item,value)
        return

    def __getitem__(self,item):
        return getattr(self,item)

    def write(self,message):
        self._queue.append(message)
        return

    def ask(self,message):
        try:
            result=self.gpib.ask(message)
        except:
            print 'asking again'
            result=self.gpib.ask(message)
        return result


    def immediate(self,message):
        try:
            result=self.gpib.write(message)
        except:
            print 'writing again'
            result=self.gpib.write(message)
        return result

    def batch(self,message):
        self._batch.append(message)
        return

    @property
    def IDN(self):
        return self.ask('*IDN?')

    @property
    def RST(self):
        return self.ask('*RST')

    @property
    def OPC(self):
        return self.ask('*OPC')

    @property
    def CLS(self):
        return self.ask('*CLS')

    @property
    def query(self):
        results=self.gpib.ask(';'.join(self._batch))
        values=OrderedDict()
        for val,name in zip(results.split(';'),self._batch):
            name=name.split(':')[-1][:-1]
            try:
                values[name]=(float(val))
            except:
                 values[name]=(val)
        self._batch=[]
        return values

    @property
    def commit(self):
        try:
            self.gpib.write(';'.join(self._queue))
        except:
            print 'commiting again'
            self.gpib.write(';'.join(self._queue))
        self._queue=[]
        return

    @property
    def error(self):
        try:
            error=self.gpib.ask(':SYSTEM:ERROR?')
            number,description=error.split(',')
            number=int(number)
            if number :
                print description
                self.lasterror=error
        except:
            print 'Getting error again'
            error=self.gpib.ask(':SYSTEM:ERROR?')
            number,description=error.split(',')
            number=int(number)
            if number :
                print description
                self.lasterror=error
        return error

    def read(self):
        return self.gpib.read()

    @property
    def idn(self):
        return self.ask('*IDN?')
