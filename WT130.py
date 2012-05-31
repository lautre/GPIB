# -*- coding: iso-8859-1 -*-


from time import *
from collections import *
from struct import *

from Generic import *
from GpibHeader import Header
from GPIB import Device

class WT130(Device):

    """WT130 Yokogawa Wattmeter"""

    name='WT130'
    headers='CALCULATE','FETCH','READ','DISPLAY','SYST','INITIATE','MEASURE'

    def initconfig(self):
        print 'init'
        self._initMeasures()

    def _initMeasures(self,liste=('V','A','W','VA','PF','VPK','APK','VHZ')):
        self.measure.normal.item.preset.immediate='NORMAL'
        for item in liste:
            self.measure.item['%s'%item].all.write='ON'
        print self.commit
        return

    def _measure(self):
        values=self.measure.value.ask
        count=0
        for name in self.measures:
            for i in self.channels:
                setattr(self,name+'_'+str(i),values[count])
                count+=1
        return values

    def ask(self,message):
        try:
            result=self.gpib.ask_wt130(message)
        except:
            print 'asking again'
            result=self.gpib.ask_no(message)
        return result


def test():
    from Prologix import Prologix
    ip=Address()
    ip['prologix']='192.168.0.100'

    instrument=Prologix(ip.prologix,2)
    wt130=WT130(instrument)
    print wt130.idn

    r= wt130.measure.value.ask
    print len(r),r
    #acin=AcIn(meter=wt,mchannel=0)
    #acout=Channel(meter=wt,mchannel=1)
    #dcin=Channel(meter=wt,mchannel=2)
    #acin.measure()
    #print acin.channels
    #print dir(acin)
    #print acin._properties
    #acin.log()
    #print acin.voltage,acin.current,dcin.voltage,acin.watts

if __name__=='__main__':
    test()
