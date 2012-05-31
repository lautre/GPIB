# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:10:32 2012

@author: Laurent Trembloy
"""
from time import sleep

from GpibHeader import Header
from GPIB import Device

class SW5250(Device):
    _preset=0

    name='SW5250'
    headers=['MEASURE','SYSTEM','PHASE','SOURCE','OUTPUT','MMEMORY','EDIT','FUNCTION','INPUT','FETCH','RATE']


    @property
    def infos(self):
        infos=dict(brand='Elgar',device='SW5250',make='A',type='Programmable AC Source',use='AC')
        return infos

    @property
    def voltage(self):
        pass
    @voltage.setter
    def voltage(self,value):
        self.source.voltage.write=value
        return

    @property
    def preset(self):
        return self._preset
    @preset.setter
    def preset(self,voltage):
        self.output.immediate=0
        if voltage<150:
            if self._preset==120:
                self.output.immediate=1
                return
            self.source.voltage.range.write=0
            self.source.voltage.protection.write=255
            self.source.current.write=39
            self.source.frequency.write=60
            self.commit
            self._preset=120
        elif voltage>=150:
            if self._preset==230:
                self.output.immediate=1
                return
            self.source.voltage.range.write=1
            self.source.voltage.protection.write=510
            self.source.current.write=19.5
            self.source.frequency.write=50
            self.commit
            self._preset=230
        else:
            return 'not allowed'
        sleep(1)
        self.output.immediate=1
        sleep(1)
        return
