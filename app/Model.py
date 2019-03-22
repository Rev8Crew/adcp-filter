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
    def get_key_round(key):


        if isinstance(key, float):
            return round(key)

        if isinstance(key, str):
            print('convert')
            return int(float(key.strip()))

        return int(key)

    def add_to_average(self, key, u, v, w, db):
        print(key, type(key))
        key = self.get_key_round(key)
        if key not in self.average_arr.keys():
            self.average_arr[key] = [u, v, w, db]

        self.average_arr[key].append([u, v, w, db])

    def get_average(self, key):
        key = self.get_key_round(key)
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

        if print_depth is False:
            depth = ''

        def print_float_count(fl):
            return float("{0:.3f}".format(fl)) if isinstance(fl, float) else "{}".format(fl)

        print(ref_frame.at[i, 'id'],
              ref_frame.at[i, 'latitude'],
              ref_frame.at[i, 'longitude'],
              ref_frame.at[i, 'distance'],
              ref_frame.at[i, 'speed'],
              depth, print_float_count(u), print_float_count(v), print_float_count(w), print_float_count(db),
              file=f)

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
            count = 0

            file_count = 0
            for i in range(ref_frame.count()[0]):
                u = dat_frame.at[i, 'U'].split(',')
                v = dat_frame.at[i, 'V'].split(',')
                w = dat_frame.at[i, 'W'].split(',')
                db = dat_frame.at[i, 'Db'].split(',')

                item = ref_frame.at[i, 'depth'].split(',')
                speed = ref_frame.at[i, 'speed']

                if Validator.ValidLen(self.N, [u, v, w, db]) is False:
                    print("Skip row at line {} [{} {} {} {} | N = {}]".format(
                        i, len(u), len(v), len(w), len(db), self.N))
                    continue

                if Validator.ValidSpeed(speed, self.speedLimit) is False:
                    continue

                for j in range(len(item)):

                    if Validator.InvalidNumber(self.get_delete_number(), [u[j], v[j], w[j], db[j]]):
                        continue

                    if self.average:
                        #item[j] - глубина
                        self.add_to_average(item[j], u[j], v[j], w[j], db[j])
                    else:
                        self.print_to_file(i, ref_frame, u[j], v[j], w[j], db[j], f, True)

                count += 1

                if count == self.average and self.average:
                    file_count += 1

                    final_array = list([0, 0, 0, 0])
                    for j in range(len(item)):
                        final_array = self.get_average(item[j])
                        self.print_to_file(file_count, ref_frame, final_array[0], final_array[1],
                                           final_array[2], final_array[3], f)

                    count = 0
                    self.ini_average()

            if count:
                file_count += 1

                for j in range(len(item)):
                    final_array = self.get_average(item[j])
                    self.print_to_file(file_count, ref_frame, final_array[0], final_array[1],
                                       final_array[2], final_array[3], f)

        return Validator.fileExist(file_save)
