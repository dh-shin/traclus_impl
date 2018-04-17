
import json
from math import asin, cos, sin, sqrt, radians
import matplotlib.pyplot as plt
def haversine(p1, p2):
    """
    :param p1: [longitude, latitude]
    :param p2: [longitude, latitude]
    :return: distance in km
    """
    # 转换成弧度
    lon1, lat1, lon2, lat2 = map(radians, [p1[0], p1[1], p2[0], p2[1]])

    # 某转换公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # 地球半径(km)
    r = 6371
    return c * r


def main():
    ssq = 0
    total_N = 0
    cc = {
        'aqua': '#00FFFF',
        'blue': '#0000FF',
        'blueviolet': '#8A2BE2',
        'brown': '#A52A2A',
        'burlywood': '#DEB887',
        'cadetblue': '#5F9EA0',
        'chartreuse': '#7FFF00',
        'chocolate': '#D2691E',
        'coral': '#FF7F50',
        'cornflowerblue': '#6495ED',
        'crimson': '#DC143C',
        'cyan': '#00FFFF',
        'darkblue': '#00008B',
        'darkcyan': '#008B8B',
        'darkgoldenrod': '#B8860B',
        'darkgray': '#A9A9A9',
        'darkgreen': '#006400',
        'darkkhaki': '#BDB76B',
        'darkmagenta': '#8B008B',
        'darkolivegreen': '#556B2F',
        'darkorange': '#FF8C00',
        'darkorchid': '#9932CC',
        'darkred': '#8B0000',
        'darkseagreen': '#8FBC8F',
        'darkslateblue': '#483D8B',
        'darkslategray': '#2F4F4F',
        'darkturquoise': '#00CED1',
        'darkviolet': '#9400D3',
        'deeppink': '#FF1493',
        'deepskyblue': '#00BFFF',
        'dodgerblue': '#1E90FF',
        'firebrick': '#B22222',
        'forestgreen': '#228B22',
        'fuchsia': '#FF00FF',
        'gold': '#FFD700',
        'goldenrod': '#DAA520',
        'green': '#008000',
        'greenyellow': '#ADFF2F',
        'hotpink': '#FF69B4',
        'indianred': '#CD5C5C',
        'indigo': '#4B0082',
        'khaki': '#F0E68C',
        'lavenderblush': '#FFF0F5',
        'lawngreen': '#7CFC00',
        'lemonchiffon': '#FFFACD',
        'lime': '#00FF00',
        'limegreen': '#32CD32',
        'magenta': '#FF00FF',
        'maroon': '#800000',
        'mediumaquamarine': '#66CDAA',
        'mediumblue': '#0000CD',
        'mediumorchid': '#BA55D3',
        'mediumpurple': '#9370DB',
        'mediumseagreen': '#3CB371',
        'mediumslateblue': '#7B68EE',
        'mediumspringgreen': '#00FA9A',
        'mediumturquoise': '#48D1CC',
        'mediumvioletred': '#C71585',
        'midnightblue': '#191970',
        'navy': '#000080',
        'olive': '#808000',
        'olivedrab': '#6B8E23',
        'orange': '#FFA500',
        'orangered': '#FF4500',
        'orchid': '#DA70D6',
        'papayawhip': '#FFEFD5',
        'peachpuff': '#FFDAB9',
        'peru': '#CD853F',
        'plum': '#DDA0DD',
        'powderblue': '#B0E0E6',
        'purple': '#800080',
        'red': '#FF0000',
        'rosybrown': '#BC8F8F',
        'royalblue': '#4169E1',
        'saddlebrown': '#8B4513',
        'salmon': '#FA8072',
        'sandybrown': '#FAA460',
        'seagreen': '#2E8B57',
        'sienna': '#A0522D',
        'skyblue': '#87CEEB',
        'slateblue': '#6A5ACD',
        'slategray': '#708090',
        'springgreen': '#00FF7F',
        'steelblue': '#4682B4',
        'tan': '#D2B48C',
        'teal': '#008080',
        'tomato': '#FF6347',
        'turquoise': '#40E0D0',
        'violet': '#EE82EE',
        'wheat': '#F5DEB3',
        'yellow': '#FFFF00',
        'yellowgreen': '#9ACD32'}
    k = len(cc)
    c=list(sorted(cc))
    with open(r'C:\Users\xiaoF\Documents\Projects\traclus_impl-master\traclus_impl\sh00101_cluster.txt') as f:
        data = json.load(f)
        print(len(data))
        i = 1
        for cluster in data:

            N = len(cluster)
            x = list(map(lambda line: (line['start']['x'] + \
                        line['end']['x'])/2, [line for line in cluster]))
            y = list(map(lambda line: (line['start']['y'] + \
                        line['end']['y']) / 2, [line for line in cluster]))
            center_point = (sum(x)/N, sum(y)/N)


            pair = list(zip(x, y))
            for point in pair:
                ssq += haversine(point, center_point)
            total_N += N
            for line in cluster:
                _x = [line['start']['x'], line['end']['x']]
                _y = [line['start']['y'], line['end']['y']]
                plt.plot(_x,_y,c[i])

            i+=1
    print('ssq:%f, %d, %f' % (ssq, total_N, ssq/total_N))
    plt.show()


if __name__=='__main__':
    main()