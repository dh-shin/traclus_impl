'''
Created on Mar 27, 2016

@author: Alex
'''

import click
import json
import os
import time
import filecmp

from geometry import Point
from coordination import run_traclus

@click.command()
@click.option(
              '--input-file', '-i',
              help='Input File. Should contain Trajectories and Traclus Parameters.' \
              'See integ_tests/raw_campus_trajectories.txt for an example.',
              required=True)
@click.option(
              '--output-file', '-o',
              help='Output File. Will contain a list of the representative trajectories as Json.',
              required=True)
@click.option(
              '--p-file', '-p',
              help='Optional file to dump the output from the partitioning stage to.')
@click.option(
              '--c-file', '-c',
              help='Optional file to dump the clusters with their line segments to.')

def main(input_file, output_file, p_file=None, c_file=None):
    print('===============================================')
    c1 = time.time()

    parsed_input = None
    with open(input_file, 'r') as read_file:
        parsed_input = json.load(read_file)

    for required_param in ['trajectories', 'epsilon', 'min_neighbors',
                        'min_num_trajectories_in_cluster',
                        'min_vertical_lines', 'min_prev_dist']:
        assert parsed_input[required_param], "missing param: " + str(required_param)

    trajs = list(map(lambda traj: list(map(lambda pt: Point(**pt), traj)), parsed_input['trajectories']))
    print('Number of input trajectories : {}'.format(len(trajs)))

    p_hook = get_partitioned_hook(p_file)
    c_hook = get_clusters_hook(c_file)

    result = run_traclus(trajs=trajs, eps=parsed_input['epsilon'], 
                        min_lns=parsed_input['min_neighbors'],
                        min_traj=parsed_input['min_num_trajectories_in_cluster'],
                        min_vline=parsed_input['min_vertical_lines'],
                        min_prev_dist=parsed_input['min_prev_dist'],
                        p_hook=p_hook, c_hook=c_hook)

    dict_result = list(map(lambda traj: list(map(lambda pt: pt.as_dict(), traj)), result))
    c2 = time.time()

    with open(output_file, 'w') as write_file:
        json.dump(dict_result, write_file, indent=4)
    
    check_file_sameness(output_file)

    print('elapsed time : %f' % (c2 - c1))
    print('===============================================')

def get_partitioned_hook(file_name):
    if not file_name:
        return None

    def func(output):
        dict_trajs = list(map(lambda traj_line_seg: traj_line_seg.line_segment.as_dict(), output))
        with open(file_name, 'w') as write_file:
            json.dump(dict_trajs, write_file, indent=4)
        
        check_file_sameness(file_name)

    return func

def get_clusters_hook(file_name):
    if not file_name:
        return None

    def func(clusters):
        all_cluster_line_segs = []
        for clust in clusters:
            line_segs = clust.get_trajectory_line_segments()
            dict_output = list(map(lambda traj_line_seg: traj_line_seg.line_segment.as_dict(),
                              line_segs))
            all_cluster_line_segs.append(dict_output)

        with open(file_name, 'w') as write_file:
            json.dump(all_cluster_line_segs, write_file, indent=4)

        check_file_sameness(file_name)

    return func

def check_file_sameness(x):
    y = x + '.org'
    if os.path.exists(x) and os.path.exists(y):
        if filecmp.cmp(x, y, shallow=False):
            print(x + ' is correct')
        else:
            print('ERROR : ' + x + ' is not correct!')
    else:
        print('ERROR : ' + x + ' not exist...')


if __name__ == '__main__':
    main()
