# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:39:22 2012

@author: Laurent Trembloy
"""

class Header(object):

    def __init__(self,name,parent='',instrument=''):
        self.name=name
        self.instrument=instrument
        if parent:
            self.query='%s:%s'%(parent,name.upper())
        else:
            self.query=':%s'%name.upper()

        self.val=0
        self.children=[]#'ask','send','write','read'
        self.last=0
        return

    def __getattr__(self,name):
        if name.lower() not in self.children:
            self.children.append(name.lower())
            h=Header(name,self.query,self.instrument)
            setattr(self,name.lower(),h)
            return h

    def __getitem__(self,item):
        return getattr(self,item)

    def __setitem__(self,item,value):
        return setattr(self,item,value)

    @property
    def ask(self):
        result=self.instrument.ask(self.query+'?')
        self.last=result
        return result

    @property
    def askvalues(self):
        result=self.instrument.gpib.ask_for_values(self.query+'?')
        self.last=result
        return result

    @property
    def batch(self):
        self.instrument.batch(self.query+'?')
        return

    @property
    def write(self):
        pass
    @write.setter
    def write(self,value):
        self.val=value
        value=str(value)
        self.instrument.write(self.query+' '+value)
        return self.query+' '+value

    @property
    def write_ns(self):
        pass
    @write.setter
    def write_ns(self,value):
        self.val=value
        value=str(value)
        self.instrument.write(self.query+value)
        return self.query+' '+value

    @property
    def immediate(self):
        pass
    @write.setter
    def immediate(self,value):
        self.value=value
        value=str(value)
        self.instrument.immediate(self.query+' '+value)
        return self.query+' '+value
