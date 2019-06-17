import os
import re
import json
from core.abstract import Global
from conf import ConfManagement


class StaClrLog(Global):

    def __init__(self):
        super(StaClrLog, self).__init__()
        test_logpath = ConfManagement().get_ini("STATUS_LOG_PATH")
        self.status_log = self.read_logs(test_logpath)
        json_path = os.path.dirname(os.path.realpath(__file__))[:-4] + 'data.json'
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        self.status_version()

    def serialization(self):
        pass

    def status_version(self):
        lines = self.status_log
        data = self.data
        if_n = True
        start = 0
        end = 0
        while if_n:
            for i in lines:
                if i == '\n':
                    if_n = False
                    end = lines.index(i)
        for i in lines[:end]:
            if i.startswith("Installed version:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_version:version")
                data.get('status_Clr').update(
                    {"clearlinux_version": num[0]}
                )


class StaClrHttpd(StaClrLog):
    """default test_status_httpd long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
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

            if i.startswith("clearlinux/httpd"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_httpd:Total")
                    data.get("status_Clr").get("httpd").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_httpd:Base_Layer")
                data.get("status_Clr").get("httpd").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_httpd:MicroService_layer")
                data.get("status_Clr").get("httpd").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrGolang(StaClrLog):
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

            if i.startswith("clearlinux/golang"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_golang:Total")
                    data.get("status_Clr").get("golang").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_golang:Base_Layer")
                data.get("status_Clr").get("golang").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_golang:MicroService_layer")
                data.get("status_Clr").get("golang").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrNginx(StaClrLog):
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
            if i.startswith("clearlinux/nginx"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_nginx:Total")
                    data.get("status_Clr").get("nginx").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_nginx:Base_Layer")
                data.get("status_Clr").get("nginx").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_nginx:MicroService_layer")
                data.get("status_Clr").get("nginx").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrMemcached(StaClrLog):
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

            if i.startswith("clearlinux/memcached"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_memcached:Total")
                    data.get("status_Clr").get("memcached").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_memcached:Base_Layer")
                data.get("status_Clr").get("memcached").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_memcached:MicroService_layer")
                data.get("status_Clr").get("memcached").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrRedis(StaClrLog):
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

            if i.startswith("clearlinux/redis"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_redis:Total")
                    data.get("status_Clr").get("redis").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_redis:Base_Layer")
                data.get("status_Clr").get("redis").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_redis:MicroService_layer")
                data.get("status_Clr").get("redis").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrPhp(StaClrLog):
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

            if i.startswith("clearlinux/php"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_php:Total")
                    data.get("status_Clr").get("php").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_php:Base_Layer")
                data.get("status_Clr").get("php").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_php:MicroService_layer")
                data.get("status_Clr").get("php").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrPython(StaClrLog):
    """default test_status_python long analysis"""

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

            if i.startswith("clearlinux/python"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_python:Total")
                    data.get("status_Clr").get("python").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_python:Base_Layer")
                data.get("status_Clr").get("python").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_python:MicroService_layer")
                data.get("status_Clr").get("python").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrNode(StaClrLog):
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

            if i.startswith("clearlinux/node"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_node:Total")
                    data.get("status_Clr").get("node").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_node:Base_Layer")
                data.get("status_Clr").get("node").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_node:MicroService_layer")
                data.get("status_Clr").get("node").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrOpenjdk(StaClrLog):
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

            if i.startswith("clearlinux/openjdk"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_openjdk:Total")
                    data.get("status_Clr").get("openjdk").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_openjdk:Base_Layer")
                data.get("status_Clr").get("openjdk").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_openjdk:MicroService_layer")
                data.get("status_Clr").get("openjdk").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrRuby(StaClrLog):
    """default test_status_openjdk long analysis"""

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

            if i.startswith("clearlinux/ruby"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_ruby:Total")
                    data.get("status_Clr").get("ruby").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_ruby:Base_Layer")
                data.get("status_Clr").get("ruby").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_ruby:MicroService_layer")
                data.get("status_Clr").get("ruby").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)


class StaClrPerl(StaClrLog):
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
                if i == "\n":
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/perl"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_Perl:Total")
                    data.get("status_Clr").get("perl").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_Perl:Base_Layer")
                data.get("status_Clr").get("perl").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_Perl:MicroService_layer")
                data.get("status_Clr").get("perl").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', "w")as f:
            json.dump(data, f)


class StaClrTensorflow(StaClrLog):
    """clearlinux test_status_tensorflow log analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data

        if_n = True
        for i in lines:
            if i.startswith("tensorflow"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == "\n":
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/tensorflow"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_tensorflow:Total")
                    data.get("status_Clr").get("tensorflow").update(
                        {"Total": num[-1] + "GB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_tensorflow:Base_Layer")
                data.get("status_Clr").get("tensorflow").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_tensorflow:MicroService_layer")
                data.get("status_Clr").get("tensorflow").update(
                    {"MicroService_layer": num[0]}
                )

        with open('data.json', 'w') as f:
            json.dump(data, f)
