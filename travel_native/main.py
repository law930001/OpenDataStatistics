import os
from natsort import natsorted
import natsort
from tqdm import tqdm
import csv

class Travel_Native():

    def __init__(self):

        self.result = {}
        self.time_all = []

    def get_time_name(self, year, name, N, country):

        if name not in self.result:
            self.result[name] = {}

        if 'country' not in self.result:
            self.result[name]['country'] = country

        for t in range(1,13):

            time = year + '/' + str(t).zfill(2)

            if time == '2021/11' or time == '2021/12':
                continue

            if time not in self.time_all:
                self.time_all.append(time)
            
            N[t-1] = 0 if N[t-1] == '' else N[t-1]

            if time not in self.result[name]:
                self.result[name][time] = int(N[t-1])
            else:
                self.result[name][time] += int(N[t-1])

    def write_result(self, type_name): 

        result_dir = './result.csv'

        with open(result_dir, 'w', encoding='utf-8') as file:

            file.write(type_name + ',country,' + ','.join(self.time_all) + '\n')

        
            for name in self.result:

                if 'country' in self.result[name]:
                    country_name = self.result[name].pop('country')

                ans = []

                for t in self.time_all:

                    if t in self.result[name]:
                        ans.append(str(self.result[name][t]))
                    else:
                        ans.append('0')

                file.write(name + ',' + country_name + ',' + ','.join(ans) + '\n')

    def country_process(self):

        data_dir = './data/data.csv'

        with open(data_dir, encoding='utf-8') as f:

            reader = csv.reader(f)

            data = list(reader)

            for line in data[1:]:

                year = line[0]

                # if year != '2021':
                #     continue

                name = line[4]
                country = line[4]
                N = line[5:-1]

                self.get_time_name(year, name, N, country)


        # write result

        self.write_result('country')



    def type_process(self):

        data_dir = './data/data.csv'

        with open(data_dir, encoding='utf-8') as f:

            reader = csv.reader(f)

            data = list(reader)

            for line in data[1:]:

                if line[1] != '國家公園':
                    continue

                year = line[0]
                name = line[3]
                country = line[4]
                N = line[5:-1]

                self.get_time_name(year, name, N, country)

        self.write_result('type')




if __name__ == '__main__':
    tn = Travel_Native()
    # tn.country_process()
    tn.type_process()


    print('Done.')

