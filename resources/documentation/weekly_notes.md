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
Αρχικα συνειδητοποιησαμε οτι πιθανοτατα το dataset κειμενων-ερωτοαπαντησεων που εχουμε, μεταφραστηκε απο αγγλικα σε ελληνικα με το helsinki translation.
This gives an unfair advantage to helsinki translation api when we compare it with other translators using this dataset.
So, in order to evaluate the translation api's, we need another dataset. **
The dataset should contain texts of different lengths and subjects. 


** All api's must be tested in both en->gr translation and gr->en. 