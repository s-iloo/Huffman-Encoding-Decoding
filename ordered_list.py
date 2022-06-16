class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None
    def __lt__(self, other):
        return self.item < other.item 
    def __eq__(self, other):
        return self.item == other.item

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        dummy = Node(None)
        dummy.next = dummy
        dummy.prev = dummy
        self.head = dummy
    def __eq__(self, other):
        if other == None:
            return False
        return self.python_list().__eq__(other.python_list())

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next == self.head


    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  MUST only use the < operator to compare items'''
        if self.search(item):
            return False
        current = self.head.next
        while current != self.head and current.item < item:
            current = current.next
        n = Node(item)
        n.next = current
        n.prev = current.prev
        current.prev.next = n
        current.prev = n
        return True


    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        if not self.search(item):
            return False
        current = self.head.next
        while current.item != item:
            current = current.next
        current.prev.next = current.next
        current.next.prev = current.prev
        return True


    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        index = 0
        current = self.head.next
        while current != self.head:
            if current.item == item:
                return index
            else:
                current = current.next
                index += 1
        return None


    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if index < 0 or index >= self.size():
            raise IndexError
        current = self.head.next
        i = 0
        while i != index:
            current = current.next
            i += 1
        item = current.item
        current.prev.next = current.next
        current.next.prev = current.prev
        return item


    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.search_helper(item, self.head.next)


    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        orderedList = []
        if self.is_empty():
            return orderedList
        current = self.head.next
        while current != self.head:
            orderedList.append(current.item)
            current = current.next
        return orderedList


    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        revList = []
        return self.python_list_reversed_helper(self.head.prev, revList)


    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.head.next)


    def search_helper(self, item, node):
        '''Takes in item and a node, and returns
           if the item given is in the given node,
           recurseivly calls itself and inputs the item and the node's next node'''
        if self.is_empty() or node == self.head:      # Empty list or reached dummy node
            return False
        elif node.item == item:
            return True
        return self.search_helper(item, node.next)


    def size_helper(self, node):
        '''Takes in a node, returns how many nodes are after it'''
        if node == self.head:
            return 0
        return 1 + self.size_helper(node.next)


    def python_list_reversed_helper(self, current, revList):
        '''Returns a list which contains the data in the OrderedList, tail first to head'''
        if current == self.head:
            return revList
        revList.append(current.item)
        return self.python_list_reversed_helper(current.prev, revList)
