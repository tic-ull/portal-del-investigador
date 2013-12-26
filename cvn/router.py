class cvnRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads always go to default.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to default.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the default/portalinvestigador pool.
        """
        db_list = ('default', 'portalinvestigador')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True
