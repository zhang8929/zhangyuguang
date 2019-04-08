#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from models import db
import logging
from logging.handlers import RotatingFileHandler
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import redis
from views_news import news_blueprint
from views_user import user_blueprint
from views_admin import admin_blueprint
from s_content import content_blueprint
from context_similar import context_blueprint
from view_unit import unit_blueprint
from view_unit_user import unit_user_blueprint

def create(config):
    app=Flask(__name__)
    #加载配置
    app.config.from_object(config)
    #初始化数据库连接

    '''conda env create -f /Users/zhangyuguang/Downloads/Installations/virtual_platform_mac.yml '''
    db.init_app(app)

    #CSRF保护
    CSRFProtect(app)
    #采用redis保存session
    Session(app)

    #添加日志
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(config.BASE_DIR + "/logs/center.log", maxBytes=1024 * 1024 * 100,backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
    app.logger_xjzx = logging

    #添加redis对象
    app.redis_cli=redis.StrictRedis(config.REDIS_HOST,config.REDIS_PORT,config.REDIS_DB)

    #注册蓝图
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(content_blueprint)
    app.register_blueprint(context_blueprint)
    app.register_blueprint(unit_blueprint)
    app.register_blueprint(unit_user_blueprint)




    return app