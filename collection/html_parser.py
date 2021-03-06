import re
from labels import Labels

SIMILAR_RESULTS_COUNT = 10


def read_and_store_repo_names(files, label):
    repos_urls = label + "/" + label + "_repos_urls.txt"
    repos_names = label + "/" + label + "_repos_names.txt"

    file_repos_urls = open(repos_urls, 'w')
    file_repos_names = open(repos_names, 'w')

    for file in files:
        lines = file.readlines()
        file.close()
        count = 0
        for line in lines:
            url = matching_urls.search(line)
            similarity = matching_similarity.search(line)
            if url != None:
                url = url.group(1)
                file_repos_urls.write(url)
                file_repos_urls.write('\n')
                if count < SIMILAR_RESULTS_COUNT:
                    split = url.split("/")
                    file_repos_names.write(split[3] + "/" + split[4])
                    file_repos_names.write('\n')
                    count += 1
                    # if (similarity != None):
                    #    print similarity.group(1)


# dev_files = []
# dev_files.append(open('dev/spring-projects_spring-boot.html', 'r'))
# dev_files.append(open('dev/facebook_react.html', 'r'))
# dev_files.append(open('dev/nodegit_nodegit.html', 'r'))
# dev_files.append(open('dev/scipy_scipy.html', 'r'))
#
# hw_files = []
# hw_files.append(open('hw/m2mtech_calculator-2015.html', 'r'))
# hw_files.append(open('hw/bcaffo_751and2.html', 'r'))
#
# edu_files = []
# edu_files.append(open('edu/DataScienceSpecialization_courses.html', 'r'))
# edu_files.append(open('edu/githubteacher_intro-november-2015.html', 'r'))
# edu_files.append(open('edu/alex_what-happens-when.html', 'r'))
# edu_files.append(open('edu/MostlyAdequate_mostly-adequate-guide.html', 'r'))
# edu_files.append(open('edu/AllThingsSmitty_jquery-tips-everyone-should-know.html', 'r'))

# docs_files = []
# docs_files.append(open('docs/bundestag_gesetze.html', 'r'))
# docs_files.append(open('docs/fsr-itse_docs.html', 'r'))
# docs_files.append(open('docs/raspberrypi_documentation.html', 'r'))
# docs_files.append(open('docs/github_maturity-model.html', 'r'))
# docs_files.append(open('docs/CMSgov_HealthCare.gov-Styleguide.html', 'r'))

web_files = []
web_files.append(open('web/ianli_elbowpatched-boilerplate.html', 'r'))
web_files.append(open('web/BloombergMedia_whatiscode.html', 'r'))


data_files = []
data_files.append(open('data/ericfischer_housing-inventory.html', 'r'))
data_files.append(open('data/GSA_data.html', 'r'))
data_files.append(open('data/OpenExoplanetCatalogue_open_exoplanet_catalogue.html', 'r'))
data_files.append(open('data/Hipo_university-domains-list.html', 'r'))
data_files.append(open('data/minimaxir_big-list-of-naughty-strings.html', 'r'))

matching_urls = re.compile("data-ng-href=\"(.*)\" target")
matching_similarity = re.compile("Similarity: (0|[1-9][0-9]*)")

read_and_store_repo_names(data_files, Labels.data)
