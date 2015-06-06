from wtforms import widgets, fields
from blog.fields import TagField
from flask import url_for

class AceEditorWidget(object):
    def __init__(self,mode='python',theme='twilight'):
        self.theme = theme
        self.mode = mode
        self.theme_js = 'editor.setTheme("ace/theme/%s");'  % self.theme
        self.mode_js = 'editor.setStyle("ace/mode/%s");' % self.mode
        self.js = '''
    <script src="http://ajaxorg.github.io/ace-builds/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
    <script src="http://code.jquery.com/jquery.js"></script>                                                                      
    <script type="text/javascript">
    $(function(){
        var editor = ace.edit('editor');
        %s
        %s
    });
    </script>
    });
        ''' % (self.mode_js,self.theme_js)
        
    def __call__(self,field,**kwargs):
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        html = '<div id="editor">%s</div>' % kwargs['value'] + '\n' + self.js
        return widgets.HTMLString(html)
    
class AceEditorField(fields.Field):
    widget = AceEditorWidget()
    
    def __init__(self,label=None,
                 validators=None,
                 mode='python',
                 theme='twilight',
                 **kwargs):
        super(AceEditorField,self).__init__(label,validators,**kwargs)
    
    
    def process_formdata(self,valuelist):
        if valuelist:
            self.data = valuelist[0]
        else:
            self.data = ''
            
    def _value(self):
        return text_type(self.data) if self.data is not None else ''
    
