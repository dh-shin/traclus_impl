'''
Created on Jan 10, 2016

@author: Alex
'''
from geometry import Point
from geometry import LineSegment
from generic_dbscan import dbscan
from trajectory import Trajectory
from trajectory import TrajectoryLineSegmentFactory
from trajectory import TrajectoryClusterFactory
from trajectory import BestAvailableClusterCandidateIndex
from trajectory import RepresentativeTrajectory
from trajectory_partitioning import call_partition_trajectory
from line_segment_averaging import get_rline_pts

# min_traj : minimum number of trajectories in cluster
# min_vline : minimum number of vertical lines
def run_traclus(trajs, eps, min_lns, min_traj, min_vline, min_prev_dist):

    # Cleaning
    trajs = [[Point(**pt) for pt in traj] for traj in trajs]
    trajs = get_cleaned_trajectories(trajs)
    print('Number of trajectories after clean : {}'.format(len(trajs)))
    trajs = [Trajectory(traj, tid) for tid, traj in enumerate(trajs)]

    # Partitioning
    cluster_candidates_tls = []
    tls_factory = TrajectoryLineSegmentFactory()
    for traj in trajs:
        p_indices = call_partition_trajectory(traj.pts)
        p_pts = filter_by_indices(p_indices, traj.pts)
        traj.p_pts = p_pts
        ls_list = get_ls_list(p_pts)
        if len(ls_list) <= 0:
            raise Exception()
        for ls in ls_list:
            tls = tls_factory.create(ls, traj.tid)
            cluster_candidates_tls.append(tls)
    print('Number of segments (cluster candidates) : {}'.format(len(cluster_candidates_tls)))

    # Clustering (DBSCAN)
    tls_index = BestAvailableClusterCandidateIndex(cluster_candidates_tls, eps)
    tcluster_factory = TrajectoryClusterFactory()
    tclusters = dbscan(tls_index, min_lns, tcluster_factory)
    print('Number of clusters : {}'.format(len(tclusters)))
    
    # Representative trajectory
    rtrajs = []
    for tc in tclusters:
        if tc.get_num_of_trajs() >= min_traj:
            tls_list = tc.get_members()
            r_pts = get_rline_pts(tls_list, min_vline, min_prev_dist)
            rtraj = RepresentativeTrajectory(r_pts, tc.cid)
            rtrajs.append(rtraj)
    print('Number of representative trajectories : {}'.format(len(rtrajs)))
            
    result = {
        'partitioned_trajectories': trajs,
        'clusters': tclusters,
        'representative_trajectories': rtrajs
    }
    
    return result

def filter_by_indices(good_indices, vals):
    vals_iter = iter(vals)
    good_indices_iter = iter(good_indices)

    first_index = good_indices[0]
    last_index = good_indices[-1]
    num_vals = len(vals)

    # First index check
    if first_index != 0:
        raise ValueError("the first index should be 0, but it was " + str(first_index))

    # length of vals check
    if num_vals < 2:
        raise ValueError("list passed in is too short")
    
    # last index check
    if last_index != num_vals - 1:
        raise ValueError("last index is " + str(last_index) + \
                         " but there were " + str(num_vals) + " vals")

    return [vals[i] for i in good_indices]

def get_cleaned_trajectories(trajs):
    trajs = [remove_spikes(pts) for pts in trajs]
    trajs = [remove_duplicate(pts) for pts in trajs]
    trajs = [pts for pts in trajs if len(pts) > 1]
    return trajs

def remove_duplicate(traj):
    cleaned = []
    prev = None
    for pt in traj:
        if prev is None:
            prev = pt
            cleaned.append(pt)
        else:
            if prev.distance_to(pt) > 0.0:
                cleaned.append(pt)
                prev = pt
    return cleaned

def remove_spikes(traj):
    if len(traj) <= 2:
        return traj[:]

    spikes_removed = []
    spikes_removed.append(traj[0])
    cur_index = 1
    while cur_index < len(traj) - 1:
        if traj[cur_index - 1].distance_to(traj[cur_index + 1]) > 0.0:
            spikes_removed.append(traj[cur_index])
        cur_index += 1
    spikes_removed.append(traj[cur_index])
    return spikes_removed

def get_ls_list(pts):
    # emptyness check
    if not pts:
        raise ValueError("pts doesn't have any values")

    # size check
    if len(pts) < 2:
        raise ValueError("pts didn't have at least two points")

    ls_list = []
    last_pt = None
    for pt in pts:
        if last_pt is not None:
            ls = LineSegment(last_pt, pt)
            ls_list.append(ls)
        last_pt = pt
        
    return ls_list
