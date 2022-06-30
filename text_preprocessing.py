import re, string

def preprocessing(self): 
    """_summary_
    """
    
    def remove_hyperlink(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return re.sub(r"http\S+", "", self)

    def to_lower(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.lower()

    def remove_number(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return re.sub(r'\d+', '', self)

    def remove_punctuation(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.translate(str.maketrans(dict.fromkeys(string.punctuation)))

    def remove_whitespace(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.strip()

    def replace_newline(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.replace('\n','')

    def remove_emoji(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F91F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', self)
        

    def remove_hashtag(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return re.sub("#[A-Za-z0-9_]+","", self)

    def remove_mentioned(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return re.sub("@[A-Za-z0-9_]+","", self)

    def clean_up_pipeline(sentence):
        """_summary_

        Args:
            sentence (_type_): _description_
        """
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

if __name__ == '__main__':
    text = "Go until jurong point, crazy.. Available only in bugis n great \
        world la e buffet... Cine there got amore wat..."
    p = preprocessing(text)