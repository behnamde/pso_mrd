from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import nltk
from itertools import product
from joblib import load
import pickle
import re
import string
from langdetect import detect, detector_factory

detector_factory.seed = 0

model = TFBertForSequenceClassification.from_pretrained("./bert_model")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

class IsToAnswer:
    """
    <describe here>
    """
    def __init__(self) -> None:
        pass
    
    def language(self):
        if detect(self) == 'en':
            return True
        else:
            return False

    def preprocessing(self): 
        
        def remove_hyperlink(self):
            return re.sub(r"http\S+", "", self)

        def to_lower(self):
            return self.lower()

        def remove_number(self):
            return re.sub(r'\d+', '', self)

        def remove_punctuation(self):
            return self.translate(str.maketrans(dict.fromkeys(string.punctuation)))

        def remove_whitespace(self):
            return self.strip()

        def replace_newline(self):
            return self.replace('\n','')

        def remove_emoji(self):
                emoji_pattern = re.compile("["
                        u"\U0001F600-\U0001F91F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
                return emoji_pattern.sub(r'', self)
            

        def remove_hashtag(self):
            return re.sub("#[A-Za-z0-9_]+","", self)

        def remove_mentioned(self):
            return re.sub("@[A-Za-z0-9_]+","", self)

        def clean_up_pipeline(sentence):
            operations = [
                to_lower,
                remove_hashtag,
                remove_mentioned,
                remove_hyperlink,
                remove_emoji,
                replace_newline,
                remove_number,
                remove_punctuation,
                remove_whitespace
        ]
            for operation in operations:
                sentence = operation(sentence)
            return sentence
        
        return clean_up_pipeline(self)

    def sentiment(self):
        batch = tokenizer(self, max_length=128, padding=True, truncation=True, return_tensors='tf')
        outputs = model(batch)
        predict = tf.nn.softmax(outputs[0], axis=-1)
        label = tf.argmax(predict, axis=1).numpy()
        labels = ['Negative','Positive']
        classes = [labels[label[i]] for i in range(len(self))]
        print(["{:.2f}% negative & {:.2f}% positive then overall is {}"\
                            .format(predict[i][0]*100,
                            predict[i][1]*100, 
                            classes[i]) for i in range(len(self))])
        return predict

    def questionPattern():
        def combineVerb(listA, listB): 
            lst = [] 
            for item in list(product(listA, listB)): 
                lst.append(item[0]+ " "+ item[1])
            return lst

        def combineVerbShort(listA, listB): 
            lst = [] 
            for item in list(product(listA, listB)): 
                lst.append(item[0]+ item[1])
            return lst

        plural_helping_verbs = ["are", "were", "do"]
        helping_verbs1 = [
            "did", "can", "may", "will", 
            "could", "should", "would", "might",
            "have", "had"
        ]
        singular_helping_verbs_3rd = ["is", "does", "was", "has"]
        wh = ["what", "who", "which", "where", "why", "how", "whom"]
        plural_pronouns = ["you", "we", "they", "these", "those"]
        singular_pronouns = ["she", "he", "it", "that", "this"]
        etc = ['am i', 'was i', 'were i', 'are there', 'is there', 'do i']
        short  = ["'s", "'ve", "'d", "'ll", "’s", "’ll", "’ve", "’d"]
        i = ['i']
        comb1 = [
            "to know", "question is", "tell me",
            "explain it", "explain them"
            "to quest", "to have answer",
            "questions are", "to ask"
        ]
        comb2 = combineVerb(helping_verbs1, singular_pronouns)
        comb3 = combineVerb(helping_verbs1, i)
        comb4 = combineVerb(plural_helping_verbs, plural_pronouns)
        comb5 = combineVerb(singular_helping_verbs_3rd, singular_pronouns)
        comb6 = combineVerb(wh, sorted(comb1 + comb2 + comb3 + comb4 + comb5))
        comb7 = combineVerb(wh, etc)
        comb8 = combineVerb(helping_verbs1, plural_pronouns)
        comb9 = combineVerbShort(wh, short)
        question_patterns = sorted(comb1 + comb2 + comb3 + comb4 + comb5 +\
                                    comb6 + comb7 + comb8 + comb9)
        return question_patterns
    
    def isQuestion(self):
        helping_verbs2 = [
            "is", "am", "are", "was", "were"
            "do", "does", "did",
            "can", "may", "will",
            "could", "should", "would", "might",
            "have", "has", "had"
        ]
        question_types = ["whQuestion", "ynQuestion"]
        
        def _features(post):
            features = {}
            for word in nltk.word_tokenize(post):
                features['contains({})'.format(word.lower())] = True
            return features

        f = open('question_classifier.pickle', 'rb')
        linear_SVC = pickle.load(f)
        f.close()
        
        def is_ques_(ques):
            question_type = linear_SVC.classify(_features(ques)) 
            return question_type in question_types
        
        patterns = self.questionPattern()

        if not is_ques_(self):
            is_ques = False
            # check if any of pattern exist in sentence
            for pattern in patterns:
                is_ques = pattern in self
                if is_ques:
                    break

            # there could be multiple sentences so divide the sentence
            sentence_arr = self.split(".")
            for sentence in sentence_arr:
                if len(sentence.strip()):
                    # if question ends with ? or start with any helping verb
                    # word_tokenize will strip by default
                    first_word = nltk.word_tokenize(sentence)[0]
                    if sentence.endswith("?") or first_word in helping_verbs2:
                        is_ques = True
                        break
            return is_ques    
        else:
            return True

    # def is_spam(self):
    #     clf = load('filename.joblib')
    #     return clf(self)
    
    def toAnswer(self: list, treshold=.8):
        text = self[0].split('.')
        text = [self.preprocessing(text[i]) for i in range(len(text))]
        sent = self.sentiment(text)
        to_answer_ = []
        how_to_answer_ = []

        for i in range(len(text)):
            lang = self.language(text[i])
            # spam = is_spam()
            quest = self.is_question(text[i])

            to_answer = True
            how_to_answer = ""

            if lang:
                if quest:
                    # print(quest)
                    to_answer = True
                    how_to_answer = 'Manually'

                else:
                    if sent[i][1] > treshold:
                        to_answer = True
                        how_to_answer = 'Automatically'

                    else:
                        to_answer = True
                        how_to_answer = 'Manually'
            else:
                print("This classifier is working for English sentences")
                to_answer = False
                how_to_answer = "Not Recognized"

            print (text[i])
            to_answer_.append(to_answer)
            how_to_answer_.append(how_to_answer)
        
        print(to_answer_)
        print(how_to_answer_)
        
        if any(to_answer_):
            to_answer = True
        
        if any(item == 'Manually' for item in how_to_answer_):
            how_to_answer = 'Manually'

        return to_answer, how_to_answer

if __name__ == "__main__":
    pass