import json, requests 

url = requests.get("http://users.ics.forth.gr/mountant/files/greek.json")
collection = url.text

data = json.loads(collection)
for x in data["data"]:
  paragraphs=x["paragraphs"]
  
  for y in paragraphs:
    print("\nNew Text")
    print(y['context'])
    for z in y['qas']:
      print("\tQuestion: "+z['question'])
      for ans in z['answers']:
       print("\t\tAnswer: "+ans['text'])
       print("\t\tAnswerStart: "+str(ans['answer_start']))