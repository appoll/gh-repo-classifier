import webbrowser
import numpy as np

from collection.labels import Labels
import os


class RepoLabelling():
    def __init__(self, browser_type='firefox', file_name='test_url.txt'):
        print webbrowser._browsers
        self.browser = webbrowser.get(browser_type)
        self.url_handler = URLFileHandler(file_name)

    def open_next_page(self):
        url = self.url_handler.nextUrl()
        # due to previously stored names, the above is not a url but a user/repo
        # TODO handle empty urls
        github_url = "https://github.com/%s" % url
        self.browser.open_new(github_url)

    def browse_url_file(self):
        print self.urls

    def print_selection(self):
        labels = Labels.toArray()
        for i, label in enumerate(labels):
            print "[ " + str(i + 1) + " ]", label
        chosen_label = self.parse_input()

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


class URLFileHandler(object):
    def __init__(self, filename):
        if not os.path.exists(filename):
            raise Exception("File %s should exist!" % filename)

        self.url_list = self.read_file(filename)
        self.file_writer = open(filename, 'wb')

    def read_file(self, filename):

        with open(filename, 'rb') as reader:
            urls = [line.rstrip('\n') for line in reader]
        return urls

    def update_file(self):
        # self.file_writer.writelines("%s\n" % l for l in self.url_list)
        self.file_writer.write('\n'.join(self.url_list))

    def nextUrl(self):
        if self.url_list:
            print len(self.url_list)
            current_url = self.url_list.pop(0)
            print current_url, self.url_list
            self.update_file()
            return current_url
        else:
            return None

    def __del__(self):
        self.file_writer.close()


if __name__ == '__main__':
    labelling = RepoLabelling('./web/web_repos_names_github.io.txt')
    labelling.print_selection()
    # labelling.open_next_page()
    # labelling.browse_url_file()
    # labelling.open_page("http://www.google.de")
    # handler = URLFileHandler("test_url_test.txt")
    # handler.nextUrl()
