from collections import deque
import sys

class IsSubscriptable(object):
    '''Abstract Class defining hidden methods to access attributes with []'''

    def __init__(self,*args,**kargs):
        self.items=[]
        for key in kargs.keys():
            self[key]=kargs[key]
        self.init(args)
        return

    def __call__(self,**kargs):
        for key,value in kargs.iteritems():
            print key,value
            setattr( self.__class__,key,value)
            return

    def init(self,*args):
        pass

    def __repr__(self):
        return str(zip(self.items,self.values))

    def __setitem__(self,item,value):
        if item not in self.items:
            self.items.append(item)
        setattr(self,item,value)
        return

    def __getitem__(self,item):
        return getattr(self,item)

    def __eq__(self,other):
        for item in other.items:
            if self[item]!=other[item]:
                return False
        return True

    def __ne__(self,other):
        for item in other.items:
            if self[item]!=other[item]:
                return True
        return False

    def __iter__(self):
        for item in self.items:
            yield self[item]
        return

    @property
    def addProperty(self):
        pass
    @addProperty.setter
    def addProperty(self,arg):
        '''require name of property, getter, setter'''
        self.items.append(arg[0])
        def getter(obj):
            return arg[1]()
        def setter(obj,val):
            try:
                return arg[2](*val)
            except:
                print 'not allowed'
        setattr(self.__class__,arg[0],property(getter,setter))

    @property
    def dict(self):
        return dict(zip(self.items,self.values))
    @dict.setter
    def dict(self,dict):
        for key,val in dict.items():
            self[key]=val
        return

    @property
    def log(self):
        return zip(self.items,self.values)

    @property
    def values(self):
        result=[]
        for item in self.items:
            result.append(self[item])
        return result

class Address(IsSubscriptable):
    pass

class Delegate(object):

    def delegate(self,function,obj):
        setattr(self,function,getattr(obj,function))
        return

    def property(self,prop,obj):
        def get(self):
            return getattr(obj,prop)
        def set(self,value):
            setattr(obj,prop,value)
        print 'property imported'
        setattr(self.__class__,prop,property(get,set))

class GpibAddress(Address):

    @property
    def address(self):
        return 'TCPIP0::%s::gpib0,%d::INSTR'%(self.ip,self.address)



class Filename(object):

    def __init__(self,root,arg):
        self.list=[]
        self.root=root
        self.name=root
        return

    @property
    def name(self):
        return '_'.join(self.list)
    @name.setter
    def name(self,items):
        if type(items)==type('hello'):
            items.replace(' ','_')
            items=[items,]
        items=[str(x).replace(' ','_') for x in items]
        self.list.extend(items)
        return

    @property
    def reset(self):
        self.list=[]
        self.name=self.root

class Path(object):

    def __init__(self,root):
        self.list=['c:',]
        self.root=root
        self.name=self.root
        return

    @property
    def name(self):
        path='\\'.join(self.list)
        try :
            os.makedirs(path)
        except:
            print 'path exists'
        return path
    @name.setter
    def name(self,items):
        if type(items)==type('hello'):
            items=[items,]
        items=[str(x) for x in items]
        self.list.extend(items)
        return

    @property
    def reset(self):
        self.list=[]
        self.name=self.root
        return

def functionFactory(*args):
    def func():
        return args[0](*args[1:])
    return func

def methodFactory(*args):
    '''add a method to an instance :
        instance,method name,function,args of function'''
    def funct():
        return args[2](*args[3:])
    setattr(args[0],args[1],funct)
    return


if __name__=='__main__':
    d=Delegate()
    def x():
        for i in range(12):
            yield i
        return
    def y(txt):
        print txt
        return txt
    IsSubscriptable.glob='test hi'
    k=IsSubscriptable(name='first')
    l=IsSubscriptable(test='hihi')
    print l,k.glob
#    k.child='hello',x,y
#    print k.hello
##    sys.exit()
#    k.hello='Hi There'
#    d.property('hello',k)
#    d.hello='from d'
#    for i,j in zip( d.hello,k.hello):
#        print i,j