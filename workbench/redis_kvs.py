import json

import redis

from xblock.runtime import KeyValueStore
from xblock.fields import Scope

class RedisKeyValueStore(KeyValueStore):
    """A `KeyValueStore` for the Workbench to use.

    This is a simple `KeyValueStore` which stores everything in a
    local redis database. It is designed to allow persistence in
    WorkBench, either for development of complex XBlocks, or for 
    """
    def __init__(self):
        super(RedisKeyValueStore, self).__init__()
        print "Using redis!"
        self.db_dict = redis.Redis()
        #self.db_dict.flushdb()

    # Workbench-special methods.

    def clear(self):
        """Clear all data from the store."""
        raise "You probably don't want to do this. If you do, comment out this line"
        self.db_dict.flushdb()

    def as_html(self):
        """Render the key value store to HTML."""
        return "Redis key-value store"
        #html = json.dumps(self.db_dict, sort_keys=True, indent=4)
        #return make_safe_for_html(html)

    # Implementation details.

    def _actual_key(self, key):
        """
        Constructs the full key name from the given `key`.

        The actual key consists of the scope, block scope id, and user_id.

        """
        key_list = []
        if key.scope == Scope.children:
            key_list.append('children')
        elif key.scope == Scope.parent:
            key_list.append('parent')
        else:
            key_list.append(key.scope.block.attr_name)

        if key.block_scope_id is not None:
            key_list.append(key.block_scope_id)
        if key.user_id:
            key_list.append(key.user_id)
        return ".".join(key_list)

    # KeyValueStore methods.

    def get(self, key):
        return json.loads(self.db_dict[self._actual_key(key)])[key.field_name]

    def set(self, key, value):
        """Sets the key to the new value"""
        old_value = self.db_dict.get(self._actual_key(key))
        if not old_value:
            old_value = "{}"
        v = json.loads(old_value)
        v[key.field_name] = value
        self.db_dict[self._actual_key(key)] = json.dumps(v)

    def delete(self, key):
        v = json.loads(self.db_dict[self._actual_key(key)])
        del v[key.field_name]
        db_dict[self._actual_key(key)] = v

    def has(self, key):
        return key.field_name in json.loads(self.db_dict[self._actual_key(key)])

    def set_many(self, update_dict):
        """
        Sets many fields to new values in one call.

        `update_dict`: A dictionary of keys: values.
        This method sets the value of each key to the specified new value.
        """
        for key, value in update_dict.items():
            # We just call `set` directly here, because this is an in-memory representation
            # thus we don't concern ourselves with bulk writes.
            self.set(key, value)
