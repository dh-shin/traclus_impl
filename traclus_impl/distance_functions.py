'''
Created on Dec 29, 2015

@author: Alex
'''
import math
    
def determine_longer_and_shorter_lines(line_a, line_b):
    if line_a.length < line_b.length:
        return (line_b, line_a)
    else:
        return (line_a, line_b)
    
    
def get_total_distance_function(line_a, line_b):
    # c1 = clock()
    _delta = 0.000000000000000000000000000000001
    alpha = (1 + math.e**(-(line_a.cose_of_angle_with(line_b))))**(-1)

    center_1 = (line_a.start + line_a.end) / 2
    center_2 = (line_b.start + line_b.end) / 2

    d1 = center_1.distance_to(center_2)


    vec_1 = line_a.start - line_b.start
    vec_2 = line_a.end - line_b.end
    vec = vec_2 - vec_1
    d2 = math.sqrt(vec.x**2 + vec.y**2)

    d = (1-alpha) * d1 + alpha * d2
    #print('alpha:%f, d1:%f, d2:%f'%(alpha,d1,d2))
    # c2 = clock()
    # print('\t%f' % (c2-c1))
    return d + _delta
    # return perpendicular_distance(line_a, line_b) + angular_distance(line_a, line_b) + \
    #         parrallel_distance(line_a, line_b)



def perpendicular_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    dist_a = shorter_line.start.distance_to_projection_on(longer_line)
    dist_b = shorter_line.end.distance_to_projection_on(longer_line)
    
    if dist_a == 0.0 and dist_b == 0.0:
        return 0.0
    
    return (dist_a * dist_a + dist_b * dist_b) / (dist_a + dist_b)
    
def __perpendicular_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    dist_a = longer_line.line.project(shorter_line.start).distance_to(shorter_line.start)
    dist_b = longer_line.line.project(shorter_line.end).distance_to(shorter_line.end)
    
    if dist_a == 0.0 and dist_b == 0.0:
        return 0.0
    else:
        return (math.pow(dist_a, 2) + math.pow(dist_b, 2)) / (dist_a + dist_b)

def angular_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    sine_coefficient = shorter_line.sine_of_angle_with(longer_line)
    return abs(sine_coefficient * shorter_line.length)

#def __parrallel_distance(line_a, line_b):

def parrallel_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    def __func(shorter_line_pt, longer_line_pt):
        return shorter_line_pt.distance_from_point_to_projection_on_line_seg(longer_line_pt, \
                                                                             longer_line)
    return min([longer_line.dist_from_start_to_projection_of(shorter_line.start), \
               longer_line.dist_from_start_to_projection_of(shorter_line.end), \
               longer_line.dist_from_end_to_projection_of(shorter_line.start), \
               longer_line.dist_from_end_to_projection_of(shorter_line.end)])
    
def dist_to_projection_point(line, proj):
    return min(proj.distance_to(line.start), proj.distance_to(line.end))

