# coding=utf-8
import ckan.model as model
import ckan.logic as logic
import ckan.lib.maintain as maintain
import ckan.lib.search as search
import ckan.lib.base as base
from ckan.controllers.home import HomeController as CoreHomeController
from ckan.common import request, response, c, _, g


render = base.render


class HomeController(CoreHomeController):
    def index(self):
        try:
            # package search
            context = {'model': model, 'session': model.Session,
                       'user': c.user or c.author, 'auth_user_obj': c.userobj}
            data_dict = {
                'q': '*:*',
                'facet.field': g.facets,
                'rows': 4,
                'start': 0,
                'sort': 'metadata_modified desc',
                'fq': 'capacity:"public"'
            }
            query = logic.get_action('package_search')(
                context, data_dict)
            c.search_facets = query['search_facets']
            c.package_count = query['count']
            c.newest_datasets = query['results']
            c.facets = query['facets']
            maintain.deprecate_context_item(
                'facets',
                'Use `c.search_facets` instead.')

            c.search_facets = query['search_facets']

            c.facet_titles = {
                'organization': _('Organizations'),
                'groups': _('Groups'),
                'tags': _('Tags'),
                'res_format': _('Formats'),
                'license': _('Licenses'),
            }

            # hot package search
            hottest_dict = {
                'q': '*:*',
                'facet.field': g.facets,
                'rows': 4,
                'start': 0,
                'sort': 'views_recent desc',
                'fq': 'capacity:"public"'
            }
            hottest_query = logic.get_action('package_search')(
                context, hottest_dict)
            c.hottest_datasets = hottest_query['results']

        except search.SearchError:
            c.package_count = 0

        return render('home/index.html', cache_force=True)

