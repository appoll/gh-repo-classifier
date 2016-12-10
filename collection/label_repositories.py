import webbrowser
import numpy as np

#from labels import Labels


class RepoLabelling():

    def __init__(self, browser_type = 'firefox', file_name = 'test_url.txt'):
        self. browser = webbrowser.get(browser_type)
        self.url_handler = URLFileHandler(file_name)


    def open_next_page(self):
        url = self.url_handler.nextUrl()
        #TODO handle empty urls
        self.browser.open_new(url)


    def browse_url_file(self):
        print self.urls


class URLFileHandler(object):

    def __init__(self, filename):
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
        if  self.url_list:
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
    labelling = RepoLabelling(file_name="test_url_test.txt")
    labelling.open_next_page()
    # labelling.browse_url_file()
    # labelling.open_page("http://www.google.de")
    # handler = URLFileHandler("test_url_test.txt")
    # handler.nextUrl()