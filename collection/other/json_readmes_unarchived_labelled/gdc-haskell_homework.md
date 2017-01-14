
GDC Haskell
============

Clone and initialize
--------------------

Just clone project is simple.
```sh

# Fork and clone your homework skeleton project.
git clone https://github.com/your-account/your-homework.git

```

If you want to track upstream tests, add homework-tests repo as a subtree.

```sh

# Add homework-tests repo as a remote and fetch.
git remote add gdc-haskell-homework-tests https://github.com/gdc-haskell/homework-tests.git
git fetch gdc-haskell-homework-tests master

# To update subtree at a later date,
git fetch gdc-haskell-homework-tests master
git subtree pull -P tests gdc-haskell-homework-tests master --squash

# If you have some problems with subtree operation, try remove `--squash`
```

First Setup
---------

```sh

# if you want to trap your project in sandbox, run
# cabal sandbox init
cabal install --only-dependencies --enable-tests
cabal configure --enable-tests

```

Write your code
---------------

Cabal project file is written as if your code is located in `src/`.

How to run test
-------------

### run all test.

```sh

cabal test

```

### run only one test.

```sh

cabal test test4

cabal test test5

...

```

How to add tests
----------------

1. Import homework file in Spec*.hs
2. Add test case like other tests.
3. Share with others!
    ```sh

    git subtree push -P tests homework-tests master-or-something [--squash]

    ```

How to improve homework skeleton
--------------------------------
