'''
Created on Jan 10, 2016

@author: Alex
'''
from generic_dbscan import dbscan
from line_segment_averaging import get_rline_from_traj_segments
from traclus_dbscan import TrajectoryLineSegmentFactory
from traclus_dbscan import TrajectoryClusterFactory
from traclus_dbscan import BestAvailableClusterCandidateIndex
from trajectory_partitioning import call_partition_trajectory
from trajectory_partitioning import get_line_segment_from_points

# min_traj : minimum number of trajectories in cluster
# min_vline : minimum number of vertical lines
# p_hook : partitioned_points_hook
# c_hook : clusters_hook

def run_traclus(trajs, eps, min_lns, min_traj, \
                min_vline, min_prev_dist, p_hook=None, c_hook=None):

    trajs = get_cleaned_trajectories(trajs)
    tls_factory = TrajectoryLineSegmentFactory()

    # Partitioning
    cluster_candidates = []
    for curr_tid, traj in enumerate(trajs):

        good_indices = call_partition_trajectory(traj)
        good_points = filter_by_indices(good_indices, traj)
        line_segments = get_consecutive_line_segments(good_points)

        if len(line_segments) <= 0:
            raise Exception()

        for segment in line_segments:
            tls = tls_factory.create(segment, curr_tid)
            cluster_candidates.append(tls)
    
    if p_hook:
        p_hook(cluster_candidates)

    # Clustering (DBSCAN)
    line_seg_index = BestAvailableClusterCandidateIndex(cluster_candidates, eps)
    clusters = dbscan(cluster_candidates_index=line_seg_index, min_neighbors=min_lns, \
                      cluster_factory=TrajectoryClusterFactory())
    
    if c_hook:
        c_hook(clusters)

    # Representative line segments
    rep_lines = []
    for traj_cluster in clusters:
        if traj_cluster.num_trajectories_contained() >= min_traj:
            trajectory_line_segs = traj_cluster.get_trajectory_line_segments()
            rline = get_rline_from_traj_segments(trajectory_line_segs, min_vline, min_prev_dist)
            rep_lines.append(rline)
            
    result = {
        "segment": cluster_candidates,
        "cluster": clusters,
        "representative": rep_lines
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
    cleaned = []
    # remove spikes & continuously duplicate points
    for traj in list(map(lambda l: with_spikes_removed(l), trajs)):
        revised_traj = []
        if len(traj) > 1:
            prev = traj[0]
            revised_traj.append(traj[0])
            for pt in traj[1:]:
                if prev.distance_to(pt) > 0.0:
                    revised_traj.append(pt)
                    prev = pt
            if len(revised_traj) > 1:
                cleaned.append(revised_traj)
    return cleaned

def with_spikes_removed(traj):
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

def get_consecutive_line_segments(items):
    
    # emptyness check
    if not items:
        raise ValueError("items doesn't have any values")

    # size check
    if len(items) < 2:
        raise ValueError("items didn't have at least two items")

    out_vals = []
    last_item = None
    for item in items:
        if last_item is not None:
            line_seg = get_line_segment_from_points(last_item, item)
            out_vals.append(line_seg)
        last_item = item
        
    return out_vals
