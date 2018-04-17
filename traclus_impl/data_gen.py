import csv
from collections import namedtuple
import os
import datetime



def time_parse(time_str):
    _datetime = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return _datetime

def main():
    start_time = datetime.datetime(2007,2,20)
    end_time = datetime.datetime(2007,2,20,0,10)
    # start_time = datetime.datetime(2008, 2, 2,18,30)
    # end_time = datetime.datetime(2008, 2, 2,20)
    # file_root = r'D:\release\taxi_log_2008_by_id'
    file_root =r'D:\上海\Taxi_070220'
    output_path = r'C:\Users\xiaoF\Documents\Projects\traclus_impl-master\sh0010test.txt'
    output_file = open(output_path, 'a')
    output_file.write('{"epsilon": 0.0016, "min_neighbors": 2, "min_num_trajectories_in_cluster": 2, '
                      '"min_vertical_lines": 2, "min_prev_dist": 0.0002, "trajectories": [')
    # for i in range(1, 10357):
    #     file_path = file_root + '\%d'%i + '.txt'
    #     with open(file_path) as f:
    #         output_file.write('[')
    #         for line in f.readlines():
    #             *_, time, y, x = line.rstrip().split(',')
    #             t= time_parse(time)
    #
    #             if start_time < t < end_time:
    #                 output_file.write('{"x": %s, "y": %s}, ' % (x, y))
    #                 print(t)
    #             elif t > end_time:
    #                 break
    #         output_file.write(r'\b], ')
    #     print('%d done' %i)
    data = []
    for root, dir_name, files in os.walk(file_root):
        for file in files:
            with open(os.path.join(root, file)) as f:
                output_file.write('[')
                for line in f.readlines():
                    i, time, y, x, *_ = line.rstrip().split(',')
                    t = time_parse(time)

                    if start_time <= t <= end_time:
                        data.append(line)
                        output_file.write('{"x": %s, "y": %s}, ' % (x, y))

                    elif t > end_time:
                        break
                output_file.write(r'\b], ')


    # print(l)
    print(len(data))
    output_file.write(r'\b]}')
    output_file.close()


def get_from_csv():
    output_path = r'C:\Users\xiaoF\Documents\Projects\traclus_impl-master\output.txt'
    output_file = open(output_path, 'a')
    output_file.write('{"epsilon": 0.00016, "min_neighbors": 2, "min_num_trajectories_in_cluster": 3, '
                      '"min_vertical_lines": 2, "min_prev_dist": 0.0002, "trajectories": [')
    file_path = r'C:\Users\xiaoF\Documents\Projects\dy_traclu\taxi_stream.csv'
    rwo_num = 10
    with open(file_path) as f:
        f_csv = csv.reader(f)
        header = next(f_csv)
        Row = namedtuple('Row', header)
        for r in f_csv:
            row = Row(*r)
            output_file.write('{"x": %s, "y": %s}, ' % (row[3], row[2]))
    output_file.write(r'\b]}')
    output_file.close()

def geolife():
    def time_parse_2(time_str):
        _datetime = datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S')
        return _datetime
    start_time = datetime.datetime(2012,2,2)
    end_time = datetime.datetime(2012,2,3)

    # file_root = r'D:\Geolife-Trajectories-1.3\Data'
    file_root = r'D:\release\taxi_log_2008_by_id'
    output_path = r'C:\Users\xiaoF\Documents\Projects\traclus_impl-master\gtest.txt'
    output_file = open(output_path, 'a')
    output_file.write('{"epsilon": 0.0016, "min_neighbors": 3, "min_num_trajectories_in_cluster": 3, '
                      '"min_vertical_lines": 2, "min_prev_dist": 0.0002, "trajectories": [')
    for i in range(182):
        file_path = file_root + '\%03d'%i + '\Trajectory'
        output_file.write('[')
        for root, *_, files in os.walk(file_path):
            for file in files:
                try:
                    time = time_parse_2(os.path.splitext(file)[0])
                except Exception as e:
                    continue
                if start_time < time < end_time:
                    with open(os.path.join(root, file)) as f:
                        for line in f.readlines()[6:]:
                                x, y, *_, date, time = line.rstrip().split(',')
                                dt = time_parse(date+' '+time)
                                if start_time < dt < end_time:
                                    output_file.write('{"x": %s, "y": %s}, ' % (x, y))
                                elif dt > end_time:
                                    break
                elif time > end_time:
                    break
        output_file.write(r'\b], ')
    output_file.write(r'\b]}')
    output_file.close()


if __name__ == '__main__':
    main()
    # get_from_csv()
    # geolife()