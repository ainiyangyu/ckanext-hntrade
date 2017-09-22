# coding=utf-8
import logging
import requests

from pylons import config
import ckan.lib.helpers as h
from ckan.common import request, g
import ckan.plugins.toolkit as toolkit


log = logging.getLogger(__name__)


class CASsettingError(Exception):
    """Exception that's raise if casproxy url didn't setting in .ini file"""
    pass


class CasproxyController(toolkit.BaseController):

    @classmethod
    def get_proxy_url(self):
        """get the CAS proxy url in .ini file"""
        try:
            return config['ckanext.hntrade.casproxy']
        except KeyError:
            message = "Didn't set the CAS url in .ini file"
            raise CASsettingError(message)

    def cas_login(self):
        # r = requests.post(self.get_proxy_url(), params={'request_me': 'true'})
        redirect = '?came_from={0}'.format(request.referer)
        h.redirect_to(self.get_proxy_url() + redirect)

        return
