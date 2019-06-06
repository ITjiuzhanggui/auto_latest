#!/usr/bin/env python

import os, sys
import re
import json
from pprint import pprint

data = {
    "default":
        {
            "httpd": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {}, "golang": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {},
        },

    "clear":
        {
            "httpd": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {}, "golang": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {},
        },

    "status_def":
        {
            "httpd": {}, "golang": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {},
        },

    "status_Clr":
        {
            "clearlinux_version": {}, "httpd": {}, "golang": {}, "nginx": {}, "memcached": {}, "redis": {},
            "php": {}, "python": {}, "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {},
        }
}

"""default test_long"""


def read_logs(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        return f.readlines()


def read_status_logs(status_log):
    with open(status_log, "r", encoding="utf-8") as s:
        return s.readlines()


def default_from_httpd(lines):
    """httpd unit tests analysis"""
    for i in lines[
             lines.index("httpd/httpd.sh\n"):
             lines.index("Default-Httpd-Server\n")]:

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
             lines.index("nginx/nginx.sh\n"):
             lines.index("Default-Nginx-Server\n")]:

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


def default_from_memcached(lines):
    '''memcached unit tests analysis'''

    for i in lines[
             lines.index("memcached/memcached.sh\n"):
             lines.index("Default-Memcached-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)
            
            data.get("default").get("memcached").update(
                {"Sets": ["Latency:"+num[-2], num[-1] +" KB/sec"]})

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)
        
            data.get("default").get("memcached").update(
                {"Gets": ["Latency:"+num[-2], num[-1] +" KB/sec"]})

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)
            
            data.get("default").get("memcached").update(
                {"Totals": ["Latency:"+num[-2], num[-1] +" KB/sec"]})


def default_from_redis(lines):
    """redis unit tests analysis"""

    influs_defaut = []
    for i in lines[
             lines.index("redis/redis.sh\n"):
             lines.index("Default-Redis-Server\n")]:

        influs_defaut.append(i)

    for i in influs_defaut[
             influs_defaut.index("====== PING_INLINE ======\n"):influs_defaut.index("====== PING_BULK ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"PING_INLINE": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== PING_BULK ======\n"):influs_defaut.index("====== SET ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"PING_BULK": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== SET ======\n"):influs_defaut.index("====== GET ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SET": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== GET ======\n"):influs_defaut.index("====== INCR ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"GET": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== INCR ======\n"):influs_defaut.index("====== LPUSH ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"INCR": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LPUSH ======\n"):influs_defaut.index("====== RPUSH ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPUSH": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== RPUSH ======\n"):influs_defaut.index("====== LPOP ======\n")]:
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

    for i in influs_defaut[influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):influs_defaut.index(
            "====== MSET (10 keys) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_600 (first 600 elements)": num[0]}
            )

    influs_defaut.append("some-redis\n")
    for i in influs_defaut[influs_defaut.index("====== MSET (10 keys) ======\n"):influs_defaut.index("some-redis\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"MSET (10 keys)": num[0]}
            )


def default_from_php(lines):
    """php unit tests analysis"""

    for i in lines[
             lines.index("php/php.sh\n"):
             lines.index("Default-Php-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("php").update(
                {"phpbench": num[0]}
            )


def default_from_python(lines):
    """python unit tests analysis"""

    for i in lines[
             lines.index("python/python.sh\n"):
             lines.index("Default-Python-Server\n")]:

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
             lines.index("openjdk/openjdk.sh\n"):
             lines.index("Default-Openjdk-Server\n")]:

        if i.startswith("o.s.MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("default").get("openjdk").update(
                {"MyBenchmark.testMethod:Score": num[1]}
            )

        if i.startswith("o.s.MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("default").get("openjdk").update(
                {"o.s.MyBenchmark.testMethod:Error": num[-1]}
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

    for i in lines[lines.index("[memcached] [INFO] Test clear docker image:\n"):lines.index("cl-memcached-server\n")]:
        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)
        
            data.get("clear").get("memcached").update(
                {"Sets": ["Latency:"+num[-2], num[-1] +" KB/sec"]})

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)
        
            data.get("clear").get("memcached").update(
                {"Gets": ["Latency:"+num[-2], num[-1] +" KB/sec"]})

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)
    
            data.get("clear").get("memcached").update(
                {"Totals": ["Latency:"+num[-2], num[-1] +" KB/sec"]})


