import json

input_file = '../resources/txt_files/greek_text_QnA_collection.txt'
output_file = '../resources/json_files/greek_text_QnA_collection.json'

if __name__ == "__main__":
    f = open(input_file)
    data = f.read()
    f.close()

    data = list(data.split("//end_of_answers\n"))

    for i in range(len(data)):
        data[i] = data[i].split("//end_of_text\n")
        data[i] = [data[i][0], data[i][1].split("//end_of_questions\n")[0], data[i][1].split("//end_of_questions\n")[1]]
        data[i][1] = list(data[i][1].split('\n'))
        del data[i][1][-1]
        data[i][2] = list(data[i][2].split('\n'))
        del data[i][2][-1]

    json_collection = {}
    json_collection['collection'] = []
    for i in range(len(data)):
        context_qna = {}
        context_qna['context'] = data[i][0]
        context_qna['questions'] = data[i][1]
        context_qna['answers'] = data[i][2]
        json_collection['collection'].append(context_qna)
        
    with open(output_file, 'w',encoding="utf8") as fp:
        json.dump(json_collection, fp, ensure_ascii=False)