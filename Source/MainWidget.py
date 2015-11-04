__author__ = 'Алексей Галкин'

import datetime
import shelve
import time

from PyQt5.QtWidgets import QWidget

from Source.ChooseCamera import ChooseCamera

Cameras = {'4278': ((5, 1), (1, 0)),
           '5577': ((4, 1), (1, 1)),
           '4861': ((3, 1), (1, 0)),
           '6300': ((5, 1), (1, 0))}

path_lovdat = 'data/lovdat'
path_LOVOZERO = 'data/LOVOZERO'


class Data(list):
    """
    производный класс от list
    каждый элемент содержит кортеж значений(угол погружения солнца, экспозиция, усиление)
    """

    def el(self, index):
        return self[index][0]

    def findEl(self, e, g):
        for el, exp, gain in self:
            if exp == e and gain == g:
                return el
        return -1

    def exp(self, index):
        return self[index][1]

    def gain(self, index):
        return self[index][2]


class DtEl:
    def __init__(self, dt, el):
        self.dt = dt
        self.el = el


def read_lovozero():
    """
    итерируемая функция, читающая файл LOVOZERO
    :return:
    при каждом вызове next возвращает кортеж значений (время, угол погружения солнца)
    """

    mouths = {b'Jan.': 1,
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

    print('Чтение файла LOVOZERO...')
    file = open(path_LOVOZERO, 'rb')
    year, mouth, day = -1, -1, -1
    for line in file:
        mas = line.rstrip().split()
        if not mas:
            continue
        elif mas[0] == b'Year':
            year = int(mas[2])
            if mas[3] in mouths:
                mouth = mouths[mas[3]]
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
                el = float(mas[2])
                yield datetime.datetime(year, mouth, day, hour, minute), el
            elif len(mas) == 5:
                hour = int(mas[0])
                minute = int(mas[1])
                el = float(mas[2] + mas[3])
                yield datetime.datetime(year, mouth, day, hour, minute), el


class MainWidget(QWidget):
    def __init__(self, QWidget_parent=None):
        QWidget.__init__(self, QWidget_parent)

        start = time.time()
        self.calculate()
        print('Time: {0} sec'.format(time.time() - start))

    def calculate(self):
        """
        вычисление календаря оптических наблюдений
        :return:
        """
        lovdat = self.read_lovdat()
        if len(lovdat):
            oldExps, oldGains, resultfiles = {k: 1 for k in lovdat}, {k: 1 for k in lovdat}, \
                                             {k: open('cal{0}.txt'.format(k), 'w') for k in lovdat}
            lovozero = read_lovozero()
            dtel0 = DtEl(*next(lovozero))
            oldLovozero = {k: dtel0 for k in lovdat}
            while True:
                try:
                    dt1, el1 = next(lovozero)
                except StopIteration:
                    break

                for cam_name in lovdat:
                    exp, gain, dt0, el0 = 1, 1, oldLovozero[cam_name].dt, oldLovozero[cam_name].el
                    data = lovdat[cam_name]
                    if data.el(-1) > el0:
                        exp = data.exp(-1)
                        gain = data.gain(-1)
                    elif data.el(0) < el0:
                        exp = 0
                        gain = 0
                    else:
                        if el1 - el0 > 0:
                            for i in reversed(range(1, len(data))):
                                if data.el(i) < el0 < data.el(i - 1):
                                    exp = data.exp(i - 1)
                                    gain = data.gain(i - 1)
                                    break
                        elif el1 - el0 < 0:
                            for i in range(len(data) - 1):
                                if data.el(i) > el0 > data.el(i + 1):
                                    exp = data.exp(i)
                                    gain = data.gain(i)
                                    break

                    if (exp == 1 and gain == 1) or (exp == oldExps[cam_name] and gain == oldGains[cam_name]):
                        oldLovozero[cam_name] = DtEl(dt1, el1)
                        continue

                    oldExps[cam_name], oldGains[cam_name] = exp, gain

                    el = data.findEl(exp, gain)
                    if abs(el) - abs(el0) > abs(el) - abs(el1):
                        dt0 = dt1

                    line = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t'.format(dt0.month, dt0.day, dt0.hour, dt0.minute, exp, gain)

                    if cam_name in Cameras:
                        on, off = Cameras[cam_name]
                    else:
                        on, off = (1, 1), (0, 1)

                    res = on if exp > 0 else off
                    line += '{0}\t{1}'.format(*res)

                    print(line, file=resultfiles[cam_name])

                    oldLovozero[cam_name] = DtEl(dt1, el1)
        print('Готово')

    def read_lovdat(self):
        """
        читаем lovdat, который содержит параметры камер
        :return:
        """
        res = {}
        print('Чтение файла lovdat...')
        with shelve.open(path_lovdat) as db:
            names = list(db.keys())
            # Form
            choose = ChooseCamera(names.copy(), self)
            choose.exec()
            #########
            for name in choose.cameras:
                if name in db:
                    res[name] = db[name]
        return res
