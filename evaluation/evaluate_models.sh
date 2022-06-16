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
echo "You can download those python packages by using 'pip install requirments.txt' in the root folder of the project."
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

echo "Iniatializing the models and putting them to work, this might take some time..."
if 
python QnA_through_translation.py -input "$dataset" -trans "$translator" --models "$formated_string" 2> /dev/null &> /dev/null; 
then
    echo -e "\n${grn}Finished question answering proccess with no errors.${clr}"
else
    echo -e "\n${red}Finished question answering with errors."
    echo "Terminating...${clr}"
fi