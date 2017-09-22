# coding=utf-8
import json
import ckan.logic as logic
import ckan.lib.navl.dictization_functions
import ckan.plugins.toolkit as toolkit
import ckan.model.types as _types

from ckanext.hntrade.model.data_dict import DataDict


_check_access = logic.check_access
get_action = logic.get_action
_validate = ckan.lib.navl.dictization_functions.validate
ValidationError = logic.ValidationError
NotFound = logic.NotFound


@toolkit.side_effect_free
def data_dict_create(context, data_dict):
    model = context['model']

    _check_access('package_create', context)
    result = []
    records = []

    accept = [k for k, v in data_dict.items() if 'field_' in k and v]
    for i in range(len(accept)):
        record = {}
        for k, v in data_dict.items():
            if v and k.endswith(str(i)):
                record[k.split('_')[0]] = v
        records.append(record)

    add = DataDict(
        id=_types.make_uuid(),
        res_id=data_dict.get('res_id'),
        pkg_id=data_dict.get('pkg_id'),
        records=json.dumps(records)
    )
    model.Session.add(add)
    model.Session.commit()

    result.append(add)
    return result
