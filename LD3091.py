# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:08:22 2012

@author: Laurent Trembloy
"""

from GpibHeader import Header
from GPIB import Device

class LD3091(Device):

    _mode='Resistive'
    _power=0

    name='3091LD'
    headers='LOAD','MEASURE','FETCH','SYSTEM'
    voltage=230
    numericNames='Power','Power Factor','Current','Crest Factor','Voltage','Frequency'
    loads={'Resistive':['res',1,1.414],'Pfc':['pow',1,1.414],
           'Computer':['pow',0.7,2.5],'Capacitive':['curr',-0.8,2.0],
            'Inductive':['curr',0.8,2.0],'Non Linear':['curr',0.8,2.2]}

    @property
    def infos(self):
        infos=dict(brand='California Instruments',device='3091LD',make=' 3000W',type='Active AC Load',use='LOAD')
        return infos

    @property
    def numericValues(self):
        '''recuperation synchrone des mesures de la charge'''
        self.measure.power.batch
        self.fetch.power.pfactor.batch
        self.fetch.current.batch
        self.fetch.current.crestfactor.batch
        self.fetch.voltage.batch
        self.fetch.frequency.batch
        results=self.query
        self.measure.power.last,self.measure.power.pfactor.last,self.measure.current.last,self.measure.current.crestfactor.last,self.measure.voltage.last,self.measure.frequency=results.values()

        return results.values()

    @property
    def readouts(self):
        return self.numericDict

    @property
    def numericArray(self):
        while 1 :
            yield self.numericValues

    @property
    def numericDict(self):
        results=OrderedDict(zip(self.numericNames,self.numericValues))
        return results

    @property
    def numericCsv(self):
        while 1:
            result=','.join([str(x) for x in self.numericValues])
            yield result

    @property
    def mode(self):
        return self._mode
    @mode.setter
    def mode(self,mode):
        self._mode=mode
        self.load.mode.write=self.loads[mode][0]
        self.load.pfactor.write=self.loads[mode][1]
        self.load.cfactor.write=self.loads[mode][2]
        self.power=self._power
        return

    @property
    def shortcut(self):
        pass
    @shortcut.setter
    def shortcut(self,state='OFF'):
        self.load.scir.immediate=state
        return

    @property
    def power(self):
        return self._power
    @power.setter
    def power(self,power):
        power=float(power)
        self._power=power
        if self.mode=='Resistive':
            if power==0:
                resistance=999
            else:
                resistance=self.voltage**2/power
            if resistance<2.5:
                resistance=2.51
            self.load.res.write=resistance
        if self.mode in ('Capacitive','Inductive','Non Linear'):
            current=float(power)/float(self.voltage)
            current=current/self.loads[self.mode][1]
            if current>29.99:
                current=29.99
            self.load.current.write=abs(current)
        if self.mode in ('Pfc',):
            power=power*self.loads[self.mode][1]
            if power>2999:
                power=2999
            self.load.power.write=power
        if self.mode in ('Computer',):
            power=power/0.8*0.7
            if power>2999:
                power=2999
            self.load.power.write=power
        return

    @property
    def csv(self):
        pass
