#!/bin/bash

# Set of Models to be evaluated
# Please insert the name of the model you want to use as an element of the array.
models=(
    "deepset/tinyroberta-squad2"
    "deepset/roberta-base-squad2-covid"
)

# Dataset that will be used to evaluate the models above.
dataset='demo_QnA_dataset.json'

# Translator used to translate the data inside the dataset to english
translator='helsinki'

# Weights for the evaluation of the model answers
# The weights must add up to 1 
nlp='0.2'
levenshtein='0.1'
substring='0.1'
sentence_transformer='0.4'
f1='0.2'

# Thresholds for the labeling
# The first threshold indicates that answers evaluated with a
# score greater than the thresholds number will be labeled as correct.
# The second threshold indicates that answers evaluated with a
# score less than the thresholds number will be labeled as wrong.
# The rest answers that were evaluated with a score less than 
# thresholds 1 and greater than thresholds 2 will be labeled as partially correct.
# Those thresholds have been set automatically and it is not advised to change them.
t1='0.65'
t2='0.5'