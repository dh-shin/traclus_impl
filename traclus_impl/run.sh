#!/bin/sh
file_path="."
prefix="raw_campus_trajectories"
i_file=$file_path"/"$prefix"_input.txt"
o_file=$file_path"/"$prefix"_output.txt"
c_file=$file_path"/"$prefix"_cluster.txt"
p_file=$file_path"/"$prefix"_partitioned.txt"

python main.py -i $i_file -o $o_file -p $p_file -c $c_file
