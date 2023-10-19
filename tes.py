from flair.nn import Classifier
from flair.data import Sentence

# load model
tagger = Classifier.load('chunk-fast')

# make English sentence
sentence = Sentence(
    'Remind me to buy groceries at 5:30 AM on the 15th of October 2023.')

# predict NER tags
tagger.predict(sentence)

# print the chunks
for chunk in sentence.get_labels():
  print(chunk)