#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import (getLogger,
                     DEBUG,
                     INFO,
                     WARNING,
                     ERROR,
                     CRITICAL,
                     BASIC_FORMAT,
                     Formatter,
                     StreamHandler,
                     FileHandler, )
from typing import Union



class Log(object):
    """
    Log类
    """



    def __init__(self,
                 name: str = None,
                 level: Union[str, int] = None,
                 formatter: str = None,
                 is_full_format: bool = False):
        """
        Log类初始化

        :parameter name: 进程名
        :type name: <class 'str'>

        :parameter level: 日志等级
        :type level: <class 'str' or class 'int'>

        :parameter formatter: 格式化字符串
        :type formatter: <class 'str'>

        :parameter is_full_format: 是否完全格式化
        :type is_full_format: <class 'bool'>
        """

        super(Log,
              self).__init__()

        if name:
            self.__logger = getLogger(name)
        else:
            self.__logger = getLogger()

        if level == "debug" or level == "Debug" or level == "DEBUG" or level == DEBUG:
            self.__logger.setLevel(DEBUG)
        elif level == "info" or level == "Info" or level == "INFO" or level == INFO:
            self.__logger.setLevel(INFO)
        elif level == "error" or level == "Error" or level == "ERROR" or level == ERROR:
            self.__logger.setLevel(ERROR)
        elif level == "critical" or level == "Critical" or level == "CRITICAL" or level == CRITICAL:
            self.__logger.setLevel(CRITICAL)
        else:
            self.__logger.setLevel(WARNING)

        self.__full_formatter = "%(asctime)s %(levelname)s-%(name)s: %(message)s   %(pathname)s   Line: %(lineno)d   " \
                                "Module: %(module)s   Function: %(funcName)s()   PID: %(process)d   Thread: %(" \
                                "threadName)s   TID: %(thread)d"

        if is_full_format:
            self.__formatter = self.__full_formatter
        else:
            if formatter:
                self.__formatter = formatter
            else:
                self.__formatter = BASIC_FORMAT

        self.__console = False
        self.__file = False
        self.__filename = None
        self.__mode = "a"
        self.__encoding = "utf-8"
        self.__console_handle = None
        self.__file_handle = None



    def get_console_handle(self):
        """
        获取控制台句柄
        """

        self.__console = True



    def get_file_handle(self,
                        filename: str = None,
                        mode: str = None,
                        encoding: str = None):
        """
        获取文件句柄

        :parameter filename: 日志文件名
        :type filename: <class 'str'>

        :parameter mode: 日志文件记录模式
        :type mode: <class 'str'>

        :parameter encoding: 日志文件编码
        :type encoding: <class 'str'>
        """

        self.__file = True

        if filename:
            if len(filename) > 4:
                if filename[-4] == ".":
                    self.__filename = filename
            else:
                self.__filename = filename + ".log"
        else:
            self.__filename = self.__logger.name + ".log"

        if mode:
            self.__mode = mode

        if encoding:
            self.__encoding = encoding



    def add_handle(self):
        """
        添加句柄
        """

        if self.__console:
            self.__console_handle = StreamHandler()
            self.__console_handle.setLevel(self.__logger.level)
            self.__console_handle.setFormatter(Formatter(self.__formatter))
            self.__logger.addHandler(self.__console_handle)

        if self.__file:
            self.__file_handle = FileHandler(self.__filename,
                                             self.__mode,
                                             self.__encoding)
            self.__file_handle.setLevel(self.__logger.level)
            self.__file_handle.setFormatter(Formatter(self.__full_formatter))
            self.__logger.addHandler(self.__file_handle)



    def print_log(self,
                  string: str):
        """
        输出日志信息

        :parameter string: 日志信息字符串
        :type string: <class 'str'>
        """

        self.__logger.log(self.__logger.level,
                          string)



    def print_traceback_error(self,
                              string: str):
        """
        输出异常日志信息

        :parameter string: 日志信息字符串
        :type string: <class 'str'>
        """

        self.__logger.exception(string,
                                exc_info=True)
