
``Github Repository Classifier``
============
The ``GitHub Repository Classifier`` is a python project developed for the 
[InformatiCup2017](https://github.com/InformatiCup/InformatiCup2017). It is using different
machine learning methods to automatically classify GitHub repositories into one of the following
classes:
- **DEV**: repositories used for development of tools, components, applications or APIs
- **HW**: repositories used for homework, assignments and other course-related work
- **EDU**: repositories used to host tutorials, lectures, educational information and code related to teaching
- **DOCS**: repositories used for tracking and storing non-educational documents
- **WEB**: repositories used to host static personal websites or blogs
- **DATA**: repositories used to store data sets
- **OTHER**: repositories with no strong correlation to any of the previous categories (e.g. empty repositories)

It runs via the command line, taking as input a text file of GitHub repository links.


Dependencies
------------
The projected was tested on Ubuntu 14.04 and requires Python 2.7. The required python packages can be installed via pip:
```
$ pip install -r requirements.txt
```

#### Troubleshooting:
If the installation of ``lxml`` failes, make sure that you have the required libraries installed:
```
$ sudo apt-get install libxml2-dev libxslt1-dev python-dev
```

Running the classification
-------------
For starting the classification, go into the prediction folder and run the input processor script
```
$ cd prediction
$ python input_processor.py input_urls.txt output.txt
```
Define in ```input_urls.txt``` the GitHub repositories you want to classify in the following way:
```
https://github.com/briantemple/homeworkr
https://github.com/spez/RottenTomatoes
https://github.com/DataScienceSpecialization/courses
https://github.com/bundestag/gesetze
https://github.com/BloombergMedia/whatiscode
https://github.com/ericfischer/housing-inventory
https://github.com/jonico/other
```
The output in ```output.txt``` will look the following:
```
https://github.com/briantemple/homeworkr DEV
https://github.com/spez/RottenTomatoes HW
https://github.com/DataScienceSpecialization/courses EDU
https://github.com/bundestag/gesetze DOCS
https://github.com/BloombergMedia/whatiscode WEB
https://github.com/ericfischer/housing-inventory DATA
https://github.com/jonico/other OTHER
```

### Fetching repositories
Make sure that you have a working and stable internet connection while running the classification.
Depending on the amount of repositories you want to classify and their corresponding sizes, this process 
can take some time, as it has to fetch information like commits, readmes and file-trees.
A cup of coffee can help to bridge the time gap.
During fetching it will save the data in folders (e.g. ```json_readmes/```), which will be used to extract the features.

### Feature extraction
In the data extraction, the repository data stored in the json folders is used to extract features from them.
The extracted features will be saved in a folder called ```features/```.

### Classification
The extracted features are then fed into pre-trained classifiers and classified into the one of the 7 classes.


Contributors
------------
The following people contributed to this project:
- Paul Anton
- Erik Fließwasser
- Thomas Hummel
- Waleed Mustafa

Questions/Problems
---------
Please contact 5fliessw@informatik.uni-hamburg.de in case of questions or problems.
