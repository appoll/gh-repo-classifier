import os
import webbrowser

from collection.labels import Labels
from config.helper import Helper


class RepoLabelling():
    def __init__(self, browser_type='firefox', file_name='test_url_test.txt'):
        self.browser = webbrowser.get(browser_type)
        self.url_handler = URLFileHandler(file_name)

        self.url_to_store = "initial_url_dummy"
        self.output_file = "hw.txt"
        # if not os.path.exists(os.path.dirname(self.output_file)):
        #     os.makedirs(os.path.dirname(self.output_file))

    def open_next_page(self, url):
        # url = self.url_handler.nextUrl()
        print url
        # due to previously stored names, the above is not a url but a user/repo
        # TODO handle empty urls
        github_url = "https://github.com/%s" % url
        self.url_to_store = github_url
        self.browser.open_new(github_url)

    def browse_url_file(self):
        print self.urls

    def print_selection(self):
        labels = Labels.toArray()
        for i, label in enumerate(labels):
            print "[ " + str(i + 1) + " ]", label
        chosen_label = self.parse_input()

        f = open(self.output_file, 'a')
        line = self.url_to_store + " " + chosen_label.value + '\n'
        f.write(line)
        f.close()

    def parse_input(self):
        while True:
            input = raw_input("Choose one repository type: ")
            if input == "1":
                return Labels.dev
            elif input == "2":
                return Labels.hw
            elif input == "3":
                return Labels.edu
            elif input == "4":
                return Labels.docs
            elif input == "5":
                return Labels.web
            elif input == "6":
                return Labels.data
            elif input == "7":
                return Labels.uncertain
            else:
                print "Wrong input"

    def update_existing(self):
        file = open(self.output_file, 'r')
        lines = file.readlines()
        for line in lines:
            repo_link = line.split(" ")[0]
            assigned_label = line.split(" ")[1].rstrip('\n')

            labelled_class = open("labelled_%s" % assigned_label, 'a')
            labelled_class.write(Helper().build_repo_name_from_repo_link(repo_link) + '\n')

class URLFileHandler(object):
    def __init__(self, filename):
        if not os.path.exists(filename):
            raise Exception("File %s should exist!" % filename)

        self.url_list = self.read_file(filename)
        # self.file_writer = open(filename, 'wb')

    def read_file(self, filename):

        with open(filename, 'rb') as reader:
            urls = [line.rstrip('\n') for line in reader]
        return urls

    def update_file(self):
        pass
        # self.file_writer.writelines("%s\n" % l for l in self.url_list)
        # self.file_writer.write('\n'.join(self.url_list))

    def nextUrl(self):
        if self.url_list:
            print len(self.url_list)
            current_url = self.url_list.pop(0)
            print current_url, self.url_list
            self.update_file()
            return current_url
        else:
            return None


def label(labelling):
    while True:
        lines = open(labelling.output_file, 'r').readlines()
        validated = False
        url = labelling.url_handler.nextUrl()
        if url is None:
            print 'You are awesome, the list is empty!'
            break
        for line in lines:
            if url in line:
                print '%s already validated.' % url
                validated = True
                break
        if not validated:
            labelling.open_next_page(url)
            labelling.print_selection()


if __name__ == '__main__':
    labelling = RepoLabelling()

    # label(labelling)

    labelling.update_existing()