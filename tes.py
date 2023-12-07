# from flair.nn import Classifier
# from flair.data import Sentence

# # load model
# tagger = Classifier.load('chunk-fast')

# # make English sentence
# sentence = Sentence(
#     'Remind me to buy groceries at 5:30 AM on the 15th of October 2023.')

# # predict NER tags
# tagger.predict(sentence)

# # print the chunks
# for chunk in sentence.get_labels():
#   print(chunk)

import spacy
from datetime import datetime as dt
import parsedatetime as pdt
import spacy.cli


class GetDateTime():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def insert_str(self, string, str_to_insert, index):
        return string[:index] + str_to_insert + string[index:]
    
    def getDateTimeinText(self, text):
        doc = self.nlp(text)
        result = ""
        date = ""
        time = ""
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"]:
                print(f"Entity: {ent.text}, Label: {ent.label_}")
                if ent.label_ == "DATE":
                    date = self.getRemindTime(ent.text)
                    result = self.insert_str(result, " "+ent.text, len(result))
                elif ent.label_ == "TIME":
                    time = self.getRemindTime(ent.text)
                    result = self.insert_str(result, ent.text , 0)
        return result, date, time

    def instrucadeclare(self, text):
        doc = self.nlp(text)

        # Initialize lists to store instructions and declarations
        instructions = []
        declarations = []

        # Iterate through the sentences in the text
        for sent in doc.sents:
            sentence_text = sent.text
            # Check if the sentence contains certain keywords
            if "remind" in sentence_text:
                instructions.append(sentence_text)
            else:
                declarations.append(sentence_text)

        # Print the identified instructions and declarations
        print("Instructions:")
        for instruction in instructions:
            print(instruction)

        print("\nDeclarations:")
        for declaration in declarations:
            print(declaration)
        return instructions, declarations
            

    def getRemindTime(self, time_string):
        cal = pdt.Calendar()
        now = dt.now()
        return cal.parseDT(time_string, now)[0]
    
getTime = GetDateTime()
text = "set a reminder to have lunch at 11 AM tomorrow"
string, date, time = getTime.getDateTimeinText(text)
print(date, time)
