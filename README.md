# Question Answering Evaluation

## Overview
The main purpose of this project is to be able to **automatically evaluate Question Answering capabilities of a (multilingual) QnA approach, which uses Machine Translation and BERT**. Currently, question answering in Greek is supported, but the same approach can be utilized for any language. Detailed information about the introduced QnA approach and the comparative evaluation can be found in the respective paper, found **here**.

The evaluation is comprised of 4 steps.
* Step 1: Question answering using the proposed approach (Machine Translation and BERT). buaoelhgdiual uahtnusahltoe
* Step 2: Evaluation of the answers. 
* Step 3:
* Step 4:
where the output data of each step is utilized as input data for the next step. The input data for the first step is a .json file that contains a collection of Greek contexts, questions on each context and the correct answers to the questions (extracted from the original context). The output data of the final step, is a .pdf that contains various important statistics, including an approximate percentage of how many questions where answered correctly/partially_correctly/wrongly, average time needed for each answer and more.



## Project roadmap
Photo from `tree .` and explanations.


## Execution environment:
To be able to execute the python scripts, you have to:
* Install Python3.8 and pip3
* Create a python virtual environment and activate it
* Install the necessary packages: `pip3 install -r requirements.txt`
* Download the English model for spaCy: `python3 -m spacy download en_core_web_lg`	

## Evaluation Steps

### Step 1: 