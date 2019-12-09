#!python


class Node(object):

    def __init__(self, data):
        """Initialize this node with the given data."""
        self.data = data
        self.next = None

    def __repr__(self):
        """Return a string representation of this node."""
        return 'Node({!r})'.format(self.data)


class LinkedList(object):

    def __init__(self, items=None, extra_optimizations = False):
        """Initialize this linked list and append the given items, if any."""
        self.head = None  # First node
        self.tail = None  # Last node
        self.node_counter = 0 if extra_optimizations else None # Length of LinkedList

        # Append given items
        if items is not None:
            for item in items:
                self.append(item)

    def __str__(self):
        """Return a formatted string representation of this linked list."""
        items = ['({!r})'.format(item) for item in self.items()]
        return '[{}]'.format(' -> '.join(items))

    def __repr__(self):
        """Return a string representation of this linked list."""
        return 'LinkedList({!r})'.format(self.items())

    def items(self):
        """Return a list (dynamic array) of all items in this linked list.
        Best and worst case running time: O(n) for n items in the list (length)
        because we always need to loop through all n nodes to get each item."""
        items = []  # O(1) time to create empty list
        # Start at head node
        node = self.head  # O(1) time to assign new variable
        # Loop until node is None, which is one node too far past tail
        while node is not None:  # O(N) Always n iterations because no early return
            items.append(node.data)  # O(1) time (on average) to append to list
            # Skip to next node to advance forward in linked list
            node = node.next  # O(1) time to reassign variable
        # Now list contains items from all nodes
        return items  # O(1) time to return list

    def is_empty(self):
        """Return a boolean indicating whether this linked list is empty.
        Running time: O(1)"""
        return self.head is None # We could've also done "return self.node_counter == 0"

    def length(self):
        """Return the length of this linked list by traversing its nodes.
        Running time: O(N) if we have do not use a node_counter variable, O(1) otherwise"""
        # TODO: Loop through all nodes and count one for each
        if self.head is None:
            return 0
        elif self.node_counter is not None:
            self.node_counter
        else:
            counter = 1
            curr = self.head
            while curr.next is not None:
                counter += 1
                curr = curr.next
            return counter

    def append(self, item):
        """Insert the given item at the tail of this linked list.
        Running time: O(1) Because we're not iterating through all items"""
        newNode = Node(item)
        if self.tail is not None:
            self.tail.next = newNode
            self.tail = newNode
        else:
            self.head = newNode
            self.tail = newNode
        if self.node_counter is not None:
            self.node_counter += 1


    def prepend(self, item):
        """Insert the given item at the head of this linked list.
        Running time: O(1) Because we're not iterating through all items"""
        newNode = Node(item)
        if self.head is not None:
            newNode.next = self.head
            self.head = newNode
        else:
            self.head = newNode
            self.tail = newNode
        if self.node_counter is not None:
            self.node_counter += 1

    def find(self, quality):
        """Return an item from this linked list satisfying the given quality.
        Best case running time: O(1) If the item is at the head or tail of the LinkedList
        Worst case running time: O(N) If the item is not the head or tail of the LinkedList"""
        if self.head is None:
            return None
        if quality(self.head.data):
            return self.head.data
        if quality(self.tail.data):
            return self.tail.data
        curr = self.head.next
        data = None
        while curr is not None and curr is not self.tail:
            if (quality(curr.data)):
                data = curr.data
                break
            curr = curr.next
        return data

    def delete(self, item):
        """Delete the given item from this linked list, or raise ValueError.
        Best case running time: O(1) If the item is at the head
        Worst case running time: O(N) If the item is not the head of the LinkedList"""
        if self.head is None:
                raise ValueError('Item not found: {}'.format(item))
        if self.head.data == item:
            if self.head is self.tail:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
        else:
            previous = self.head
            curr = self.head.next
            while curr is not None and curr.data != item:
                previous = curr
                curr = curr.next
            if curr is None:
                raise ValueError('Item not found: {}'.format(item))
            else:
                previous.next = curr.next
                if curr is self.tail:
                    self.tail = previous
        if self.node_counter is not None:
            self.node_counter -= 1

def test_linked_list():
    ll = LinkedList()
    print('list: {}'.format(ll))

    print('\nTesting append:')
    for item in ['A', 'B', 'C']:
        print('append({!r})'.format(item))
        ll.append(item)
        print('list: {}'.format(ll))

    print('head: {}'.format(ll.head))
    print('tail: {}'.format(ll.tail))
    print('length: {}'.format(ll.length()))

    # Enable this after implementing delete method
    delete_implemented = False
    if delete_implemented:
        print('\nTesting delete:')
        for item in ['B', 'C', 'A']:
            print('delete({!r})'.format(item))
            ll.delete(item)
            print('list: {}'.format(ll))

        print('head: {}'.format(ll.head))
        print('tail: {}'.format(ll.tail))
        print('length: {}'.format(ll.length()))


if __name__ == '__main__':
    test_linked_list()
