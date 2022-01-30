import os
import numpy as np
from tqdm import tqdm

class DeadReason():
    def __init__(self):

        self.pos = {}
        self.cause = {}
        self.data = []
        self.age = {}
        self.result = {}

        # 81~96, 97~109
        self.start = 81
        self.end = 109

        


    def get_position_table(self):

        pos_dir = './position/'

        pos_year = ['79','93','97','100']

        for year in pos_year:

            temp_pos = {}

            with open(pos_dir + year + '.txt', 'r', encoding="utf-8") as file:
                for line in file.readlines():
                    info = line.strip().split(',')
                    temp_pos[info[0]] = info[1][:3]

            self.pos[year] = temp_pos

        print("Get position table: " + ",".join(pos_year))
        
    def get_cause_table(self):
        
        cause_dir = './cause/'

        cause_year = ['96', '97']

        for year in cause_year:
            
            temp_cause = {}

            with open(cause_dir + year + '.txt', 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    info = line.strip().split(',')
                    temp_cause[info[0]] = info[1]

            self.cause[year] = temp_cause

        print("Get cause table: " + ",".join(cause_year))

    def get_dead_data(self, col):

        dead_dir = './data/'

        for year in tqdm(range(self.start, self.end+1)):
            
            with open(dead_dir + 'dead' + str(year) + '.txt', 'r', encoding='utf-8') as file:
                for line in file.readlines()[1:]:
                    info = line.strip().split(',')

                    temp_col = []
                    for i in range(0,6):
                        if i in col:
                            temp_col.append(info[i])

                    self.data.append(temp_col)

        print("Get dead data from " + str(self.start) + " to " + str(self.end) + ": " + str(len(self.data)))

    def get_age_data(self):

        age_dir = './age/'

        with open(age_dir + 'age.txt', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                info = line.strip().split(',')

                self.age[info[0]] = info[1]

        print('Get age table')


    def cause_year_process(self):

        self.get_cause_table()

        self.get_dead_data([0,2,5])

        print('Processing data...')

        for line in tqdm(self.data):

            year, cause, N = line

            cause_name = self.cause['97'][cause] if int(year) >= 97 else self.cause['96'][cause]

            if cause_name not in self.result:
                self.result[cause_name] = {}

            if year not in self.result[cause_name]:
                self.result[cause_name][year] = int(N)
            else:
                self.result[cause_name][year]+= int(N)

        # save result

        print('Writing result...')

        result_file = './result.csv'

        with open(result_file, 'w', encoding='utf-8') as file:

            file.write('Cause,' + ','.join(str(x) for x in range(self.start, self.end+1)) + '\n')

            for cause in tqdm(self.result):

                result_line = []

                for year in range(self.start, self.end+1):
                    if str(year) in self.result[cause]:
                        result_line.append(str(self.result[cause][str(year)]))
                    else:
                        result_line.append('0')

                file.write(cause + ',' + ','.join(result_line) + '\n')

    def pos_year_process(self):

        self.get_position_table()

        self.get_dead_data([0,1,5])

        print('Processing data...')

        for line in tqdm(self.data):

            year, pos, N = line

            try:
                if int(year) <= 92:
                    pos_name = self.pos['79'][pos]
                elif int(year) >= 93 and int(year) <= 96:
                    pos_name = self.pos['93'][pos]
                elif int(year) >= 97 and int(year) <= 99:
                    pos_name = self.pos['97'][pos]
                elif int(year) >= 100:
                    pos_name = self.pos['100'][pos]
            except:
                print(year, pos, N)
                continue


            if pos_name not in self.result:
                self.result[pos_name] = {}

            if year not in self.result[pos_name]:
                self.result[pos_name][year] = int(N)
            else:
                self.result[pos_name][year]+= int(N)

        # save result

        print('Writing result...')

        result_file = './result.csv'

        with open(result_file, 'w', encoding='utf-8') as file:

            file.write('Cause,' + ','.join(str(x) for x in range(self.start, self.end+1)) + '\n')

            for cause in tqdm(self.result):

                result_line = []

                for year in range(self.start, self.end+1):
                    if str(year) in self.result[cause]:
                        result_line.append(str(self.result[cause][str(year)]))
                    else:
                        result_line.append('0')

                file.write(cause + ',' + ','.join(result_line) + '\n')
        
    def age_gender_year_process(self):

        self.get_age_data()

        self.get_dead_data([0,3,4,5])

        print('Processing data...')

        for line in tqdm(self.data):

            year, gender, age, N = line

            age_name = self.age[age]

            gender_name = '男' if gender == '1' else '女'

            if age_name not in self.result:
                self.result[age_name] = {}
                self.result[age_name]['男'] = {}
                self.result[age_name]['女'] = {}
                

            if year not in self.result[age_name][gender_name]:
                self.result[age_name][gender_name][year] = int(N)
            else:
                self.result[age_name][gender_name][year]+= int(N)

        # save result

        print('Writing result...')

        result_file = './result.csv'

        with open(result_file, 'w', encoding='utf-8') as file:

            file.write('age,gender,' + ','.join(str(x) for x in range(self.start, self.end+1)) + '\n')

            for age in tqdm(self.result):

                for gender in ['男','女']:

                    result_line = []

                    for year in range(self.start, self.end+1):
                        if str(year) in self.result[age][gender]:
                            result_line.append(str(self.result[age][gender][str(year)]))
                        else:
                            result_line.append('0')

                    file.write(age + ',' + gender + ',' + ','.join(result_line) + '\n')



if __name__ == '__main__':
    DR = DeadReason()
    # DR.cause_year_process()
    # DR.pos_year_process()
    DR.age_gender_year_process()

    print('Done.')
