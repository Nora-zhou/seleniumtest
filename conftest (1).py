#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-09-02 22:29
# @Author  : Colorful.Jiang

import pytest
from _pytest import terminal
import time
import os
import platform
import sys, os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))


def getTime():
    string_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    return string_time


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    # print(terminalreporter.stats)
    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    percentage = passed / total

    platform_name = platform.platform()[0:4]
    if platform_name == 'Linu':
        success_env = passed
        fail_env = failed
        total_env = total
        error_env = error
        pass_percent_env = '{:.2%}'.format(percentage)
        env_path = os.getenv('QCI_ENV_FILE', None)
        if env_path:
            with open(env_path, 'a+') as f:  # 注意是追加
                f.write("UI_CASE_TOTAL=%s\n" % total_env)
                f.write("UI_CASE_SUCCESS=%s\n" % success_env)
                f.write("UI_CASE_FAIL=%s\n" % fail_env)
                f.write("UI_CASE_ERROR=%s\n" % error_env)
                f.write("UI_PASS_PERCENTAGE=%s\n" % pass_percent_env)

    # print("total:", terminalreporter._numcollected)
    # print('passed:', len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown']))
    # print('failed:', len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown']))
    # print('error:', len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown']))
    # print('skipped:', len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown']))
    # print('成功率：%.2f' % (len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected * 100) + '%')

    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', duration, 'seconds')


if __name__ == '__main__':
    string_time = getTime()
    pytest.main(["--html=report/report"+string_time+".html"])
    # pytest.main(['--html=report/report.html', 'test_inquiryShop_oa.py'])
