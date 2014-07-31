from hashlib import md5
from urllib import urlencode
import json
from requests import session

class SugarSession(session):
    _base_url = None
    _service = 'rest'
    _user_auth = None
    _session_id = None

    def __init__(self,base_url,user=None,password=None,service=None,*args,**kwargs):
        self._base_url = base_url
        self.service = service or self._service
        self.url = self._base_url + '/' + self.service + '.php'
        self.user_auth = self._make_auth(user,password)
        self._login()
        
        if self.user_auth is not None:
            self._session_id = self._login()
        super(SugarSession,self).__init__(*args,**kwargs)
            
    def _make_entry_list_params(self,module,query='',order_by='',offset='0',select_fields={}):
        rtn =[
                self._session_id,
                module,
                query,
                order_by,
                offset,
                select_fields,
                {},
                '50',
                '0',
                False,
        ]
        return rtn
     
    def _make_auth(self,username,password):
        if username is None:
            return None
        self._post_data = {
                'user_auth': {
                        'user_name':username,
                        'password': self._make_hashed_pw(password),
                        }
                }
        return json.dumps(self._post_data)

    def _make_hashed_pw(self,pw):
        return md5(pw).hexdigest()

    def _make_request_args(self,method,data):
        return  'method={}&input_type=JSON&response_type=JSON&rest_data={}'.format(method,data)

    def _login(self,user=None,pw=None):
        if self.user_auth is None:
            self.user_auth = self._make_auth(user,pw)
        args = self._make_request_args('login',self.user_auth)
        if self._session_id is None:
            return str(self.post(params=args).json()['id'])                
        return self._session_id

    def post(self,*args,**kwargs):
        json_params = kwargs.pop('params',None)
        request = self._make_request_args(kwargs.pop('method',''),json_params)
        return super(SugarSession,self).post(self.url,params=request,*args,**kwargs)

    
    def send_request(self,method,params):
        #print self._session_id
        return self.post(method=method,params=params).json()

    def get_module_records(self,module,select_fields):
        print self._session_id
        return self.send_request('get_entry_list',self._make_entry_list_params(module,select_fields=select_fields))
    def get_module_layout(self,module,mtype='default',view='list'):
        return self.send_request('get_module_layout',self._make_post_params(module,mtype,view))

    def _make_post_params(self,*args):
        args = list(args)
        args.insert(0,self._session_id)
        return args

    def get_upcoming_activities(self):
        return self.send_request('get_upcoming_activities',[self._session_id])
    
    def search_by_module(self,search_string,module,offset,max_results,assigned_user_id='',
                                select_fields=[],unified_search_only=True,favorites=False):
        return self.send_request('search_by_module',self._make_post_params(search_string,module,offset,
                                                    max_results,assigned_user_id,select_fields,
                                                    unified_search_only,favorites))
    def get_module_fields(self,module):
        return self.send_request('get_module_fields',self._make_post_params(module))

def get_session():
    return SugarSession('http://sugar.phxgroup.com/service/v4_1','admin','14wp88','rest')

if __name__ == "__main__":
    sess  = SugarSession('http://sugar.phxgroup.com/service/v4_1','admin','14wp88','rest')
    records =  sess.get_module_records('Calls',['id','name','subject','status','email_reminder_time','email_reminder_sent','email_reminder_chacked'])
    #a = sess.get_module_fields('Calls')
    from pprint import pprint
    pprint(records,indent=4)




