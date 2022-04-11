from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,pipeline

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-grk-en")

model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-grk-en")
translation=pipeline("translation",model=model,tokenizer=tokenizer)
text="Ο Νίκος Ξυλούρης γεννήθηκε  στις 7 Ιουλίου του  1936, στο ορεινό χωριό Ανώγεια Μυλοποτάμου Ρεθύμνου της Κρήτης από οικογένεια με μουσική παράδοση και πολλούς λυράρηδες. Στα πέντε του χρόνια, όταν οι Γερμανοί έκαψαν το χωριό του, ξεριζώθηκε από τον τόπο του μαζί με τους υπόλοιπους κατοίκους, οι οποίοι μεταφέρθηκαν σε χωριό της επαρχίας Μυλοποτάμου όπου παρέμειναν μέχρι και την απελευθέρωση της Κρήτης. Αδέλφια του είναι οι επίσης γνωστοί μουσικοί της κρητικής μουσικής ο Αντώνης Ξυλούρης (Ψαραντώνης) και ο Γιάννης Ξυλούρης (Ψαρογιάννης). Στα 17 του αποφάσισε να μετακομίσει στο Ηράκλειο και έπιασε δουλειά στο νυχτερινό κέντρο Κάστρο." 
text2="Τα πράγματα όμως δεν ήταν όπως τα περίμενε γιατί βρέθηκε αντιμέτωπος με τη μόδα της Ευρωπαϊκής μουσικής, κάτι τελείως ξένο για αυτόν. Τα έσοδα του μόλις και μετά βίας έφταναν να τον συντηρήσουν και πέρασε δύσκολες εποχές. O μεγάλος ερμηνευτής υπήρξε φανατικός οπαδός του ΟΦΗ, εκ των ιδρυτικών μελών μάλιστα του Συνδέσμου Φιλάθλων ΟΦΗ Αθηνών, ο οποίος σήμερα φέρει και το όνομά του."
text3="Επανέρχεται όμως και στα παραδοσιακά τραγούδια της Κρήτης, ενώ λέει και κάποια λαϊκά τραγούδια του Στέλιου Βαμβακάρη. Όμως, η ζωή του επιφυλάσσει μία δυσάρεστη έκπληξη. Το 1979 είναι μια δύσκολη χρονιά για τον Νίκο Ξυλούρη. Αν και η καριέρα του βρίσκεται στο απόγειό της, ο ίδιος υποφέρει από έντονους πόνους στο κεφάλι και στο θώρακα. "
text4="Ταξιδεύει στη Νέα Υόρκη και εισάγεται για εξετάσεις στο Memorial Hospital, όπου διαπιστώνεται ότι πάσχει από καρκίνο. Τα χαράματα της Παρασκευής 8 Φεβρουαρίου ο Νίκος Ξυλούρης απεβίωσε... Στις 9 Φεβρουαρίου χιλιάδες κόσμου, επώνυμοι κι ανώνυμοι, αποχαιρετούν τον «Αρχάγγελο της Κρήτη» με δάκρια στα μάτια και τραγουδούν:"

context=translation(text)
context2=translation(text2)
context3=translation(text3)
context4=translation(text4)

qa_model = pipeline("question-answering")

greek1="Ποιο έτος γεννήθηκε"
greek2="Τι προβλήματα υγείας είχε "
greek3="Ποια χρονιά δεν ήταν εύκολη"

question =translation(greek1)
question2 =translation(greek2)
question3 =translation(greek3)
print(question[0]["translation_text"])
print(question2[0]["translation_text"])
answer=qa_model(question = [question[0]["translation_text"],question2[0]["translation_text"],question3[0]["translation_text"]],context = context[0]["translation_text"]+context2[0]["translation_text"]+context3[0]["translation_text"]+context4[0]["translation_text"])
print(answer)

tokenizer2 = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-el")
model2 = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-el")
translation2=pipeline("translation",model=model2,tokenizer=tokenizer2)

print(greek1)
print(translation2(answer[0]['answer']))

print(greek2)
print(translation2(answer[1]['answer']))

print(greek3)
print(translation2(answer[2]['answer']))