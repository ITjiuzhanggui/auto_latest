import json
import re
from core.abstract import Global
from conf import ConfManagement


class ClrTestLog(Global):

    def __init__(self):
        super(ClrTestLog, self).__init__()
        test_logpath = ConfManagement().get_ini("TEST_LOG_PATH")
        self.test_log = self.read_logs(test_logpath)

        with open('data.json', 'r') as f:
            self.data = json.load(f)

    def serialization(self):
        pass


class ClrHttpd(ClrTestLog):
    """clearlinux test_case httpd analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[httpd] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Httpd-Server\n")]:

            if i.startswith("Time taken for tests"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux httpd:Time taken for tests")

                data.get("clear").get("httpd").update(
                    {"Time taken for tests": num[0]}
                )

            if i.endswith("[ms] (mean)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux httpd:Time per request")
                data.get("clear").get("httpd").update(
                    {"Time per request": num[0]}
                )

            if i.endswith("(mean, across all concurrent requests)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux httpd:Time per request(all)")
                data.get("clear").get("httpd").update(
                    {"Time per request(all)": num[0]}
                )

            if i.startswith("Requests per second"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux httpd:Requests per second")
                data.get("clear").get("httpd").update(
                    {"Requests per second": num[0]}
                )

            if i.startswith("Transfer rate"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux httpd:Transfer rate")
                data.get("clear").get("httpd").update(
                    {"Transfer rate": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrNginx(ClrTestLog):
    """clearlinux test_case nginx analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[nginx] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Nginx-Server\n")]:

            if i.startswith("Time taken for tests"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_nginx:Time taken for tests")
                data.get("clear").get("nginx").update(
                    {"Time taken for tests": num[0]}
                )

            if i.endswith("[ms] (mean)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_nginx:Time per request")
                data.get("clear").get("nginx").update(
                    {"Time per request": num[0]}
                )

            if i.endswith("(mean, across all concurrent requests)\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_nginx:Time per request(all)")
                data.get("clear").get("nginx").update(
                    {"Time per request(all)": num[0]}
                )

            if i.startswith("Requests per second"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_nginx:Requests per second")
                data.get("clear").get("nginx").update(
                    {"Requests per second": num[0]}
                )

            if i.startswith("Transfer rate"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_nginx:Transfer rate")
                data.get("clear").get("nginx").update(
                    {"Transfer rate": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrMemcached(ClrTestLog):
    """clearlinux test_case memcached analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[memcached] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Memcached-Server\n")]:

            if i.startswith("Sets"):
                num = re.findall("---|\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux memcached:Sets")
                data.get("clear").get("memcached").update(
                    {"Sets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

            if i.startswith("Gets"):
                num = re.findall("---|\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux memcached:Gets")
                data.get("clear").get("memcached").update(
                    {"Gets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

            if i.startswith("Totals"):
                num = re.findall("---|\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux memcached:Totals")
                data.get("clear").get("memcached").update(
                    {"Totals": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrRedis(ClrTestLog):
    """clearlinux  test_case redis analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data
        influs_defaut = []

        for i in lines[
                 lines.index("[redis] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Redis-Server\n")]:
            influs_defaut.append(i)

        for i in influs_defaut[
                 influs_defaut.index("====== PING_INLINE ======\n"):
                 influs_defaut.index("====== PING_BULK ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:PING_INLINE")
                data.get("clear").get("redis").update(
                    {"PING_INLINE": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== PING_BULK ======\n"):
                 influs_defaut.index("====== SET ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:PING_BULK")
                data.get("clear").get("redis").update(
                    {"PING_BULK": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== SET ======\n"):
                 influs_defaut.index("====== GET ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:SET")
                data.get("clear").get("redis").update(
                    {"SET": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== GET ======\n"):
                 influs_defaut.index("====== INCR ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:GET")
                data.get("clear").get("redis").update(
                    {"GET": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== INCR ======\n"):
                 influs_defaut.index("====== LPUSH ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:INCR")
                data.get("clear").get("redis").update(
                    {"INCR": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LPUSH ======\n"):
                 influs_defaut.index("====== RPUSH ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LPUSH")
                data.get("clear").get("redis").update(
                    {"LPUSH": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== RPUSH ======\n"):
                 influs_defaut.index("====== LPOP ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:RPUSH")
                data.get("clear").get("redis").update(
                    {"RPUSH": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LPOP ======\n"):
                 influs_defaut.index("====== RPOP ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LPOP")
                data.get("clear").get("redis").update(
                    {"LPOP": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== RPOP ======\n"):
                 influs_defaut.index("====== SADD ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:RPOP")
                data.get("clear").get("redis").update(
                    {"RPOP": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== SADD ======\n"):
                 influs_defaut.index("====== HSET ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:SADD")
                data.get("clear").get("redis").update(
                    {"SADD": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== HSET ======\n"):
                 influs_defaut.index("====== SPOP ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:HSET")
                data.get("clear").get("redis").update(
                    {"HSET": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== SPOP ======\n"):
                 influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:SPOP")
                data.get("clear").get("redis").update(
                    {"SPOP": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):
                 influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LPUSH (needed to benchmark LRANGE)")
                data.get("clear").get("redis").update(
                    {"LPUSH (needed to benchmark LRANGE)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):
                 influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LRANGE_100 (first 100 elements)")
                data.get("clear").get("redis").update(
                    {"LRANGE_100 (first 100 elements)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):
                 influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LRANGE_300 (first 300 elements)")
                data.get("clear").get("redis").update(
                    {"LRANGE_300 (first 300 elements)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):
                 influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LRANGE_500 (first 450 elements)")
                data.get("clear").get("redis").update(
                    {"LRANGE_500 (first 450 elements)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):
                 influs_defaut.index("====== MSET (10 keys) ======\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:LRANGE_600 (first 600 elements)")
                data.get("clear").get("redis").update(
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


class ClrPhp(ClrTestLog):
    """clearlinux test_case php analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[php] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Php-Server\n")]:

            if i.startswith("Score"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_Php:Score")
                data.get("clear").get("php").update(
                    {"Score": num[0]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrPython(ClrTestLog):
    """clearlinux test_case python analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[python] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Python-Server\n")]:

            if i.startswith("Totals"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_python:Totals")
                num[0] = {"minimum": num[0]}
                num[1] = {"average": num[1]}
                data.get("clear").get("python").update(
                    {"Totals": num[-2:]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrGoalng(ClrTestLog):
    """clearlinux test_case golang analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[golang] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Golang-Server\n")]:

            if i.startswith("BenchmarkBuild"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "clearlinux_golang:BenchmarkBuild")
                data.get("clear").get("golang").update(
                    {"BenchmarkBuild": num[0][:-6]}
                )

            if i.startswith("BenchmarkGarbage"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "clearlinux:BenchmarkGarbage")
                data.get("clear").get("golang").update(
                    {"BenchmarkGarbage": num[0][:-6]}
                )

            if i.startswith("BenchmarkHTTP"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "clearlinux:BenchmarkHTTP")
                data.get("clear").get("golang").update(
                    {"BenchmarkHTTP": num[0][:-6]}
                )

            if i.startswith("BenchmarkJSON"):
                num = re.findall("\d+\.?\d* ns/op", i)
                self.exception_to_response(num, "clearlinux:BenchmarkJSON")
                data.get("clear").get("golang").update(
                    {"BenchmarkJSON": num[0][:-6]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrNode(ClrTestLog):
    """clearlinux test_case node analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[node] [INFO] Test clear docker image:\n"):
                 lines.index("Clr-Node-Server\n")]:

            if i.startswith("Score"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_node:benchmark-node-octane")
                data.get("clear").get("node").update(
                    {"benchmark-node-octane": num[-1]}
                )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrOpenjdk(ClrTestLog):
    """clearlinux test_case openjdk analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for item in lines:
            if item.startswith("[openjdk] [INFO] Test clear docker image:\n"):
                start = lines.index(item)

        for i in lines[start:]:
            if i.startswith("Benchmark"):
                end = lines[start:].index(i) + start

        for item in lines[start:end + 8]:
            if i.startswith("MyBenchmark.testMethod"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_openjdk:MyBenchmark.testMethod.Score")
                data.get("clear").get("openjdk").update(
                    {"MyBenchmark.testMethod.Score": num[-2]}
                )

            if i.startswith("MyBenchmark.testMethod"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_openjdk:MyBenchmark.testMethod.Error")
                data.get("clear").get("openjdk").update(
                    {"MyBenchmark.testMethod.Error": num[-1]}
                )
        # for i in lines[
        #          lines.index("[openjdk] [INFO] Test clear docker image:\n"):
        #          lines.index("clr-openjdk\n")]:
        #
        #     if i.startswith("o.s.MyBenchmark.testMethod"):
        #         num = re.findall("\d+\.?\d+", i)
        #         self.exception_to_response(num, "clearlinux_openjdk:MyBenchmark.testMethod:Score")
        #         data.get("clear").get("openjdk").update(
        #             {"MyBenchmark.testMethod:Score": num[1]}
        #         )
        #
        #     if i.startswith("o.s.MyBenchmark.testMethod"):
        #         num = re.findall("\d+\.?\d+", i)
        #         self.exception_to_response(num, "clearlinux_openjdk:o.s.MyBenchmark.testMethod:Error")
        #         data.get("clear").get("openjdk").update(
        #             {"o.s.MyBenchmark.testMethod:Error": num[-1]}
        #         )

        with open("data.json")as f:
            json.dump(data, f)


class ClrRuby(ClrTestLog):
    """clearlinux test_case ruby analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[ruby] [INFO] Test docker hub official image first:\n"):
                 lines.index("Clr-Ruby-Server\n")]:

            if i.endswith("s/i)\n"):
                if "app_answer" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_answer")
                    data.get("clear").get("ruby").update(
                        {"app_answer": num[-2]}
                    )
            if i.endswith("s/i)\n"):
                if "app_aobench" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_aobench")
                    data.get("clear").get("ruby").update(
                        {"app_aobench": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_erb" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_erb")
                    data.get("clear").get("ruby").update(
                        {"app_erb": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_factorial" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_factorial")
                    data.get("clear").get("ruby").update(
                        {"app_factorial": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_fib" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_fib")
                    data.get("clear").get("ruby").update(
                        {"app_fib": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_lc_fizzbuzz" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_lc_fizzbuzz")
                    data.get("clear").get("ruby").update(
                        {"app_lc_fizzbuzz": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_mandelbrot" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_mandelbrot")
                    data.get("clear").get("ruby").update(
                        {"app_mandelbrot": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_pentomino" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_pentomino")
                    data.get("clear").get("ruby").update(
                        {"app_pentomino": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_raise" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_raise")
                    data.get("clear").get("ruby").update(
                        {"app_raise": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_strconcat" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_strconcat")
                    data.get("clear").get("ruby").update(
                        {"app_strconcat": num[-2]}
                    )

            if i.endswith("s/i)\n"):
                if "app_tak" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_tak")
                    data.get("clear").get("ruby").update(
                        {"app_tak": num[-2]}

                    )

            if i.endswith("s/i)\n"):
                if "app_tarai" in i:
                    num = re.findall("\d+\.?\d*", i)
                    self.exception_to_response(num, "clearlinux_ruby:app_tarai")
                    data.get("clear").get("ruby").update(
                        {"app_tarai": num[-2]}
                    )

        with open("data.json", 'w') as f:
            json.dump(data, f)


class ClrPerl(ClrTestLog):
    """clearlinux test_case perl analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data
        start = end = 0
        up = down = 0
        for item in lines:
            if item.startswith("[perl] [INFO] Test clear docker image:\n"):
                start = lines.index(item)

        for i in lines[start:]:
            if i.startswith("Test: benchmarks/statement/inc.b"):
                end = lines[start:].index(i) + start

        for item in lines[start:end]:
            if item.startswith("Test-File: benchmarks/app/podhtml.b\n"):
                up = lines[start:end].index(item) + start

            if item.startswith("Test: benchmarks/startup/noprog.b"):
                down = lines[start:end].index(item) + start

        for i in lines[up:down]:
            if i.startswith("Avg:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_perl:podhtml.b")
                data.get("clear").get("perl").update(
                    {"podhtml.b": num[0]}
                )

        for item in lines[start:end]:
            if item.startswith("Test: benchmarks/startup/noprog.b"):
                up = lines[start:end].index(item) + start

            if item.startswith("Test: benchmarks/statement/assign-int.b"):
                down = lines[start:end].index(item) + start

        for i in lines[up:down]:
            if i.startswith("Avg:"):
                num = re.findall("\d+\.\d*", i)
                self.exception_to_response(num, "clearlinux_perl:noprog.b")
                data.get("clear").get("perl").update(
                    {"noprog.b": num[0]}
                )

        with open("data.json", "w")as f:
            json.dump(data, f)
