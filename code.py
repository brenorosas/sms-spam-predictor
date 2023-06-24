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