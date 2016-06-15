#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 添加append_slash=True让request具有自动重定向功能
"""
from wsgiref.simple_server import make_server
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.config import Configurator

__author__ = '__L1n__w@tch'


def not_found(request):
    return HTTPNotFound("什么都没有找到")


def no_slash(request):
    return Response("No slash")


def has_slash(request):
    return Response("Has slash")


def main(g, **settings):
    config = Configurator()
    config.add_route("no_slash", "no_slash")
    config.add_route("has_slash", "has_slash/")

    config.add_view(no_slash, route_name="no_slash")
    config.add_view(has_slash, route_name="has_slash")

    config.add_notfound_view(not_found, append_slash=True)

    app = config.make_wsgi_app()
    server = make_server("localhost", 23330, app)
    server.serve_forever()


if __name__ == "__main__":
    main("??")
