import datetime

__author__ = 'Aleksey Galkin'

Mouths = {b'Jan.': 1,
          b'Febr.': 2,
          b'Mars': 3,
          b'April': 4,
          b'May': 5,
          b'Juni': 6,
          b'Juli': 7,
          b'Aug.': 8,
          b'Sept': 9,
          b'Oct.': 10,
          b'Nov.': 11,
          b'Dec.': 12}

Cameras = {'4278': ((5, 1), (1, 0)),
           '5577': ((4, 1), (1, 1)),
           '4861': ((3, 1), (1, 0)),
           '6300': ((5, 1), (1, 0))}


def readFile1():
    file = open('LOVOZERO', 'rb')
    year, mouth, day = -1, -1, -1
    for line in file:
        mas = line.rstrip().split()
        if not mas:
            continue
        elif mas[0] == b'Year':
            year = int(mas[2])
            if mas[3] in Mouths:
                mouth = Mouths[mas[3]]
                day = int(mas[4])
            continue
        elif mas[0] == b'Hour':
            continue
        elif year == -1 or mouth == -1:
            continue
        else:
            if len(mas) == 4:
                hour = int(mas[0])
                minute = int(mas[1])
                az = float(mas[2])
                yield datetime.datetime(year, mouth, day, hour, minute), az
            elif len(mas) == 5:
                hour = int(mas[0])
                minute = int(mas[1])
                az = float(mas[2] + mas[3])
                yield datetime.datetime(year, mouth, day, hour, minute), az


class Data(list):
    def az(self, index):
        return self[index][0]

    def exp(self, index):
        return self[index][1]

    def gain(self, index):
        return self[index][2]


def readFile2():
    res = {}
    print('Read lovdat.txt...')
    names = open('lovdat.txt').readline().rstrip().split()
    for i, name in enumerate(names):
        data = Data([])
        file = open('lovdat.txt')
        next(file)
        for line in file:
            mas = line.rstrip().split()
            if not mas:
                continue
            az = float(mas[0])
            e = int(mas[i * 2 + 1])
            g = int(mas[i * 2 + 2])
            data.append((az, e, g))
        res[name] = data
    return res


def calculate1():
    lovdat = readFile2()
    for name in lovdat:
        resultfile = open('cal{0}.txt'.format(name), 'w')
        print('Create file cal{0}.txt...'.format(name))
        data = lovdat[name]
        lovozero = readFile1()
        oldexp, oldgain = 1, 1
        while True:
            try:
                dt0, az0 = next(lovozero)
                dt1, az1 = next(lovozero)
            except StopIteration:
                break

            exp, gain = 1, 1

            if data.az(-1) > az0:
                exp = data.exp(-1)
                gain = data.gain(-1)
            elif data.az(0) < az0:
                exp = data.exp(0)
                gain = data.gain(0)
            else:
                if az1 - az0 > 0:
                    for i in reversed(range(1, len(data))):
                        if data.az(i) < az0 < data.az(i - 1):
                            exp = data.exp(i - 1)
                            gain = data.gain(i - 1)
                elif az1 - az0 < 0:
                    for i in range(len(data) - 1):
                        if data.az(i) > az0 > data.az(i + 1):
                            exp = data.exp(i)
                            gain = data.gain(i)

            if (exp == 1 and gain == 1) or (exp == oldexp and gain == oldgain):
                continue

            oldexp, oldgain = exp, gain

            line = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t'.format(dt0.month, dt0.day, dt0.hour, dt0.minute, exp, gain)

            if name in Cameras:
                on, off = Cameras[name]
            else:
                on, off = (1, 1), (0, 1)

            res = on if exp > 0 else off
            line += '{0}\t{1}'.format(*res)

            print(line, file=resultfile)
    print('End')


def calculate2():
    lovdat = readFile2()
    oldExps, oldGains, resultfiles = {k: 1 for k in lovdat}, {k: 1 for k in lovdat}, \
                                     {k: open('cal{0}.txt'.format(k), 'w') for k in lovdat}
    lovozero = readFile1()
    while True:
        try:
            dt0, az0 = next(lovozero)
            dt1, az1 = next(lovozero)
        except StopIteration:
            break

        exp, gain = 1, 1

        for name in lovdat:
            data = lovdat[name]
            if data.az(-1) > az0:
                exp = data.exp(-1)
                gain = data.gain(-1)
            elif data.az(0) < az0:
                exp = data.exp(0)
                gain = data.gain(0)
            else:
                if az1 - az0 > 0:
                    for i in reversed(range(1, len(data))):
                        if data.az(i) < az0 < data.az(i - 1):
                            exp = data.exp(i - 1)
                            gain = data.gain(i - 1)
                elif az1 - az0 < 0:
                    for i in range(len(data) - 1):
                        if data.az(i) > az0 > data.az(i + 1):
                            exp = data.exp(i)
                            gain = data.gain(i)

            if (exp == 1 and gain == 1) or (exp == oldExps[name] and gain == oldGains[name]):
                continue

            oldExps[name], oldGains[name] = exp, gain

            line = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t'.format(dt0.month, dt0.day, dt0.hour, dt0.minute, exp, gain)

            if name in Cameras:
                on, off = Cameras[name]
            else:
                on, off = (1, 1), (0, 1)

            res = on if exp > 0 else off
            line += '{0}\t{1}'.format(*res)

            print(line, file=resultfiles[name])


import time

def startCalCal(func):
    start = time.clock()
    func()
    print('{0} time:'.format(func.__name__), time.clock() - start)


#startCalCal(calculate1)
startCalCal(calculate2)

