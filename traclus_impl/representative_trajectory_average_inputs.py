'''
Created on Jan 1, 2016

@author: Alex
'''
from linked_list import LinkedList
from linked_list import LinkedListNode
from operator import attrgetter

DECIMAL_MAX_DIFF_FOR_EQUALITY = 0.0000001

class TrajectoryLineSegmentEndpoint:
    def __init__(self, horizontal_position, rsegment, rsegment_id, list_node):
        self.horizontal_position = horizontal_position
        self.rsegment = rsegment
        self.rsegment_id = rsegment_id
        self.list_node = list_node

def get_sorted_line_seg_endpoints(tls_list):
    line_segment_endpoints = []
    cur_id = 0
    for tls in tls_list:
        list_node = LinkedListNode(tls)
        e1 = TrajectoryLineSegmentEndpoint(tls.rsegment.start.x, tls, cur_id, list_node)
        e2 = TrajectoryLineSegmentEndpoint(tls.rsegment.end.x, tls, cur_id, list_node)
        line_segment_endpoints.append(e1)
        line_segment_endpoints.append(e2)
        cur_id += 1
    return sorted(line_segment_endpoints, key=attrgetter('horizontal_position'))

def numbers_within(a, b, max_diff):
    return abs(a - b) <= max_diff

def possibly_append_to_active_list(active_list, out, prev_pos, min_prev_dist, min_lines):
    if (len(out) == 0 or prev_pos - out[len(out) - 1]['horizontal_position'] >= min_prev_dist) and len(active_list) >= min_lines:
        temp = []
        line_list = []
        tmp  = active_list.head
        while tmp:
            if tmp.item:
                line_list.append(tmp.item.rsegment)
            tmp = tmp.next
            if tmp == active_list.head:
                break
        for line_seg in line_list:
            temp.append(line_seg)
        out.append({'lines': temp, 'horizontal_position': prev_pos})
        
def line_segments_were_adjacent(trajectory_seg_a, trajectory_seg_b):
    return trajectory_seg_a.trajectory_id == trajectory_seg_b.trajectory_id and \
        abs(trajectory_seg_a.position_in_trajectory - trajectory_seg_b.position_in_trajectory) == 1
    
def same_trajectory_line_segment_connects(seg, line_seg_endpoint_list):
    for other in line_seg_endpoint_list:
        if line_segments_were_adjacent(seg, other.line_segment):
            return True
    return False
        
def remove_duplicate_points_from_adjacent_lines_of_same_trajectories(active_list, insert_list, delete_list):
    insertion_line_seg_set = set()
    for endpoint in insert_list:
        insertion_line_seg_set.add(endpoint.line_segment)
    
    deletion_keeper_list = []
    for endpoint in delete_list:
        if (not endpoint.line_segment in insertion_line_seg_set) and \
        same_trajectory_line_segment_connects(endpoint.line_segment, insert_list):
            active_list.remove_node(endpoint.list_node)
        else:
            deletion_keeper_list.append(endpoint)
            
    delete_list[:] = deletion_keeper_list

def get_representative_trajectory_average_inputs(tls_list, min_lines, min_prev_dist):
    cur_active = [False] * len(tls_list)
    active_list = LinkedList()        
    insert_list = [] 
    delete_list = []
    out = []
    
    line_segment_endpoints = get_sorted_line_seg_endpoints(tls_list)
        
    i = 0
    while i < len(line_segment_endpoints):
        insert_list[:] = []
        delete_list[:] = []
        prev_pos = line_segment_endpoints[i].horizontal_position
        
        while i < len(line_segment_endpoints) and numbers_within(line_segment_endpoints[i].horizontal_position, \
                                                                 prev_pos, DECIMAL_MAX_DIFF_FOR_EQUALITY):
            if not cur_active[line_segment_endpoints[i].rsegment_id]:
                insert_list.append(line_segment_endpoints[i])
                cur_active[line_segment_endpoints[i].rsegment_id] = True
            elif cur_active[line_segment_endpoints[i].rsegment_id]:
                delete_list.append(line_segment_endpoints[i])
                cur_active[line_segment_endpoints[i].rsegment_id] = False
            i += 1
            
        for line_seg_endpoint in insert_list:
            active_list.add_last_node(line_seg_endpoint.list_node)
        possibly_append_to_active_list(active_list, out, prev_pos, min_prev_dist, min_lines)
        for line_seg in delete_list:
            active_list.remove_node(line_seg.list_node)
    
    return out
            