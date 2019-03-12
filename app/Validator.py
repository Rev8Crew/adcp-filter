from pathlib import Path

class Validator:

    @staticmethod
    def ValidSpeed( iniSpeed, minSpeed):
        if ( iniSpeed < minSpeed):
            return False

        return True

    @staticmethod
    def ValidLen( neededLen : int, params: list):

        for item in params:
            if len(item) != neededLen:
                return False

        return True

    @staticmethod
    def InvalidNumber( invalid : str, params : list ):

        for item in params:
            if ( item == invalid):
                return True

        return False

    @staticmethod
    def fileExist( filePath : str):
        return Path(filePath).is_file()