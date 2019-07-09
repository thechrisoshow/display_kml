from google.appengine.ext import ndb

class Settings(ndb.Model):
    """
    Get sensitive data setting from DataStore.

    key:String -> value:String
    key:String -> Exception

    Thanks to: Martin Omander @ Stackoverflow
    https://stackoverflow.com/a/35261091/1463812
    """
    name = ndb.StringProperty()
    value = ndb.StringProperty()

    @staticmethod
    def get(name):
        retval = Settings.query(Settings.name == name).get()
        if not retval:
            raise Exception(('Setting %s not found in the database. A placeholder ' +
                             'record has been created. Go to the Developers Console for your app ' +
                             'in App Engine, look up the Settings record with name=%s and enter ' +
                             'its value in that record\'s value field.') % (name, name))
        return retval.value

    @staticmethod
    def set(name, value):
        exists = Settings.query(Settings.name == name).get()
        if not exists:
            s = Settings(name=name, value=value)
            s.put()
        else:
            exists.value = value
            exists.put()

        return True
