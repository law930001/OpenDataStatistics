from pandas_ods_reader import read_ods
import numpy as np
import os
from natsort import natsorted
from tqdm import tqdm

def get_time(ori):

    data = ori.split('至')

    year = data[1].split('年')[0]
    month = data[1].split('年')[1].split('月')[0]
    day = data[1].split('月')[1].split('日')[0]

    res = year + '/' + month.zfill(2) + '/' + day.zfill(2)

    return res

def main():

    crime_dir = './data/'

    time_all = []
    crime_cat = ['強盜', '搶奪', '強制性交', '汽車竊盜', '住宅竊盜', '毒品', '機車竊盜']
    result = {}

    for c in crime_cat:
        result[c] = {}

    for file_name in tqdm(natsorted(os.listdir(crime_dir))):

        if '無資料' in file_name:
            continue

        time = get_time(file_name.replace('.ods', ''))
        time_all.append(time)

        base_path = crime_dir + file_name
        data = np.array(read_ods(base_path , 1).values.tolist())

        # print(data[2,1:8])

        for i, c in enumerate(result):

            N = data[2,i+1]

            N = '0' if N == '  -  ' else N

            if time not in result[c]:
                result[c][time] = int(N)
            else:
                result[c][time] += int(N)


        # write result

        result_dir = './result.csv'

        with open(result_dir, 'w', encoding='utf-8') as file:
            file.write('crime,' + ','.join(time_all) + '\n')


            for c in crime_cat:

                ans = []

                for time in time_all:
                    ans.append(str(result[c][time]))

                file.write(c + ',' + ','.join(ans) + '\n')






if __name__ == '__main__':
    main()
    print('Done.')