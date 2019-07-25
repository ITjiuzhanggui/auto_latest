#!/usr/bin/env python3

import os, sys
import re
import json
from pprint import pprint

data = {
    "default":
        {
            "httpd": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {}, "golang": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {}, "postgres": {}, "mariadb": {},
            "rabbitmq": {}
        },

    "clear":
        {
            "httpd": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {}, "golang": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {}, "postgres": {}, "mariadb": {},
            "rabbitmq": {}
        },

    "status_def":
        {
            "httpd": {}, "golang": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {}, "postgres": {}, "mariadb": {},
            "rabbitmq": {}
        },

    "status_Clr":
        {
            "clearlinux_version": {}, "httpd": {}, "golang": {}, "nginx": {}, "memcached": {}, "redis": {},
            "php": {}, "python": {}, "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {},
            "postgres": {}, "mariadb": {}, "rabbitmq": {}
        }
}

# !/usr/bin/env python3
# import time
# import os
#
# cmd = "make memcached"
# logs_path = "/home/log"
# for i in range(5):
#     os.system("{} > {}/{}.log 2>&1 ".format(cmd, logs_path,\
#         time.strftime("%Y-%m-%d-%H:%M:%S", \
#         time.localtime()).replace(' ',':').replace(':', ':')))

"""default test_long"""


def read_logs(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        return f.readlines()


def read_status_logs(status_log):
    with open(status_log, "r", encoding="utf-8") as s:
        return s.readlines()


def default_from_httpd(lines):
    """httpd unit tests analysis"""
    for i in lines[lines.index("httpd/httpd.sh\n"):lines.index("httpd-server\n")]:
        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Transfer rate": num[0]}
            )


def default_from_nginx(lines):
    """nginx unit tests analysis"""

    for i in lines[
             lines.index("[nginx] [INFO] Test docker hub official image first:\n"):
             lines.index("[nginx] [INFO] Test clear docker image:\n")]:

        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Transfer rate": num[0]}
            )


# def default_from_memcached(lines):
#     '''memcached unit tests analysis'''
#
#     for i in lines[lines.index("memcached/memcached.sh\n"):lines.index("memcached-server\n")]:
#         if i.startswith("Sets"):
#             num = re.findall("---|\d+\.?\d*", i)
#             num[-1] += " KB/sec"
#             data.get("default").get("memcached").update(
#                 {"Sets": num[-2:]})
#
#         if i.startswith("Gets"):
#             num = re.findall("---|\d+\.?\d*", i)
#             num[-1] += " KB/sec"
#             data.get("default").get("memcached").update(
#                 {"Gets": num[-2:]})
#
#         if i.startswith("Totals"):
#             num = re.findall("---|\d+\.?\d*", i)
#             num[-1] += " KB/sec"
#             data.get("default").get("memcached").update(
#                 {"Totals": num[-2:]})


