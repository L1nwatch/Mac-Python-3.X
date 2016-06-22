#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Pyramid 中有关遍历的相关学习
"""
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

__author__ = '__L1n__w@tch'


class Resource(dict):
    pass


def get_root(request):
    return Resource({"a": Resource({"b": Resource({"C": Resource()})})})


def hello_world_of_resources(context, request):
    output = "Here's a resource and its children: {}".format(context)
    return Response(output)


if __name__ == "__main__":
    config = Configurator(root_factory=get_root)
    config.add_view(hello_world_of_resources, context=Resource)
    app = config.make_wsgi_app()
    server = make_server("127.0.0.1", 23330, app)
    server.serve_forever()
