from enum import Enum

class Labels(Enum):
    dev = 'dev'
    hw = 'hw'
    edu = 'edu'
    docs = 'docs'
    web = 'web'
    data = 'data'
    uncertain = 'other'

    @staticmethod
    def toArray():
        return [Labels.dev,
                Labels.hw,
                Labels.edu,
                Labels.docs,
                Labels.web,
                Labels.data,
                Labels.uncertain]