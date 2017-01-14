Scitran Data |travis_badge|
===========================

.. |travis_badge| image:: https://travis-ci.org/scitran/data.svg?branch=ksh-dataio
    :target: https://travis-ci.org/scitran/data

**TODO** put some sort of warning that upgrading from this package BREAKS WORLDS, and does
not replace nimsdata, rather scitran.data will install along side.

Data handling utilities.

Provides class and functions for parsing, identifying and writing scientific datasets. Currently,
medical images (such as various flavors of MRI, dicoms, niftis, and some raw-files) are supported.

Also provides base classes that can be used to extend this package to cover additional data-domains.

Note that these utilites also have command-line interfaces, so you don't need a full NIMS
instance to use them. E.g., you can run our image reconstruction pipeline.


How to use the documentation
----------------------------
Documentation is available as docstrings provided within the code, and
`additional narrative documentation <https://scitran.github.io/data>`_.


Dependencies
------------

development version is currently using the following:

================ ====================
package          version
================ ====================
Pillow           2.6.1
numpy            1.9.2
nibabel          1.4.0dev
pydicom          0.9.9
dcmstack         0.7.0dev
pytz             2014.10
scipy            0.14.0
mne              0.9
================ ====================


installation on fresh ubuntu 14.04
----------------------------------
- install dependencies, **had to chmod o+w /var/local to allow regular user to write; not ideal**
    - **python-dev** is required to build numpy, and pillow.
    - **python-virtualenv** is required to make use of python virtual environment.
    - **libjeg-dev** is required for pillow JPEG support.  Pillow must be compiled with JPEG support.  See `this stack overflow question
      <http://stackoverflow.com/questions/8915296/python-image-library-fails-with-message-decoder-jpeg-not-available-pil>`_ for more information.
    - **git** is required to pip install from git repositories.

.. code:: bash

    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install python-dev python-virtualenv libjpeg-dev git
    sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib

- create and activate virtualenv

.. code:: bash

    virtualenv data_env
    source data_env/bin/bin/activate

- install dependencies, these are VERY specific version. once these versions are available
  through pypi, these installation commands will change.  (subject to change)

.. code:: bash

    pip install numpy==1.9.0
    pip install scipy==0.14
    pip install git+https://github.com/scitran/pydicom.git@0.9.9_value_vr_mismatch
    pip install git+https://github.com/nipy/nibabel.git
    pip install git+https://github.com/moloney/dcmstack.git@6d49fe01235c08ae63c76fa2f3943b49c9b9832d
    pip install pillow
    pip install pytz
    pip install mne

- install scitran data from github

.. code:: bash

    pip install git+https://github.com/scitran/data.git


Basic Conversion
----------------
The software consists of the python package, *scitran.data*, with a single command line interface
`data.py`.

NIMSData has a semi-standard input filetype, a tgz, that contains raw data and a json that
indicates the raw data filetype, header data, and metadata corrections.

`data.py` expects at least 3 options, *<input.tgz>*, *--parser <filetype>*, *--writer <filetype>*.

The following shell command will take the *dicom* input *input.tgz* and convert it to nifti, *outprefix.nii.gz*.

.. code-block:: sh

    data.py -p dicom input.tgz -w nifti outprefix.nii.gz


And the equivelant command in python.

.. code-block:: python

    import scitran.data as scidata
    ds = scidata.parse('/path/to/input.gz', filetype='dicom')
    ds.load_data()
    scidata.write(ds, ds.data, 'outprefix', filetype='nifti')


For more information on using Scitran Data in bash, see `CLI tutorial <https://scitran.github.io/cli_tutorial.html>`_.

For more information on using Scitran Data in python see `Python tutorial <https://scitran.github.io/nimsdata/python_tutorial.html>`_.


Developer Notes
---------------

To install scitran data from github in 'editable mode', in a directory of your choosing, provide the `-e` and
`--src <destination>` arguments.

.. code:: bash

    pip install -e git+https://github.com/scitran/data.git#egg=scitran.data --src ./

to run tests locally, you will need coverage and nose

.. code:: bash

    pip install coverage nose

To generate the docs locally, you will need sphinx, and numpydoc.

.. code:: bash

    pip install sphinx numpydoc


numpy 1.9 changes how numpy.unique() behaves when given an array of arrays.  Pre 1.9, np.unique
would return each unique array. Post 1.9, np.unique returns unique items from the arrays. dcmstack
is compatible with numpy 1.9, but numpy throws some FutureWarnings.  The current version of
dcmstack (0.7.0dev) may not be compatible with future version of numpy.

run the following git config commands to enable a git filter for the branch name.

.. code:: bash

    git config filter.brancher.smudge "./git_branch_filter.py smudge"
    git config filter.brancher.clean "./git_branch_filter.py clean"

Combined with .gitattributes, the smudge and clean filters will replace 'branch=\_\_BRANCH\_\_' to indicate
the current branch.


Testdata is not distributed with this package.  Downloading/cloning the testdata is necessary
to run tests locally.  clone the `testdata` repository into `scitran/data/test/testdata`.

.. code:: bash

    git clone https://github/com/scitran/testdata.git <path to clone of scitran-data>/scitran/data/test/testdata

Probing site data
-----------------

To probe functionality, you can set the API to insecure mode in ``config.toml``.
The API can the directly be browsed at e.g. https://localhost:8443/api.
Type in your email address, click ``Generate Custom Links``, and then browse
different tabs like ``/projects`` link.
`JSONView <https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en>`_
is a helpful Chrome plugin for this process.
