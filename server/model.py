import pickle
from pyvi import ViTokenizer, ViPosTagger
import re
from string import digits


class ClassifierModel:
    def __init__(self, path_model, path_tokenzier, total_comment: list):
        self.model = 0
        self.tokenizer = 0
        self.path_model = path_model
        self.path_tokenizer = path_tokenzier
        self.comments = total_comment

    def load_model(self):
        with open(self.path_tokenizer, 'rb') as f1:
            self.tokenizer = pickle.load(f1)

        with open(self.path_model, 'rb') as f2:
            self.model = pickle.load(f2)

    @staticmethod
    def add_postag(comment):
        comment = comment.lower()
        a = ViPosTagger.postagging(ViTokenizer.tokenize(comment))
        X = []
        for i in range(len(a[0])):
            test = a[0][i] + "_" + a[1][i]
            X.append(test)
        b = " ".join(X)
        return b

    @staticmethod
    def pre_processing(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        remove_digits = str.maketrans('', '', digits)
        text = text.translate(remove_digits)

        return text

    def predict(self, cmt):
        text = self.pre_processing(cmt)
        text = self.add_postag(text)
        tokenize = self.tokenizer.transform([text])
        pred = self.model.predict(tokenize)
        if pred == 0:
            return 'negative'
        elif pred == 1:
            return 'neutral'
        else:
            return 'positive'

    def counting_sentiment(self):
        negative = neutral = positive = 0
        for comment in self.comments:
            pred = self.predict(comment)
            if pred == 'negative':
                negative = negative + 1
            if pred == 'neutral':
                neutral = neutral + 1
            if pred == "positive":
                positive = positive + 1

        return {"negative": negative, "positive": positive, "neutral": neutral}
