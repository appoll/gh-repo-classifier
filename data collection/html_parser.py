import re

#repo_spring_boot = open('dev/spring-projects_spring-boot.html', 'r')
#repo_spring_boot = open('dev/facebook_react.html', 'r')
#repo_spring_boot = open('dev/nodegit_nodegit.html', 'r')
repo_spring_boot = open('dev/scipy_scipy.html', 'r')

lines = repo_spring_boot.readlines()
repo_spring_boot.close()

matching_urls = re.compile("data-ng-href=\"(.*)\" target")
matching_similarity = re.compile("Similarity: (0|[1-9][0-9]*)")

urls = []
for line in lines:
    url = matching_urls.search(line)
    similarity = matching_similarity.search(line)
    if url != None:
        print url.group(1)
    if (similarity != None):
        print similarity.group(1)
