# Question Answering Evaluation

## Overview
The main purpose of this project is to be able to **automatically evaluate Question Answering capabilities of a (multilingual) QnA approach, which uses Machine Translation and BERT**. Currently, question answering in Greek is supported, but the same approach can be utilized for any language. Detailed information about the introduced QnA approach and the comparative evaluation can be found in the respective paper, found **here**.

The evaluation is comprised of 4 steps that form a pipeline:
1. **Question answering** using the proposed approach (Machine Translation and BERT). 
2. **Evaluation of the answers**. The answers given by the BERT models are compared with the correct ones, using a variety of string comparison metrics. 
3. **Labeling of each answer** as "correct", "partially_correct", and "wrong" based on the string comparison metrics (calculated in the previous step) and thresholds values (more information on those values can be found in the respective paper).
4. **Calculation of statistics** based on the generated data from the previous steps.

These steps are implemented as a python script execution pipeline, but there is also the option to run any step in isolation.<br />
It is also worth mentioning that:
* The input data for the first step is a .json file that contains a collection of Greek contexts, questions on each context and the correct answers to the questions (extracted from the original context). 
* Each time, the output data of previous steps is utilized as input data for the current step. 
* The output data of the final step, is a .pdf that contains various important statistics, including an approximate percentage of how many questions where answered correctly/partially_correctly/wrongly, average time needed for each answer and more.


## Execution environment
To be able to execute the python scripts, you have to:
* Install Python3.8 and pip3
* Create a python virtual environment and activate it
* Install the necessary packages: `pip3 install -r requirements.txt`
* Download the English model for spaCy: `python3 -m spacy download en_core_web_lg`	

## Configuration

In the `$PROJECT_ROOT/evaluation/` directory there is a bash script named `config.sh`. This script contains all the configuration parameters (like BERT model selection) for a fully automated execution of the python script pipeline. Each configuration parameter is briefly explained in the comments contained in the configuration script.
<br />
<br />
Also, in each python script there is a detailed comment above main() function which explains a few more configuration options.

## Execution
In the `$PROJECT_ROOT/evaluation/` directory there is another bash script named `evaluate_models.sh`. This script parses the configuration parameters that are set in the `config.sh` script and uses them to execute all the evaluation steps, one by one, which automates the evaluation process. All you have to do, is run this script.
<br />
There is also the option to run each evaluation step in isolation. Navigate to `$PROJECT_ROOT/evaluation/$STEP_OF_YOUR_CHOICE/scripts/` and execute the script of your choice. You will be prompted to select configuration parameters for the execution.
