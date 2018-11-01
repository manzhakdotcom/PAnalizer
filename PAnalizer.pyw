import re


def get_protocol():
    with open('test/ЦУП.115') as file:
        data = []
        for line in file.readlines():
            if not re.findall('^t=|[dMhms]', line):
                data[-1][1] += line.rstrip()
            if re.findall(r'd:(\d+)', line):
                day = re.findall(r'd:(\d+)', line)[0]
            if re.findall(r'M:(\d+)', line):
                month = re.findall(r'M:(\d+)', line)[0]
            if re.findall(r'h:(\d+)', line):
                hour = re.findall(r'h:(\d+)', line)[0]
            if re.findall(r'm:(\d+)', line):
                minute = re.findall(r'm:(\d+)', line)[0]
            if re.findall(r's:(\d+)', line):
                second = re.findall(r's:(\d+)', line)[0]
            if re.findall(r'^t=([^,]+),(.+)$', line):
                station = re.findall(r'^t=([^,]+),(.+)$', line)[0][0]
                impulse = re.findall(r'^t=([^,]+),(.+)$', line)[0][1]
                data.append([station])
                data[-1].append('{} {}-{} {}:{}:{} --- {}'.format(station, month, day, hour, minute, second, impulse))

    with open('test/result', 'a') as file:
        print('================================================================================\n', file=file)
        print('ФОРМАТ ЗАПИСИ: <СТАНЦИЯ> <ГГГГ-ММ-ДД> <ЧЧ:ММ:СС> --- <СПИСОК ИМПУЛЬСОВ>\n', file=file)
        sdata = sorted(data)
        station = ''
        for line in sdata:
            if not line[0] in station:
                print('================================================================================\n', file=file)
                station = line[0]
            print(line[1], file=file)


def main():
    get_protocol()


if __name__ == '__main__':
    main()
