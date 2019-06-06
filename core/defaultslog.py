import json
import re
from core.abstract import Global
from conf import ConfManagement


class DefTestLog(Global):

    def __init__(self):
        super(DefTestLog, self).__init__()
        test_logpath = ConfManagement().get_ini("TEST_LOG_PATH")
        self.test_log = self.read_logs(test_logpath)

        with open('data.json', 'r') as f:
            self.data = json.load(f)

    def serialization(self):
        pass


class DefHttpd(DefTestLog):
    """default test_case httpd analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data
        for i in lines[
                 lines.index("httpd/httpd.sh\n"):
                 lines.index("Default-Httpd-Server\n")]:

            if i.startswith("Time taken for tests"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_httpd:Time taken for tests")

                data.get("default").get("httpd").update(
                    {"Time taken for tests": num[0]}
                )

            if i.endswith("[ms] (mean)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_httpd:Time per request")
                data.get("default").get("httpd").update(
                    {"Time per request": num[0]}
                )

            if i.endswith("(mean, across all concurrent requests)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_httpd:Time per request(all)")
                data.get("default").get("httpd").update(
                    {"Time per request(all)": num[0]}
                )

            if i.startswith("Requests per second"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_httpd:Requests per second")
                data.get("default").get("httpd").update(
                    {"Requests per second": num[0]}
                )

            if i.startswith("Transfer rate"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_httpd:Transfer rate")
                data.get("default").get("httpd").update(
                    {"Transfer rate": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefNginx(DefTestLog):
    """default test_case nginx analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("nginx/nginx.sh\n"):
                 lines.index("Default-Nginx-Server\n")]:

            if i.startswith("Time taken for tests"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_nginx:Time taken for tests")
                data.get("default").get("nginx").update(
                    {"Time taken for tests": num[0]}
                )

            if i.endswith("[ms] (mean)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_nginx:Time per request")
                data.get("default").get("nginx").update(
                    {"Time per request": num[0]}
                )

            if i.endswith("(mean, across all concurrent requests)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_nginx:Time per request(all)")
                data.get("default").get("nginx").update(
                    {"Time per request(all)": num[0]}
                )

            if i.startswith("Requests per second"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_nginx:Requests per second")
                data.get("default").get("nginx").update(
                    {"Requests per second": num[0]}
                )

            if i.startswith("Transfer rate"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_nginx:Transfer rate")
                data.get("default").get("nginx").update(
                    {"Transfer rate": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefMemcached(DefTestLog):
    """default test_case memcached analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("memcached/memcached.sh\n"):
                 lines.index("Default-Memcached-Server\n")]:

            if i.startswith("Sets"):
                num = re.findall("---|\d+\.?\d*", i)
                self.exception_to_response(num, "default_memcached:Sets")
                data.get("default").get("memcached").update(
                    {"Sets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

            if i.startswith("Gets"):
                num = re.findall("---|\d+\.?\d*", i)
                self.exception_to_response(num, "default_memcached:Gets")
                data.get("default").get("memcached").update(
                    {"Gets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

            if i.startswith("Totals"):
                num = re.findall("---|\d+\.?\d*", i)
                self.exception_to_response(num, "default_memcached:Totals")
                data.get("default").get("memcached").update(
                    {"Totals": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefRedis(DefTestLog):
    """default test_case redis analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data
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
                self.exception_to_response(num, "default_redis:PING_INLINE")
                data.get("default").get("redis").update(
                    {"PING_INLINE": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== PING_BULK ======\n"):
                 influs_defaut.index("====== SET ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:PING_BULK")
                data.get("default").get("redis").update(
                    {"PING_BULK": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== SET ======\n"):
                 influs_defaut.index("====== GET ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:SET")
                data.get("default").get("redis").update(
                    {"SET": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== GET ======\n"):
                 influs_defaut.index("====== INCR ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:GET")
                data.get("default").get("redis").update(
                    {"GET": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== INCR ======\n"):
                 influs_defaut.index("====== LPUSH ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:INCR")
                data.get("default").get("redis").update(
                    {"INCR": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LPUSH ======\n"):
                 influs_defaut.index("====== RPUSH ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LPUSH")
                data.get("default").get("redis").update(
                    {"LPUSH": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== RPUSH ======\n"):
                 influs_defaut.index("====== LPOP ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:RPUSH")
                data.get("default").get("redis").update(
                    {"RPUSH": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LPOP ======\n"):
                 influs_defaut.index("====== RPOP ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LPOP")
                data.get("default").get("redis").update(
                    {"LPOP": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== RPOP ======\n"):
                 influs_defaut.index("====== SADD ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:RPOP")
                data.get("default").get("redis").update(
                    {"RPOP": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== SADD ======\n"):
                 influs_defaut.index("====== HSET ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:SADD")
                data.get("default").get("redis").update(
                    {"SADD": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== HSET ======\n"):
                 influs_defaut.index("====== SPOP ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:HSET")
                data.get("default").get("redis").update(
                    {"HSET": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== SPOP ======\n"):
                 influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:SPOP")
                data.get("default").get("redis").update(
                    {"SPOP": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):
                 influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LPUSH (needed to benchmark LRANGE)")
                data.get("default").get("redis").update(
                    {"LPUSH (needed to benchmark LRANGE)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):
                 influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LRANGE_100 (first 100 elements)")
                data.get("default").get("redis").update(
                    {"LRANGE_100 (first 100 elements)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):
                 influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LRANGE_300 (first 300 elements)")
                data.get("default").get("redis").update(
                    {"LRANGE_300 (first 300 elements)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):
                 influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LRANGE_500 (first 450 elements)")
                data.get("default").get("redis").update(
                    {"LRANGE_500 (first 450 elements)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):
                 influs_defaut.index("====== MSET (10 keys) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_redis:LRANGE_600 (first 600 elements)")
                data.get("default").get("redis").update(
                    {"LRANGE_600 (first 600 elements)": num[0]}
                )

        influs_defaut.append("some-redis\n")

        for i in influs_defaut[
                 influs_defaut.index("====== MSET (10 keys) ======\n"):
                 influs_defaut.index("some-redis\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:MSET (10 keys)")
                data.get("clear").get("redis").update(
                    {"MSET (10 keys)": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefPhp(DefTestLog):
    """default test_case php analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("php/php.sh\n"):
                 lines.index("Default-Php-Server\n")]:

            if i.startswith("Score"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_linux_Php:Score")
                data.get("default").get("php").update(
                    {"Score": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefPython(DefTestLog):
    """default test_case python analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("python/python.sh\n"):
                 lines.index("Default-Python-Server\n")]:

            if i.startswith("Totals"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_python:Totals")
                num[0] = {"minimum": num[0]}
                num[1] = {"average": num[1]}
                data.get("default").get("python").update(
                    {"Totals": num[-2:]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefGoalng(DefTestLog):
    """default test_case golang analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("golang/golang.sh\n"):
                 lines.index("Default-Golang-Server\n")]:

            if i.startswith("BenchmarkBuild"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "default_golang:BenchmarkBuild")
                data.get("default").get("golang").update(
                    {"BenchmarkBuild": num[0][:-6]}
                )

            if i.startswith("BenchmarkGarbage"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "default_golang:BenchmarkGarbage")
                data.get("default").get("golang").update(
                    {"BenchmarkGarbage": num[0][:-6]}
                )

            if i.startswith("BenchmarkHTTP"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "default_golang:BenchmarkHTTP")
                data.get("default").get("golang").update(
                    {"BenchmarkHTTP": num[0][:-6]}
                )

            if i.startswith("BenchmarkJSON"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "default_golang:BenchmarkJSON")
                data.get("default").get("golang").update(
                    {"BenchmarkJSON": num[0][:-6]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefNode(DefTestLog):
    """default test_case node analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("node/node.sh\n"):
                 lines.index("Default-Node-Server\n")]:

            if i.startswith("Score"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_node:benchmark-node-octane")
                data.get("default").get("node").update(
                    {"benchmark-node-octane": num[-1]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class DefOpenjdk(DefTestLog):
    """default test_case openjdk analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[openjdk] [INFO] Test docker hub official image:\n"):
                 lines.index("offi-openjdk\n")]:

            if i.startswith("o.s.MyBenchmark.testMethod"):
                num = re.findall("\d+\.?\d+", i)
                self.exception_to_response(num, "default_openjdk:MyBenchmark.testMethod:Score")
                data.get("default").get("openjdk").update(
                    {"MyBenchmark.testMethod:Score": num[1]}
                )

            if i.startswith("o.s.MyBenchmark.testMethod"):
                num = re.findall("\d+\.?\d+", i)
                self.exception_to_response(num, "default_openjdk:o.s.MyBenchmark.testMethod:Error")
                data.get("default").get("openjdk").update(
                    {"o.s.MyBenchmark.testMethod:Error": num[-1]}
                )

        with open("data.json")as f:
            json.dump(data, f)


class DefRuby(DefTestLog):
    """default test_case ruby analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("ruby/ruby.sh\n"):
                 lines.index("Default-Ruby-Server\n")]:

            if i.endswith("s/i)\n"):
                if "app_answer" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_answer")
                    data.get("default").get("ruby").update(
                        {"app_answer": num[-2]}
                    )
            if i.endswith("s/i)\n"):
                if "app_aobench" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_aobench")
                    data.get("default").get("ruby").update(
                        {"app_aobench": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_erb" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_erb")
                    data.get("default").get("ruby").update(
                        {"app_erb": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_factorial" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_factorial")
                    data.get("default").get("ruby").update(
                        {"app_factorial": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_fib" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_fib")
                    data.get("default").get("ruby").update(
                        {"app_fib": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_lc_fizzbuzz" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_lc_fizzbuzz")
                    data.get("default").get("ruby").update(
                        {"app_lc_fizzbuzz": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_mandelbrot" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_mandelbrot")
                    data.get("default").get("ruby").update(
                        {"app_mandelbrot": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_pentomino" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_pentomino")
                    data.get("default").get("ruby").update(
                        {"app_pentomino": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_raise" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_raise")
                    data.get("default").get("ruby").update(
                        {"app_raise": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_strconcat" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_strconcat")
                    data.get("default").get("ruby").update(
                        {"app_strconcat": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_tak" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_tak")
                    data.get("default").get("ruby").update(
                        {"app_tak": num[-2]}

                    )

            if i.endswith("s/i)\n"):
                if "app_tarai" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "default_ruby:app_tarai")
                    data.get("default").get("ruby").update(
                        {"app_tarai": num[-2]}
                    )

        with open("data.json", 'w') as f:
            json.dump(data, f)
