import pandas as pd

from .Validator import Validator


class Model:
    N = 0
    deleteNumber = '-32768'
    sep = ',,'

    def __init__(self, n=50, delete_num=-32768, v=1, sep=',,', average: int = 20):
        self.N = n
        self.speedLimit = v

        self.deleteNumber = self.check_delete_num(delete_num)
        self.sep = sep

        self.fileData = ""
        self.fileRef = ""

        self.average = average

    @staticmethod
    def check_delete_num(delete_num) -> str:
        if isinstance(delete_num, int):
            return delete_num

        return str(delete_num)

    def get_delete_number(self) -> str:
        return self.deleteNumber

    def set_average_num(self, num):
        self.average = int(num)

    def set_speed_limit(self, speed_limit):
        self.speedLimit = int(speed_limit)

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

    def from_two_files(self, file_data: str, file_ref: str, file_save='ret.txt'):

        if Validator.fileExist(file_ref) is False:
            raise FileExistsError("Файл[REF] '%s' не найден" % file_ref)

        if Validator.fileExist(file_data) is False:
            raise FileExistsError("Файл[DATA] '%s' не найден" % file_data)

        ref_frame = self.read_file(file_ref, ["id", "latitude", "longitude", "distance", "speed", "maxDepth", "depth"])
        dat_frame = self.read_file(file_data, ['U', 'V', 'W', 'Db'])

        with open(file_save, 'w') as f:
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

                    print(ref_frame.at[i, 'id'],
                          ref_frame.at[i, 'latitude'],
                          ref_frame.at[i, 'longitude'],
                          ref_frame.at[i, 'distance'],
                          speed,
                          ref_frame.at[i, 'maxDepth'],
                          item[j], u[j], v[j], w[j], db[j],
                          file=f)

        return Validator.fileExist(file_save)