def clr_from_redis(lines):
    """clearlinux unit tests analysis"""

    influs_defaut = []
    for i in lines[
             lines.index("[redis] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Redis-Server\n")]:
        influs_defaut.append(i)

    for i in influs_defaut[
             influs_defaut.index("====== PING_INLINE ======\n"):influs_defaut.index("====== PING_BULK ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"PING_INLINE": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== PING_BULK ======\n"):influs_defaut.index("====== SET ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"PING_BULK": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== SET ======\n"):influs_defaut.index("====== GET ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SET": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== GET ======\n"):influs_defaut.index("====== INCR ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"GET": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== INCR ======\n"):influs_defaut.index("====== LPUSH ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"INCR": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LPUSH ======\n"):influs_defaut.index("====== RPUSH ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPUSH": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== RPUSH ======\n"):influs_defaut.index("====== LPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"RPUSH": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LPOP ======\n"):influs_defaut.index("====== RPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPOP": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== RPOP ======\n"):influs_defaut.index("====== SADD ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"RPOP": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== SADD ======\n"):influs_defaut.index("====== HSET ======\n")]:
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

    for i in influs_defaut[influs_defaut.index("====== SPOP ======\n"):influs_defaut.index(
            "====== LPUSH (needed to benchmark LRANGE) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):influs_defaut.index(
                 "====== LRANGE_100 (first 100 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPUSH (needed to benchmark LRANGE)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):influs_defaut.index(
            "====== LRANGE_300 (first 300 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_100 (first 100 elements)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):influs_defaut.index(
            "====== LRANGE_500 (first 450 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_300 (first 300 elements)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):influs_defaut.index(
            "====== LRANGE_600 (first 600 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_500 (first 450 elements)": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):influs_defaut.index(
            "====== MSET (10 keys) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_600 (first 600 elements)": num[0]}
            )

    influs_defaut.append("some-redis\n")
    for i in influs_defaut[influs_defaut.index("====== MSET (10 keys) ======\n"):influs_defaut.index("some-redis\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"MSET (10 keys)": num[0]}
            )


def clr_from_php(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[php] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Php-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("php").update(
                {"Score": num[0]}
            )


def clr_from_python(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[python] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Python-Server\n")]:

        if i.startswith("Totals"):
            num = re.findall("\d+\.?\d*", i)
            num[0] = {"minimum": num[0]}
            num[1] = {"average": num[1]}
            data.get("clear").get("python").update(
                {"Totals": num[-2:]}
            )


def clr_from_golang(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[golang] [INFO] Test clear docker image:\n"):
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


def clr_form_openjdk(lines):
    """clearlinux unit tests analysis"""
    for i in lines[
             lines.index("[openjdk] [INFO] Test clear docker image first:\n"):
             lines.index("Clr-Openjdk-Server\n")]:

        if i.startswith("o.s.MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("clear").get("openjdk").update(
                {"MyBenchmark.testMethod:Score": num[1]}
            )

        if i.startswith("o.s.MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("clear").get("openjdk").update(
                {"o.s.MyBenchmark.testMethod:Error": num[-1]}
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
                {"MicroService_layer": num[0]}
            )


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
    """"default test_status_node long analysis"""

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
    """default test_status_openjdk long analysis"""

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
    """clearlinux test_status_ruby long analysis"""

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


def main():
    file_name = 'test_LOG.log'
    status_log = 'status_LOG.log'
    test = read_logs(file_name)
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

    # clr_from_httpd(test)
    # clr_from_nginx(test)
    # clr_from_memcached(test)
    # clr_from_redis(test)
    # clr_from_php(test)
    # clr_from_python(test)
    # clr_from_golang(test)
    # clr_from_nodejs(test)
    # clr_form_openjdk(test)
    # clr_from_ruby(test)


    # StaDefHttpd(status)
    # StaDefNginx(status)
    # StaDefMemcached(status)
    # StaDefRedis(status)
    # StaDefPhp(status)
    # StaDefPython(status)
    # StaDefGolang(status)
    # StaDefNode(status)
    # StaDefOpenjdk(status)
    # StaDefRuby(status)
    #
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

    # with open('data_NEW.json', 'w') as f:
    #     json.dump(data, f)


if __name__ == '__main__':
    main()
    pprint(data)
