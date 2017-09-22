import logging

from ckan.lib.cli import CkanCommand


class InitDB(CkanCommand):
    """
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def __init__(self, name):
        super(InitDB, self).__init__(name)

    def command(self):
        self._load_config()
        log = logging.getLogger(__name__)

        import ckan.model as model
        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)
        #model.repo.new_revision()
        log.info("Database access initialised")

        import ckanext.hntrade.model.data_dict as d_d_model
        d_d_model.init_tables(model.meta.engine)
        log.debug('data_dict table is setup.')