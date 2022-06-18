#!/bin/bash
source config.sh
echo "Initialization was successfull"

# Error checking
python_packets=`pip freeze`
if [ -z "$python_packets" ]
then
    echo "You don't have the required python packages to run this script."
    echo "Please use 'pip install requirments.txt' in the root folder of the project."
    exit 0
fi

echo -e "\nBefore you run the script you must have the required python packages."
echo "You can download those python packages by using 'pip install -r requirments.txt' in the root folder of the project."
echo "Are you sure you want to continue ? [y/n]: "
read confirmation
if [ "$confirmation" = "n" ] || [ "$confirmation" != "y" ]; then
    exit 0
fi

# 1. QnA with the selected models from config.sh
cd 1.BERT_models_QnA/scripts/ > /dev/null
echo -e "\nRunning Question and Answering with the following models: "
for str in ${models[@]}; do
  echo -e $ylw $str $clr
done
echo -e "Input dataset: ${grn} ${dataset} ${clr}"
echo -e "Translator: ${blu}${translator}${clr}"

model_array_to_model_string

echo "Putting the models to work..."
echo "Depending on the number of models and the size of the dataset, "
echo "this process could last very long, so go grab a snack!"
if 
python QnA_through_translation.py -input "$dataset" -trans "$translator" --models $formated_string 2> /dev/null &> /dev/null
then
    echo -e "\n${grn}Finished question answering proccess with no errors.${clr}"
else
    echo -e "\n${red}Finished question answering with errors."
    echo -e "Terminating...${clr}"
    exit 0
fi


# 2. Evaluate given answers from step (1).
cd ../../2.BERT_model_answers_evaluation/scripts > /dev/null

input_file="${dataset/_QnA/''}"
input_file="${input_file/.json/''}"
input_file="QnA_on_${input_file}_with_${translator}.csv"


echo -e "\nThe answer evaluation begins."
echo -e "Input file: ${grn}${input_file}${clr}"
echo -e "NLP Weight: ${blu}${nlp}${clr}"
echo -e "Levenshtein Weight: ${blu}${levenshtein}${clr}"
echo -e "Substring Weight: ${blu}${substring}${clr}"
echo -e "Sentence Transformer Weight: ${blu}${sentence_transformer}${clr}"
echo -e "F1 Weight: ${blu}${f1}${clr}"

if 
python evaluate_model_answers.py -input "$input_file" --weights -nlp "$nlp" -levenshtein "$levenshtein" \
    -substring "$substring" -sentence_trans "$sentence_transformer" -f1 "$f1" 
then
    echo -e "\n${grn}Finished question evaluation with no errors.${clr}"
else
    echo -e "\n${red}Finished question evaluation with errors."
    echo -e "Terminating...${clr}"
    exit 0
fi


# 3. Model answer labeling.
cd ../../3.BERT_model_answer_labeling/scripts > /dev/null

input_file="${input_file/QnA/'evaluated_answers'}"

echo -e "\nThe model answer labeling begins."
echo -e "Input file: ${grn}${input_file}${clr}"
echo -e "Theshold1: ${blu}${t1}${clr}"
echo -e "Threshold2: ${blu}${t2}${clr}"

if 
python label_model_answers.py -input "$input_file" --thresholds -t1 "$t1" -t2 "$t2"
then
    echo -e "\n${grn}Finished answer labeling with no errors.${clr}"
else
    echo -e "\n${red}Finished answer labeling with errors."
    echo -e "Terminating...${clr}"
    exit 0
fi


# 4. Model statistics.
cd ../../4.BERT_model_statistics/scripts > /dev/null

input_file="${input_file/evaluated_answers/'QnA'}"
input_file="${input_file/.csv/'_auto_labeled.csv'}"

echo -e "\nStatistics generation begins."
echo -e "Input file: ${grn}${input_file}${clr}"
if ! [[ -z "$statistics_flag" ]]; then
    echo "Extra statistics selected."
fi 

if 
python statistics.py -input "$input_file" "$statistics_flag"
then
    echo -e "\n${grn}Finished statistics generation with no errors.${clr}"
else
    echo -e "\n${red}Finished statistics generation with errors."
    echo -e "Terminating...${clr}"
    exit 0
fi

output_pdf="${input_file/.csv/'.pdf'}"
echo -e "${grn}The automated evaluation process has finished successfully.${clr}"
echo -e "Model statistics are in ${blu}PROJECT_ROOT/4.BERT_model_statistics/output_data/statistics_for_${input_file}${clr}"
