import csv
import re

def main():
    data_dir = './data/data.csv'

    time_all = []

    with open(data_dir, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

        time_all = data[0][2:]

        # write result
        with open('./result.csv', 'w', encoding='utf-8') as file:

            file.write('國家,地區,' + ','.join(time_all) + '\n')

            for line in data[1:]:

                region = line[0]

                if region == '全區': continue
                region = region.replace('地區', '')

                nation = re.sub(r'\s*[A-Za-z]+\b', '' , line[1]).replace('.','')
                if '合計' in nation: continue
        
                N = [x.replace(',','') if x != '-' else '0' for x in line[2:]]

                file.write(nation + ',' + region + ',' + ','.join(N) + '\n')





if __name__ == '__main__':
    main()
    print('Done.')