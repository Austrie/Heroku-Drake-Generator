#!python

from linkedlist import LinkedList


class HashTable(object):

    def __init__(self, init_size=8, extra_optimizations = False):
        """Initialize this hash table with the given initial size."""
        # Create a new list (used as fixed-size array) of empty linked lists
        self.buckets = [
            LinkedList(extra_optimizations=extra_optimizations)
            for _ in range(init_size)
        ]

    def __str__(self):
        """Return a formatted string representation of this hash table."""
        items = ['{!r}: {!r}'.format(key, val) for key, val in self.items()]
        return '{' + ', '.join(items) + '}'

    def __repr__(self):
        """Return a string representation of this hash table."""
        return 'HashTable({!r})'.format(self.items())

    def _bucket_index(self, key):
        """Return the bucket index where the given key would be stored."""
        # Calculate the given key's hash code and transform into bucket index
        return hash(key) % len(self.buckets)

    def _get_all(self, keys=False, values=False):
        """Modularize common code for getting keys and/or values"""

        return [] if not keys and not values else [
            (
                key_value_tuple
                if keys and values
                else key_value_tuple[0] if keys else key_value_tuple[1]
            )
            for bucket in self.buckets
            for key_value_tuple in bucket.items()
        ]

    def keys(self):
        """Return a list of all keys in this hash table.
        Running time: O(N) Because we iterate through all items in the HashTable"""
        # Collect all keys in each bucket
        return self._get_all(keys=True)

    def values(self):
        """Return a list of all values in this hash table.
        Running time: O(N) Because we iterate through all items in the HashTable"""
        return self._get_all(values=True)

    def items(self):
        """Return a list of all items (key-value pairs) in this hash table.
        Running time: O(N) Because we iterate through all items in the HashTable"""
        # Collect all pairs of key-value entries in each bucket
        return self._get_all(keys=True, values=True)

    def length(self):
        """Return the number of key-value entries by traversing its buckets.
        Running time: O(N) because we iterate through all items in the HashTable due to the extra_optimizations flag being False, else O(M) because we only need to go through each LinkedList O(1) Length method"""
        counter = 0
        for bucket in self.buckets:
            for node in bucket.items():
                counter += 1
        return counter

    def contains(self, key):
        """Return True if this hash table contains the given key, or False.
        Running time: O(N) Because we iterate through all items in the HashTable"""
        index = self._bucket_index(key)
        bucket = self.buckets[index]

        for pKey, pValue in bucket.items():
            if pKey == key:
                return True
        return False

    def get(self, key):
        """Return the value associated with the given key, or raise KeyError.
        Running time: O(N) Because we iterate through all items in the HashTable"""
        index = self._bucket_index(key)
        bucket = self.buckets[index]

        print "Calling get for " + key
        for pKey, pValue in bucket.items():
            if pKey == key:
                return pValue
            else:
                print "pKey: " + pKey
                print "key: " + key

        raise KeyError('Key not found: {}'.format(key))

    def set(self, key, value):
        """Insert or update the given key with its associated value.
        TODO: Running time: O(1) Because the linkedlist append method is O(1) and we didn't have to go through all the items"""
        # TODO: Find bucket where given key belongs
        # TODO: Check if key-value entry exists in bucket
        # TODO: If found, update value associated with given key
        # TODO: Otherwise, insert given key-value entry into bucket
        try:
            self.delete(key)
        except:
            # print "No previous value"
            pass

        # print "append about to happen"
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        bucket.append((key, value))

    def delete(self, key):
        """Delete the given key from this hash table, or raise KeyError.
        Running time: O(N) Because we iterate through all items in the HashTable"""
        index = self._bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket.items():
            if node[0] == key:
                bucket.delete(node)
                return

        raise KeyError('Key not found: {}'.format(key))


def test_hash_table():
    ht = HashTable()
    print('hash table: {}'.format(ht))

    print('\nTesting set:')
    for key, value in [('I', 1), ('V', 5), ('X', 10)]:
        print('set({!r}, {!r})'.format(key, value))
        ht.set(key, value)
        print('hash table: {}'.format(ht))

    print('\nTesting get:')
    for key in ['I', 'V', 'X']:
        value = ht.get(key)
        print('get({!r}): {!r}'.format(key, value))

    print('contains({!r}): {}'.format('X', ht.contains('X')))
    print('length: {}'.format(ht.length()))

    # Enable this after implementing delete method
    delete_implemented = False
    if delete_implemented:
        print('\nTesting delete:')
        for key in ['I', 'V', 'X']:
            print('delete({!r})'.format(key))
            ht.delete(key)
            print('hash table: {}'.format(ht))

        print('contains(X): {}'.format(ht.contains('X')))
        print('length: {}'.format(ht.length()))


if __name__ == '__main__':
    test_hash_table()
