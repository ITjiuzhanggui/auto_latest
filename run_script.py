#!/usr/bin/env python3
import time
import os
from logs import SetLog
from core.abstract import exect_contest
from conf import ConfManagement
from core.defaultslog import *
from core.clearlogs import *
from core.statusDef import *
from core.statusCle import *

auto_path = ConfManagement().get_ini("AUTOMATEDLOGPARSING")

date = time.strftime("%Y-%m-%d", time.localtime()).replace(' ', ':').replace(':', ':')

CURPATH = os.path.dirname(os.path.realpath(__file__)) + "/%s" % date
os.makedirs(CURPATH, exist_ok=True)

JSON_PATH = os.path.join(CURPATH, "json")
os.makedirs(JSON_PATH, exist_ok=True)
JSON_STATUS_PATH = os.path.join(JSON_PATH, "status")
JSON_TEST_PATH = os.path.join(JSON_PATH, "test")
os.makedirs(JSON_TEST_PATH, exist_ok=True)
os.makedirs(JSON_STATUS_PATH, exist_ok=True)
os.system("chmod a+x 1.sh")
os.system("cp 1.sh %s/" % auto_path)


def get_log_update(cmd, logs_patg):
    SetLog().info("updte:cmd:%s" % cmd)
    for i in range(1):
        os.system("{} > {}/{}.log 2>&1 ".format(
            cmd, logs_patg, time.strftime( \
                "%Y-%m-%d-%H:%M:%S", \
                time.localtime()).replace(' ', ':'). \
                replace(':', ':'))
        )


path = os.path.join(CURPATH, "update")
os.makedirs(path, exist_ok=True)
make_path = auto_path + "/1.sh"
make_path += " %s make update" % auto_path


# get_log_update(make_path, path)


def get_log_status(cmd, logs_patg):
    SetLog().info("status:cmd:%s" % cmd)
    for i in range(1):
        SetLog().info("++++++++++++++++")
        os.system("{} > {}/{}.log 2>&1 ".format(
            cmd, logs_patg, time.strftime( \
                "%Y-%m-%d-%H:%M:%S", \
                time.localtime()).replace(' ', ':'). \
                replace(':', ':'))
        )


path = os.path.join(CURPATH, "status_log")
os.makedirs(path, exist_ok=True)
make_path = auto_path + '/1.sh'
make_path += " %s make status" % auto_path
get_log_status(make_path, path)

test_cmd = ["make memcached", "make php", "make python", "make golang", "make openjdk", "make perl", "make ruby"]


def get_log_test(cmd, logs_patg):
    SetLog().info("test:cmd:%s" % cmd)
    for i in range(5):
        SetLog().info("-----------------------")
        os.system("{} > {}/{}.log 2>&1 ".format(
            cmd, logs_patg, time.strftime( \
                "%Y-%m-%d-%H:%M:%S", \
                time.localtime()).replace(' ', ':'). \
                replace(':', ':'))
        )



def status_anlies(num):
    list = os.listdir(CURPATH)

    if "status_log" in list:
        logs = os.path.join(CURPATH, "status_log")
        i = os.listdir(logs)[num]
        curl_path = os.path.join(logs, i)
        ConfManagement().set_ini(session="STATUS_LOG_PATH", value=curl_path)
        exect_contest(StaDefHttpd().serialization)
        exect_contest(StaClrHttpd().serialization)
        exect_contest(StaDefNginx().serialization)
        exect_contest(StaClrNginx().serialization)
        exect_contest(StaDefMemcached().serialization)
        exect_contest(StaClrMemcached().serialization)
        exect_contest(StaDefRedis().serialization)
        exect_contest(StaClrRedis().serialization)
        exect_contest(StaDefPhp().serialization)
        exect_contest(StaClrPhp().serialization)
        exect_contest(StaDefPython().serialization)
        exect_contest(StaClrPython().serialization)
        exect_contest(StaDefGolang().serialization)
        exect_contest(StaClrGolang().serialization)
        exect_contest(StaDefNode().serialization)
        exect_contest(StaClrNode().serialization)
        exect_contest(StaDefOpenjdk().serialization)
        exect_contest(StaClrOpenjdk().serialization)
        exect_contest(StaDefRuby().serialization)
        exect_contest(StaClrRuby().serialization)
        exect_contest(StaDefPerl().serialization)
        exect_contest(StaClrPerl().serialization)
        os.system("cp data.json %s" % (JSON_STATUS_PATH + "/%d.json" % int(time.time() + num)))
    os.system("cp ini_data.json data.json")


def test_anlies(num):
    list = os.listdir(CURPATH)

    if "test_log" in list:
        test_json_path = os.path.dirname(os.path.realpath(__file__)) + "/data.json"
        test_json_ini = os.path.dirname(os.path.realpath(__file__)) + "/ini_data.json"
        logs = os.path.join(CURPATH, "test_log")
        for i in os.listdir(logs):
            log = os.path.join(logs, i)
            if "httpd" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefHttpd().serialization)
                exect_contest(ClrHttpd().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "nginx" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefNginx().serialization)
                exect_contest(ClrNginx().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "memcached" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefMemcached().serialization)
                exect_contest(ClrMemcached().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "redis" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefRedis().serialization)
                exect_contest(ClrRedis().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "php" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefPhp().serialization)
                exect_contest(ClrPhp().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "python" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefPython().serialization)
                exect_contest(ClrPython().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "golang" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefGoalng().serialization)
                exect_contest(ClrGoalng().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "node" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefNode().serialization)
                exect_contest(ClrNode().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "openjdk" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefOpenjdk().serialization)
                exect_contest(ClrOpenjdk().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "ruby" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefRuby().serialization)
                exect_contest(ClrRuby().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

            if "perl" in log:
                files = os.listdir(log)[num]
                p = os.path.join(log, files)
                ConfManagement().set_ini(session="TEST_LOG_PATH", value=p)
                exect_contest(DefPerl().serialization)
                exect_contest(ClrPerl().serialization)
                os.system("cp {} {}".format(test_json_path, JSON_TEST_PATH + "/test_json_%d.json" % num))

        os.system("cp {} {}".format(test_json_ini, test_json_path))


for i in test_cmd:
    path = os.path.join(CURPATH, "test_log")
    path = os.path.join(path, i.split(' ')[-1])
    os.makedirs(path, exist_ok=True)
    make_path = auto_path + '/1.sh'
    make_path += " {} {} ".format(auto_path, i)
#    get_log_test(make_path, path)

for num in range(1):
    status_anlies(num)
SetLog().info("Successfully written：status_json")

for num in range(5):
    test_anlies(num)
SetLog().info("Successfully written：test_json")

sh = auto_path + '/1.sh'
os.system("rm %s" % sh)
