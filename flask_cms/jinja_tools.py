from jinja2 import Template
from flask.templating import render_template, render_template_string

class JinjaBase(object):
    _symbols = {'start':'{%','end':'%}'}
    _name = None
    _content = ''
    _type = None
    
    def render(self,context={}):
        return render_template_string(str(self),**context)
        
    def _set_ends(self):
        self._set_start()
        self._set_end()
        
    def _set_start(self):
        if self._type is None:
            raise NotImplementedError
        self._start = self._symbols['start'] + self._type + ' ' + self._name + ' ' + self._symbols['end']
        
    def _set_end(self):
        if self._type is None:
            raise NotImplementedError
        self._end = self._symbols['start'] + ' end' + self._type + ' ' + self._name + ' ' + self._symbols['end']
        

class Block(JinjaBase):
    '''
        represents a jinja2 block that can be renderd in a template when called
    '''
    _type = 'block'
    
    def __init__(self,**kwargs):
        if kwargs.get('name',None) is not None:
            self._name = kwargs.pop('name')
        if kwargs.get('content',None) is not None:
            self._content = kwargs.pop('content')
        if self._name:
            self._set_ends()
            
    def __call__(self,context={}):
        return self.render(context)
    
    def __add__(self,other):
        if type(other) == type(self):
            if self._name == other._name:
                return str(Block(name=self._name,content=(str(self._content) + '\n' + str(other._content))))
            else:
                return str(self) + '\n' + str(other)
        else:
            return self % other

    def __mod__(self,other):
        if not type(other) == str:
            raise TypeError('cannot render a %s' % type(other))
        return Block(name=self._name,content=(self._content % other))
    
    def __str__(self):
        return self._str

    def __repr__(self):
        return self._name

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self,content):
        self._content = content

    @property
    def name(self):
        if self._name is None:
            return ''
        else:
            return self._name
    @name.setter
    def name(self,name):
        self._name = name
        self._set_ends()

    @property
    def _str(self):
        return self._start+'\n'+self._content+'\n'+self._end+'\n'
    

class Macro(JinjaBase):
    _args = {}
    _type = 'macro'
    
    def _set_start(self):
        args = ''
        if self._args:
            for k,v in self.args.items():
                if args.keys().index(k) != 0:
                    args += ','
                args += '{}={}'
                if k == args.keys()[-1]:
                    args += ','
        self._start = self._symbols['start'] + self._type + ' ' + self._name + '(' + args + ')' + self._symbols['end']
    
    
        
        
        
