from nltk.tokenize import word_tokenize
import re
import random
from spellchecker import SpellChecker
import requests
from nltk.corpus import words
from nltk import WordNetLemmatizer
import spacy
import os
import json

nlp = spacy.load("en_core_web_sm")
    
def grammatical_term (grammatical_term, word_pos_list):
    result = []
    
    if grammatical_term == "n":
        result = [term for term in word_pos_list if term [1] == "n" ]
    
    elif grammatical_term == "a":
        result = [term for term in word_pos_list if term [1] == "a" ]
    
    elif grammatical_term == "v":
        result = [term for term in word_pos_list if term [1] == "v" ]
        
    elif grammatical_term == "UH":
        result = [term for term in word_pos_list if term [1] == "UH" ]
        
    elif grammatical_term == "r":
        result = [term for term in word_pos_list if term [1] == "r" ]
        
    return result

def text_Lemmatizer (text, gramma_term):
    lemeize = WordNetLemmatizer()
    doc = nlp(text)
    words = [token.text for token in doc]
    tag = [token.tag_ for token in doc]

    pos_mapping = {
        'JJ':'a', 'JJR':'a', 
        'JJS':'a', 'NN':'n',
        'NNS':'n', 'VBD':'v',
        'VBG':'v','VBN':'v',
        'VBP':'v', 'VBZ':'v',
        'UH': 'UH', 'RB': 'r'
        }

    word_pos_tuples = [list(items) for items in zip(words, tag)]
    # New_word_pos_tuples = 

    for i in range(len(word_pos_tuples)):
        for j in pos_mapping:
            if j == word_pos_tuples[i][1]:
                word_pos_tuples[i][1] = pos_mapping[j]
                if word_pos_tuples[i][1] != 'UH':
                    word_pos_tuples[i][0] = lemeize.lemmatize(word_pos_tuples[i][0], word_pos_tuples[i][1]) 
    
    if gramma_term != None:
        
        gramma = grammatical_term(gramma_term, word_pos_tuples)    
        if not gramma:
            return tuple()
        
        word_leme = tuple([leme_word for leme_word, tags in gramma])
    
    else:
        word_leme = [leme_word for leme_word, tags in word_pos_tuples]
        
    return word_leme

def get_synonyms_datamuse(word, gramma_term):
    english_words = set(words.words()) # Create a set of English words

    response = requests.get(f"https://api.datamuse.com/words?ml={word}")
    synonyms = [word_obj['word'] for word_obj in response.json()] # list of synonyms
    
    # Filter the list to include only English words
    filtered_synonyms = [words for words in synonyms if words.lower() in english_words]
    sentence = " ".join(filtered_synonyms)

    return text_Lemmatizer(sentence, gramma_term)

class Chatbot:
    def __init__(self, user_input, rule, username, rule_priority):
        self.user_input = user_input
        self.rule = rule
        self.username = username
        self.rule_priority = rule_priority if rule_priority is not None else 0
        
    @staticmethod
    def correct_spell(user_input): # get correct spelling
        if not user_input:  # Check if input is None or empty
            return "No input provided", 0
        
        spell = SpellChecker()
        custom_words = ['pakpaokite', 'Sukhothai','%quiz', '%puzzle']  # Add more words as needed
        spell.word_frequency.load_words(custom_words)
        tokenize = word_tokenize(user_input)
        correct_word = [spell.correction(correct_word) for correct_word in tokenize]
        
        word = " ".join(correct_word)
        word_leme = text_Lemmatizer(word, None)
        joined = " ".join(word_leme)
        
        return joined 
    
    def key_match(self):
        directory = 'chat_log_history'
        file_path = os.path.join(directory, f"{self.username}.json")        
        # quits = get_synonyms_datamuse(Processed_Text, "n")
        priority_of_rule = self.rule_priority
        priority_time = 0

        if not self.user_input or self.user_input.strip() == "":
            return None, 0
        
        Processed_Text = Chatbot.correct_spell(self.user_input)

        if isinstance(Processed_Text, list):
            Processed_Text = " ".join(Processed_Text)
        
        matched_responses = []
        
        with open (file_path, "r") as f:
            data = json.load(f)
            if len(data[self.username]) >= 2:
                last_chat_log = data[self.username][-2]['chatlog']
            else:
                last_chat_log = None
            
            if 4 >= priority_of_rule >= 3:
                if last_chat_log != "Would you like to play some game related to pakpaokite?\nIf so, type %puzzle and if you want to play the puzzle game or type %quiz if you want to play quiz game.":
                    matched_responses.append("Would you like to play some game related to pakpaokite?\nIf so, type %puzzle and if you want to play the puzzle game or type %quiz if you want to play quiz game.") 
                    return matched_responses[0], 1

                elif last_chat_log == "Would you like to play some game related to pakpaokite?\nIf so, type %puzzle and if you want to play the puzzle game or type %quiz if you want to play quiz game.":
                    if Processed_Text == '% quiz':
                        matched_responses.append("We will start the quiz game now")
                        return matched_responses[0], 1
                    elif Processed_Text == '% puzzle':
                        matched_responses.append("We will start the puzzle game now")
                        return matched_responses[0], 1
                    else:
                        return "Ok", 1
                
        for priority in sorted(self.rule.keys(), reverse=False):  # Sort priority low to high
        
            rules = self.rule[priority]  # Access rules for the current priority level
            
            for key, response in rules.items():
                    
                if re.search(key, Processed_Text):  # Check if the input matches any rule key
                    # Check for specific command matches
                    if re.search(rf"(?i)\b(what)\b.*\bmy\b.*\b(name)\b", Processed_Text):
                        matched_responses.append(f"Your name is {self.username}")
                    
                    elif re.search(rf"(?i)\b(any)\b.*\b(command)\b", Processed_Text):
                        matched_responses.append(f"Type: quit\n What is the current weather?\n Delete history\n")
                    
                    elif re.search(rf"(?i)\b(delete)\b.*\b(history)\b", Processed_Text):
                        file_path = f"chat_log_history/{self.username}.json"
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        matched_responses.append(f"The {self.username} chat log history has been deleted")
                    
                    elif re.search(rf"(?i)\b(quit)\b", Processed_Text):
                        matched_responses.append("end")
                    
                    # Set priority_time to 1 if the priority is either 1 or 2
                    if priority in [1, 2]:
                        priority_time = 1  
                    
                    # Append a random response for the matched key
                    matched_responses.append(random.choice(response))

        # Debugging print statement
        if matched_responses:
            return matched_responses[0], priority_time  # Return the first matched response and priority_time
        else:
            print("No response found")
            return "No response found", priority_time  # Default response if no match found

#idk why self.rule_priority is not check