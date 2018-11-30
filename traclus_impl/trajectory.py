'''
Created on Dec 31, 2015

@author: Alex
'''
from distance_functions import get_total_distance_function
from generic_dbscan import Cluster, ClusterCandidate, ClusterFactory, ClusterCandidateIndex

class Trajectory():
    def __init__(self, pts, id):
        self.pts = pts
        self.p_pts = []
        self.tid = id

    def __repr__(self):
        return str(self.pts)

    def as_dict(self):
        return {
            'id': self.tid,
            'trajectories': [pt.as_dict() for pt in self.pts],
            'p_trajectories': [pt.as_dict() for pt in self.p_pts]
        }

class TrajectoryLineSegmentFactory():
    def __init__(self):
        self.next_sid = 0
        
    def create(self, segment, tid):
        if (segment == None) or (tid == None) or (tid < 0):
            raise Exception("invalid arguments")
        curr_sid = self.next_sid
        self.next_sid += 1
        return TrajectoryLineSegment(segment, tid, curr_sid)

class TrajectoryLineSegment(ClusterCandidate):
    def __init__(self, segment, tid, id=None):
        ClusterCandidate.__init__(self)
        if (segment == None) or (tid < 0):
            raise Exception("invalid arguments")

        self.segment = segment
        self.rsegment = None
        self.tid = tid
        self.id = id
        self.num_neighbors = -1

    def as_dict(self):
        return {
            'start': self.segment.start.as_dict(),
            'end': self.segment.end.as_dict(),
            'trajectory_id': self.tid
        }
        
    def get_num_neighbors(self):
        if self.num_neighbors == -1:
            raise Exception("haven't counted num neighbors yet")
        return self.num_neighbors
    
    def set_num_neighbors(self, num_neighbors):
        if (self.num_neighbors != -1) and (self.num_neighbors != num_neighbors):
            raise Exception("neighbors count should never be changing")
        self.num_neighbors = num_neighbors
        
    def distance_to_candidate(self, other_candidate):
        if (other_candidate == None) or (other_candidate.segment == None) or (self.segment == None):
            raise Exception("invalid arguments")
        return get_total_distance_function(self.segment, other_candidate.segment)
            
class TrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
    def __init__(self, candidates, epsilon):
        ClusterCandidateIndex.__init__(self, candidates, epsilon)
        
    def find_neighbors_of(self, cluster_candidate):
        neighbors = ClusterCandidateIndex.find_neighbors_of(self, cluster_candidate)
        cluster_candidate.set_num_neighbors(len(neighbors))
        return neighbors

class RtreeTrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
    def __init__(self, candidates, epsilon):
        ClusterCandidateIndex.__init__(self, candidates, epsilon)
        self.candidates_by_ids = [None] * len(candidates)
        self.idx = index.Index()
        for cluster_candidate in candidates:
            if self.candidates_by_ids[cluster_candidate.id] != None:
                raise Exception("should have all unique ids")
            
            self.candidates_by_ids[cluster_candidate.id] = cluster_candidate
            line_seg = cluster_candidate.segment
            bounding_box = self.get_bounding_box_of_line_segment(line_seg)
            self.idx.insert(cluster_candidate.id, bounding_box, cluster_candidate)

    def find_neighbors_of(self, cluster_candidate):
        bounding_box = \
        self.get_bounding_box_of_line_segment(cluster_candidate.segment)
        possible_neighbor_ids = [n for n in self.idx.intersection(bounding_box)]
        actual_neighbors = []
        
        for id in possible_neighbor_ids:
            if id == None:
                raise Exception("ids on these need to be set")
            if id != cluster_candidate.id and \
            cluster_candidate.distance_to_candidate(self.candidates_by_ids[id]) <= \
            self.epsilon:
                actual_neighbors.append(self.candidates_by_ids[id])
                
        cluster_candidate.set_num_neighbors(len(actual_neighbors))
        return actual_neighbors 

    def get_bounding_box_of_line_segment(self, line_seg):
        btm = min(line_seg.start.y, line_seg.end.y) - self.epsilon
        top = max(line_seg.start.y, line_seg.end.y) + self.epsilon
        left = min(line_seg.start.x, line_seg.end.x) - self.epsilon
        right = max(line_seg.start.x, line_seg.end.x) + self.epsilon
        return (left, btm, right, top)

class TrajectoryCluster(Cluster):
    def __init__(self, id):
        Cluster.__init__(self)
        self.cid = id
        self.trajectories = set()

    def as_dict(self):
        return {
            'segments': [tls.as_dict() for tls in self.members],
            'cluster_id': self.cid
        }

    def add_member(self, tls):
        Cluster.add_member(self, tls)
        if not (tls.tid in self.trajectories):
            self.trajectories.add(tls.tid)
        
    def get_num_of_trajs(self):
        return len(self.trajectories)
    
    def get_members(self):
        return self.members
    
class TrajectoryClusterFactory(ClusterFactory):
    def __init__(self):
        self.next_cid = 0

    def create(self):
        curr_cid = self.next_cid
        self.next_cid += 1
        return TrajectoryCluster(curr_cid)

# Use an r tree index for line segments during dbscan if it's available, 
# otherwise use the pure python n squared dbscan.
BestAvailableClusterCandidateIndex = None
import sys, os
try:
    from rtree import index
    BestAvailableClusterCandidateIndex = RtreeTrajectoryLineSegmentCandidateIndex
    sys.stderr.write(str(os.path.realpath(__file__)) + ": rtree import succeeded." + \
                     " Using an r-tree for clustering\n")
except ImportError:
    BestAvailableClusterCandidateIndex = TrajectoryLineSegmentCandidateIndex
    sys.stderr.write(str(os.path.realpath(__file__)) + ": rtree import failed." + \
                     " Using plain python quadratic clustering\n")
    
    
