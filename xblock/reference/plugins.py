## edX-internal prototype services

from djfs import djfs

def public(**kwargs):
    ''' Mark a function as public. 
    '''
    def wrapper(f):
        return f

    return wrapper

class Service(object):
    ''' Top-level definition for an XBlocks service. 
    This is intended as a starting point for discussion, not a finished interface. 

    Possible goals: 

    * Right now, they derive from object. We'd like there to be a common superclass. 
    * We'd like to be able to provide both language-level and service-level bindings. 
    * We'd like them to have a basic knowledge of context (what block they're being 
      called from, access to the runtime, dependencies, etc.
    * That said, we'd like to not over-initialize. Services may have expensive 
      initializations, and a per-block initialization may be prohibitive. 
    * We'd like them to be able to load through Stevedor, and have a plug-in 
      mechanism similar to XBlock. 

    This superclass should go somewhere else. This is an interrim location until we
    figure out where. 
    '''
    def __init__(self, context):
        self._runtime = context['runtime']
        self._xblock = context['xblock']

    def xblock(self):
        return self._xblock

    def runtime(self):
        retrun self._runtime


class FSService(Service):
    def __init__(self, context):
        super().__init__(context)

    @public()
    def load(self, instance, xblock):
        return djfs.get_filesystem(scope_key(instance, xblock))
    
    def __repr__(self):
        return "File system object"
