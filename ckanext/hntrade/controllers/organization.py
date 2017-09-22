import logging

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.model as model
import ckan.lib.plugins
from ckan.common import OrderedDict, c, g, request, _, config
from ckan.controllers.organization import OrganizationController as CoreOrganizationController


log = logging.getLogger(__name__)

render = base.render
abort = base.abort

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
get_action = logic.get_action

lookup_group_controller = ckan.lib.plugins.lookup_group_controller


class OrganizationController(CoreOrganizationController):

    def read(self, id, limit=20):
        # check the auth of reading limited group
        limited = config.get('ckanext.hntrade.limited.organization', '')
        limited_organization = limited.split(' ')
        if not c.user and id in limited_organization:
            h.redirect_to(controller='user', action='login',
                          came_from='/organization/{0}'.format(id),
                          from_ckan='true')

        group_type = self._ensure_controller_matches_group_type(
            id.split('@')[0])

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author,
                   'schema': self._db_to_form_schema(group_type=group_type),
                   'for_view': True}
        data_dict = {'id': id}

        # unicode format (decoded from utf8)
        c.q = request.params.get('q', '')

        try:
            # Do not query for the group datasets when dictizing, as they will
            # be ignored and get requested on the controllers anyway
            data_dict['include_datasets'] = False
            c.group_dict = self._action('group_show')(context, data_dict)
            c.group = context['group']
        except NotFound:
            abort(404, _('Group not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read group %s') % id)

        self._read(id, limit, group_type)
        # get current organization
        g.redirect_to_me = request.path
        return render(self._read_template(c.group_dict['type']),
                      extra_vars={'group_type': group_type})