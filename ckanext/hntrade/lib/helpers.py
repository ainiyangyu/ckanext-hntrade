# coding=utf-8
import logging
from urllib import urlencode

from ckan.common import c, config, request
import ckan.logic as logic
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.activity_streams as activity_streams

import ckanext.hntrade.model.hn_user as hn_model

log = logging.getLogger(__name__)
get_action = logic.get_action


def restricted_get_user_id():
    return str(c.user)


def get_hn_user():
    user_name = c.user
    hn_user = hn_model.HnUser.get_by_login_name(user_name)
    if hn_user:
        return hn_user.user_id
    else:
        return None


def get_package_name(pkg_id):
    return model.Package.get(pkg_id).name


def check_data_factory(package_id):
    factory_org = config.get('ckanext.hntrade.factory_org', 'datafactory')
    pkg = model.Package.get(package_id)
    org_info = get_action('organization_show')({}, {'id': pkg.owner_org,
                                                    'include_datasets': False})
    if org_info.get('name') == factory_org:
        return True
    else:
        return False


def get_package_activities(pkg_id):
    context = {'model': model, 'session': model.Session,
               'user': c.user or c.author, 'for_view': True,
               'auth_user_obj': c.userobj}
    data_dict = {'id': pkg_id}
    activities = get_action('package_activity_list')(context, data_dict)
    activity_list = []
    for activity in activities:
        activity_type = activity['activity_type']
        if activity_type == 'changed package':
            details = get_action('activity_detail_list')(context=context,
                                                         data_dict={'id': activity['id']})
            if len(details) == 1:
                detail = details[0]
                object_type = detail['object_type']

                new_activity_type = '%s %s' % (detail['activity_type'],
                                               object_type.lower())
                if new_activity_type in activity_streams.activity_stream_string_functions:
                    activity_type = new_activity_type

        activity_msg = activity_streams.activity_stream_string_functions[activity_type](
            context, activity)
        if u'dataset' and u'resource' in activity_msg:
            msg = u'管理员更新了该数据集中的数据文件'
        else:
            msg = u'管理员更新了该数据集的信息'

        activity_list.append({'msg': msg, 'datetime': activity['timestamp']})

    return activity_list


def get_package_views(pkg_id):
    return model.TrackingSummary.get_for_package(pkg_id).get('total')


def get_needed_facet():
    instance = config.get('ckanext.hntrade.instance', '')
    match_facet = {'gov': ['organization', 'groups'], 'comm': ['groups']}
    if not instance:
        log.warning('No specified instance type in config file! Please set it as "gov" or "comm".')
        return None
    return match_facet[instance]


def custom_get_facet_list(original, name):
    # 获取数据分类的选中状态
    state = {}
    for item in original:
        state[item.get('name')] = item.get('active')
    # 只获取有数据集的机构，用于搜索页数据分类的展示
    facet_info = []
    if name == 'groups':
        action_name = 'group_list'
    else:
        action_name = 'organization_list'
    items = get_action(action_name)({}, {'all_fields': True,
                                         'sort': 'package_count'})
    for i in items:
        if i.get('package_count', ''):
            name = i.get('name')
            facet_info.append({'name': name,
                               'display_name': i.get('display_name'),
                               'count': i.get('package_count'),
                               'active': state.get(name)})
    return facet_info


def custom_add_url_param(new_params):
    params_nopage = [(k, v) for k, v in request.params.items() if k not in ['page', 'ext_login']]
    if new_params:
        # 删去已选的机构或群组，机构或群组都只能单选
        match = ['groups', 'organization']
        # 判断 match 与 new_params.keys 是否有交集，有则证明 params 中含有 match 的元素
        if list(set(match) & set(new_params.keys())):
            params = set([p for p in params_nopage if p[0] not in ['organization', 'groups']])
        else:
            params = set(new_params.items())
        params |= set(new_params.items())
    else:
        params = set(params_nopage)
    controller = c.controller
    action = c.action
    url = h.url_for(controller=controller, action=action)
    if not params:
        return url
    params = [(k, v.encode('utf-8') if isinstance(v, basestring) else str(v))
              for k, v in params]
    return url + u'?' + urlencode(params)


def get_data_dict(res_id=None):
    if res_id is None:
        return {}
    try:
        return get_action('data_dict_show')(
            {}, {'id': res_id}
        )
    except (logic.NotFound, logic.ValidationError, logic.NotAuthorized):
        return {}