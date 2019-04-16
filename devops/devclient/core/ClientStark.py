#_*_coding:utf-8_*_
import info_colleciton
from conf import settings
import urllib,urllib2,sys,os,json,datetime
import api_token

class ArgvHandler(object):
    def __init__(self,argv_list):
        self.argvs=argv_list
        self.parse_argv()

    def parse_argv(self):
        if len(self.argvs) >1:
            if hasattr(self,self.argvs[1]):
                func=getattr(self,self.argvs[1])
                func()
            else:
                self.helpmsg()
        else:
            self.helpmsg()

    def helpmsg(self):
        msg="""
        collect_data
        run_forever
        get_asset_id
        report_asset
        """
        print(msg)

    def collect_data(self):
        obj=info_colleciton.InfoCollection()
        asset_data=obj.collect()
        print asset_data
    def run_forever(self):
        pass
    def get_asset_id(self):
        pass

    def load_asset_id(self,sn=None):
        asset_id_file=settings.Params['asset_id']
        has_asset_id=False
        if os.path.isfile(asset_id_file):
            asset_id=open(asset_id_file).read().strip()
            if asset_id.isdigit():
                return asset_id
            else:
                has_asset_id=False
        else:
            has_asset_id = False

    def report_asset(self):
        obj=info_colleciton.InfoCollection()
        asset_data=obj.collect()
        asset_id=self.load_asset_id()
        if asset_id:
            asset_data["asset_id"]=asset_id
            post_url="asset_report"
        else:
            asset_data["asset_id"] = None
            post_url="asset_report_with_no_id"

        data={"asset_data":json.dumps(asset_data)}
        response = self.__submit_data(post_url, data, method="post")
        if "asset_id" in response:
            self.__update_asset_id(response["asset_id"])
        self.log_record(response)

    def __submit_data(self,action_type,data,method):
            if action_type in settings.Params['urls']:
                if type(settings.Params['port']) is int:
                    url = "http://%s:%s%s"%(settings.Params['server'], settings.Params['port'], settings.Params['urls'][action_type])
                else:
                    url = "http://%s%s" % (settings.Params['server'], settings.Params['urls'][action_type])
#implent method  __attach_token
                url = self.__attach_token(url)
                print('Connecting [%s], it may take a minute' % url)
                if method == "get":
                    args = ""
                    for k, v in data.items():
                        args += "&%s=%s" % (k, v)
                    args = args[1:]
                    url_with_args = "%s?%s" % (url, args)
                    try:
                        req = urllib2.Request(url_with_args)
                        req_data = urllib2.urlopen(req, timeout=settings.Params['request_timeout'])
                        callback = req_data.read()
                        print("-->server response:", callback)
                        return callback
                    except urllib2.URLError as e:
                        sys.exit("\033[31;1m%s\033[0m" % e)
                elif method == "post":
                    try:
                        data_encode = urllib.urlencode(data)
                        req = urllib2.Request(url=url, data=data_encode)
                        res_data = urllib2.urlopen(req, timeout=settings.Params['request_timeout'])
                        callback = res_data.read()
                        callback = json.loads(callback)
                        print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" % (method, url, callback))
                        return callback
                    except Exception as e:
                        sys.exit("\033[31;1m%s\033[0m" % e)
            else:
                raise KeyError

    def __attach_token(self,url_str):
        user = settings.Params['auth']['user']
        token_id = settings.Params['auth']['token']
        md5_token,timestamp = api_token.get_token(user,token_id)
        url_arg_str = "user=%s&timestamp=%s&token=%s" %(user,timestamp,md5_token)
        if "?" in url_str:#already has arg
            new_url = url_str + "&" + url_arg_str
        else:
            new_url = url_str + "?" + url_arg_str
        return  new_url

    def __update_asset_id(self,new_asset_id):
        asset_id_file=settings.Params['asset_id']
        f=open(asset_id_file,"wb")
        f.write(str(new_asset_id))
        f.close()

    def log_record(self,log,action_type=None):
        f = open(settings.Params["log_file"],"ab")
        if log is str:
            pass
        if type(log) is dict:

            if "info" in log:
                for msg in log["info"]:
                    log_format = "%s\tINFO\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    #print msg
                    f.write(log_format)
            if "error" in log:
                for msg in log["error"]:
                    log_format = "%s\tERROR\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
            if "warning" in log:
                for msg in log["warning"]:
                    log_format = "%s\tWARNING\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)

        f.close()


