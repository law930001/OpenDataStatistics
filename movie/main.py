import os
from natsort import natsorted
import pandas as pd
from tqdm import tqdm


def get_time(ori):

    data = ori.split('至')

    if len(data[1].split('年')) == 1: # no year back
        year = data[0].split('年')[0]
        month = data[1].split('月')[0]
        day = data[1].split('月')[1].replace('日', '')
    else:
        year = data[1].split('年')[0]
        month = data[1].split('年')[1].split('月')[0]
        day = data[1].split('月')[1].replace('日', '')

    res = year + '/' + month.zfill(2) + '/' + day.zfill(2)

    return res



def main():

    data_dir = './data/'

    result = {}

    time_all = []

    for file_name in tqdm(natsorted(os.listdir(data_dir))):

        time = get_time(file_name.replace('.csv',''))

        if time.split('/')[0] in ['2020']:
            pass
        else:
            continue

        time_all.append(time)

        df = pd.read_csv(data_dir + file_name)

        file = df.values.tolist()


        for line in file:

            nation, name, N = str(line[1]), str(line[2]), str(line[7])

            if nation != '中華民國':
                continue

            name = name.replace('?', '')
            N = N.replace(',', '')

            # print(time, nation, name, N)

            if name not in result:
                result[name] = {}
                result[name]['nation'] = nation
            
            result[name][time] = N
    

    # write result

    print('Writing result...')

    result_dir = './result.csv'

    with open(result_dir, 'w', encoding='utf-8') as file:
        file.write('movie,nation,' + ','.join(time_all) + '\n')

        for name in tqdm(result):

            nation = result[name]['nation']
            del result[name]['nation']

            ans = []

            for time in time_all:
                
                if time in result[name]:
                    ans.append(result[name][time])
                else:
                    ans.append('0')

            file.write(name + ',' + nation + ',' + ','.join(ans) + '\n')



if __name__ == '__main__':
    main()
    print("Done.")