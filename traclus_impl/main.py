'''
Created on Mar 27, 2016

@author: Alex
'''

import click
import json
import os
import time
import filecmp

from traclus import run_traclus

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
    
    parsed_input = None
    with open(input_file, 'r') as read_file:
        parsed_input = json.load(read_file)

    for required_param in ['trajectories', 'epsilon', 'min_neighbors',
                        'min_num_trajectories_in_cluster',
                        'min_vertical_lines', 'min_prev_dist']:
        assert parsed_input[required_param], "missing param: " + str(required_param)

    raw_trajs = parsed_input['trajectories']
    print('Number of input trajectories : {}'.format(len(raw_trajs)))

    c1 = time.time()

    result = run_traclus(trajs=raw_trajs, eps=parsed_input['epsilon'], 
                        min_lns=parsed_input['min_neighbors'],
                        min_traj=parsed_input['min_num_trajectories_in_cluster'],
                        min_vline=parsed_input['min_vertical_lines'],
                        min_prev_dist=parsed_input['min_prev_dist'])   
    c2 = time.time()

    print('Elapsed time : %f' % (c2 - c1))
    print('===============================================')


    p_trajs = result['partitioned_trajectories']
    tclusters = result['clusters']
    repr_lines = result['representative_trajectories']

    write_partitioned_trajectories(p_file, p_trajs)
    write_clusters(c_file, tclusters)
    write_repr_lines(output_file, repr_lines)

    print('===============================================')

def write_partitioned_trajectories(file_name, p_trajs):
    if file_name:
        dict_result = [traj.as_dict() for traj in p_trajs]
        with open(file_name, 'w') as write_file:
            json.dump(dict_result, write_file, indent=4)
        check_output_parity(file_name)

def write_clusters(file_name, tclusters):
    if file_name:
        dict_result = [tc.as_dict() for tc in tclusters]
        with open(file_name, 'w') as write_file:
            json.dump(dict_result, write_file, indent=4)
        check_output_parity(file_name)     

def write_repr_lines(file_name, repr_lines):
    dict_result = [[pt.as_dict() for pt in pt_list] for pt_list in repr_lines]
    with open(file_name, 'w') as write_file:
        json.dump(dict_result, write_file, indent=4)
    check_output_parity(file_name)

def check_output_parity(x):
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
