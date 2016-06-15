#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 另一种自动重定向的方式
"""
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config, notfound_view_config
from pyramid.request import Response
from pyramid.config import Configurator
from wsgiref.simple_server import make_server

__author__ = '__L1n__w@tch'


@notfound_view_config(append_slash=True)
def not_found(request):
    return HTTPNotFound("什么都没有找到")


@view_config(route_name="no_slash")
def no_slash(request):
    return Response("No slash")


@view_config(route_name="has_slash")
def has_slash(request):
    return Response("Has slash")


if __name__ == "__main__":
    config = Configurator()
    config.add_route("no_slash", "no_slash")
    config.add_route("has_slash", "has_slash/")
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("localhost", 23330, app)
    server.serve_forever()
