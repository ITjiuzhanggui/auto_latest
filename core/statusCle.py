import os
import re
import json
from core.abstract import Global
from conf import ConfManagement
from logs import SetLog


class StaClrLog(Global):

    def __init__(self):
        super(StaClrLog, self).__init__()
        test_logpath = ConfManagement().get_ini("STATUS_LOG_PATH")
        self.status_log = self.read_logs(test_logpath)
        self.json_path = os.path.dirname(os.path.realpath(__file__))[:-4] + 'data.json'
        with open(self.json_path, 'r') as f:
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
    """clearlinux test_status_httpd long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/httpd version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_httpd:VERSION_ID")
                data.get("status_Clr").get("httpd").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrGolang(StaClrLog):
    """clearlinux test_status_golang long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/golang version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_golang:VERSION_ID")
                data.get("status_Clr").get("golang").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrNginx(StaClrLog):
    """clearlinux test_status_nginx long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/nginx version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_nginx:VERSION_ID")
                data.get("status_Clr").get("nginx").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrMemcached(StaClrLog):
    """clearlinux test_status_memcached long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/memcached version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_memcached:VERSION_ID")
                data.get("status_Clr").get("memcached").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrRedis(StaClrLog):
    """clearlinux test_status_redis long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/redis version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_redis:VERSION_ID")
                data.get("status_Clr").get("redis").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrPhp(StaClrLog):
    """clearlinux test_status_php long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/php version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_php:VERSION_ID")
                data.get("status_Clr").get("php").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrPython(StaClrLog):
    """clearlinux test_status_python long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/python version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_python:VERSION_ID")
                data.get("status_Clr").get("python").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
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

        for i in lines[start:]:
            if i.startswith("clearlinux/node version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_node:VERSION_ID")
                data.get("status_Clr").get("node").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrOpenjdk(StaClrLog):
    """clearlinux test_status_openjdk long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/openjdk version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_openjdk:VERSION_ID")
                data.get("status_Clr").get("openjdk").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrRuby(StaClrLog):
    """clearlinux test_status_openjdk long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/ruby version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_ruby:VERSION_ID")
                data.get("status_Clr").get("ruby").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrPerl(StaClrLog):
    """clearlinux test_status_perl long analysis"""

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

        for i in lines[start:]:
            if i.startswith("clearlinux/perl version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_Perl:VERSION_ID")
                data.get("status_Clr").get("perl").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, "w")as f:
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

        for i in lines[start:]:
            if i.startswith("clearlinux/tensorflow version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_tensorflow:VERSION_ID")
                data.get("status_Clr").get("tensorflow").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrPostgres(StaClrLog):
    """clearlinux test_status_postgres long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data

        if_n = True
        for i in lines:
            if i.startswith("postgres"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/postgres"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_postgres:Total")
                    data.get("status_Clr").get("postgres").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_postgres:Base_Layer")
                data.get("status_Clr").get("postgres").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_postgres:MicroService_layer")
                data.get("status_Clr").get("postgres").update(
                    {"MicroService_layer": num[0]}
                )

        for i in lines[start:]:
            if i.startswith("clearlinux/postgres version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_postgres:VERSION_ID")
                data.get("status_Clr").get("postgres").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrMariadb(StaClrLog):
    """clearlinux test_status_mariadb long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True
        for i in lines:
            if i.startswith("mariadb"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/mariadb"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_mariadb:Total")
                    data.get("status_Clr").get("mariadb").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_mariadb:Base_Layer")
                data.get("status_Clr").get("mariadb").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_mariadb:MicroService_layer")
                data.get("status_Clr").get("mariadb").update(
                    {"MicroService_layer": num[0]}
                )

        for i in lines[start:]:
            if i.startswith("clearlinux/mariadb version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_mariadb:VERSION_ID")
                data.get("status_Clr").get("mariadb").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrRabbitmq(StaClrLog):
    """clearlinux test_status_openjdk long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data

        if_n = True
        for i in lines:
            if i.startswith("rabbitmq"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/rabbitmq"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_rabbitmq:Total")
                    data.get("status_Clr").get("rabbitmq").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_rabbitmq:Base_Layer")
                data.get("status_Clr").get("rabbitmq").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_rabbitmq:MicroService_layer")
                data.get("status_Clr").get("rabbitmq").update(
                    {"MicroService_layer": num[0]}
                )

        for i in lines[start:]:
            if i.startswith("clearlinux/rabbitmq version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_rabbitmq:VERSION_ID")
                data.get("status_Clr").get("rabbitmq").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrFlink(StaClrLog):
    """clearlinux test_status_flink long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data
        if_n = True

        for i in lines:
            if i.startswith("flink"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/flink"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_flink:Total")
                    data.get("status_Clr").get("flink").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_flink:Base_Layer")
                data.get("status_Clr").get("flink").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_flink:MicroService_layer")
                data.get("status_Clr").get("flink").update(
                    {"MicroService_layer": num[0]}
                )

        for i in lines[start:]:
            if i.startswith("clearlinux/flink version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_flink:VERSION_ID")
                data.get("status_Clr").get("flink").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrCassandra(StaClrLog):
    """clearlinux test_status_cassandra long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data

        if_n = True
        for i in lines:
            if i.startswith("cassandra"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/cassandra"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_cassandra:Total")
                    data.get("status_Clr").get("cassandra").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_cassandra:Base_Layer")
                data.get("status_Clr").get("cassandra").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_cassandra:MicroService_layer")
                data.get("status_Clr").get("cassandra").update(
                    {"MicroService_layer": num[0]}
                )

        for i in lines[start:]:
            if i.startswith("clearlinux/cassandra version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_cassandra:VERSION_ID")
                data.get("status_Clr").get("cassandra").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class StaClrWordpress(StaClrLog):
    """clearlinux test_status_wordpress long analysis"""

    def serialization(self):
        lines = self.status_log
        data = self.data

        if_n = True
        for i in lines:
            if i.startswith("wordpress"):
                if "latest" in i:
                    start = lines.index(i)

        while if_n:
            for i in lines[start:]:
                if i == '\n':
                    if_n = False
                    end = lines[start:].index(i)

        for i in lines[start:end + start]:

            if i.startswith("clearlinux/wordpress"):
                if "latest" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "status_Clr_wordpress:Total")
                    data.get("status_Clr").get("wordpress").update(
                        {"Total": num[-1] + "MB"}
                    )

            if i.startswith("clearlinux base layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_wordpress:Base_Layer")
                data.get("status_Clr").get("wordpress").update(
                    {"Base_Layer": num[0]}
                )

            if i.startswith("clearlinux microservice added layer Size:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "status_Clr_wordpress:MicroService_layer")
                data.get("status_Clr").get("wordpress").update(
                    {"MicroService_layer": num[0]}
                )

        for i in lines[start:]:
            if i.startswith("clearlinux/wordpress version:\n"):
                end = lines[start:].index(i) + 1
                num = re.findall("\d+\.?\d*", lines[start:][end])
                self.exception_to_response(num, "status_Clr_wordpress:VERSION_ID")
                data.get("status_Clr").get("wordpress").update(
                    {"VERSION_ID": num[0]}
                )

        with open(self.json_path, 'w') as f:
            json.dump(data, f)