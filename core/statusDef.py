import re
import os
import json
from core.abstract import Global
from conf import ConfManagement


class StaDefLog(Global):

    def __init__(self):
        super(StaDefLog, self).__init__()
        status_logpath = ConfManagement().get_ini("STATUS_LOG_PATH")
        self.status_log = self.read_logs(status_logpath)
        json_path = os.path.dirname(os.path.realpath(__file__))[:-4] + 'data.json'
#        print("status_Def[json_path]%s"%json_path)
        with open(json_path, 'r') as f:
            self.data = json.load(f)

    def serialization(self):
        pass


class StaDefHttpd(StaDefLog):
    """default test_status_httpd long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        start = 0
        for i in lines:
            if i.startswith("httpd"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("httpd"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_httpd:Total")
                    data.get("status_def").get("httpd").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_httpd:Base_Layer")
                data.get("status_def").get("httpd").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_httpd:MicroService_layer")
                data.get("status_def").get("httpd").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefGolang(StaDefLog):
    """default test_status_golang long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("golang"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("golang"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_golang:Total")
                    data.get("status_def").get("golang").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_golang:Base_Layer")
                data.get("status_def").get("golang").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_golang:MicroService_layer")
                data.get("status_def").get("golang").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefNginx(StaDefLog):
    """default test_status_nginx long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("nginx"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("nginx"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_nginx:Total")
                    data.get("status_def").get("nginx").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_nginx:Base_Layer")
                data.get("status_def").get("nginx").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_nginx:MicroService_layer")
                data.get("status_def").get("nginx").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefMemcached(StaDefLog):
    """default test_status_memcached long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("memcached"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("memcached"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_memcached:Total")
                    data.get("status_def").get("memcached").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_memcached:Base_Layer")
                data.get("status_def").get("memcached").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_memcached:MicroService_layer")
                print(num)
                data.get("status_def").get("memcached").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefRedis(StaDefLog):
    """default test_status_redis long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("redis"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("redis"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_redis:Total")
                    data.get("status_def").get("redis").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_redis:Base_Layer")
                data.get("status_def").get("redis").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_redis:MicroService_layer")
                data.get("status_def").get("redis").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefPhp(StaDefLog):
    """default test_status_php long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("php"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("php"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_php:Total")
                    data.get("status_def").get("php").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_php:Base_Layer")
                data.get("status_def").get("php").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_php:MicroService_layer")
                data.get("status_def").get("php").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefPython(StaDefLog):
    """default test_status_php long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("python"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("python"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_python:Total")
                    data.get("status_def").get("python").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_python:Base_Layer")
                data.get("status_def").get("python").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_python:MicroService_layer")
                data.get("status_def").get("python").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefNode(StaDefLog):
    """default test_status_node long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("node"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("node"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_node:Total")
                    data.get("status_def").get("node").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_node:Base_Layer")
                data.get("status_def").get("node").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_node:MicroService_layer")
                data.get("status_def").get("node").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefOpenjdk(StaDefLog):
    """default test_status_openjdk long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("openjdk"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("openjdk"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_openjdk:Total")
                    data.get("status_def").get("openjdk").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_openjdk:Base_Layer")
                data.get("status_def").get("openjdk").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_openjdk:MicroService_layer")
                data.get("status_def").get("openjdk").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefRuby(StaDefLog):
    """default test_status_ruly long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("ruby"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("ruby"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_ruby:Total")
                    data.get("status_def").get("ruby").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_ruby:Base_Layer")
                data.get("status_def").get("ruby").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_ruby:MicroService_layer")
                data.get("status_def").get("ruby").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class StaDefPerl(StaDefLog):
    """default test_status_perl long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("perl"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:
            if i.startswith("perl"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_def_Perl:Total")
                    data.get("status_def").get("perl").update(
                        {"Toatl": num[-1] + "MB"}
                    )

            if i.startswith("default base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_Perl:Base_Layer")
                data.get("status_def").get("perl").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("default microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_def_Perl:MicroService_layer")
                data.get("status_def").get("perl").update(
                    {"MicroService_layer": num[0]}
                )

        with open("data.json", "w")as f:
            json.dump(data, f)