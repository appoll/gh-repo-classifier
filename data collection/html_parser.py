import re

SIMILAR_RESULTS_COUNT = 10

dev_files = []
dev_files.append(open('dev/spring-projects_spring-boot.html', 'r'))
dev_files.append(open('dev/facebook_react.html', 'r'))
dev_files.append(open('dev/nodegit_nodegit.html', 'r'))
dev_files.append(open('dev/scipy_scipy.html', 'r'))

dev_repos_urls = open('dev/dev_repos_urls.txt', 'w')
dev_repos_names = open('dev/dev_repos_names.txt', 'a')


matching_urls = re.compile("data-ng-href=\"(.*)\" target")
matching_similarity = re.compile("Similarity: (0|[1-9][0-9]*)")

for file in dev_files:
    lines = file.readlines()
    file.close()
    count = 0
    for line in lines:
        url = matching_urls.search(line)
        similarity = matching_similarity.search(line)
        if url != None:
            url = url.group(1)
            dev_repos_urls.write(url)
            dev_repos_urls.write('\n')
            if count < SIMILAR_RESULTS_COUNT:
                split = url.split("/")
                dev_repos_names.write(split[3] + "/" + split[4])
                dev_repos_names.write('\n')
                count+=1
       # if (similarity != None):
       #    print similarity.group(1)
