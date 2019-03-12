import pandas as pd

from .Validator import Validator

class Model:

    N = 0
    deleteNumber = '-32768'
    sep = ',,'

    def __init__(self, N = 50, deleteNum=-32768, v = 1, sep = ',,'):
        self.N = N
        self.speedLimit = v

        self.deleteNumber = self.iniDeleteNumber(deleteNum)
        self.sep = sep

    def iniDeleteNumber(self, deleteNum) -> str:
        if ( type(deleteNum) == type('str')):
            return deleteNum

        return str(deleteNum)

    def getDeleteNumber(self) -> str:
        return self.deleteNumber

    def setSpeedLimit(self, speedLimit):
        self.speedLimit = speedLimit

    def setDeleteNum(self, deleteNum):
        self.deleteNumber = self.iniDeleteNumber( deleteNum )

    def readCsv(self, file : str, names : list) -> pd.DataFrame:
        return pd.read_csv( file, sep= self.sep, engine="python", names=names)

    def setTwoFiles(self, fileData : str, fileRef : str) -> bool:

        if Validator.fileExist(fileRef) and Validator.fileExist(fileData):
            self.fileData = fileData
            self.fileRef = fileRef

            return True

        return False


    def fromTwoFiles(self, fileData : str, fileRef : str, fileSave : str = 'ret.txt'):

        if ( Validator.fileExist(fileRef) == False ):
            raise FileExistsError("Файл[REF] '%s' не найден" % fileRef)

        if ( Validator.fileExist(fileData) == False ):
            raise FileExistsError("Файл[DATA] '%s' не найден" % fileData)


        refFrame = self.readCsv(fileRef, [ "id", "latitude", "longitude", "distance", "speed", "maxDepth", "depth"])
        datFrame = self.readCsv(fileData, [ 'U', 'V', 'W', 'Db'])

        with open(fileSave, 'w') as f:
            for i in range(refFrame.count()[0]):
                u =     datFrame.at[i, 'U'].split(',')
                v =     datFrame.at[i, 'V'].split(',')
                w =     datFrame.at[i, 'W'].split(',')
                db =    datFrame.at[i, 'Db'].split(',')

                item = refFrame.at[i, 'depth'].split(',')
                speed = refFrame.at[i, 'speed']


                if ( Validator.ValidLen( self.N, [ u, v, w, db]) == False):
                    print("Skip row at line {} [{} {} {} {} | N = {}]".format(
                        i, len(u),len(v),len(w),len(db), self.N))
                    continue

                if ( Validator.ValidSpeed(speed, self.speedLimit) == False ):
                    continue


                for j in range(len(item)):

                    if ( Validator.InvalidNumber(self.getDeleteNumber(), [ u[j],v[j], w[j], db[j]]) ):
                        continue

                    print(refFrame.at[i, 'id'],
                          refFrame.at[i, 'latitude'],
                          refFrame.at[i, 'longitude'],
                          refFrame.at[i, 'distance'],
                          speed,
                          refFrame.at[i, 'maxDepth'],
                          item[j], u[j], v[j], w[j],db[j],
                          file=f)




