from textblob import TextBlob
import nltk
nltk.download('punkt') # tokenizer
nltk.download('stopwords') # stopwords

class NaiveBayes:
    compressed_dataset = {}
    dataset_len = 0
    total_by_class = {}
    def __init__(self, dataset):
        self.dataset_len = len(dataset)
        for i in range(len(dataset)):
            class_name = dataset[i][-1]
            if class_name in self.total_by_class:
                self.total_by_class[class_name] += 1
            else:
                self.total_by_class[class_name] = 1

            if class_name not in self.compressed_dataset:
                self.compressed_dataset[class_name] = {}
            for j in range(len(dataset[i]) - 1):
                if (j,dataset[i][j]) in self.compressed_dataset[class_name]:
                    self.compressed_dataset[class_name][(j,dataset[i][j])] += 1
                else:
                    self.compressed_dataset[class_name][(j,dataset[i][j])] = 1
                

    def get_class_for_data(self, data):
        max_prob = 0
        max_class = ''
        print(self.compressed_dataset)
        for class_name in self.total_by_class:
            prob = self.total_by_class[class_name] / self.dataset_len
            for i in range(len(data)):
                prob *= self.compressed_dataset[class_name][(i, data[i])] / self.total_by_class[class_name]
            if prob > max_prob:
                max_prob = prob
                max_class = class_name

        return max_class

class SmsDatasetProcessor:
    processed_dataset = []
    attributes = []
    key_words = []
    stopwords = []
    def __init__(self, dataset):
        self.attributes = ["text_length", "number_of_words", "number_of_capital_letters", "number_of_numbers", "number_of_simbols", "sentiment_analysis", "number_of_key_words"]
        self.stopwords = nltk.corpus.stopwords.words('english')
        spam_words_count = {}
        for data in dataset:
            if data[0] == "spam":
                tokens = self.__tokenize_and_remove_stopwords(data[1])
                for token in tokens:
                    if token in spam_words_count:
                        spam_words_count[token] += 1
                    else:
                        spam_words_count[token] = 1

        spam_words_count = sorted(spam_words_count.items(), key=lambda x: x[1], reverse=True)
        self.key_words = [spam_words_count[i][0] for i in range(10)]

        for data in dataset:
            self.__add_sms_text(data[0], data[1])

    def __add_sms_text(self, class_name, sms_text):
        self.processed_dataset.append([])
        idx = len(self.processed_dataset) - 1
        for attribute in self.attributes:
            if attribute == "text_length":
                self.processed_dataset[idx].append(len(sms_text))
            elif attribute == "number_of_words":
                self.processed_dataset[idx].append(self.__get_number_of_words(sms_text))
            elif attribute == "number_of_capital_letters":
                self.processed_dataset[idx].append(self.__get_number_of_capital_letters(sms_text))
            elif attribute == "number_of_numbers":
                self.processed_dataset[idx].append(self.__get_number_of_numbers(sms_text))
            elif attribute == "number_of_simbols":
                self.processed_dataset[idx].append(self.__get_number_of_simbols(sms_text))
            elif attribute == "sentiment_analysis":
                self.processed_dataset[idx].append(self.__analyze_sentiment(sms_text))
            elif attribute == "number_of_key_words":
                self.processed_dataset[idx].append(self.__get_number_of_key_words(sms_text))
        self.processed_dataset[idx].append(class_name)

    def __get_number_of_capital_letters(self, sms_text):
        return sum(c.isupper() for c in sms_text)

    def __get_number_of_words(self, sms_text):
        return len(sms_text.split())

    def __get_number_of_numbers(self, sms_text):
        return sum(c.isdigit() for c in sms_text)

    def __get_number_of_simbols(self, sms_text):
        return sum(not (c.isalpha() or c.isdigit()) for c in sms_text)

    def __tokenize_and_remove_stopwords(self, sms_text):
        frase = sms_text.lower()
        tokens = nltk.word_tokenize(frase)

        return tokens

    def __analyze_sentiment(self, sms_text):
        blob = TextBlob(sms_text)
        polaridade = blob.sentiment.polarity

        if polaridade > 0:
            ans = 'positive'
        elif polaridade < 0:
            ans = 'negative'
        else:
            ans = 'neutral'

        return ans
    
    def __get_number_of_key_words(self, sms_text):
        tokens = self.__tokenize_and_remove_stopwords(sms_text)
        return sum(token in self.key_words for token in tokens)


# read lines untill EOF
dataset = []
while True:
    try:
        line = input().split()
        sms_class = line[0]
        sms_text = ' '.join(line[1:])
        dataset.append([sms_class, sms_text])
    except EOFError:
        break

# process dataset
processor = SmsDatasetProcessor(dataset)

