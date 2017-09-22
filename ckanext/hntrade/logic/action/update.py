# coding=utf-8
import json
from datetime import datetime
import ckan.logic as logic
import ckan.logic.schema
import ckan.plugins as plugins
import ckan.lib.dictization.model_save as model_save
import ckan.lib.navl.dictization_functions
import ckan.plugins.toolkit as toolkit

from ckanext.hntrade.model.data_dict import DataDict


_check_access = logic.check_access
_get_or_bust = logic.get_or_bust
get_action = logic.get_action
_validate = ckan.lib.navl.dictization_functions.validate
ValidationError = logic.ValidationError
NotFound = logic.NotFound


@toolkit.side_effect_free
def data_dict_update(context, data_dict):
    model = context['model']
    id = _get_or_bust(data_dict, 'id')

    _check_access('package_update', context)

    old_data = get_action('data_dict_show')(context, {'id': id})
    if not old_data:
        raise NotFound

    records = []
    accept = [k for k, v in data_dict.items() if 'field_' in k and v]
    for i in range(len(accept)):
        record = {}
        for k, v in data_dict.items():
            if v and k.endswith(str(i)):
                record[k.split('_')[0]] = v
        records.append(record)

    model.Session.query(DataDict).filter(DataDict.res_id == id).\
        update({'records': json.dumps(records),
                'modified': datetime.now()})
    model.Session.commit()

    return get_action('data_dict_show')(context, data_dict)