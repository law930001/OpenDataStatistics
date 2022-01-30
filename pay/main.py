import xml.etree.ElementTree as ET
from tqdm import tqdm

def main():
    tree = ET.parse('pay.xml')
    root = tree.getroot()

    result = {}
    time_all = []

    for row in tqdm(root):

        time = 0

        for child in row:
            if child.tag == '年月別_Year_and_onth' and len(child.text) == 4:
                break

            if child.tag == '年月別_Year_and_onth' and len(child.text) == 6:
                time = child.text
                time = time[:4] + '/' + time[4:]
                time_all.append(time)
                continue

            job, pay = child.tag.split('_')[0], child.text

            if job not in result:
                result[job] = {}

            if time not in result[job]:
                pay = '0' if pay == '-' else pay
                result[job][time] = int(pay)
            else:
                result[job][time] += int(pay)

    print("Get data")

    # write result

    result_dir = './result.csv'

    with open(result_dir, 'w', encoding='utf-8') as file:

        file.write('職業,' + ','.join(time_all) + '\n')

        for job in result:
            
            pay = [result[job][time] for time in result[job]]

            file.write(job + ',' + ','.join([str(x) for x in pay]) + '\n')

            





if __name__ == "__main__":
    main()
    print('Done.')