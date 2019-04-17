import pandas as pd

from .Validator import Validator


class Model:
    N = 0
    deleteNumber = '-32768'
    sep = ',,'

    def __init__(self, n=50, delete_num=-32768, v=1, sep=',,', average: int = 0):
        self.N = n
        self.speedLimit = v

        self.deleteNumber = self.check_delete_num(delete_num)
        self.sep = sep

        self.fileData = ""
        self.fileRef = ""

        self.average = average

    @staticmethod
    def check_delete_num(delete_num) -> str:
        if isinstance(delete_num, str):
            return delete_num

        return str(delete_num)

    def get_delete_number(self) -> str:
        return self.deleteNumber

    def set_average_num(self, num):
        self.average = int(float(num))

    def set_speed_limit(self, speed_limit):
        self.speedLimit = int(float(speed_limit))

    def set_delete_num(self, delete_num):
        self.deleteNumber = self.check_delete_num(delete_num)

    def read_file(self, file: str, names: list) -> pd.DataFrame:
        return pd.read_csv(file, sep=self.sep, engine="python", names=names)

    def set_two_files(self, file_data: str, file_ref: str) -> bool:

        if Validator.fileExist(file_ref) and Validator.fileExist(file_data):
            self.fileData = file_data
            self.fileRef = file_ref

            return True

        return False

    def ini_average(self):
        self.average_arr = {}

    @staticmethod
    def lineplot(x_data, y_data, x_label="", y_label="", title=""):

        import matplotlib.pyplot as plt

        # Create the plot object
        _, ax = plt.subplots()

        # Plot the best fit line, set the linewidth (lw), color and
        # transparency (alpha) of the line
        ax.plot(x_data, y_data, lw=2, color='#539caf', alpha=1)

        # Label the axes and provide a title
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        plt.show()


    @staticmethod
    def get_key_round(key):

        if isinstance(key, float):
            return round(key)

        if isinstance(key, str):
            return int(float(key.strip()))

        return int(key)

    def add_to_average(self, key, u, v, w, db):
        key = self.get_key_round(key)
        if key not in self.average_arr.keys():
            self.average_arr[key] = [[u, v, w, db]]
            return;

        self.average_arr[key].append([u, v, w, db])

    def get_average(self, key):
        key = self.get_key_round(key)

        if key not in self.average_arr.keys():
            return False

        u = 0
        v = 0
        w = 0
        db = 0

        ln = len(self.average_arr[key])

        for item in self.average_arr[key]:

            u += float(item[0]) / ln
            v += float(item[1]) / ln
            w += float(item[2]) / ln
            db += float(item[3]) / ln

        return [u, v, w, db]

    @staticmethod
    def print_to_file(i, ref_frame, u, v, w, db, f, print_depth=False):
        depth = ref_frame.at[i, 'maxDepth']

        if print_depth:
            depth = print_depth

        def print_float_count(fl):
            return float("{0:.3f}".format(fl)) if isinstance(fl, float) else "{}".format(fl)

        print(ref_frame.at[i, 'id'],
              ref_frame.at[i, 'latitude'],
              ref_frame.at[i, 'longitude'],
              ref_frame.at[i, 'distance'],
              ref_frame.at[i, 'speed'],
              depth, print_float_count(u), print_float_count(v), print_float_count(w), print_float_count(db),
              file=f)

    def get_real_vector(self, file='ret.txt'):

        import math
        dat_frame = pd.read_csv(file, sep=' ', names=['id', 'lat', 'long', 'dist', 'speed', 'depth', 'u', 'v', 'w', 'db' ])

        print(dat_frame)

        d = {}
        dept = {}
        for i in range(dat_frame.count()[0]):
            dist = dat_frame.at[i, 'dist']
            speed = dat_frame.at[i, 'speed']
            depth = dat_frame.at[i, 'depth']

            u = float(dat_frame.at[i, 'u'])
            v = float(dat_frame.at[i, 'v'])
            w = float(dat_frame.at[i, 'w'])
            db = float(dat_frame.at[i, 'db'])

            if dist not in d.keys():
                angle = 0

                if u > 1.0 and v > 1.0:
                    angle = math.atan( v / u)
                elif u > 1.0 and v < 1.0:
                    angle = 90.0 + math.atan( abs(v) / u)
                elif u < 1.0 and v < 1.0:
                    angle = 180.0 + math.atan(abs(v) / abs(u))
                elif u < 1.0 and v > 1.0:
                    angle = 270.0 + math.atan(v / abs(u))

                d[dist] = [math.sqrt( u** 2 + v** 2), angle]
                dept[depth] = [math.sqrt(u ** 2 + v ** 2), angle]

        for item in d.keys():
            print("{}: Real:[{}] | Angle:[{}]".format(item, d[item][0], d[item][1]))

        self.lineplot( d.keys(), [d[x][0] for x in d.keys()] , "Distance", "Speed", "Real components")
        self.lineplot(dept.keys(), [d[x][0] for x in dept.keys()], "depth", "Speed", "Real components")

    def from_two_files(self, file_data: str = '', file_ref: str = '', file_save='ret.txt'):

        if file_data == '':
            file_data = self.fileData
            print('[Q] file_data is %s' % file_data)

        if file_ref == '':
            file_ref = self.fileRef
            print('[Q] file_ref is %s' % file_ref)

        if Validator.fileExist(file_ref) is False:
            raise FileExistsError("Файл[REF] '%s' не найден" % file_ref)

        if Validator.fileExist(file_data) is False:
            raise FileExistsError("Файл[DATA] '%s' не найден" % file_data)

        ref_frame = self.read_file(file_ref, ["id", "latitude", "longitude", "distance", "speed", "maxDepth", "depth"])
        dat_frame = self.read_file(file_data, ['U', 'V', 'W', 'Db'])

        with open(file_save, 'w') as f:
            self.ini_average()

            #Для подсчета осреднения
            count = 0

            # Номер который будет записан в файле если есть осреднение
            file_count = 0
            for i in range(ref_frame.count()[0]):

                # Компонента потока U
                u = dat_frame.at[i, 'U'].split(',')
                # Компонента потока V
                v = dat_frame.at[i, 'V'].split(',')
                # Компонента потока W
                w = dat_frame.at[i, 'W'].split(',')
                # Уровень сигнала
                db = dat_frame.at[i, 'Db'].split(',')

                # Разбиение по глубине
                item = ref_frame.at[i, 'depth'].split(',')
                # Фильтр по скорости лодки
                speed = ref_frame.at[i, 'speed']

                if Validator.ValidLen(self.N, [u, v, w, db]) is False:
                    print("Skip row at line {} [{} {} {} {} | N = {}]".format(
                        i, len(u), len(v), len(w), len(db), self.N))
                    continue

                if Validator.ValidSpeed(speed, self.speedLimit) is False:
                    continue

                # Для каждой ячейки глубины
                for j in range(len(item)):

                    if Validator.InvalidNumber(self.get_delete_number(), [u[j], v[j], w[j], db[j]]):
                        continue

                    # Если задано усреднение то добавляем текущие значения компонентов потока U, V, W, DB
                    # Если не задано то записываем в файл сразу

                    if self.average:
                        #item[j] - глубина
                        self.add_to_average(item[j], u[j], v[j], w[j], db[j])
                    else:
                        self.print_to_file(i, ref_frame, u[j], v[j], w[j], db[j], f)

                count += 1

                if count == self.average and self.average:
                    #Осредненные компоненты
                    final_array = list([0, 0, 0, 0])
                    for j in range(len(item)):
                        final_array = self.get_average(item[j])

                        if final_array is False:
                            continue

                        self.print_to_file(file_count * self.average, ref_frame, final_array[0], final_array[1],
                                           final_array[2], final_array[3], f, print_depth=item[j])

                    file_count += 1
                    count = 0
                    self.ini_average()

            if count and self.average:
                # Осредненные компоненты
                final_array = list([0, 0, 0, 0])
                for j in range(len(item)):
                    final_array = self.get_average(item[j])

                    if final_array is False:
                        continue

                    self.print_to_file(file_count * self.average, ref_frame, final_array[0], final_array[1],
                                       final_array[2], final_array[3], f, print_depth=item[j])

        self.get_real_vector()
        return Validator.fileExist(file_save)
