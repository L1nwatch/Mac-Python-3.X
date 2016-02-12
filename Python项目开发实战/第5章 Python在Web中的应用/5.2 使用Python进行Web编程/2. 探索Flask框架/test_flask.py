#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 创建核心Flask文件

如果你还没有创建模版,你仍然看不到任何东西.模版是浏览器实际展示给用户的东西.模版可以向Python中间件传送数据
'''
__author__ = '__L1n__w@tch'

import sqlite3, os, lendydata
# 只导入实际使用的模块和库
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash  # 创建了一个Flask对象,并将其命名为app

# Python脚本的运行情况依赖于它的执行方式.它可以作为__main__模块通过python app.py直接执行
# 也可以在另一个(主)Python文件中被导入而间接执行.Python解释器将__name__变量设置为__main__或被导入的文件名
# 在此将__name__变量传给Flask和config.from_object方法.

app = Flask(__name__)


def get_db():
    """
    Opens a new database connection if one does not exist for our current request
    context (the g object helps with this task)

    在get_db()方法调用中还有一点Flask特性.这个函数在没有连接存在时会打开一个新的连接,而g变量在Flask中是一个特殊对象,
    它只对激活请求有效.这在不同的请求对象间保持了数据的一致性.
    :return:
    """
    if not hasattr(g, "sqlite_db"):
        lendydata.init_db()
        g.sqlite_db = lendydata.db

        return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request. Note the 'g' object which makes sure
    we only operate on the current request.

    g对象保持每个请求分开.这样在关闭一个数据库连接时,并不会关闭所有数据库连接.
    :param error:
    :return:
    """
    if hasattr(g, "sqlite_db"):
        lendydata.close_db()


# Flask使用了修饰符方法来创建HTTP路由.当有人访问/login路径或根目录(/)时,login函数就会被调用,并处理请求方法的只
@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("show_inventory"))
    # 通过render_template()方法将用户带入login.html模版.从本质上说,希望用户访问网站的登录页面
    return render_template("login.html", error=error)


# 注意,这个端点在route()方法中并没有methods=参数,这是因为默认的方法是GET,所以不需要传递这个参数
@app.route("/inventory")
def show_inventory():
    get_db()
    all_items = lendydata.get_items()
    # 创建了一个在网站中使用的字段名和值的字典,将这个字典传入模版中并填充内容.
    inventory = [dict(zip(["name", "description"], [item[1], item[2]])) for item in all_items]
    return render_template("items.html", items=inventory)


@app.route("/add", methods=["POST"])
def add_item():
    if not session.get("logged_in"):
        abort(401)
    get_db()
    owner_id = [row[0] for row in lendydata.get_members() if row[1] == request.form["owner"]]
    try:
        owner_id = owner_id[0]
    except IndexError:
        # implies no owners match name
        # should raise error/create new member
        owner_id = 1  # use default member for now

    lendydata.insert_item(request.form["name"], request.form["description"], owner_id, request.form["price"],
                          request.form["condition"])
    flash("New entry was successfully posted")
    return redirect(url_for("show_inventory"))


def main():
    global app

    # 设置了Flask的配置属性.由于所有东西在Python中都是一个first-class对象,因此应该在需要时修改这个对象
    # Load default config and override config from an environment variable
    app.config.update(dict(
            DATABASE=os.path.join(app.root_path, "lendy.db"),  # DATABSE变量声明了数据库文件的位置
            DEBUG=True,  # 处于开发模式下设置为True,当准备好将Flask项目放到生产环境时,设置为False
            SECRET_KEY="heheda",  # 这个key有助于你保证客户端会话的安全
            USERNAME="admin",  # 这些是应用的证书,由于是示例代码故放在配置中而不是数据库中
            PASSWORD="admin"  # 正式情况下应该被加密后放进数据库
    ))
    # 设置了一个名为LENDY_SETTINGS的环境变量,其中包含了配置变量.然而,你已经在代码中设置了,所以这个配置文件其实并不存在
    # 设置silent=True,则它会忽略配置文件不存在时产生的错误.如果想要增加一个配置文件,则需要将LENDY_SETTINGS变量指向那个配置文件
    app.config.from_envvar("LENDY_SETTINGS", silent=True)

    app.run()


if __name__ == "__main__":
    # 当这个脚本作为第一个Python脚本执行时,这个__name__属性被设置为__main__.这样解释器就知道这是第一个脚本.
    # 任何在__main__(通过导入语句)之后调用的脚本都会把它们的__name__变量设置为它们的文件名
    main()
