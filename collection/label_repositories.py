import webbrowser
import numpy as np

#from labels import Labels


class RepoLabelling():

    def __init__(self, browser_type = 'firefox', file_name = 'test_url.txt'):
        self. browser = webbrowser.get(browser_type)
        self.file = file_name

        self.load_urls()

    def load_urls(self):
        self.urls = np.genfromtxt(self.file, dtype=None, delimiter='\n')

    def open_page(self, url):
        self.browser.open_new(url)


    def browse_url_file(self):
        print self.urls



if __name__ == '__main__':
    labelling = RepoLabelling()
    labelling.browse_url_file()
    labelling.open_page("http://www.google.de")