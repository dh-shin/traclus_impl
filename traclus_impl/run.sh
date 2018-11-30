#!/bin/sh
file_path="."
prefix="raw_campus_trajectories"
i_file=$file_path"/"$prefix"_input.json"
o_file=$file_path"/"$prefix"_output.json"
c_file=$file_path"/"$prefix"_cluster.json"
p_file=$file_path"/"$prefix"_partitioned.json"

python main.py -i $i_file -o $o_file -p $p_file -c $c_file
