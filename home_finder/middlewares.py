# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from random import choice

from scrapy import signals
from scrapy.exceptions import NotConfigured


class RotateUserAgentMiddleware(object):
    """Rotate user-agent for each request."""
    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_LIST', [])

        if not user_agents:
            raise NotConfigured("USER_AGENT_LIST not set or empty")

        middleware_klass = cls(user_agents)
        crawler.signals.connect(middleware_klass.spider_opened, signal=signals.spider_opened)

        return middleware_klass

    def spider_opened(self, spider):
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        if not self.enabled or not self.user_agents:
            return

        request.headers['user-agent'] = choice(self.user_agents)

