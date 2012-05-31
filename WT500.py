# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:11:22 2012

@author: rde
"""

from Generic import IsSubscriptable
from GpibHeader import Header
from GPIB import Device

class WT500(Device):

    class Harmonics(IsSubscriptable):
        _names=[]
        _batch=[]

    class Numerics(IsSubscriptable):

        _names=''
        _channels='AC','DC','OUT'

        def __iter__(self):
            while 1:
                return self.dict

        def __getitem__(self,item):
            return self.dict[item]

        def __setitem__(self,item,value):
            if item not in self.items:
                self.items.append(item)
            setattr(self,item,value)
            return

        @property
        def functions(self):
            return self.names
        @functions.setter
        def functions(self,args):
            self.wt.functions=args
            self._names=''
            return

        @property
        def channels(self):
            return self._channels
        @channels.setter
        def channels(self,channels):
            self._channels=channels
            self._names=''
            return

        @property
        def names(self):
            if not self._names:
                 names=self.wt.numeric.normal.ask
                 names=names.replace(',1','_%s'%self.channels[0])
                 names=names.replace(',2','_%s'%self.channels[1])
                 names=names.replace(',3','_%s'%self.channels[2])
                 names=names.split(';')[1:]
                 self._names=[name.split(' ')[1] for name in names]
            return  self._names

        def log(self, duration=2):
            starttime=time()
            self.wt.display.mode.immediate='NUMERIC'
            self.wt.numeric.hold.immediate=0
            sleep(self.wt.rate)
            while time()-starttime<duration:
                yield self.dict
            return

        def wait(self,measure,op,value,timeout=30):

            self.wt.display.mode.immediate='NUMERIC'
            self.wt.numeric.hold.immediate=0
            sleep(self.wt.rate)
            starttime=time()
            print 'waiting',measure
            if type(value)==type('hello'):
                while not(getattr(operator,op)(self[measure],self[value])):
                    if (time()-starttime)>timeout:
                        print 'Time out',measure,self[measure],op,value,self[value]
                        return -1
            else:
                while not(getattr(operator,op)(self[measure],value)):
                    if (time()-starttime)>timeout:
                        print 'Time out',measure,self[measure],op,value
                        return -1
            return 0

        @property
        def values(self):
            sleep(self.wt.rate)
            values=self.wt.numeric.value.ask.split(',')
            values=[float(value) for value in values]
            return values

        @property
        def dict(self):
            results=OrderedDict()
            for name,value in zip(self.names,self.values):
                results[name]=float(value)
            self.last=results
            return results

    class Waveforms(IsSubscriptable):
        pass

    headers='MEASURE','SYSTEM','READ','FILE','DISPLAY','HARMONICS','HOLD','IMAGE','INPUT','NUMERIC','WAVEFORM'
    name='WT3000'
    traces='U1','I1','U2','I2','U3','I3','U4','I4'
#    statics
    _rate=0

    def initconfig(self):
        self.numerics=self.Numerics()
        self.numerics.wt=self
        return

    @property
    def last(self):
        return self.numerics.last

    @property
    def infos(self):
        infos=dict(brand='Yokogawa',device='WT500',make='GPIB',type='Power Analyser',use='METER')
        return infos

    @property
    def trigger(self):
        self.display.mode.immediate='WAVE'
        sleep(self.rate)
        self.io.trigger=1
        sleep(self.rate)
        return
    @trigger.setter
    def trigger(self,io):
        self.io=io
        return

    @property
    def error(self):
        return 'not available'

    @property
    def functions(self):
        return self._functions
    @functions.setter
    def functions(self,funcs):
        print 'setting functions ',funcs
        self._functions=[x+', 1' for x in funcs]
        self._functions.extend([x+', 2' for x in funcs])
        self._functions.extend([x+', 3' for x in funcs])

        for count,func in enumerate(self._functions):
            count+=1
            self.numeric.item.write_ns='%d %s'%(count,func)
        self.numeric.number.write =count
        self.commit
        return

    @property
    def rate(self):
        print self.ask('RATE?')
        if not self._rate:
            self._rate=float(self.ask('RATE?').split()[1])
        return self._rate
    @rate.setter
    def rate(self,rate):
        rate=str(rate)
        self.immediate('RATE %s'%rate)
        print self.ask('RATE?')
        self._rate=float(self.ask('RATE?'))#.split()[1])WT500
        return

    @property
    def preset(self):
        return
    @preset.setter
    def preset(self,number):
        length={1:40,2:60,3:60,4:96}
        self.numeric.preset.write=number
        self.numeric.number.write=length[number]
        self.commit
        return

    @property
    def readouts(self):
        return self.numerics.dict

    @property
    def waveformArrayBin(self):
        for trace in self.waveformBin.split('#44008')[1:]:
            yield trace[:4000]
        return

    @property
    def waveformArray(self):
        traces=[]
        for trace in self.waveformArrayBin:
            length=int( len(trace)/4)
            trace=unpack('>%df'%length,trace[:(length*4)])
            traces.append(trace)
        return traces

    @property
    def waveformBin(self):
        traces=''
        for tr in self.traces:
            self.waveform.trace.immediate=tr
            traces+=self.waveform.send.ask
        return traces

    @property
    def waveformDict(self):
        traces=OrderedDict(zip(self.traces,self.waveformArray))
        return traces