def default_from_memcached(lines):
    '''memcached unit tests analysis'''

    for i in lines[
             lines.index("memcached/memcached.sh\n"):
             lines.index("Default-Memcached-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)
            data.get("default").get("memcached").update(
                {"Sets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)
            data.get("default").get("memcached").update(
                {"Gets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)
            data.get("default").get("memcached").update(
                {"Totals": ["Latency:" + num[-2], num[-1] + " KB/sec"]})


def default_from_redis(lines):
    """redis unit tests analysis"""

    influs_defaut = []
    for i in lines[
             lines.index("redis/redis.sh\n"):
             lines.index("Default-Redis-Server\n")]:
        influs_defaut.append(i)

    for i in influs_defaut[
             influs_defaut.index("====== PING_INLINE ======\n"):
             influs_defaut.index("====== PING_BULK ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"PING_INLINE": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== PING_BULK ======\n"):
             influs_defaut.index("====== SET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"PING_BULK": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SET ======\n"):
             influs_defaut.index("====== GET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== GET ======\n"):
             influs_defaut.index("====== INCR ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"GET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== INCR ======\n"):
             influs_defaut.index("====== LPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"INCR": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH ======\n"):
             influs_defaut.index("====== RPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPUSH ======\n"):
             influs_defaut.index("====== LPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"RPUSH": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LPOP ======\n"):influs_defaut.index("====== RPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPOP": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== RPOP ======\n"):influs_defaut.index("====== SADD ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"RPOP": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== SADD ======\n"):influs_defaut.index("====== HSET ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SADD": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== HSET ======\n"):influs_defaut.index("====== SPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"HSET": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== SPOP ======\n"):influs_defaut.index(
            "====== LPUSH (needed to benchmark LRANGE) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):influs_defaut.index(
                 "====== LRANGE_100 (first 100 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPUSH (needed to benchmark LRANGE)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):influs_defaut.index(
            "====== LRANGE_300 (first 300 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_100 (first 100 elements)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):influs_defaut.index(
            "====== LRANGE_500 (first 450 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_300 (first 300 elements)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):influs_defaut.index(
            "====== LRANGE_600 (first 600 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_500 (first 450 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):
             influs_defaut.index("====== MSET (10 keys) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_600 (first 600 elements)": num[0]}
            )

    influs_defaut.append("Default-Redis-Server\n")
    for i in influs_defaut[
             influs_defaut.index("====== MSET (10 keys) ======\n"):
             influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"MSET (10 keys)": num[0]}
            )


def default_from_php(lines):
    """php unit tests analysis"""

    for i in lines[lines.index("php/php.sh\n"):lines.index("[php] [INFO] Test clear docker image:\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("php").update(
                {"phpbench": num[0]}
            )


def default_from_python(lines):
    """python unit tests analysis"""

    for i in lines[lines.index("python/python.sh\n"):lines.index("Default-Python-Server\n")]:

        if i.startswith("Totals"):
            num = re.findall("\d+\.?\d*", i)
            num[0] = {"minimum": num[0]}
            num[1] = {"average": num[1]}
            data.get("default").get("python").update(
                {"Totals": num[-2:]}
            )


def default_from_golang(lines):
    """golang unit tests analysis"""

    for i in lines[
             lines.index("golang/golang.sh\n"):
             lines.index("Default-Golang-Server\n")]:

        if i.startswith("BenchmarkBuild"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkBuild": num[0][:-6]}
            )

        if i.startswith("BenchmarkGarbage"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkGarbage": num[0][:-6]}
            )

        if i.startswith("BenchmarkHTTP"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkHTTP": num[0][:-6]}
            )

        if i.startswith("BenchmarkJSON"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkJSON": num[0][:-6]}
            )


def default_from_nodejs(lines):
    """nodejs unit tests analysis"""
    for i in lines[
             lines.index("node/node.sh\n"):
             lines.index("Default-Node-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("node").update(
                {"benchmark-node-octane": num[-1]}
            )


def default_from_openjdk(lines):
    """openjdk unit tests analysis"""
    for i in lines[
             lines.index("[openjdk] [INFO] Test docker hub official image first:\n"):
             lines.index("[openjdk] [INFO] Test clear docker image:\n")]:

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("default").get("openjdk").update(
                {"MyBenchmark.testMethod.Score": num[-2]}
            )

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("default").get("openjdk").update(
                {"MyBenchmark.testMethod.Error": num[-1]}
            )


def default_from_ruby(lines):
    """ruby unit tests analysis"""

    for i in lines[
             lines.index("ruby/ruby.sh\n"):
             lines.index("Default-Ruby-Server\n")]:

        if i.endswith("s/i)\n"):
            if "app_answer" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_answer": num[-2]}
                )
        if i.endswith("s/i)\n"):
            if "app_aobench" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_aobench": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_erb" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_erb": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_factorial" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_factorial": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_fib" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_fib": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_lc_fizzbuzz" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_lc_fizzbuzz": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_mandelbrot" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_mandelbrot": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_pentomino" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_pentomino": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_raise" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_raise": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_strconcat" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_strconcat": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_tak" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_tak": num[-2]}

                )

        if i.endswith("s/i)\n"):
            if "app_tarai" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("ruby").update(
                    {"app_tarai": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_uri" in i:
                num = re.findall("\d")


def default_from_perl(lines):
    """perl unit tests analysis"""

    influs_default = []
    for i in lines[
             lines.index("perl/perl.sh\n"):
             lines.index("[perl] [INFO] Test clear docker image:\n")]:
        influs_default.append(i)

    for item in influs_default:
        if item.startswith("Test: benchmarks/app/podhtml.b"):
            start = lines.index(item)

        if item.startswith("Test: benchmarks/startup/noprog.b"):
            end = lines.index(item)

    for item in lines[start:end]:
        if item.startswith("Avg:"):
            num = re.findall("\d+\.?\d*", item)

            data.get("default").get("perl").update(
                {"podhtml.b": num[0]}
            )

    for i in influs_default:
        if i.startswith("Test: benchmarks/startup/noprog.b"):
            start = lines.index(i)

        # if i.startswith("Std-Dev:"):
        if i.startswith("[perl] [INFO] Test clear docker image:\n"):
            end = lines.index(i)

    for i in lines[start:end + 15]:
        if i.startswith("Avg:"):
            num = re.findall("\d+\.?\d*", i)

            data.get("default").get("perl").update(
                {"noprog.b": num[0]}
            )


def default_from_postgres(lines):
    """postgres unit tests analysis"""
    lines_a = lines[1:lines.index("[postgres] [INFO] Test clear docker image:\n")].copy()
    line_nu = []
    for i in lines_a:
        if re.search(r"excluding", i) != None:
            line_nu.append(lines_a.index(i))
    pprint(line_nu)
    bsw = lines_a[int(line_nu[0])].split()
    bsr = lines_a[int(line_nu[1])].split()
    bnw = lines_a[int(line_nu[2])].split()
    bnr = lines_a[int(line_nu[3])].split()
    bhw = lines_a[int(line_nu[4])].split()
    bhr = lines_a[int(line_nu[5])].split()
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_WRITE": bsw[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_ONLY": bsr[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_WRITE": bnw[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_ONLY": bnr[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr[2]}
    )


def default_from_tensorflow(lines):
    """tensorflow unit tests analysis"""
    for i in lines[
             lines.index("[tensorflow] [INFO] Test docker hub official image first:\n"):
             lines.index("[tensorflow] [INFO] Test clear docker image:\n")]:

        if i.startswith("Total duration"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("tensorflow").update(
                {"Total duration": num[0]})


def default_from_mariadb(lines):
    """mariadb unit tests analysis"""

    for i in lines[
             lines.index("[mariadb] [INFO] Test docker hub official image first:\n"):
             lines.index("[mariadb] [INFO] Test clear docker image:\n")]:

        i = i.strip()
        if i.startswith("Average number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("mariadb").update(
                {"Average number of seconds to run all queries": num[0]}
            )

        if i.startswith("Minimum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("mariadb").update(
                {"Minimum number of seconds to run all queries": num[0]}
            )

        if i.startswith("Maximum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("mariadb").update(
                {"Maximum number of seconds to run all queries": num[0]}
            )


def default_from_rabbitmq(lines):
    """rabbitmq unit tests analysis"""
    for i in lines[
             lines.index("[rabbitmq] [INFO] Test docker hub official image first:\n"):
             lines.index("[rabbitmq] [INFO] Test clear docker image:\n")]:

        if "sending rate avg:" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("rabbitmq").update(
                {"sending rate avg": num[-1]}
            )

        if "receiving rate avg:" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("rabbitmq").update(
                {"receiving rate avg": num[-1]}
            )


"""clearlinux test_log"""


def clr_from_httpd(lines):
    """clearlinux unit tests analysis"""
    for i in lines[
             lines.index("[httpd] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Httpd-Server\n")]:

        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Transfer rate": num[0]}
            )


def clr_from_nginx(lines):
    """clearlinux unit test analysis"""

    for i in lines[
             lines.index("[nginx] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Nginx-Server\n")]:

        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Transfer rate": num[0]}
            )


def clr_from_memcached(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[memcached] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Memcached-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("clear").get("memcached").update(
                {"Sets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)
            # num[-1] += " KB/sec"
            data.get("clear").get("memcached").update(
                {"Gets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)
            # num[-1] += " KB/sec"
            data.get("clear").get("memcached").update(
                {"Totals": ["Latency:" + num[-2], num[-1] + " KB/sec"]})


def clr_from_redis(lines):
    """clearlinux unit tests analysis"""

    influs_defaut = []
    for i in lines[
             lines.index("[redis] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Redis-Server\n")]:
        influs_defaut.append(i)
        print(influs_defaut)

    for i in influs_defaut[
             influs_defaut.index("====== PING_INLINE ======\n"):
             influs_defaut.index("====== PING_BULK ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"PING_INLINE": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== PING_BULK ======\n"):
             influs_defaut.index("====== SET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"PING_BULK": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SET ======\n"):
             influs_defaut.index("====== GET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== GET ======\n"):
             influs_defaut.index("====== INCR ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"GET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== INCR ======\n"):
             influs_defaut.index("====== LPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"INCR": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH ======\n"):
             influs_defaut.index("====== RPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPUSH ======\n"):
             influs_defaut.index("====== LPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"RPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPOP ======\n"):
             influs_defaut.index("====== RPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPOP ======\n"):
             influs_defaut.index("====== SADD ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"RPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SADD ======\n"):
             influs_defaut.index("====== HSET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SADD": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== HSET ======\n"):influs_defaut.index("====== SPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"HSET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SPOP ======\n"):
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):
             influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPUSH (needed to benchmark LRANGE)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):
             influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_100 (first 100 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):
             influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_300 (first 300 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_500 (first 450 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):
             influs_defaut.index("====== MSET (10 keys) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_600 (first 600 elements)": num[0]}
            )

    influs_defaut.append("Clr-Redis-Server\n")
    for i in influs_defaut[
             influs_defaut.index("====== MSET (10 keys) ======\n"):
             influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"MSET (10 keys)": num[0]}
            )


def clr_from_php(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[php] [INFO] Test clear docker image:\n"):lines.index("python/python.sh\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("php").update(
                {"Score": num[0]}
            )


def clr_from_python(lines):
    """clearlinux unit tests analysis"""

    for i in lines[lines.index("[python] [INFO] Test clear docker image:\n"):lines.index("Clr-Python-Server\n")]:

        if i.startswith("Totals"):
            num = re.findall("\d+\.?\d*", i)
            num[0] = {"minimum": num[0]}
            num[1] = {"average": num[1]}
            data.get("default").get("python").update(
                {"Totals": num[-2:]}
            )


def clr_from_golang(lines):
    """clearlinux unit tests analysis"""

    for i in lines[lines.index("[golang] [INFO] Test clear docker image:\n"):
    lines.index("Clr-Golang-Server\n")]:

        if i.startswith("BenchmarkBuild"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkBuild": num[0][:-6]}
            )

        if i.startswith("BenchmarkGarbage"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkGarbage": num[0][:-6]}
            )

        if i.startswith("BenchmarkHTTP"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkHTTP": num[0][:-6]}
            )

        if i.startswith("BenchmarkJSON"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkJSON": num[0][:-6]}
            )


def clr_from_nodejs(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[node] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Node-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("node").update(
                {"benchmark-node-octane": num[-1]}
            )


def clr_from_openjdk(lines):
    """perl unit tests analysis"""
    # for i in lines[
    #          lines.index("[openjdk] [INFO] Test clear docker image:\n"):
    #          lines.index("clr-openjdk\n")]:
    #
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Score": num[-2]})
    #
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Error": num[-1]})

    # for item in lines:
    #     if item.startswith("[openjdk] [INFO] Test clear docker image:\n"):
    #         start = lines.index(item)
    #
    # for i in lines[start:]:
    #     if i.startswith("Benchmark"):
    #         end = lines[start:].index(i) + start
    #
    # if i in lines[start:end]:
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Score": num[-2]}
    #         )
    #
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Error": num[-1]}
    #         )
    for i in lines[lines.index("[openjdk] [INFO] Test clear docker image:\n"):]:

        i.strip()

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("openjdk").update(
                {"MyBenchmark.testMethod.Score": num[-2]}
            )

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("openjdk").update(
                {"MyBenchmark.testMethod.Error": num[-1]}
            )


def clr_from_ruby(lines):
    """ruby unit tests analysis"""

    for i in lines[
             lines.index("[ruby] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Ruby-Server\n")]:
        if i.endswith("s/i)\n"):
            if "app_answer" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_answer": num[-2]}
                )
        if i.endswith("s/i)\n"):
            if "app_aobench" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_aobench": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_erb" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_erb": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_factorial" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_factorial": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_fib" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_fib": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_lc_fizzbuzz" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_lc_fizzbuzz": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_mandelbrot" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_mandelbrot": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_pentomino" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_pentomino": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_raise" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_raise": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_strconcat" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_strconcat": num[-2]}
                )

        if i.endswith("s/i)\n"):
            if "app_tak" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_tak": num[-2]}

                )

        if i.endswith("s/i)\n"):
            if "app_tarai" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("clear").get("ruby").update(
                    {"app_tarai": num[-2]}
                )


def clr_from_perl(lines):
    """perl unit tests analysis"""

    for item in lines:
        if item.startswith("[perl] [INFO] Test clear docker image:\n"):
            start = lines.index(item)

    for item in lines[start:]:
        if item.startswith("Test: benchmarks/startup/noprog.b"):
            end = lines[start:].index(item) + start

    for item in lines[start:end]:
        if item.startswith("Avg:"):
            num = re.findall("\d+\.?\d*", item)
            data.get("clear").get("perl").update(
                {"podhtml.b": num[0]}
            )

    for i in lines[start:end + 2]:
        if i.startswith("Test: benchmarks/startup/noprog.b"):
            up = lines[start:end + 2].index(i) + start

    for i in lines[up:]:
        if i.startswith("Avg:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("perl").update(
                {"noprog.b": num[0]}
            )

    # for item in lines:
    #     if item.startswith("[perl] [INFO] Test clear docker image:\n"):
    #         start = lines.index(item)
    #
    # for i in lines[start:]:
    #     if i.startswith("Test: benchmarks/startup/noprog.b"):
    #         end = lines[start:].index(i) + start
    #
    # for item in lines[start:end]:
    #     if item.startswith("Test-File: benchmarks/app/podhtml.b\n"):
    #         up = lines[start:end].index(item) + start
    #
    #     if item.startswith("Test: benchmarks/startup/noprog.b"):
    #         down = lines[start:end].index(item) + start
    #
    # for i in lines[up:down]:
    #     if i.startswith("Avg"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("perl").update(
    #             {"podhtml.b": num[0]}
    #         )
    #
    # for item in lines[start:end]:
    #     if item.startswith("Test: benchmarks/startup/noprog.b"):
    #         up = lines[start:end].index(item) + start
    #
    #     if item.startswith("Test: benchmarks/statement/assign-int.b"):
    #         down = lines[start:end].index(item) + start
    #
    # for i in lines[up:down]:
    #     if i.startswith("Avg:"):
    #         num = re.findall("\d+\.\d*", i)
    #         data.get("clear").get("perl").update(
    #             {"noprog.b": num[0]}
    #         )


def clr_from_postgres(lines):
    """perl unit test analysis"""
    lines_b = lines[lines.index("[postgres] [INFO] Test clear docker image:\n"):].copy()
    line_nu2 = []
    for i in lines_b:
        if re.search(r"excluding", i) != None:
            line_nu2.append(lines_b.index(i))
    #    pprint(line_nu2)
    bsw2 = lines_b[int(line_nu2[0])].split()
    bsr2 = lines_b[int(line_nu2[1])].split()
    bnw2 = lines_b[int(line_nu2[2])].split()
    bnr2 = lines_b[int(line_nu2[3])].split()
    bhw2 = lines_b[int(line_nu2[4])].split()
    bhr2 = lines_b[int(line_nu2[5])].split()
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_WRITE": bsw2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_ONLY": bsr2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_WRITE": bnw2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_ONLY": bnr2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr2[2]}
    )


def clr_from_tensorflow(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[tensorflow] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Tensorflow-Server\n")]:

        if i.startswith("Total duration"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("tensorflow").update(
                {"Total duration": num[0]})


def clr_from_mariadb(lines):
    """mariadb unit tests analysis"""
    for i in lines[
             lines.index("[mariadb] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Mariadb\n")]:

        i = i.strip()
        if i.startswith("Average number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("mariadb").update(
                {"Average number of seconds to run all queries": num[0]}
            )

        if i.startswith("Minimum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("mariadb").update(
                {"Minimum number of seconds to run all queries": num[0]}
            )

        if i.startswith("Maximum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("mariadb").update(
                {"Maximum number of seconds to run all queries": num[0]}
            )


def clr_from_rabbitmq(lines):
    """rabbitmq unit tests analysis"""
    for i in lines[
             lines.index("[rabbitmq] [INFO] Test clear docker image:\n"):
             lines.index("clr-rabbitmq\n")]:

        if "sending rate avg:" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("rabbitmq").update(
                {"sending rate avg": num[-1]}
            )

        if "receiving rate avg:" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("rabbitmq").update(
                {"receiving rate avg": num[-1]}
            )

"""STATUS_default_log"""


def StaDefHttpd(lines):
    """default test_status_httpd long analysis"""

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
        if i.startswith("httpd"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("httpd").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("httpd").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("httpd").update(
                {"MicroService_layer": num[0]})


def StaDefNginx(lines):
    """default test_status_nginx long analysis"""

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
                data.get("status_def").get("nginx").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("nginx").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("nginx").update(
                {"MicroService_layer": num[0]}
            )


def StaDefMemcached(lines):
    """default test_status_nginx long analysis"""

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
                data.get("status_def").get("memcached").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("memcached").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("memcached").update(
                {"MicroService_layer": num[0]}
            )


def StaDefRedis(lines):
    """default test_status_redis long analysis"""

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
                data.get("status_def").get("redis").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("redis").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("redis").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPhp(lines):
    """default test_status_php long analysis"""

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
                data.get("status_def").get("php").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("php").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("php").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPython(lines):
    """default test_status_python long analysis"""

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
                data.get("status_def").get("python").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("python").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("python").update(
                {"MicroService_layer": num[0]}
            )


def StaDefGolang(lines):
    """default test_status_golang long analysis"""

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
                data.get("status_def").get("golang").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("golang").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("golang").update(
                {"MicroService_layer": num[0]}
            )


def StaDefNode(lines):
    """"default test_status_node log analysis"""

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
                data.get("status_def").get("node").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("node").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("node").update(
                {"MicroService_layer": num[0]}
            )


def StaDefOpenjdk(lines):
    """default test_status_openjdk log analysis"""

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
                data.get("status_def").get("openjdk").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("openjdk").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("openjdk").update(
                {"MicroService_layer": num[0]}
            )


def StaDefRuby(lines):
    """clearlinux test_status_ruby log analysis"""

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
                data.get("status_def").get("ruby").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("ruby").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("ruby").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPerl(lines):
    """clearlinux test_status_perl log analysis"""

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
                data.get("status_def").get("perl").update(
                    {"Toatl": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("perl").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("perl").update(
                {"MicroService_layer": num[0]}
            )


def StaDefTensorflow(lines):
    """default test_status_tensorflow log analysis"""

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

        if i.startswith("tensorflow"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("tensorflow").update(
                    {"Total": num[-1] + "GB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("tensorflow").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("tensorflow").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPostgres(lines):
    """default test_status_postgres long analysis"""

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

        if i.startswith("postgres"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("postgres").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("postgres").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("postgres").update(
                {"MicroService_layer": num[0]}
            )


def StaDefMariadb(lines):
    """default test_status_postgres long analysis"""

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

        if i.startswith("mariadb"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("mariadb").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("mariadb").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("mariadb").update(
                {"MicroService_layer": num[0]}
            )


def StaDefRabbitmq(lines):
    """default test_status_perl log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("rabbitmq"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("rabbitmq"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("rabbitmq").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("rabbitmq").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("rabbitmq").update(
                {"MicroService_layer": num[0]}
            )


"""STATUS_clearlinux_log"""


def StaClrHttpd(lines):
    """clearlinux test_status_httpd long analysis"""

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
                data.get("status_Clr").get("httpd").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("httpd").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("httpd").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/httpd version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("httpd").update(
                {"VERSION_ID": num[0]}
            )


def StaClrNginx(lines):
    """clearlinux test_status_nginx long analysis"""

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
                data.get("status_Clr").get("nginx").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("nginx").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("nginx").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/nginx version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("nginx").update(
                {"VERSION_ID": num[0]}
            )


def StaClrMemcached(lines):
    """clearlinux test_status_nginx long analysis"""

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
                data.get("status_Clr").get("memcached").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("memcached").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("memcached").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/memcached version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("memcached").update(
                {"VERSION_ID": num[0]}
            )


def StaClrRedis(lines):
    """default test_status_redis long analysis"""

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
                data.get("status_Clr").get("redis").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("redis").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("redis").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/redis version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("redis").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPhp(lines):
    """default test_status_php long analysis"""

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
                data.get("status_Clr").get("php").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("php").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("php").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/php version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("php").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPython(lines):
    """clearlinux test_status_python long analysis"""

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
                data.get("status_Clr").get("python").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("python").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("python").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/python version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("python").update(
                {"VERSION_ID": num[0]}
            )


def StaClrGolang(lines):
    """clearlinux test_status_golang long analysis"""

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
                data.get("status_Clr").get("golang").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("golang").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("golang").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/golang version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("golang").update(
                {"VERSION_ID": num[0]}
            )


def StaClrNode(lines):
    """default test_status_node long analysis"""

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
                data.get("status_Clr").get("node").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("node").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("node").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/node version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("node").update(
                {"VERSION_ID": num[0]}
            )


def StaClrOpenjdk(lines):
    """clearlinux test_status_openjdk long analysis"""

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
                data.get("status_Clr").get("openjdk").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("openjdk").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("openjdk").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/openjdk version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("openjdk").update(
                {"VERSION_ID": num[0]}
            )


def StaClrRuby(lines):
    """clearlinux test_status_openjdk long analysis"""

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
                data.get("status_Clr").get("ruby").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("ruby").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("ruby").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/ruby version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("ruby").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPerl(lines):
    """clearlinux test_status_perl log analysis"""

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
                data.get("status_Clr").get("perl").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("perl").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("perl").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/perl version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("perl").update(
                {"VERSION_ID": num[0]}
            )


def StaClrTensorflow(lines):
    """clearlinux test_status_tensorflow log analysis"""

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
                data.get("status_Clr").get("tensorflow").update(
                    {"Total": num[-1] + "GB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("tensorflow").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("tensorflow").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/tensorflow version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("tensorflow").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPostgres(lines):
    """default test_status_postgres long analysis"""

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
                data.get("status_Clr").get("postgres").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("postgres").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("postgres").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/postgres version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("postgres").update(
                {"VERSION_ID": num[0]}
            )


def StaClrMariadb(lines):
    """default test_status_mariadb long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("mariadb"):
            if "latest" in i:
                start = lines.index(i)
                # print(start)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/mariadb"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("mariadb").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("mariadb").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("mariadb").update(
                {"MicroService_layer": num[0]})

    for i in lines[start:]:
        if i.startswith("clearlinux/mariadb version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("mariadb").update(
                {"VERSION_ID": num[0]}
            )


def StaClrRabbitmq(lines):
    """clearlinux test_status_perl log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("rabbitmq"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/rabbitmq"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("rabbitmq").update(
                    {"Total": num[-1] + "GB"}

                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("rabbitmq").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("rabbitmq").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/perl version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("rabbitmq").update(
                {"VERSION_ID": num[0]}
            )


def main():
    file_name = r"/home/zxh/auto_latest/2019-07-03/test_log/rabbitmq/2019-07-02-23:36:43.log"
    test = read_logs(file_name)

    status_log = r"/home/zxh/auto_latest/2019-07-03/json/status/1562122078.json"
    status = read_status_logs(status_log)

    # default_from_httpd(test)
    # default_from_nginx(test)
    # default_from_memcached(test)
    # default_from_redis(test)
    # default_from_php(test)
    # default_from_python(test)
    # default_from_golang(test)
    # default_from_nodejs(test)
    # default_from_openjdk(test)
    # default_from_ruby(test)
    # default_from_perl(test)
    # default_from_postgres(test)
    # default_from_tensorflow(test)
    # default_from_mariadb(test)
    default_from_rabbitmq(test)

    # clr_from_httpd(test)
    # clr_from_nginx(test)
    # clr_from_memcached(test)
    # clr_from_redis(test)
    # clr_from_php(test)
    # clr_from_golang(test)
    # clr_from_python(test)
    # clr_from_nodejs(test)
    # clr_from_openjdk(test)
    # clr_from_ruby(test)
    # clr_from_perl(test)
    # clr_from_postgres(test)clr_from_rabbitmq
    # clr_from_tensorflow(test)
    # clr_from_mariadb(test)
    clr_from_rabbitmq(test)

    # StaDefHttpd(status)
    # StaDefRuby(status)
    # StaDefNginx(status)
    # StaDefMemcached(status)
    # StaDefRedis(status)
    # StaDefPhp(status)
    # StaDefPython(status)
    # StaDefGolang(status)
    # StaDefNode(status)
    # StaDefOpenjdk(status)
    # StaDefPerl(status)
    # StaDefTensorflow(status)
    # StaDefPostgres(status)
    # StaDefMariadb(status)
    # StaDefRabbitmq(status)

    # StaClrHttpd(status)
    # StaClrNginx(status)
    # StaClrMemcached(status)
    # StaClrRedis(status)
    # StaClrPhp(status)
    # StaClrPython(status)
    # StaClrGolang(status)
    # StaClrNode(status)
    # StaClrOpenjdk(status)
    # StaClrRuby(status)
    # StaClrPerl(status)
    # StaClrTensorflow(status)
    # StaClrPostgres(status)
    # StaClrMariadb(status)
    # StaClrRabbitmq(status)


# with open('data_NEW_1.json', 'w') as f:
#     json.dump(data, f)


if __name__ == '__main__':
    main()
    pprint(data)

"""
test_cmd = ["make httpd", "make nginx", "make memcached", "make redis", "make php", "make python", "make node",
            "make golang", "make postgres", "make tensorflow", "make mariadb", "make perl", "make openjdk",
            "make ruby"]


"""
