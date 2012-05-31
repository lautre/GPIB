# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:47:03 2012

@author: Laurent Tremboy
"""

from time import *
from collections import *
from struct import *

from Generic import *
from GpibHeader import Header
from GPIB import Device

class LMG500(Device):

    class Voltage(IsSubscriptable):
        def __iter__(self):
            for item in self.items:
                for ytem in self[item].items:
                    yield item,ytem,self[item][ytem]
            return
    class Current(IsSubscriptable):
        def __iter__(self):
            for item in self.items:
                for ytem in self[item].items:
                    yield item,ytem,self[item][ytem]
            return

    class Power(IsSubscriptable):
        def __iter__(self):
            for item in self.items:
                for ytem in self[item].items:
                    yield item,ytem,self[item][ytem]
            return

    class Readouts(IsSubscriptable):
        def __iter__(self):
            for item in self.items:
                for ytem in self[item].items:
                    yield item,ytem,self[item][ytem]
            return

    class Waveforms(IsSubscriptable):
        _batch=[]
        _names=[]

    class Harmonics(IsSubscriptable):
        _batch=[]
        _names=[]

        def init(self,args):
            self.items=['voltage','current']

        def __iter__(self):
            for item in self.items:
                for ytem in self[item].items:
                    yield item,ytem,self[item][ytem]

        @property
        def voltage(self):
            self.lmg.instrument.select.immediate='HRMHUN'
            self.lmg.read.harmonics.voltage.thdistort1.batch
            self.lmg.fetch.harmonics.voltage.thdistort2.batch
            self.lmg.fetch.harmonics.voltage.thdistort3.batch
            self.lmg.fetch.harmonics.voltage.thdistort4.batch
            self.lmg.fetch.harmonics.voltage.thdistort5.batch
            self.lmg.fetch.harmonics.voltage.thdistort6.batch
            self.lmg.fetch.harmonics.voltage.thdistort7.batch
            self.lmg.fetch.harmonics.voltage.thdistort8.batch
            values=self.lmg.query
            self.lmg.instrument.select.immediate='NORML'
            return LMG500.Readouts(thd=values.values())

        @property
        def current(self):
            self.lmg.instrument.select.immediate='HRMHUN'
            self.lmg.read.harmonics.current.thdistort1.batch
            self.lmg.fetch.harmonics.current.thdistort2.batch
            self.lmg.fetch.harmonics.current.thdistort3.batch
            self.lmg.fetch.harmonics.current.thdistort4.batch
            self.lmg.fetch.harmonics.current.thdistort5.batch
            self.lmg.fetch.harmonics.current.thdistort6.batch
            self.lmg.fetch.harmonics.current.thdistort7.batch
            self.lmg.fetch.harmonics.current.thdistort8.batch
            values=self.lmg.query
            self.lmg.instrument.select.immediate='NORML'
            return LMG500.Readouts(thd=values.values())

    class Numerics(IsSubscriptable):
        _names=[]
        _batch=[]

        def __iter__(self):
            while 1:
                return self.dict

        def __getitem__(self,item):
            if item=='dict':
                return self.dict
            return self.dict[item]

        def __setitem__(self,item,value):
            if item in self.names:
                return self.wait(item,value)
            else:
                if item not in self.items:
                    self.items.append(item)
                setattr(self,item,value)
            return

        @property
        def functions(self):
            return self.names
        @functions.setter
        def functions(self,args):
            self._batch=[]
            for func in args:
                func,subsfuncts=func.split()
                for sub in subsfuncts.split(','):
                    for index in range(1,9):
                        self._batch.append([func.lower(),'%s%d'%(sub.lower(),index)])
            self._names=''
            return

        @property
        def names(self):
            if not self._names:
                 self._names=['_'.join(name) for name in self._batch]
            return  self._names
        @names.setter
        def names(self,args):
            self.functions=args
            self._names=[]
            return

        def log(self, duration=2,rate=0.2):
            starttime=time()
            while time()-starttime<duration:
                print time()-starttime
                yield self.readouts
#                sleep(rate)
            return

        def wait(self,measure,value,tolerance=0.05):
            print 'testing',abs((self[measure]/value)-1)
            while (abs((self[measure]/value)-1))>tolerance:
                print (self[measure]/value)-1
                print 'waiting'

        @property
        def values(self):
            self.lmg.read[self._batch[0][0]][self._batch[0][1]].batch
            for p1,p2 in self._batch[1:]:
                self.lmg.fetch[p1][p2].batch
            values=self.lmg.query
            return values.values()

        @property
        def readouts(self):
            results=LMG500.Readouts()
            values=self.values
            for name,value in zip(self.names,values):
                value=float(value)
                param,mode=name[:-1].split('_')
                if param not in results.items:
                    results[param]=LMG500.Readouts()
                if mode not in results[param].items:
                    results[param][mode]=[]
                results[param][mode].append(value)
            return results

        @property
        def dict(self):
            results=OrderedDict()
            for name,value in zip(self.names,self.values):
                value=float(value)
                param,mode=name[:-1].split('_')
                if not results.has_key(param):
                    results[param]={}
                if not results[param].has_key(mode):
                    results[param][mode]=[]
                results[param][mode].append(value)
            return results


    name='LMG500'
    headers='CALCULATE','FETCH','READ','DISPLAY','SYST','INITIATE','INSTRUMENT'
    _functions=[]

    def __init__(self,instrument):
        print 'Initialization',self.name
        self.gpib=instrument
        for header in self.headers:
            self.makeHeader(header)
        self._queue=[]
        self._batch=[]
        self.initconfig()
        return

    def initconfig(self):
        self.numerics=self.Numerics()
        self.numerics.lmg=self

        self.harmonics=self.Harmonics()
        self.harmonics.lmg=self

    @property
    def query(self):
        results=self.gpib.ask(';'.join(self._batch))
        values=OrderedDict()
        for val,name in zip(results,self._batch):
            name='_'.join(name.split(':')[-2:])[:-1]
            try:
                values[name]=(float(val))
            except:
                 values[name]=(val)
        self._batch=[]
        return values

    @property
    def functions(self):
        return self._functions
    @functions.setter
    def functions(self,args):
        pass

    @property
    def readouts(self):
        return self.numerics.readouts

def run():

    from Prologix import Prologix
    ip=Address()
    ip['prologix']='192.168.0.94'

    instrument=Prologix(ip.prologix,0)

    lmg=LMG500(instrument)
    lmg.instrument.select.immediate='NORML'
    sleep(1)
    lmg.read['current']['trms1'].batch
    lmg.fetch['voltage']['trms1'].batch
    lmg.numerics.functions='VOLTAGE TRMS','CURRENT TRMS','POWER ACTIVE', 'POWER APPARENT','CURRENT AC','CURRENT DC'
#    print lmg.numerics['voltage']['trms']
    readouts=lmg.readouts
    print lmg.readouts
    for p,s,val in readouts:
        print p,s,val
    return
    for data in lmg.numerics.log():
        for p,s,val in data:
            print p,s,val

    for p,s,val in lmg.harmonics:
        print p,s,val

    return lmg.numerics.readouts.voltage.trms
#    lmg.numerics['voltage_trms1']=230
#    lmg.syst.lang.immediate='SCPI'

#    sys.exit()
#    dc    = Powernet(ip.labjack)
#    load  = LD3091  (ip.agilent,3)
#    ac    = SW5250  (ip.agilent,25)
    meter = WT500   (ip.agilent,1)
    meter.numerics['URMS_3']=238
    for measures in meter.numerics.log(5):
        print measures

if __name__=='__main__':
    print run()
