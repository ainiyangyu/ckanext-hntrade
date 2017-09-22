# coding=utf-8
import logging
import uuid
import pylons

import ckan.plugins as plugins
from pylons import config
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.model as model
from ckan.config.routing import SubMapper
from ckan.common import request, c

from ckanext.hntrade.lib import helpers
import ckanext.hntrade.logic.auth.get as auth_get
import ckanext.hntrade.logic.action.get as action_get
import ckanext.hntrade.logic.action.create as action_create
import ckanext.hntrade.logic.action.update as action_update


log = logging.getLogger('ckanext.hntrade')
COUNT = []


class HntradePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    # plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthenticator)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'hntrade')

    # IActions
    def get_actions(self):
        # 注释掉的部分是控制数据文件查看权限，暂不用加
        # return {'resource_view_list': action_get.restricted_resource_view_list,
        #         'package_show': action_get.restricted_package_show,
        #         'resource_search': action_get.restricted_resource_search,
        #         'package_search': action_get.restricted_package_search,
        #         'data_dict_create': action_create.data_dict_create
        #         }
        return {'data_dict_create': action_create.data_dict_create,
                'data_dict_show': action_get.data_dict_show,
                'data_dict_update': action_update.data_dict_update
                }

    # IAuthFunctions
    # 注释掉的部分是控制数据文件查看权限，暂不用加
    # def get_auth_functions(self):
    #     return {'resource_show': auth_get.restricted_resource_show,
    #             'resource_view_show': auth_get.restricted_resource_show
    #             }

    # ITemplateHelpers
    def get_helpers(self):
        from inspect import getmembers, isfunction

        helper_dict = {}

        functions_list = [o for o in getmembers(helpers, isfunction)]
        for name, fn in functions_list:
            if not name.startswith('_'):
                helper_dict[name] = fn

        return helper_dict

    def login(self):
        """give up the login function"""
        pass

    def _verify_loggin(self):
        """verify a user whether logged in cas server, if a new user and create him."""
        r_params = toolkit.request.params

        if 'ext_login' in r_params:
            c.get_request = True
            if r_params['ext_login'] == '-1':
                self._delete_session_item()
            else:
                user = get_user(r_params['ext_login'])
                if not user:
                    user = toolkit.get_action('user_create')(
                        context={'ignore_auth': True,
                                 'model': model,
                                 'session': model.Session},
                        data_dict={'name': r_params['ext_login'],
                                   'email': generate_email(user),
                                   'password': generate_password()}
                    )

                # store the pylons session
                pylons.session['ckanext-hntrade-user'] = user['name']
                pylons.session.save()

    def identify(self):
        """
        Identify which user is logged in via CASProxy,
        if a user is found, set toolkit.c.user to be their user name.
        """
        self._verify_loggin()
        user = pylons.session.get('ckanext-hntrade-user')
        if user:
            c.user = user

    def _delete_session_item(self):
        if 'ckanext-hntrade-user' in pylons.session:
            del pylons.session['ckanext-hntrade-user']
        pylons.session.save()

    def logout(self):
        logout_url = config.get('ckanext.hntrade.logout_url', '')
        self._delete_session_item()
        h.redirect_to(logout_url)

    def abort(self, status_code, detail, headers, comment):
        self._delete_session_item()
        return status_code, detail, headers, comment

    # IRoutes
    def before_map(self, map):

        GET = dict(method=['GET'])
        PUT = dict(method=['PUT'])
        POST = dict(method=['POST'])
        DELETE = dict(method=['DELETE'])
        GET_POST = dict(method=['GET', 'POST'])

        home_controller = 'ckanext.hntrade.controllers.home:HomeController'
        with SubMapper(map, controller=home_controller) as m:
            m.connect('home', '/', action='index')

        cas_login_controller = 'ckanext.hntrade.controllers.casproxy:CasproxyController'
        with SubMapper(map, controller=cas_login_controller) as m:
            m.connect('cas_login', '/cas_login', action='cas_login')

        data_dict_controller = 'ckanext.hntrade.controllers.data_dict:DataDictController'
        with SubMapper(map, controller=data_dict_controller) as m:
            m.connect('add_data_dict', '/dataset/{pkg_id}/resource/{res_id}/add_data_dict', action='add')
            m.connect('edit_data_dict', '/dataset/{pkg_id}/resource/{res_id}/edit_data_dict', action='edit')
            m.connect('delete_data_dict', '/dataset/{pkg_id}/resource/{res_id}/delete_data_dict', action='delete')

        return map


def get_user(user_name):
    """
    Return the ckan user with given user_name
    :param user_name: user name from CAS proxy
    :return: a ckan user dict
    """
    import ckan.model
    user = ckan.model.User.get(user_name)

    if user:
        user_dict = toolkit.get_action('user_show')(data_dict={'id': user.id})
        return user_dict
    else:
        return None


def generate_email(user_name):
    """
    generate a fake user email
    :param user_name: user name
    :return: a fake email
    """
    return str('{0}@fake.com'.format(user_name))


def generate_password():
    return str(uuid.uuid4())


def _get_logic_functions(module_root, logic_functions={}):

    for module_name in ['get', 'create', 'update', 'patch', 'delete']:
        module_path = '%s.%s' % (module_root, module_name,)

        module = __import__(module_path)

        for part in module_path.split('.')[1:]:
            module = getattr(module, part)

        for key, value in module.__dict__.items():
            if not key.startswith('_') and (hasattr(value, '__call__')
                                            and (value.__module__ == module_path)):
                logic_functions[key] = value

    return logic_functions
