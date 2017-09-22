# coding=utf-8
import logging

import ckan.lib.dictization as d
import ckan.logic as logic
from ckan import model
from ckan.common import c, request
from ckan.lib.base import BaseController, abort, h, redirect_to, render
from ckan.lib.helpers import flash_success, flash_error
import ckan.lib.navl.dictization_functions as dictization_functions

from ckanext.hntrade.model.data_dict import DataDict

log = logging.getLogger(__name__)

check_access = logic.check_access
get_action = logic.get_action
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
clean_dict = logic.clean_dict
tuplize_dict = logic.tuplize_dict
parse_params = logic.parse_params
_validate = dictization_functions.validate

DataError = dictization_functions.DataError
unflatten = dictization_functions.unflatten


class DataDictController(BaseController):

    def _dictize(self, model_obj, context):
        result_dict = d.table_dictize(model_obj, context)
        del result_dict['id']

        return result_dict

    def add(self, pkg_id, res_id):
        context = {'model': model, 'user': c.user}
        check_access('package_create', context, {'id': pkg_id})

        try:
            c.resource = get_action('resource_show')(context, {'id': res_id})
            c.pkg_dict = get_action('package_show')(context, {'id': pkg_id})
            c.pkg = context['package']
        except NotFound:
            abort(404, u'没有找到该资源')

        # 确保单点的 POST 请求不会导致表单提交
        ignore = ''
        for k in request.params.keys():
            if k == 'ext_login':
                ignore += k

        if request.method == 'POST' and not ignore:
            data_dict = clean_dict(unflatten(
                tuplize_dict(parse_params(request.POST))))
            success = False
            data_dict['pkg_id'] = pkg_id
            data_dict['res_id'] = res_id
            try:
                d_dict = get_action('data_dict_create')(context, data_dict)
                success = True
            except ValidationError, e:
                flash_error(e)

            if success:
                flash_success(u'成功添加字段说明')
                redirect_to(str('/dataset/{0}/resource/{1}'.format(pkg_id, res_id)))

        return render('package/data_dict_new.html')

    def edit(self, pkg_id, res_id):
        context = {'model': model, 'user': c.user}
        check_access('package_update', context, {'id': pkg_id})

        try:
            c.resource = get_action('resource_show')(context, {'id': res_id})
            c.pkg_dict = get_action('package_show')(context, {'id': pkg_id})
            c.pkg = context['package']
            c.res_data_dict = get_action('data_dict_show')(context, {'id': res_id})
        except NotFound:
            abort(404, u'没有找到该资源')

        # 确保单点的 POST 请求不会导致表单提交
        ignore = ''
        for k in request.params.keys():
            if k == 'ext_login':
                ignore += k

        if request.method == 'POST' and not ignore:
            data_dict = clean_dict(unflatten(
                tuplize_dict(parse_params(request.POST))))
            success = False
            data_dict['id'] = res_id
            try:
                d_dict = get_action('data_dict_update')(context, data_dict)
                success = True
            except ValidationError, e:
                flash_error(e)
            except NotFound:
                flash_error(u'没有找到该字段说明')

            if success:
                flash_success(u'成功修改字段说明')
                redirect_to(str('/dataset/{0}/resource/{1}'.format(pkg_id, res_id)))

        return render('package/data_dict_edit.html')

    def delete(self, pkg_id, res_id):
        context = {'model': model, 'user': c.user}
        check_access('package_delete', context, {'id': pkg_id})

        # data = DataDict.get(res_id)
        # data.delete()
        DataDict.delete(res_id)

        flash_success(u'已删除字段说明')
        redirect_to(str('/dataset/{0}/resource/{1}'.format(pkg_id, res_id)))
