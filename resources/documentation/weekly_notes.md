# Notes to track our weekly progress.

  

  

## Translation model evaluation:

  

The quality of the translation was evaluated through 2 unbiased human reviewers based on 2 factors:

1) Its INTELLIGIBILITY (the translation is understandable).
	 - Reads clear and easily; has no stylistic infelicities.
	- Absence of grammatical errors.
	- Use of terminology appropriate for the field.
	- Correct syntactic arrangements.
	- The message is clearly transmitted. It is not necessary to read twice.

2) its FIDELITY (the message transmitted by the translation corresponds exactly to the original message).
	- The translation conveys the same meanings of the source text.
	 - There are no misapprehensions or mistranslations of words or sentences.
	- All sections have been translated completely, no additions or omissions (in some cases a translator may divide a sentence in two or join two sentences in one to avoid unintelligibility problems in a passage).

  

We realized that probably the dataset of contexts-QnA we have, was translated from english to greek using helsinki translation

  

This gives an unfair advantage to helsinki translation api when we compare it with other translators using this dataset.

  

So, in order to evaluate the translation api's, we need another dataset. **

  

The dataset should contain texts of different lengths and subjects.

  

We found a nice set of greek texts [here](https://www.greek-language.gr/certification/dbs/teachers/index.html) and added a few of them in our set (texts_for_translation.txt).

  

  

The helsinki translation api cannot handle long text, so we decided to split each text in sentences. We used the spark nlp multilanguage model for the splitting.

  

The google translation api could not handle text with more than 2.500 characters, so we splitted each large text to multiple smaller subtexts. The splitting occurs only at the end of a sentence, so that it

  

does not affect the comprehension of the initial text.

  

  

We also created a utility python script that provides us with a list of working proxies. They way it does it is by scraping some of the most popular websites that have a list of free proxies. We provide the urls of those sites and with the use of the BeautifulSoup python library we scrape those websites for proxies that support https. We need proxies when we have to handle multiple api calls because the api's block us from after a certain ammount of calls. By adding to proxies and calling the api's with a different proxy everytime we ensure that we won't be blocked.

  

  

After analyzing the translated texts, we made the following remarks:

  

   1. The main issue of all translators, is that many times they translate the text literally. Helsinki and Bing translators seem to have an edge over the others in this aspect.

```
Eg1: "Πηγαίνω τα αγόρια στο ποδόσφαιρό"
	- "I go boys in football" (actual wrong result)
		- "I take the kids to football" (expected correct result, also given by the google translate web app)

Eg2: "Το βραδάκι βλέπουμε τηλεόραση"
	- "The evening we see television" (actual wrong result)
		- "In the evening we watch TV" (expected correct result, also given by the google translate web app)
```
 
   2. Greek names may be interpreted as words. Helsinki and Bing had an edge here too.

```
Eg1: "Έχω ένα μικρό σκυλάκι, την Τάμι"
	- "I have a little dog, tomato" (actual wrong result)
		- "I have a little dog, Tammy" (expected correct result, also given by the google translate web app)
```

   3. Textblob translator generally underperformed.

  

   4. Goslate translator could not be tested enough because we almost instantly got a server error for issuing too many requests.

  

   5. Helsinki and Bing seemed to grasp better the context of the text and provide a more accurate, more human-like translation.

  

   6. All translators got vastly outperformed by google translate web app.

  

  

We consider the translation step, a very important part of our QnA procedure. So we may need to consider using selenium + google translate web application for translation.

  

  

** All api's must be tested in both en->gr translation and gr->en.