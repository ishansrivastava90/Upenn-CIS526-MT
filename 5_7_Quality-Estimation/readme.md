There are three Python programs here (`-h` for usage):

+ `./default` performs clustering on the training data
+ `./baseline` performs k-nearest-neighbor
+ `./grade` compares the predicted score with the actual score and returns the accuracy

The first two commands are designed to work in a pipeline with the last. For instance, this is a valid invocation:

```
./baseline | ./grade
```

The `data-train/` directory contains

    + `es-en_score.train`, which contains the score assigned to each sentence (one score per line)
    + `es-en_source.train`, which contains 1050 Spanish sentences
    + `es-en_target.train`, which contains 1050 English translations
    + `train_features`, which contains the values of each of the 17 features for each sentence

as well as the `feature-list`, which contains the list of features being used.

The `data-dev/` directory contains:

    + `es-en_score.dev`, which contains the score assigned to every alternate sentence in the test data, i.e. 225 scores. This is what is used to develop locally.

The `data-test/` directory contains:

    + `es-en_source.test`, which contains 450 Spanish sentences
    + `es-en_target.test`, which contains 450 English translations
    + `test_features`, which contains the values of each of the 17 features for each test sentence
