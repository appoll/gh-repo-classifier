Compare multiple classifiers' performances and visualize it?  
- performance measure 1: training time
    
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        print("train time: %0.3fs" % train_time)
    
- performance measure 2: testing time
   
        t0 = time()
        pred = clf.predict(X_test)
        test_time = time() - t0
        print("test time:  %0.3fs" % test_time)

- performance measure 3: scikit's [accuracy_score](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
        
        score = metrics.accuracy_score(y_test, pred)
        print("accuracy:   %0.3f" % score)
