#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 添加路由前缀
"""
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

__author__ = '__L1n__w@tch'


@view_config(route_name="show_users")
def show_users(request):
    return Response("Test")


def users_include(config):
    config.add_route("show_users", "/show")


if __name__ == "__main__":
    config = Configurator()
    config.include(users_include, route_prefix="/users")
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("localhost", 23330, app)
    server.serve_forever()
