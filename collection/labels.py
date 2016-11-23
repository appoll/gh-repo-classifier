from enum import Enum

class Labels(Enum):
    dev = 'dev'
    hw = 'hw'
    edu = 'edu'
    docs = 'docs'
    web = 'web'
    data = 'data'

    @staticmethod
    def toArray():
        return [Labels.dev.value,
                Labels.hw.value,
                Labels.edu.value,
                Labels.docs.value,
                Labels.web.value,
                Labels.data.value]