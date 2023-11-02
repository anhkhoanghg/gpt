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

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")  # Load English language model

data = {
    "edu-activities": [
        "Go to school",
        "Go to university",
        "Complete an essays",
        "Study for final examinations",
        "Repair for the next examinations",
        "Meet with a teacher for extra help",
        "Join a school club",
        "Attend a school dance",
        "Study for upcoming exams",
        "Join a school sports team",
        "Use a computer for research",
        "Meet with a school counselor",
        "Help with school library activities",
        "Reading textbooks and class materials",
        "Writing essays, reports, and papers",
        "Studying and reviewing notes",
        "Attending lectures and classes",
        "Participating in discussions and seminars",
        "Taking exams and quizzes",
        "Doing homework assignments",
        "Completing worksheets and workbooks",
        "Working on group projects",
        "Making flashcards and study guides",
        "Doing mathematical",
        "Performing lab experiments",
        "Analyzing literature and texts",
        "Learning vocabularies",
        "Studying maps, charts, and diagrams",
        "Memorizing facts, formulas, and concepts",
        "Taking practice tests and mock exams",
        "Meeting with study groups and tutors",
        "Preparing presentations",
        "Read a chapter from book",
        "Watch a documentary",
        "Practice a foreign language",
        "Solve a crossword puzzle",
        "Listen to an educational podcast",
        "Research a historical event",
        "Study a new scientific concept",
        "Review and organize class notes",
        "Explore an art history topic",
        "Watch a TED Talk",
        "Try a new math problem",
        "Learn a new recipe and cook a meal",
        "Practice meditation or mindfulness",
        "Explore a new coding concept",
        "Review the periodic table of elements",
        "Study a world geography topic",
        "Learn about a famous philosopher",
        "Study the basics of astronomy",
        "Explore a topic in psychology",
        "Practice a musical instrument",
        "Research a famous historical figure",
        "Watch a tutorial on a new software tool",
        "Learn about a new culture's traditions",
        "Learn about a recent scientific discovery",
        "Study a famous piece of literature",
        "Practice speed reading techniques",
        "Explore a new architectural style",
        "Learn about a famous mathematician",
        "Research a contemporary world issue",
        "Study a topic in environmental science",
        "Learn about a famous composer",
        "Watch a wildlife documentary",
        "Study a new language's basic phrases",
        "Explore a new dance style",
        "Learn about a famous scientist",
        "Research a space exploration mission",
        "Study a famous historical speech",
        "Watch a historical reenactment",
        "Learn about a famous inventor",
        "Study a world religion or belief system",
        "Research a famous explorer",
        "Explore a new political ideology",
        "Study a topic in sociology",
        "Practice basic origami",
        "Watch a classic film or documentary",
        "Learn about a famous musician or band",
        "Research a new art movement",
        "Study a historical war or battle",
        "Explore a topic in ethics",
        "Learn about a significant medical breakthrough",
        "Study a famous landmark",
        "Research a cultural festival",
        "Study a famous sculpture or statue",
        "Research a famous artwork's history",
        "Study a famous painting technique",
        "Watch a classic ballet performance",
        "Learn about a famous poet",
        "Study a famous architectural structure",
        "Explore a topic in anthropology",
        "Research a natural disaster or phenomenon",
        "Explore a topic in performing arts",
        "Learning foreign languages"
    ]
}

noun_activities = []

# Process each activity and extract nouns
for activity in data["edu-activities"]:
    doc = nlp(activity)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    noun_activities.append(" ".join(nouns))

# Print the converted noun activities
for noun_activity in noun_activities:
    print(noun_activity)
