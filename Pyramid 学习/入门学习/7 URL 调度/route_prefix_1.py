#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 添加多个路由前缀
"""
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

__author__ = '__L1n__w@tch'


@view_config(route_name="show_users")
def show_users(request):
    return Response("I am show_users view call")


@view_config(route_name="show_times")
def show_times(request):
    return Response("I am show_times view call")


def timing_include(config):
    config.add_route("show_times", "/times")


def users_include(config):
    config.add_route("show_users", "/show")
    config.include(timing_include, route_prefix="timing")


if __name__ == "__main__":
    config = Configurator()
    config.include(users_include, route_prefix="/users")
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("localhost", 23330, app)
    server.serve_forever()
