

class Macro(object):
    _start = '{% '
    _end = ' %}'

    def __init__(self,*args,**kwargs):
        self.args = kwargs.pop('arguments',[])
        self._make_arg_string()

    def _make_arg_string(self):
        self.arg_string = ''
        count = 0
        for arg in self.args:
            count += 1
            if count > 1:
                self.arg_string += ','
            if type(arg) == str:
                self.arg_string += '%s' % arg
            else:
                fmt = '%s=%s'
                if type(arg) == dict:
                    self.arg_string += fmt % arg.items()[0]
                else: 
                    self.arg_string += fmt % (arg[0],arg[1])

                
                
            
                
        
            

                
                



