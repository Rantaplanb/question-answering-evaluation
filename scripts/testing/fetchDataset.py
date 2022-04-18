import requests
import json

if __name__ == "__main__":
    collection = requests.get("http://users.ics.forth.gr/mountant/files/greek.json").text
    data = json.loads(collection)
    f = open("../../resources/txt_files/QnA_formated.txt", "a")

    for x in data["data"]:
        paragraphs=x["paragraphs"]

        for y in paragraphs:
            greek_context = y['context']
            f.write(greek_context)
            f.write('[delimiter]')

    f.close()
             