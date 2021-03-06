import json
import os
import re
from core.abstract import Global
from conf import ConfManagement


class DefTestLog(Global):

    def __init__(self):
        super(DefTestLog, self).__init__()
        test_logpath = ConfManagement().get_ini("TEST_LOG_PATH")
        self.test_log = self.read_logs(test_logpath)
        self.json_path = os.path.dirname(os.path.realpath(__file__))[:-4] + 'data.json'
        with open(self.json_path, 'r') as f:
            self.data = json.load(f)

    def serialization(self):
        pass


class DefHttpd(DefTestLog):
    """default test_case httpd analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data
        for i in lines[
                 lines.index("[httpd] [INFO] Test docker hub official image first:\n"):
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

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class DefNginx(DefTestLog):
    """default test_case nginx analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[nginx] [INFO] Test docker hub official image first:\n"):
                 lines.index("[nginx] [INFO] Test clear docker image:\n")]:

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

        with open(self.json_path, 'w') as f:
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

        with open(self.json_path, 'w') as f:
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

        influs_defaut.append("Default-Redis-Server\n")

        for i in influs_defaut[
                 influs_defaut.index("====== MSET (10 keys) ======\n"):
                 influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n")]:

            if i.endswith("requests per second\n"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "clearlinux_redis:MSET (10 keys)")
                data.get("default").get("redis").update(
                    {"MSET (10 keys)": num[0]}
                )

        for i in influs_defaut[
                 influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n"):
                 influs_defaut.index("Default-Redis-Server\n")]:

            if i.startswith("Sets"):
                num = re.findall("---|\d+\.?\d*", i)

                data.get("default").get("redis").update(
                    {"Sets-Latency": num[-2]})
                data.get("default").get("redis").update(
                    {"Sets-KB/sec": num[-1]}
                )

            if i.startswith("Gets"):
                num = re.findall("---|\d+\.?\d*", i)

                data.get("default").get("redis").update(
                    {"Gets-Latency": num[-2]})
                data.get("default").get("redis").update(
                    {"Gets-KB/sec": num[-1]}
                )

            if i.startswith("Totals"):
                num = re.findall("---|\d+\.?\d*", i)

                data.get("default").get("redis").update(
                    {"Totals-Latency": num[-2]})
                data.get("default").get("redis").update(
                    {"Totals-KB/sec": num[-1]}
                )

        with open(self.json_path, 'w') as f:
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

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class DefPython(DefTestLog):
    """default test_case python analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        # for i in lines[
        #          lines.index("python/python.sh\n"):
        #          lines.index("Default-Python-Server\n")]:
        lines = lines[lines.index("python/python.sh\n"):
                      lines.index("[python] [INFO] Test clear docker image:\n")].copy()

        for i in lines:
            if i.startswith("Totals"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_python:Totals")
                num[0] = {"minimum": num[0]}
                num[1] = {"average": num[1]}
                data.get("default").get("python").update(
                    {"Totals": num[-2:]}
                )

        with open(self.json_path, 'w') as f:
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

        with open(self.json_path, 'w') as f:
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

        with open(self.json_path, 'w') as f:
            json.dump(data, f)


class DefOpenjdk(DefTestLog):
    """default test_case openjdk analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[openjdk] [INFO] Test docker hub official image first:\n"):
                 lines.index("[openjdk] [INFO] Test clear docker image:\n")]:

            if i.startswith("MyBenchmark.testMethod") and "thrpt " in i:
                num = re.findall("\d+\.?\d+", i)
                self.exception_to_response(num, "default_openjdk:MyBenchmark.testMethod.Score")
                data.get("default").get("openjdk").update(
                    {"MyBenchmark.testMethod.Score": num[-2]}
                )

            if i.startswith("MyBenchmark.testMethod") and "thrpt " in i:
                num = re.findall("\d+\.?\d+", i)
                self.exception_to_response(num, "default_openjdk:MyBenchmark.testMethod.Error")
                data.get("default").get("openjdk").update(
                    {"MyBenchmark.testMethod.Error": num[-1]}
                )

        # for i in lines[
        #          lines.index("[openjdk] [INFO] Test docker hub official image:\n"):
        #          lines.index("offi-openjdk\n")]:
        #
        #     if i.startswith("o.s.MyBenchmark.testMethod"):
        #         num = re.findall("\d+\.?\d+", i)
        #         self.exception_to_response(num, "default_openjdk:MyBenchmark.testMethod:Score")
        #         data.get("default").get("openjdk").update(
        #             {"MyBenchmark.testMethod:Score": num[1]}
        #         )
        #
        #     if i.startswith("o.s.MyBenchmark.testMethod"):
        #         num = re.findall("\d+\.?\d+", i)
        #         self.exception_to_response(num, "default_openjdk:o.s.MyBenchmark.testMethod:Error")
        #         data.get("default").get("openjdk").update(
        #             {"o.s.MyBenchmark.testMethod:Error": num[-1]}
        #         )

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefRuby(DefTestLog):
    """default test_case ruby analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        newlines = lines[
                   lines.index("[ruby] [INFO] Test docker hub official image first:\n"):
                   lines.index("[ruby] [INFO] Test clear docker image:\n")].copy()

        line_str_key = "Calculating"
        line_dict = {}
        ret_lines = []
        for i in range(0, len(newlines)):
            line_dict[i] = newlines[i].split("\n")[0]

        for lineno, line_str in line_dict.items():
            if line_str.startswith(line_str_key):

                tmp_line_no = lineno + 1
                while True:
                    if newlines[tmp_line_no] != "\n":
                        if "so_k_nucleotidepreparing" in newlines[tmp_line_no]:
                            ret_lines.append("so_k_nucleotidepreparing " + newlines[tmp_line_no + 1])
                        if "so_reverse_complementpreparing" in newlines[tmp_line_no]:
                            ret_lines.append("so_reverse_complementpreparing " + newlines[tmp_line_no + 1])
                        ret_lines.append(newlines[tmp_line_no])
                    else:
                        break
                    tmp_line_no += 1

        ret_line_list = []
        for line in ret_lines:

            line_split = line.split()
            key_str = line_split[0]
            value = line_split[1]
            if "Time" in line:
                time_line_split = line.split("s -")[0].split(")")

                time_key = time_line_split[0].strip() + ")"
                time_value = time_line_split[-1].strip()

                ret_line_list.append({time_key: time_value})
            elif not value.startswith("/"):

                try:
                    key_str = float(str(key_str))
                except Exception:
                    pass
                if not isinstance(key_str, float):
                    ret_line_list.append({key_str: value})

        for tmp_dict in ret_line_list:
            data.get("default").get("ruby").update(tmp_dict)

        with open(self.json_path, 'w') as f:
            json.dump(data, f)
        # influs_list = ["app_answer", "app_aobench", "app_erb", "app_factorial",
        #                "app_fib", "app_lc_fizzbuzz", "app_mandelbrot", "app_pentomino",
        #                "app_raise", "app_strconcat", "app_tak", "app_tarai", "app_uri",
        #                "array_sample_100k_10", "array_sample_100k_11", "array_sample_100k__100",
        #                "array_sample_100k__1k", "array_sample_100k__6k", "array_sample_100k___10k",
        #                "array_sample_100k___50k", "array_shift", "array_small_and", "array_small_diff",
        #                "array_small_or", "array_sort_block", "array_sort_float", "array_values_at_int",
        #                "array_values_at_range", "bighash", "complex_float_add", "complex_float_div",
        #                "complex_float_mul", "complex_float_new", "complex_float_power", "complex_float_sub",
        #                "dir_empty_p", "enum_lazy_grep_v_100", "enum_lazy_grep_v_20", "enum_lazy_grep_v_50",
        #                "enum_lazy_uniq_100", "enum_lazy_uniq_20", "enum_lazy_uniq_50", "erb_render",
        #                "fiber_chain", "file_chmod", "file_rename", "hash_aref_dsym", "hash_aref_dsym_long",
        #                "hash_aref_fix", "hash_aref_flo", "hash_aref_miss", "hash_aref_str", "hash_aref_sym",
        #                "hash_aref_sym_long", "hash_flatten", "hash_ident_flo", "hash_ident_num", "hash_ident_obj",
        #                "hash_ident_str", "hash_ident_sym", "hash_keys", "hash_literal_small2", "hash_literal_small4",
        #                "hash_literal_small8", "hash_long", "hash_shift", "hash_shift_u16", "hash_shift_u24",
        #                "hash_shift_u32", "hash_small2", "hash_small4", "hash_small8", "hash_to_proc",
        #                "hash_values", "int_quo", "io_copy_stream_write", "io_copy_stream_write_socket",
        #                "io_file_create", "io_file_read", "io_file_write", "io_nonblock_noex", "io_nonblock_noex2",
        #                "io_pipe_rw", "io_select", "io_select2", "io_select3", "loop_for", "loop_generator",
        #                "loop_times", "loop_whileloop", "loop_whileloop2", "marshal_dump_flo", "marshal_dump_load_geniv",
        #                "marshal_dump_load_time",
        #                "Calculating-(1..1_000_000).last(100)",
        #                "Calculating-(1..1_000_000).last(1000)",
        #                "Calculating-(1..1_000_000).last(10000)",
        #                "capitalize-1",
        #                "capitalize-10",
        #                "capitalize-100",
        #                "capitalize-1000",
        #                "downcase-1",
        #                "downcase-10",
        #                "downcase-100",
        #                "downcase-1000",
        #                "require", "require_thread", "securerandom", "so_ackermann",
        #                "so_array", "so_binary_trees", "so_concatenate", "so_count_words", "so_exception", "so_fannkuch",
        #                "so_fasta", "so_k_nucleotidepreparing", "so_lists", "so_mandelbrot", "so_matrix",
        #                "so_meteor_contest",
        #                "so_nbody", "so_nested_loop", "so_nsieve", "so_nsieve_bits", "so_object", "so_partial_sums",
        #                "so_pidigits", "so_random", "so_reverse_complementpreparing", "so_sieve", "so_spectralnorm",
        #                "string_index", "string_scan_re",
        #                "string_scan_str",
        #                "to_chars-1",
        #                "to_chars-10",
        #                "to_chars-100",
        #                "to_chars-1000",
        #                "swapcase-1",
        #                "swapcase-10",
        #                "swapcase-100",
        #                "swapcase-1000",
        #                "upcase-1",
        #                "upcase-10",
        #                "upcase-100",
        #                "upcase-1000",
        #                """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""",
        #                """Time.strptime("1", "%s")""",
        #                """Time.strptime("0 +0100", "%s %z")""",
        #                """Time.strptime("0 UTC", "%s %z")""",
        #                """Time.strptime("1.5", "%s.%N")""",
        #                """Time.strptime("1.000000000001", "%s.%N")""",
        #                """Time.strptime("20010203 -0200", "%Y%m%d %z")""",
        #                """Time.strptime("20010203 UTC", "%Y%m%d %z")""",
        #                """Time.strptime("2018-365", "%Y-%j")""",
        #                """Time.strptime("2018-091", "%Y-%j")""",
        #                "time_subsec", "vm1_attr_ivar",
        #                "vm1_attr_ivar_set",
        #                "vm1_block", "vm1_blockparam", "vm1_blockparam_call", "vm1_blockparam_pass",
        #                "vm1_blockparam_yield",
        #                "vm1_const", "vm1_ensure", "vm1_float_simple", "vm1_gc_short_lived",
        #                "vm1_gc_short_with_complex_long",
        #                "vm1_gc_short_with_long", "vm1_gc_short_with_symbol", "vm1_gc_wb_ary", "vm1_gc_wb_ary_promoted",
        #                "vm1_gc_wb_obj", "vm1_gc_wb_obj_promoted", "vm1_ivar", "vm1_ivar_set", "vm1_length",
        #                "vm1_lvar_init",
        #                "vm1_lvar_set", "vm1_neq", "vm1_not", "vm1_rescue", "vm1_simplereturn", "vm1_swap", "vm1_yield",
        #                "vm2_array", "vm2_bigarray", "vm2_bighash", "vm2_case", "vm2_case_lit", "vm2_defined_method",
        #                "vm2_dstr", "vm2_eval", "vm2_fiber_switch", "vm2_freezestring", "vm2_method",
        #                "vm2_method_missing",
        #                "vm2_method_with_block", "vm2_module_ann_const_set", "vm2_module_const_set", "vm2_mutex",
        #                "vm2_newlambda",
        #                "vm2_poly_method", "vm2_poly_method_ov", "vm2_poly_singleton", "vm2_proc", "vm2_raise1",
        #                "vm2_raise2",
        #                "vm2_regexp", "vm2_send", "vm2_string_literal", "vm2_struct_big_aref_hi",
        #                "vm2_struct_big_aref_lo",
        #                "vm2_struct_big_aset", "vm2_struct_big_href_hi", "vm2_struct_big_href_lo", "vm2_struct_big_hset",
        #                "vm2_struct_small_aref", "vm2_struct_small_aset", "vm2_struct_small_href",
        #                "vm2_struct_small_hset",
        #                "vm2_super", "vm2_unif1", "vm2_zsuper", "vm3_backtrace", "vm3_clearmethodcache", "vm3_gc",
        #                "vm3_gc_old_full",
        #                "vm3_gc_old_immediate", "vm3_gc_old_lazy", "vm_symbol_block_pass", "vm_thread_alive_check1",
        #                "vm_thread_close",
        #                "vm_thread_condvar1", "vm_thread_condvar2", "vm_thread_create_join", "vm_thread_mutex1",
        #                "vm_thread_mutex2",
        #                "vm_thread_mutex3", "vm_thread_pass", "vm_thread_pass_flood", "vm_thread_pipe",
        #                "vm_thread_queue",
        #                "vm_thread_sized_queue", "vm_thread_sized_queue2", "vm_thread_sized_queue3",
        #                "vm_thread_sized_queue4"
        #                ]
        # data_ruby = {}
        # for i in lines[
        #          lines.index("ruby/ruby.sh\n"):
        #          lines.index("[ruby] [INFO] Test clear docker image:\n")]:
        #
        #     for startwith_item in influs_list:
        #         if i.endswith("s/i)\n") and startwith_item in i:
        #             num = re.findall("\d+\.?\d* s|ERROR", i)
        #             data_ruby.update({startwith_item: num[-1][:-1]})
        #
        #     if "so_reverse_complementpreparing" in i:
        #         start = lines.index(i)
        #         so_reverse_complementpreparing = lines[start + 1]
        #         num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
        #         self.exception_to_response(num, "default_Ruby:so_reverse_complementpreparing %d line" % (start + 2))
        #         data_ruby.update({"so_reverse_complementpreparing": num[-1][:-1]})
        #
        #     if "so_k_nucleotidepreparing" in i:
        #         start = lines.index(i)
        #         so_reverse_complementpreparing = lines[start + 1]
        #         num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
        #         self.exception_to_response(num, "default_Ruby:so_k_nucleotidepreparing %d line" % (start + 2))
        #         data_ruby.update({"so_k_nucleotidepreparing": num[-1][:-1]})
        #
        # lines = lines[lines.index("ruby/ruby.sh\n"):lines.index("[ruby] [INFO] Test clear docker image:\n")]
        #
        # for item in lines:
        #     if item.startswith("Warming up --------------------------------------\n"):
        #         up = lines.index(item)
        #
        # for item in lines[up:]:
        #     if item.startswith("Comparison:\n"):
        #         down = lines[up:].index(item) + up
        #
        # for i in lines[up:down]:
        #
        #     if "(1..1_000_000).last(100)" in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"(1..1_000_000).last(100)": num[-4]})
        #
        #     if "(1..1_000_000).last(1000)" in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"(1..1_000_000).last(1000)": num[-4]})
        #
        #     if "(1..1_000_000).last(10000)" in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"(1..1_000_000).last(10000)": num[-4]})
        #
        # for i in lines[down:]:
        #
        #     if i.startswith("Warming up --------------------------------------\n"):
        #         capit_start = lines[down:].index(i) + down
        #
        # for i in lines[capit_start:]:
        #
        #     if i.startswith("Calculating -------------------------------------\n"):
        #         calc_start = lines[capit_start:].index(i) + capit_start
        #
        # for i in lines[calc_start:]:
        #
        #     if i.startswith("Comparison:\n"):
        #         calc_end = lines[calc_start:].index(i) + calc_start
        #
        # for i in lines[calc_start:calc_end]:
        #
        #     if "capitalize-1  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"capitalize-1": num[1]})
        #
        #     if "capitalize-10  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"capitalize-10": num[1]})
        #
        #     if "capitalize-100  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"capitalize-100": num[1]})
        #
        #     if "capitalize-1000  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"capitalize-1000": num[1]})
        #
        # for i in lines[calc_end:]:
        #     if i.startswith("Calculating -------------------------------------\n"):
        #         downcase_start = lines[calc_end:].index(i) + calc_end
        #
        # for i in lines[downcase_start:]:
        #
        #     if i.startswith("Comparison:\n"):
        #         downcase_end = lines[downcase_start:].index(i) + downcase_start
        #
        # for i in lines[downcase_start:downcase_end]:
        #
        #     if "downcase-1  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"downcase-1": num[1]})
        #
        #     if "downcase-10  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"downcase-10": num[1]})
        #
        #     if "downcase-100  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"downcase-100": num[1]})
        #
        #     if "downcase-1000  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"downcase-1000": num[1]})
        #
        # for i in lines[downcase_end:]:
        #     if i.startswith("Warming up --------------------------------------\n"):
        #         to_chars = lines[downcase_end:].index(i) + downcase_end
        #
        # for i in lines[to_chars:]:
        #
        #     if i.startswith("Calculating -------------------------------------\n"):
        #         to_chars_start = lines[to_chars:].index(i) + to_chars
        #
        # for i in lines[to_chars_start:]:
        #
        #     if i.startswith("Comparison:\n"):
        #         to_chars_end = lines[to_chars_start:].index(i) + to_chars_start
        #
        # for i in lines[to_chars_start:to_chars_end]:
        #
        #     if "to_chars-1  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"to_chars-1": num[1]})
        #
        #     if "to_chars-10  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"to_chars-10": num[1]})
        #
        #     if "to_chars-100  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"to_chars-100": num[1]})
        #
        #     if "to_chars-1000  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"to_chars-1000": num[1]})
        #
        # for i in lines[to_chars_end:]:
        #
        #     if i.startswith("Warming up --------------------------------------\n"):
        #         swapcase = lines[to_chars_end:].index(i) + to_chars_end
        #
        # for i in lines[swapcase:]:
        #
        #     if i.startswith("Calculating -------------------------------------\n"):
        #         swapcase_start = lines[swapcase:].index(i) + swapcase
        #
        # for i in lines[swapcase_start:]:
        #
        #     if i.startswith("Comparison:\n"):
        #         swapcase_end = lines[swapcase_start:].index(i) + swapcase_start
        #
        # for i in lines[swapcase_start:swapcase_end]:
        #
        #     if "swapcase-1  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"swapcase-1": num[1]})
        #
        #     if "swapcase-10  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"swapcase-10": num[1]})
        #
        #     if "swapcase-100  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"swapcase-100": num[1]})
        #
        #     if "swapcase-1000  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"swapcase-1000": num[1]})
        #
        # for i in lines[swapcase_end:]:
        #
        #     if i.startswith("Calculating -------------------------------------\n"):
        #         upcase_start = lines[swapcase_end:].index(i) + swapcase_end
        #
        # for i in lines[upcase_start:]:
        #
        #     if i.startswith("Comparison:\n"):
        #         upcase_end = lines[upcase_start:].index(i) + upcase_start
        #
        # for i in lines[upcase_start:upcase_end]:
        #
        #     if "upcase-1  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"upcase-1": num[1]})
        #
        #     if "upcase-10  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"upcase-10": num[1]})
        #
        #     if "upcase-100  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"upcase-100": num[1]})
        #
        #     if "upcase-1000  " in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"upcase-1000": num[1]})
        #
        # for i in lines[upcase_end:]:
        #
        #     if i.startswith("Calculating -------------------------------------\n"):
        #         time_start = lines[upcase_end:].index(i) + upcase_end
        #
        # for i in lines[time_start:]:
        #
        #     if i.startswith("Comparison:\n"):
        #         time_end = lines[time_start:].index(i) + time_start
        #
        # for i in lines[time_start:time_end]:
        #
        #     if """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""": num[-4]})
        #
        #     if """Time.strptime("1", "%s")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("1", "%s")""": num[-4]})
        #
        #     if """Time.strptime("0 +0100", "%s %z")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("0 +0100", "%s %z")""": num[-4]})
        #
        #     if """Time.strptime("0 UTC", "%s %z")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("0 UTC", "%s %z")""": num[-4]})
        #
        #     if """Time.strptime("1.5", "%s.%N")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("1.5", "%s.%N")""": num[-4]})
        #
        #     if """Time.strptime("1.000000000001", "%s.%N")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("1.000000000001", "%s.%N")""": num[-4]})
        #
        #     if """Time.strptime("20010203 -0200", "%Y%m%d %z")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("20010203 -0200", "%Y%m%d %z")""": num[-4]})
        #
        #     if """Time.strptime("20010203 UTC", "%Y%m%d %z")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("20010203 UTC", "%Y%m%d %z")""": num[-4]})
        #
        #     if """Time.strptime("2018-365", "%Y-%j")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("2018-365", "%Y-%j")""": num[-4]})
        #
        #     if """Time.strptime("2018-091", "%Y-%j")  """ in i:
        #         num = re.findall("\d+\.?\d*", i)
        #         data_ruby.update({"""Time.strptime("2018-091", "%Y-%j")""": num[-4]})
        #
        # data.get("default").get("ruby").update(data_ruby)
        # for i in lines[
        #          lines.index("ruby/ruby.sh\n"):
        #          lines.index("Default-Ruby-Server\n")]:
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_answer" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_answer")
        #             data.get("default").get("ruby").update(
        #                 {"app_answer": num[-2]}
        #             )
        #     if i.endswith("s/i)\n"):
        #         if "app_aobench" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_aobench")
        #             data.get("default").get("ruby").update(
        #                 {"app_aobench": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_erb" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_erb")
        #             data.get("default").get("ruby").update(
        #                 {"app_erb": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_factorial" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_factorial")
        #             data.get("default").get("ruby").update(
        #                 {"app_factorial": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_fib" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_fib")
        #             data.get("default").get("ruby").update(
        #                 {"app_fib": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_lc_fizzbuzz" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_lc_fizzbuzz")
        #             data.get("default").get("ruby").update(
        #                 {"app_lc_fizzbuzz": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_mandelbrot" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_mandelbrot")
        #             data.get("default").get("ruby").update(
        #                 {"app_mandelbrot": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_pentomino" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_pentomino")
        #             data.get("default").get("ruby").update(
        #                 {"app_pentomino": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_raise" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_raise")
        #             data.get("default").get("ruby").update(
        #                 {"app_raise": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_strconcat" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_strconcat")
        #             data.get("default").get("ruby").update(
        #                 {"app_strconcat": num[-2]}
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_tak" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_tak")
        #             data.get("default").get("ruby").update(
        #                 {"app_tak": num[-2]}
        #
        #             )
        #
        #     if i.endswith("s/i)\n"):
        #         if "app_tarai" in i:
        #             num = re.findall("\d+\.?\d*", i)
        #             self.exception_to_response(num, "default_ruby:app_tarai")
        #             data.get("default").get("ruby").update(
        #                 {"app_tarai": num[-2]}
        #             )

        # with open(self.json_path, 'w') as f:
        #     json.dump(data, f)


class DefPerl(DefTestLog):
    """default test_case Perl analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data
        #        start = end = 0
        influs_default = []

        for i in lines[
                 lines.index("perl/perl.sh\n"):
                 lines.index("[perl] [INFO] Test clear docker image:\n")]:
            influs_default.append(i)

        for item in influs_default:
            if item.startswith("Test-File: benchmarks/app/podhtml.b"):
                start = lines.index(item)

            if item.startswith("Test: benchmarks/startup/noprog.b"):
                end = lines.index(item)

        for item in lines[start:end]:
            if item.startswith("Avg:"):
                num = re.findall("\d+\.?\d*", item)
                self.exception_to_response(num, "default_perl:podhtml.b")
                data.get("default").get("perl").update(
                    {"podhtml.b": num[0]}
                )

        for i in influs_default:
            if i.startswith("Test: benchmarks/startup/noprog.b"):
                start = lines.index(i)

            if i.startswith("[perl] [INFO] Test clear docker image:\n"):
                end = lines.index(i)

        for i in lines[start:end + 15]:
            if i.startswith("Avg:"):
                num = re.findall("\d+\.?\d*", i)
                self.exception_to_response(num, "default_perl:noprog.b")
                data.get("default").get("perl").update(
                    {"noprog.b": num[0]}
                )

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefPostgres(DefTestLog):
    """default test_case postgres analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        lines_a = lines[1:lines.index("[postgres] [INFO] Test clear docker image:\n")].copy()
        # lines_a = lines[
        #           lines.index("[postgres] [INFO] Test extra official docker image, postgres9.6:\n"):
        #           lines.index("Extra Test on postgres9.6\n")].copy()
        line_nu = []

        for i in lines_a:
            if re.search(r"excluding", i) != None:
                line_nu.append(lines_a.index(i))

        bsw = lines_a[int(line_nu[0])].split()
        bsr = lines_a[int(line_nu[1])].split()
        bnw = lines_a[int(line_nu[2])].split()
        bnr = lines_a[int(line_nu[3])].split()
        # bhw = lines_a[int(line_nu[4])].split()
        # bhr = lines_a[int(line_nu[5])].split()
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
        # data.get("default").get("postgres").update(
        #     {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw[2]}
        # )
        # data.get("default").get("postgres").update(
        #     {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr[2]}
        # )

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefTensorflow(DefTestLog):
    """default test_case Tensorflow analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[tensorflow] [INFO] Test docker hub official image first:\n"):
                 lines.index("[tensorflow] [INFO] Test clear docker image:\n")]:

            if i.startswith("Total duration"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("tensorflow").update(
                    {"Total duration": num[0]})

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefMariadb(DefTestLog):
    """default test_case Mariadb analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

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

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefRabbitmq(DefTestLog):
    """default test_case Rabbitmq analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

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

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefFlink(DefTestLog):
    """default test_case Flink analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        for i in lines[
                 lines.index("[flink] [INFO] Test docker hub official image first:\n"):
                 lines.index("Default-Flink-Server\n")]:

            if i.startswith("KeyByBenchmarks.arrayKeyBy"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"KeyByBenchmarks.arrayKeyBy": num[-2]})

            if i.startswith("KeyByBenchmarks.tupleKeyBy"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"KeyByBenchmarks.tupleKeyBy": num[-2]})

            if i.startswith("MemoryStateBackendBenchmark.stateBackends") and "MEMORY" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"MemoryStateBackendBenchmark.stateBackends-MEMORY": num[-2]})

            if i.startswith("MemoryStateBackendBenchmark.stateBackends") and " FS " in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"MemoryStateBackendBenchmark.stateBackends-FS": num[-2]})

            if i.startswith("MemoryStateBackendBenchmark.stateBackends") and "_ASYNC " in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"MemoryStateBackendBenchmark.stateBackends-FS_ASYNC": num[-2]})

            if i.startswith("RocksStateBackendBenchmark.stateBackends") and " ROCKS " in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"RocksStateBackendBenchmark.stateBackends-ROCKS": num[-2]})

            if i.startswith("RocksStateBackendBenchmark.stateBackends") and "_INC " in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"RocksStateBackendBenchmark.stateBackends-ROCKS_INC": num[-2]})

            if i.startswith("SerializationFrameworkMiniBenchmarks.serializerAvro"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"SerializationFrameworkMiniBenchmarks.serializerAvro": num[-2]})

            if i.startswith("SerializationFrameworkMiniBenchmarks.serializerKryo"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"SerializationFrameworkMiniBenchmarks.serializerKryo": num[-2]})

            if i.startswith("SerializationFrameworkMiniBenchmarks.serializerPojo"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"SerializationFrameworkMiniBenchmarks.serializerPojo": num[-2]})

            if i.startswith("SerializationFrameworkMiniBenchmarks.serializerRow"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"SerializationFrameworkMiniBenchmarks.serializerRow": num[-2]})

            if i.startswith("SerializationFrameworkMiniBenchmarks.serializerTuple"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"SerializationFrameworkMiniBenchmarks.serializerTuple": num[-2]})

            if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1,100ms" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1,100ms": num[-2]})

            if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "100,1ms" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-100,1ms": num[-2]})

            if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1000,1ms" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,1ms": num[-2]})

            if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1000,100ms" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,100ms": num[-2]})

            if i.startswith("SumLongsBenchmark.benchmarkCount"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"SumLongsBenchmark.benchmarkCount": num[-2]})

            if i.startswith("WindowBenchmarks.globalWindow"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"WindowBenchmarks.globalWindow": num[-2]})

            if i.startswith("WindowBenchmarks.sessionWindow"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"WindowBenchmarks.sessionWindow": num[-2]})

            if i.startswith("WindowBenchmarks.slidingWindow"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"WindowBenchmarks.slidingWindow": num[-2]})

            if i.startswith("WindowBenchmarks.tumblingWindow"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"WindowBenchmarks.tumblingWindow": num[-2]})

            if i.startswith("StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("flink").update(
                    {"StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1": num[-2]})

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefCassandra(DefTestLog):
    """default test_case Cassandra analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        lines_a = lines[1:lines.index("[cassandra] [INFO] Test clear docker image:\n")].copy()
        line_nu11 = []
        line_nu12 = []

        for i in lines_a:
            if re.search(r"Op rate", i) != None:
                line_nu11.append(lines_a.index(i))

        for j in lines_a:
            if re.search(r"Latency mean", j) != None:
                line_nu12.append(lines_a.index(j))

        wo = lines_a[int(line_nu11[0])].split()
        r4o = lines_a[int(line_nu11[-1])].split()
        r8o = lines_a[int(line_nu11[-2])].split()
        r16o = lines_a[int(line_nu11[-3])].split()
        r24o = lines_a[int(line_nu11[-4])].split()
        r36o = lines_a[int(line_nu11[-5])].split()

        wl = lines_a[int(line_nu12[0])].split()
        r4l = lines_a[int(line_nu12[-1])].split()
        r8l = lines_a[int(line_nu12[-2])].split()
        r16l = lines_a[int(line_nu12[-3])].split()
        r24l = lines_a[int(line_nu12[-4])].split()
        r36l = lines_a[int(line_nu12[-5])].split()

        data.get("default").get("cassandra").update(
            {"cassandra-stress write test - Op rate(op/s)": wo[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress write test - Latency mean(ms)": wl[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 5 threads - Op rate(op/s)": r4o[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 5 threads - Latency mean(ms)": r4l[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 4 threads - Op rate(op/s)": r8o[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 4 threads - Latency mean(ms)": r8l[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 3 threads - Op rate(op/s)": r16o[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 3 threads - Latency mean(ms)": r16l[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 2 threads - Op rate(op/s)": r24o[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 2 threads - Latency mean(ms)": r24l[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 1 threads - Op rate(op/s)": r36o[3]}
        )
        data.get("default").get("cassandra").update(
            {"cassandra-stress read test - 1 threads - Latency mean(ms)": r36l[3]}
        )

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefWordpress(DefTestLog):
    """default test_case Wordpress analysis"""

    def serialization(self):
        lines = self.test_log
        data = self.data

        lines = lines[lines.index("[wordpress] [INFO] Test official docker image:\n"):
                      lines.index("Official-Wordpress\n")].copy()

        for i in lines:
            i = i.strip()
            if i.startswith("Throughput:"):
                throughput = i.split()
                data.get("default").get("wordpress").update(
                    {"Throughput": throughput[1]})

        with open(self.json_path, "w")as f:
            json.dump(data, f)


class DefTensorflow_serving(DefTestLog):
    """default test_case Tensorflow_serving analysis"""
    def serialization(self):
        lines = self.test_log
        data = self.date

        lines = lines[lines.index("[tensorflow-serving] [INFO] Test docker hub official image first:\n"):
                lines.index("Default-Tensorflow-Serving-Server\n")].copy()

        for i in lines:
            if i.startswith("Time taken for tests"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("tensorflow-serving").update(
                    {"Time taken for tests": num[0]}
                )

            if i.endswith("[ms] (mean)\n"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("tensorflow-serving").update(
                    {"Time per request": num[0]}
                )

            if i.endswith("(mean, across all concurrent requests)\n"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("tensorflow-serving").update(
                    {"Time per request(all)": num[0]}
                )

            if i.startswith("Requests per second"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("tensorflow-serving").update(
                    {"Requests per second": num[0]}
                )

            if i.startswith("Transfer rate"):
                num = re.findall("\d+\.?\d*", i)
                data.get("default").get("tensorflow-serving").update(
                    {"Transfer rate": num[0]}
                )

        with open(self.json_path, "w")as f:
            json.dump(data, f)