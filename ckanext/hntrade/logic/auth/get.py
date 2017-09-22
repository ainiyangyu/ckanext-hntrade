# coding=utf-8
import json
from logging import getLogger

import ckan.plugins.toolkit as toolkit
import ckan.authz as authz
import ckan.logic.auth as logic_auth
import ckan.logic as logic


log = getLogger(__name__)
_get_or_bust = logic.get_or_bust
get_action = logic.get_action

NotFound = logic.NotFound


def _restricted_check_user_resource_access(user, resource_dict, package_dict):
    restricted_level = 'public'
    allowed_users = []

    # check in resource_dict
    if resource_dict:
        extras = resource_dict.get('extras', {})
        restricted = resource_dict.get('restricted',
                                       extras.get('restricted', {}))
        if not isinstance(restricted, dict):
            try:
                restricted = json.loads(restricted)
            except BaseException:
                log.info(
                    'Error loading restricted value: "{0}"'.format(restricted))
                restricted = {}

        if restricted:
            restricted_level = restricted.get('level', 'public')
            allowed_users = restricted.get('allowed_users', '').split(',')

    # Public resources (DEFAULT)
    if not restricted_level or restricted_level == 'public':
        return {'success': True}

    # Registered user
    if not user:
        return {
            'success': False,
            'msg': 'Resource access restricted to registered users'}
    else:
        if restricted_level == 'registered' or not restricted_level:
            return {'success': True}

    # Since we have a user, check if it is in the allowed list
    if user in allowed_users:
        return {'success': True}
    elif restricted_level == 'only_allowed_users':
        return {
            'success': False,
            'msg': 'Resource access restricted to allowed users only'}

    # Get organization list
    user_organization_dict = {}

    context = {'user': user}
    data_dict = {'permission': 'read'}

    for org in logic.get_action(
            'organization_list_for_user')(context, data_dict):
        name = org.get('name', '')
        id = org.get('id', '')
        if name and id:
            user_organization_dict[id] = name

    # Any Organization Members (Trusted Users)
    if not user_organization_dict:
        return {
            'success': False,
            'msg': 'Resource access restricted to members of an organization'}
    if restricted_level == 'any_organization':
        return {'success': True}

    pkg_organization_id = package_dict.get('owner_org', '')

    # Same Organization Members
    if restricted_level == 'same_organization':
        if pkg_organization_id in user_organization_dict.keys():
            return {'success': True}

    return {
        'success': False,
        'msg': 'Resource access restricted to same organization (' + pkg_organization_id + ') members'}


@toolkit.auth_allow_anonymous_access
def restricted_resource_show(context, data_dict=None):

    # Ensure user who can edit the package can see the resource
    resource = data_dict.get('resource', context.get('resource', {}))
    if not resource:
        resource = logic_auth.get_resource_object(context, data_dict)
    if not isinstance(resource, dict):
        resource = resource.as_dict()

    if authz.is_authorized(
            'package_update', context, {
            'id': resource.get('package_id')}).get('success'):
        return {'success': True}

    # custom restricted check
    auth_user_obj = context.get('auth_user_obj', None)
    user_name = ""
    if auth_user_obj:
        user_name = auth_user_obj.as_dict().get('name', '')
    else:
        if authz.get_user_id_for_username(
                context.get('user'), allow_none=True):
            user_name = context.get('user', '')
    #log.debug("restricted_resource_show: USER:" + user_name)

    package = data_dict.get('package', {})
    if not package:
        model = context['model']
        package = model.Package.get(resource.get('package_id'))
        package = package.as_dict()

    return _restricted_check_user_resource_access(
        user_name, resource, package)
