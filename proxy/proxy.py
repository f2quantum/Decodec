
from mitmproxy import http
from mitmproxy.http import Headers
import json
import time
import random
import datetime

CheckMachineCode_json = open("./CheckMachineCode.json")
Login_json_file = open("./Login.json")

CheckMachineCode = json.load(CheckMachineCode_json)
Login = json.load(Login_json_file)
class Proxy:
    def request(self, flow: http.HTTPFlow):
        return

    def response(self,flow: http.HTTPFlow):
        if "API/APIUnified" in flow.request.path:
            data  = flow.request.get_text()
            print("Method"+data,end="\n");
            print(flow.response.text)
            if "CheckMachineCode" in data:
                flow.response.text = json.dumps(CheckMachineCode, ensure_ascii=False)
            elif "Login" in data:
                flow.response.text = json.dumps(Login, ensure_ascii=False)

        return


addons = [
    Proxy()
]
