import json

class ExampleData:

    def __init__(self):

        self.files = [
            'DATA_big-list-of-naughty-strings_basics.txt',
            'DATA_data_basics.txt',
            'DATA_housing_basics.txt',
            'DATA_open_exoplanet_catalogue_basics.txt',
            'DATA_university-domains-list_basics.txt',
            'DEV_homeworkr_basics.txt',
            'DEV_nodegit_basics.txt',
            'DEV_react_basics.txt',
            'DEV_scipy_basics.txt',
            'DEV_spring-boot_basics.txt',
            'DOCS_docs_basics.txt',
            'DOCS_documentation_basics.txt',
            'DOCS_gesetze_basics.txt',
            'DOCS_HealthCare.gov-Styleguide_basics.txt',
            'DOCS_maturity-model_basics.txt',
            'EDU_courses_basics.txt',
            'EDU_intro-november-2015_basics.txt',
            'EDU_jquery_basics.txt',
            'EDU_mostly-adequate-guide_basics.txt',
            'EDU_what-happens-when_basics.txt',
            'HW_751and2_basics.txt',
            'HW_calculator-2015_basics.txt',
            'HW_python-homework_basics.txt',
            'HW_RottenTomatoes_basic.txt',
            #'HW_SWT16-Project-08_basics.txt',
            'WEB_elbowpatched-boilerplate_basics.txt',
            'WEB_jacerobinson8.github.io_basics.txt',
            'WEB_rubymonstas-zurich.github.io_basics.txt',
            'WEB_whatiscode_basics.txt',
            'WEB_whoisjuan.github.io_basics.txt'
        ]

        self.objects = []

        for file in self.files:
            self.objects.append((json.load(open(file)),file[:file.find('_')]))

        #print self.objects

#ExampleData()