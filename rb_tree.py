class Node(object):
    def __init__(self, data, left = None, right = None, parent = None, color = 'red'):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color


class rb_tree(object):
    """rb_tree
    Red Black Trees are Node-based binary tree data structures satisfying
    the following the binary tree criteria as well as the following
        - every node is either red or black
        - every leaf counts as black
        - if a node is red, then both of its children are black
        - every simple path from a node to a descendant lead contains the same 
          number of black nodes
        - the root node is always black
    ...

    Attributes
    ----------
    root: Node
        A Node type which will be the root of the RB tree
    sentinel: Node
        A Node type with no data value and color is black. Will be the child
        of any node without children and the parent of the root.

    Methods
    -------
    print_tree():
        Prints the data of all nodes in order.
    __print_tree(curr_node):
        Recursively prints a subtree (in preorder), rooted at curr_node.
    __print_with_colors(curr_node):
        Recursively prints a subtree (in preorder), rooted at curr_node and 
        extracts the color of the node then prints it in the format -dataC- where
        C is the color
    print_with_colors():
        Prints the data of all nodes but with color indicators
    __iter__():
        Iterate over nodes with inorder traversal.
    inorder():
        Iterate over nodes with inorder traversal.
    preorder():
        Iterate over nodes with preorder traversal.
    postorder():
        Iterate over nodes with postorder traversal.
    __traverse(curr_node, traversal_type):
        Helper method for the three traversal iterators.
    find_min():
        Returns node with the min value of a subtree, if tree is empty returns sentinel
    find_node(data):
        Returns the Node object for the given data, returns error if data isn't found or
        if tree is empty.
    __get(data, current_node):
        Helper function which returns the node with the given data starting with 
        the given node, returns None if current_node does not exist.
    find_successor(data):
        Private method which returns the successor of the given data, else reutrns None
    insert(data):
        Adds node with given data to the tree and fixes up the coloring of the nodes.
    bst_insert(data):
        Insertion of BST.
    __put(data, current_node):
        Helper function that finds the approporiate place to add a node in the tree.
    delete(data):
        Find and delete node with given data, then fixes up the coloring of the nodes.
    left_rotate(current_node):
        Rotates at current_node to the left. If the current_node does not have a 
        left child, raise KeyError.
    right_rotate(current_node):
        Rotates at current_node to the right. If the current_node does not have a 
        right child, raise KeyError.
    __rb_insert_fixup(z):
        Maintains the balancing and coloring properity after BST insertion.
    __rb_delete_fixup(x):
        Maintains the balancing and coloring properity after BST deletion.

    """

    PREORDER = 1
    INORDER = 2
    POSTORDER = 3
    # initialize root and size
    def __init__(self):
        self.root = None
        self.sentinel = Node(None, color = 'black')
        self.sentinel.parent = self.sentinel
        self.sentinel.left = self.sentinel
        self.sentinel.right = self.sentinel
    
    def print_tree(self):
        """Prints the data of all nodes in order."""
        self.__print_tree(self.root)
    
    def __print_tree(self, curr_node):
        """Recursively prints a subtree (in preorder), rooted at curr_node
        
        Parameters
        ----------
        curr_node: Node
            Will be the root of printed subtree"""
        if curr_node is not self.sentinel:
            print(str(curr_node.data), end=' ')  # save space
            self.__print_tree(curr_node.left)
            self.__print_tree(curr_node.right)

    def __print_with_colors(self, curr_node):
        """"Recursively prints a subtree (in preorder), rooted at curr_node and 
        extracts the color of the node then prints it in the format -dataC- where
        C is the color
        
        Parameters
        ----------
        curr_node: Node
            Will be the root of printed subtree"""
        if curr_node is not self.sentinel:

            if curr_node.color is "red":
                node_color = "R"
            else:
                node_color = "B"

            print(str(curr_node.data)+node_color, end=' ')  # save space
            self.__print_with_colors(curr_node.left)
            self.__print_with_colors(curr_node.right)

    def print_with_colors(self):
        """Prints the data of all nodes but with color indicators."""
        self.__print_with_colors(self.root)
            
            
    def __iter__(self):
        """Iterates over nodes with inorder traversal."""
        return self.inorder()

    def inorder(self):
        """Iterate over nodes with inorder traversal."""
        return self.__traverse(self.root, rb_tree.INORDER)

    def preorder(self):
        """Iterate over nodes with preorder traversal."""
        return self.__traverse(self.root, rb_tree.PREORDER)

    def postorder(self):
        """Iterate over nodes with postorder traversal."""
        return self.__traverse(self.root, rb_tree.POSTORDER)

    def __traverse(self, curr_node, traversal_type):
        """Helper method for the tree traversal iterators.
        
        Parameters
        ----------
        curr_node: Node
            Node to start traversing at
        traversal_type: int or traversal trypes declared in class
        """
        if curr_node is not self.sentinel:
            if traversal_type == self.PREORDER:
                yield curr_node
            yield from self.__traverse(curr_node.left, traversal_type)
            if traversal_type == self.INORDER:
                yield curr_node
            yield from self.__traverse(curr_node.right, traversal_type)
            if traversal_type == self.POSTORDER:
                yield curr_node

    def find_min(self):
        """Returns node with the min value of a subtree (this is also the node that has no 
        leftChild), if tree is empty returns sentinel."""
        current_node = self.root
        while current_node.left:
            current_node = current_node.left
        return current_node
    
    # find_node expects a data and returns the Node object for the given data
    def find_node(self, data):
        """Returns the node object for the given data
        
        Parameters
        ----------
        data: int
            data value of the node to be found
        
        Raises
        ------
        KeyError
            If node is not in tree or if tree is empty"""
        if self.root:
            res = self.__get(data, self.root)
            if res:
                return res
            else:
                raise KeyError('Error, data not found')
        else:
            raise KeyError('Error, tree has no root')


    def __get(self, data, current_node):
        """Helper function which returns the node with the given data starting with
        the given node, returns None if current_node does not exist.
        
        Parameters
        ----------
        data: int
            data value of the node to get
        current_node: Node
            node which search will begin and go down"""
        if current_node is self.sentinel: # if current_node does not exist return None
            print("couldnt find data: {}".format(data))
            return None
        elif current_node.data == data:
            return current_node
        elif data < current_node.data:
            # recursively call __get with data and current_node's left
            return self.__get( data, current_node.left )
        else: # data is greater than current_node.data
            # recursively call __get with data and current_node's right
            return self.__get( data, current_node.right )
    

    def find_successor(self, data):
        """Private method which returns the successor of the given data
        
        Parameters
        ----------
        data: int
            data value of the node to find the successor of
            
        Raises
        ------
        KeyError
            If tree is empty data is not in tree or if tree is empty"""
        current_node = self.find_node(data)

        if current_node is self.sentinel:
            raise KeyError

        # Travel left down the rightmost subtree
        if current_node.right:
            current_node = current_node.right
            while current_node.left is not self.sentinel:
                current_node = current_node.left
            successor = current_node

        # Travel up until the node is a left child
        else:
            parent = current_node.parent
            while parent is not self.sentinel and current_node is not parent.left:
                current_node = parent
                parent = parent.parent
            successor = parent

        if successor:
            return successor
        else:
            return None

    def insert(self, data):
        """"Adds node with given data to the tree and fixes up the rb properties
        
        Parameters
        ----------
        data: int
            data of the node to insert"""
        # if the tree has a root
        if self.root:
            # use helper method __put to add the new node to the tree
            new_node = self.__put(data, self.root)
            self.__rb_insert_fixup(new_node)
        else: # there is no root
            # make root a Node with values passed to put
            self.root = Node(data, parent = self.sentinel, left = self.sentinel, right = self.sentinel)
            new_node = self.root
            self.__rb_insert_fixup(new_node)
    
    def bst_insert(self, data):
        """Insert of BST
        
        Parameters
        ----------
        data: int
            data of the node to insert"""
        # if the tree has a root
        if self.root:
            # use helper method __put to add the new node to the tree
            self.__put(data, self.root)
        else: # there is no root
            # make root a Node with values passed to put
            self.root = Node(data, parent = self.sentinel, left = self.sentinel, right = self.sentinel)
        
    def __put(self, data, current_node):
        """Helper function that finds the approporiate place to add a node in the tree
        
        Parameter
        ---------
        data: int
            data of the node to find and place
        current_node: Node
            starting point to search down
        """
        if data < current_node.data:
            if current_node.left != self.sentinel:
                new_node = self.__put(data, current_node.left)
            else: # current_node has no child
                new_node = Node(data,
                    parent = current_node,
                    left = self.sentinel,
                    right = self.sentinel )
                current_node.left = new_node
        else: # data is greater than or equal to current_node's data
            if current_node.right != self.sentinel:
                new_node = self.__put(data, current_node.right)
            else: # current_node has no right child
                new_node = Node(data,
                    parent = current_node,
                    left = self.sentinel,
                    right = self.sentinel )
                current_node.right = new_node
        return new_node
    

    
    def delete(self, data):
        """"Find and delete node with given data, then fixes up the coloring of the nodes.
        
        Parameters
        ----------
        data: int
            data of the node to delete
        
        Raises
        ------
        KeyError
            if data isn't in tree or if tree is empty"""
        # Same as binary tree delete, except we call rb_delete fixup at the end.


        # 1. tree is empty or the data is not in the tree -> note: checking if the data is 
        # in the tree does both
        node = self.find_node(data)
        
        # 2. Tree has the data, depending on how many children, how do we delete?

        # case 1: node has no children -> can set its parent's pointer to None
        if (node.right is self.sentinel) and (node.left is self.sentinel):
            if node.parent is self.sentinel:
                self.root = None
            else: 
                if (node.parent.left is not self.sentinel) and (node.parent.left == node):
                    node.parent.left = self.sentinel
                else:
                    node.parent.right = self.sentinel
            self.__rb_delete_fixup(node)
        
        # case 2: node has 1 child -> make the node's parent point to R/L child and vice versa
        
        # case 2.a: node only has a left child
        elif (node.right is self.sentinel) and (node.left is not self.sentinel):

            # if the current node is a left child
            if node.parent.left == node:
                node.parent.left = node.left
                node.left.parent = node.parent

            # if the current node is a right child
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
            node = node.left
            self.__rb_delete_fixup(node)
            
        
        # case 2.b: node only has a right child
        elif (node.right is not self.sentinel and node.left is self.sentinel):

            # if the current node is a left child
            if node.parent.left == node:
                node.parent.left = node.right
                node.right.parent = node.parent
                

            # if the current node is a right child
            else:
                node.parent.right = node.right
                node.right.parent = node.parent
            node = node.right
            self.__rb_delete_fixup(node)
            


        # case 3: node has 2 children
        # -> find successor and promote successor (this element would have at most one child)
        else:
            successor = self.find_successor(data)
            # note that the successor can never be the root and always has a parent as
            # the node has two children thus one of their subtrees must contain 
            # successor meaning successor is always below current node
            
            # case 3a: successor has one child
            # -> we take the successor's child and point it to the successor's parent
            saved_data = successor.data
            self.delete(successor.data)
            node.data = saved_data
        

        
    def left_rotate(self, current_node):
        """Rotates at current_node to the left. If x is the root of the tree to rotate with left 
        child subtree T1 and right child y, where T2 and T3 are the left and right children of y then:
        x becomes left child of y and T3 as its right child of y T1 becomes left child of x and T2 
        becomes right child of x.

        Parameters
        ----------
        current_node: Node
            node which to be rotated at
        
        Raises
        ------
        KeyError
            if current_node has no right child (nothing to rotate with)
        """
        # refer page 328 of CLRS book for rotations

        if self.root is None:
            raise KeyError

        if current_node is not None:
            if current_node.right is self.sentinel:
                raise KeyError
                
            y = current_node.right
            current_node.right = y.left

            if y.left is not self.sentinel:
                y.left.parent = current_node
            
            y.parent = current_node.parent

            if current_node.parent is self.sentinel:
                self.root = y

            elif current_node == current_node.parent.left:
                current_node.parent.left = y
            
            else:
                current_node.parent.right = y

            y.left = current_node
            current_node.parent = y

    
    def right_rotate(self, current_node):
        """Rotates at current_node to the right. If y is the root of the tree to rotate 
        with right child subtree T3 and left child x, where T1 and T2 are the left and
        right children of x then: y becomes right child of x and T1 as its left child of x
        T2 becomes left child of y and T3 becomes right child of y
        
        Parameters
        ----------
        current_node: Node
            node which to rotate at
        
        Raises
        ------
        KeyError
            if current_node does not have a left child so nothing to rotate with"""     
        # refer page 328 of CLRS book for rotations

        # 1. check if RB tree is empty, raise error
        if self.root is None:
            raise KeyError

        # 2. only work with nodes (aka no None)
        if current_node is not None:
            
            # 3. check if node has left to rotate with, else raise error
            if current_node.left is self.sentinel:
                raise KeyError

            # 4. get left of current node
            y = current_node.left

            # 5. update child/parent staus of current and left's right child
            current_node.left = y.right

            if y.right is not self.sentinel:
                y.right.parent = current_node
            
            # 6. update parent status of left
            y.parent = current_node.parent

            if current_node.parent is self.sentinel:
                self.root = y

            # 7. update child/parent status of left
            elif current_node == current_node.parent.left:
                current_node.parent.left = y
            else:
                current_node.parent.right = y
            
            # 8. update child/parent relationship of left and current
            y.right = current_node
            current_node.parent = y
        

    
    def __rb_insert_fixup(self, z):
        """Maintains the balancing and coloring property after bst insertion into the tree
        
        Parameters
        ----------
        z: Node
            node which to start the balancing of the properties of the RB tree"""
        # refer page 330 of CLRS book and lecture slides for rb_insert_fixup

        # only work with double red (assume everything else is good - it is)
        while z.parent.color == "red":
            # note: if parent does have a parent then it is the root which would be black thus not
            # pass previous check

            # CASE 1: parent is a left child
            if z.parent == z.parent.parent.left:
                # 1. get uncle
                y = z.parent.parent.right

                # CASE 1A: uncle is red
                # 2. if red then we can change it to black, parent to black, and their parent to red, then
                # recursively fix on that parent (grandparent)
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent

                # CASE 1B: uncle is black
                else:
                    # 2. if the uncle is black then we can rotate left on the parent if z is the right child
                    # note: this is basically just bringing the parent down as the (left) child of z
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    # 3. change the original node to black and the now parent of that node to red
                    # note: the z node (this was the parent of original node) is red
                    # note: we need to keep the black heigh property in tacked which is why we don't 
                    # change the z node colroing to black
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    # 4. now right rotate on the grandparent of the leaf node (this is the now parent of the original node)
                    # which will bring up that black to be the root of the subtree, the now red grandparent goes down to the 
                    # right (this doesn't change the black height bc we replace the was black node of the grandparent with the 
                    # new node) and bring up the original node with the old parent as its (left) child
                    self.right_rotate(z.parent.parent)
            
            # CASE 2: parent is a right child
            else:
                # 1. get uncle
                y = z.parent.parent.left

                # CASE 2A: uncle is red
                if y.color == "red":
                    # 2. change parent to black, uncle to black, grandparent red, and recursively fix on that parent (grandparent)
                    # by setting z to grandparent
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                
                # CASE 2B: uncle is black
                else:
                    # 2. right rotate on the parent if z is the left child
                    # note: this is basically just bringing down the parent as the (right) child of z
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    # 3. change original node to black, now parent of that node to red (would have been black before to keep properties)
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    # 4. left rotate on the grandparent which brings up the originally inserted node as the black root of the sub tree
                    # (replaces the spot of the grandparent), brings down the red grandparent to the left
                    self.left_rotate(z.parent.parent)

        # !! change the root to black in case we changed the root to red in the loop but bc it doesn't have a parent, need to 
        # !! manually change at the end
        self.root.color = "black"
            

    def __rb_delete_fixup(self, x):
        """Maintains the balancing and coloring property after BST deletion from the tree
        
        Parameters
        ----------
        x: Node
            node where to start the balancing of RB properties"""
        # refer page 338 of CLRS book and lecture slides for rb_delete_fixup

        # don't work with root or if x is red
        while x is not self.root and x.color == "black":

            # CASE 1: x is a left child
            if x == x.parent.left:

                # 1. get the right child
                w = x.parent.right
                
                # CASE 1A: if sibling is red
                if w.color == "red":

                    # 2. recolor sibling to be black
                    w.color = "black"

                    # 3. recolor their parent to be red
                    x.parent.color = "red"

                    # 4. rotate left on the parent
                    self.left_rotate(x.parent)

                    # 5. set the sibling as the right child of the parent of x
                    # note: this is bc if during the rotation, the siblings left child becomes the right child of the 
                    # parent, then we need to set this equal the thing we are checking in case i
                    w = x.parent.right

                # CASE 1B: if sibling is black, left child of sibling is black, and right child of sibling is black
                if w.left.color == "black" and w.right.color == "black":

                    # color sibling red and reassign x as the parent so that we can keep calling on this node
                    w.color = "red"

                    # set parent as the new possible black node (if red then it will be changed to black at the end)
                    x = x.parent
                
                # CASE 1C: if sibling is black and left child is red 
                else:
                    # CASE 1C: if sibling is black with red left child and black right child
                    if w.right.color == "black":
                        w.left.color = "black"
                        w.color = "red"
                        self.right_rotate(w)
                        w = x.parent.right
                    

                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root

            # CASE 2: x is a right child
            else:
                # 1. get the sibling
                w = x.parent.left

                # CASE 2A: sibling is red
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                
                # CASE 2B: sibling is black and only has black children
                if w.right.color == "black" and w.left.color == "black":
                    w.color = "red"
                    x = x.parent
                
                else:
                    # CASE 2C: sibling is black and left child is black
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        self.left_rotate(w)
                        w = x.parent.left

                    # CASE 2D: sibling is left child is red
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "black"


    


    
    