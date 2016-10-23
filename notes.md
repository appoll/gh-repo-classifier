Various notes from literature helping to build up our proposal.

We’re going to assume that we have a set of labeled examples of the categories we want
to learn how to identify. These examples consist of a label, which we’ll also call a class
or type, and a series of measured variables that describe each example. We’ll call these
measurements features or predictors. The height and weight columns we worked with
earlier are examples of features that we could use to guess the “male” and “female”
labels we were working with before. [Machine Learning for Hackers, chapter 3] (http://pdf.th7.cn/down/files/1312/machine_learning_for_hackers.pdf)

To accurately classify repositories, we have to include more information from many more repository features (other than the usual ones such as programming language). Extracting these features requires mining of the repository contents and represents the initial step in building the classifier.  


https://developer.github.com/v3/repos/contents/#get-the-readme
As a starting point, we could fool with classifying the README documents based on the contained text paragraphs and the bag-of-words approach, using the below as a skeleton:
  - https://github.com/scikit-learn/scikit-learn/blob/master/examples/text/document_classification_20newsgroups.py
  - http://scikit-learn.org/stable/auto_examples/text/document_classification_20newsgroups.html#sphx-glr-auto-examples-text-document-classification-20newsgroups-py



High order feature extraction is confirmed as an important but difficult task [ML - a probabilistic perspective, page 6]. 
[http://clopinet.com/fextract-book/IntroFS.pdf](An introduction to feature extraction): features can be binary/categorical/continuous and building up a data representation is highly domain specific. The raw input data needs to be converted into a set of useful features, by human expertise which is best complimented by automatic methods. Features are rankable according to their predictive power.	

