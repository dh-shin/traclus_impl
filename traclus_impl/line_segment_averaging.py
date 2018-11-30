'''
Created on Jan 5, 2016

@author: Alex
'''

from geometry import Point
from representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY
from representative_trajectory_average_inputs import get_representative_trajectory_average_inputs
from representative_line_finding import get_average_vector
from representative_line_finding import get_rotated_segment

def get_rline_pts(tls_list, min_vline, min_prev_dist):
    segments = list(map(lambda tls: tls.segment, tls_list))
    avg_vec = get_average_vector(segments)
    for tls in tls_list:
        tls.rsegment = get_rotated_segment(tls.segment, -avg_vec.angle)
    inputs = get_representative_trajectory_average_inputs(tls_list, min_vline, min_prev_dist)
    rline_pts = []
    for line_seg_averaging_input in inputs:
        vert_val = get_mean_vertical_coordinate_in_line_segments(line_seg_averaging_input)
        rline_pts.append(Point(line_seg_averaging_input['horizontal_position'], vert_val))
    return [pt.rotated(avg_vec.angle) for pt in rline_pts]

def interpolate_within_line_segment(line_segment, horizontal_coordinate):
    min_x = min(line_segment.start.x, line_segment.end.x)
    max_x = max(line_segment.start.x, line_segment.end.x)
    
    if not (min_x <= horizontal_coordinate + DECIMAL_MAX_DIFF_FOR_EQUALITY \
            and max_x >= horizontal_coordinate - DECIMAL_MAX_DIFF_FOR_EQUALITY):
        raise Exception("horizontal coordinate " + str(horizontal_coordinate) + \
                        " not within horizontal range of line segment" + \
                        " with bounds " + str(min_x) + " and " + str(max_x))
    elif line_segment.start.y - line_segment.end.y == 0.0:
        return line_segment.start.y
    elif line_segment.start.x - line_segment.end.x == 0.0:
        return (line_segment.end.y - line_segment.start.y) / 2.0 + line_segment.start.y
    else:
        return float((horizontal_coordinate - line_segment.start.x)) / (line_segment.end.x - line_segment.start.x) * \
            (line_segment.end.y - line_segment.start.y) + line_segment.start.y        
        
def line_segment_averaging_set_iterable(line_segments_to_average):
    line_segment_averaging_set = []
    horizontal_coord = line_segments_to_average['horizontal_position']
    for seg in line_segments_to_average['lines']:
        line_segment_averaging_set.append({'horizontal_pos': horizontal_coord, 'line_seg': seg})
    
    return line_segment_averaging_set

def number_average(iter_ob, func):
    count = len(iter_ob)
    if count == 0:
        raise Exception("no input given to take average of")
    total = 0.0
    for item in iter_ob:
        total += func(item)
    return total / count
        
def get_mean_vertical_coordinate_in_line_segments(line_segments_to_average):
    def apply_interpolation_to_line_segment(interpolation_info):
        if interpolation_info['line_seg'] == None or interpolation_info['horizontal_pos'] == None:
            raise Exception("nil key. " + str(interpolation_info) + " was passed to apply_interpolation_to_line_segment")
        return interpolate_within_line_segment(interpolation_info['line_seg'], interpolation_info['horizontal_pos'])
       
    return number_average(line_segment_averaging_set_iterable(line_segments_to_average), \
                          apply_interpolation_to_line_segment)