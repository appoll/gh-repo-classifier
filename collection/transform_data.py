import glob
import json
import os

import requests
from requests.auth import HTTPBasicAuth

#from config.reader import ConfigReader

# class that reads json files associated with repositories and transforms
# a given value of the object into a numerical value
class UrlToNumeric:

    def __init__(self):
        #self.username, self.password = ConfigReader().getCredentials()
        self.username = 'appoll'
        self.password = 'Menth00Lgithub' 
        self.repos_folder = "../collection/%s/repos/"
        self.updated_repos_folder = "../collection/%s/updated_repos/"
        
    def branchCount(self, label):
        folder = self.repos_folder % label

        for filename in glob.glob(folder+'*'):
            f = open (filename, 'r')
            repoObject = json.load(f)
            f.close()
            branches_url = repoObject["branches_url"]
            #del repoObject[branches_url]
            branches_url = branches_url.split('{')[0]
            print branches_url
            r = requests.get(branches_url, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                    branchesObject = json.dumps((r.json()))
                    branches_count = len(branchesObject)
                    print branches_count
                    repoObject["branches_count"]  = branches_count
                    new_filename = filename.replace("repos", "updated_repos")
                    if not os.path.exists(os.path.dirname(new_filename)):
                        os.makedirs(os.path.dirname(new_filename))
                    with open(new_filename, 'w') as file:
                        print "Writing to %s" % file.name
                        file.write(repoObject)
                        file.close()
            else :
                print r
feature_converter = UrlToNumeric()
feature_converter.branchCount('dev')


