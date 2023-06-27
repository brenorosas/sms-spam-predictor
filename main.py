from textblob import TextBlob
import nltk
nltk.download('punkt') # tokenizer
nltk.download('stopwords') # stopwords
import re

class NaiveBayes:
    compressed_dataset = {}
    dataset_len = 0
    total_by_class = {}
    dataset = []
    def __init__(self, dataset):
        self.dataset = dataset
        self.dataset_len = len(dataset)
        for i in range(len(dataset)):
            class_name = dataset[i][-1]
            dataset[i]
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

    def get_accuracy(self):
        right = 0
        wrong = 0
        false_spam = 0
        false_ham = 0
        for data in self.dataset:
            class_founded = self.__get_class_for_data_in_out(data)
            class_name = data[-1]
            if class_founded == class_name:
                right += 1
            else:
                if class_name == 'spam':
                    false_spam += 1
                else:
                    false_ham += 1
                wrong += 1
                
        print("total: ", right + wrong)
        print("right: ", right)
        print("wrong: ", wrong)
        print("false spam: ", false_spam)
        print("false ham: ", false_ham)
        print("accuracy: ", right / (right + wrong))
        print("accuracy: ", "{:.2f}".format(right / (right + wrong) * 100), "%")


    def __get_class_for_data_in_out(self, data):
        expected_class_name = data[-1]
        self.total_by_class[expected_class_name] -= 1
        for j in range(len(data) - 1):
            self.compressed_dataset[expected_class_name][(j,data[j])] -= 1

        class_founded = self.get_class_for_data(data[:-1])

        self.total_by_class[expected_class_name] += 1
        for j in range(len(data) - 1):
            self.compressed_dataset[expected_class_name][(j,data[j])] += 1

        return class_founded
    
    def get_class_for_data(self, data):
        max_prob = -1
        class_founded = ''
        for class_name in self.total_by_class:
            prob = self.total_by_class[class_name] / self.dataset_len
            for i in range(len(data)):
                if (i, data[i]) not in self.compressed_dataset[class_name]:
                    prob *= 0
                else:
                    prob *= self.compressed_dataset[class_name][(i, data[i])] / self.total_by_class[class_name]
            if prob > max_prob:
                max_prob = prob
                class_founded = class_name
        
        return class_founded

class SmsDatasetProcessor:
    processed_dataset = []
    attributes = []
    key_words = []
    stopwords = []
    def __init__(self, dataset):
        # self.attributes.append("text_length")
        # self.attributes.append("number_of_words")
        self.attributes.append("number_of_capital_letters")
        self.attributes.append("number_of_numbers")
        # self.attributes.append("number_of_simbols")
        # self.attributes.append("number_of_key_words")
        self.attributes.append("sentiment_analysis")
        self.attributes.append("has_link")
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
        self.key_words = [spam_words_count[i][0] for i in range(5)]

        for data in dataset:
            self.__add_sms_text(data[0], data[1])

        self.__normalize_dataset()

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
            elif attribute == "number_of_key_words":
                self.processed_dataset[idx].append(self.__get_number_of_key_words(sms_text))
            elif attribute == "sentiment_analysis":
                self.processed_dataset[idx].append(self.__analyze_sentiment(sms_text))
            elif attribute == "has_link":
                self.processed_dataset[idx].append(self.__check_for_link(sms_text))
            elif attribute == "has_phone_number":
                self.processed_dataset[idx].append(self.__check_for_phone_number(sms_text))
        self.processed_dataset[idx].append(class_name)

    def __get_number_of_capital_letters(self, sms_text):
        return sum(c.isupper() for c in sms_text)

    def __get_number_of_words(self, sms_text):
        return len(sms_text.split())

    def __get_number_of_numbers(self, sms_text):
        return sum(c.isdigit() for c in sms_text)

    def __get_number_of_simbols(self, sms_text):
        return sum(not (c.isalpha() or c.isdigit()) for c in sms_text)

    def __check_for_link(self, sms_text):
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        match = re.search(pattern, sms_text)
        if match:
            return True
        else:
            return False

    def __tokenize_and_remove_stopwords(self, sms_text):
        frase = sms_text.lower()
        tokens = nltk.word_tokenize(frase)
        tokens = [token for token in tokens if token not in self.stopwords]

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

    def __classify_attribute_in_large_medium_or_small(self, idx):
        values = sorted(list(set([self.processed_dataset[i][idx] for i in range(len(self.processed_dataset))])))
        # get three range of values
        first_range = [0, values[len(values) // 3]]
        second_range = [values[len(values) // 3], values[2 * len(values) // 3]]
        third_range = [values[2 * len(values) // 3], values[-1]]
        # classify each value
        for i in range(len(self.processed_dataset)):
            if self.processed_dataset[i][idx] in range(first_range[0], first_range[1]):
                self.processed_dataset[i][idx] = 'small'
            elif self.processed_dataset[i][idx] in range(second_range[0], second_range[1]):
                self.processed_dataset[i][idx] = 'medium'
            else:
                self.processed_dataset[i][idx] = 'large'

    def __normalize_dataset(self):
        for i in range(len(self.attributes)):
            if self.__attribute_needs_be_normalized(self.attributes[i]):
                self.__classify_attribute_in_large_medium_or_small(i)

    def __attribute_needs_be_normalized(self, attribute):
        if attribute == "text_length":
            return False
        elif attribute == "number_of_words":
            return False
        elif attribute == "number_of_capital_letters":
            return False
        elif attribute == "number_of_numbers":
            return False
        elif attribute == "number_of_simbols":
            return False
        elif attribute == "number_of_key_words":
            return False
        elif attribute == "sentiment_analysis":
            return False
        elif attribute == "has_link":
            return False

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

# train naive bayes
naive_bayes = NaiveBayes(processor.processed_dataset)
naive_bayes.get_accuracy()