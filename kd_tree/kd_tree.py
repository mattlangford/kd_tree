import numpy as np
class Node():
    def __init__(self,point):
        self.point = np.array(point)
        self.lesser = None
        self.greater = None
        self.d = len(point)

    def __repr__(self):
        return str(self.point)

    def dist_to_point(self, point):
        point = np.array(point)
        return np.linalg.norm(self.point-point)

    def search(self, point, axis):
        axis += 1
        if axis == self.d: axis = 0

        #print axis,self,"LESSER:",self.lesser,"GREATER:",self.greater
        if point[axis] < self.point[axis]:
            #print " Lesser"
            if self.lesser is None:
                return [self.dist_to_point(point),self]
            else:
                closest = self.lesser.search(point,axis)
                #print self,closest, "-"
                # If this node is closer then the closest then return it as the new closest.
                node_dist = self.dist_to_point(point)
                if node_dist < closest[0]:
                    return [node_dist,self]

                # Is hyperplane in the hypersphere
                if abs(self.point[axis] - point[axis]) < closest[0]:
                    if self.greater is None: return closest
                    other_closest = self.greater.search(point,axis)
                    if other_closest[0] < closest[0]:
                        return other_closest
                    else:
                        return closest
        elif point[axis] >= self.point[axis]:
            #print " Greater or Equal"
            if self.greater is None:
                return [self.dist_to_point(point),self]
            else:
                closest = self.greater.search(point,axis)
                #print self,closest, "+"
                # If this node is closer then the closest then return it as the new closest.
                node_dist = self.dist_to_point(point)
                if node_dist < closest[0]:
                    return [node_dist,self]

                # Is hyperplane in the hypersphere
                if abs(self.point[axis] - point[axis]) < closest[0]:
                    if self.lesser is None: return closest
                    other_closest = self.lesser.search(point,axis)
                    if other_closest[0] < closest[0]:
                        return other_closest
                    else:
                        return closest
        return closest

    def insert(self, new_node, axis):
        axis += 1
        if axis == self.d: axis = 0

        if new_node.point[axis] < self.point[axis]:
            if self.lesser is None:
                self.lesser = new_node
            else:
                self.lesser.insert(new_node,axis)

        elif new_node.point[axis] >= self.point[axis]:
            if self.greater is None:
                self.greater = new_node
            else:
                self.greater.insert(new_node,axis)
        return
        
class KDTree():
    def __init__(self, duplicate_tolerance = 1):
        # Init with the number of dimensions
        self.base_node = None
        self.points = []

        # When checking for duplicates, use this as the tolerance when identifying the same point
        self.duplicate_tolerance = duplicate_tolerance

    def insert(self,point):
        n = Node(point)

        # If this is the first node we are trying to insert make it the base.
        if self.base_node is None:
            self.points.append(point) 
            self.base_node = n
            return
        
        self.points.append(point)
        self.base_node.insert(n,-1)

    def insert_unique(self,point):
        n = Node(point)

        # If this is the first node we are trying to insert make it the base.
        if self.base_node is None: 
            self.points.append(point)
            self.base_node = n
            return

        if self.base_node.search(np.array(point),-1)[0] >= self.duplicate_tolerance:
            self.points.append(point)
            self.base_node.insert(n,-1)

    def search(self, point):
        if self.base_node is None: 
            print "Empty Tree!"
            return

        return self.base_node.search(np.array(point),-1)