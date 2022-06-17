#!/bin/bash

# Defines
blk='\033[01;30m'   # Black
red='\033[01;31m'   # Red
grn='\033[01;32m'   # Green
ylw='\033[01;33m'   # Yellow
blu='\033[01;34m'   # Blue
pur='\033[01;35m'   # Purple
cyn='\033[01;36m'   # Cyan
wht='\033[01;37m'   # White
clr='\033[00m'      # Reset

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
t1='0.57'
t2='0.55'

# When the flag is empty, the normal statistcs are written.
# If you want extra statistics, change flag's value to '--extra'
statistics_flag=''

# Functions
model_array_to_model_string() {
    formated_string=''
    counter=1
    for str in ${models[@]}; do
        formated_string="${formated_string} -m${counter} ${str}"
        counter=$((counter + 1))
    done
}