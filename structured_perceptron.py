############################################################
# Section 1: Perceptrons
############################################################


class BinaryPerceptron(object):
    """ binary perceptron class"""
    def __init__(self, examples, iterations):
        self.w = {}
        for iter in range(0, iterations):
            for example in examples:
                # iterating over each examplein the training data #iteration times
                y_i = self.predict(example[0])
                if y_i != example[1]:
                    # if the prediction is wrong - need correctness
                    if example[1]:
                        self.add_to_w(example[0])
                    else:
                        self.sub_from_w(example[0])

    def get_w(self):
        return self.w

    def add_to_w(self, x):
        keys = list(self.w.keys())
        x_keys = list(x.keys())
        for feature in x_keys:
            # correcting each feature in w
            if feature in keys:
                self.w[feature] += x[feature]
            else:
                self.w[feature] = x[feature]

    def sub_from_w(self, x):
        keys = list(self.w.keys())
        x_keys = list(x.keys())
        for feature in x_keys:
            if feature in keys:
                # correcting each feature in w
                self.w[feature] -= x[feature]
            else:
                self.w[feature] = -x[feature]

    def compute_prediction(self, x):
        keys = list(self.w.keys())
        x_keys = list(x.keys())
        predict_right = 0  # number of good prediction per feature
        for feature in x_keys:
            if feature in keys:
                # if the prediction is correct +1 for feature correctness
                predict_right += x[feature] == self.w[feature]
            else:
                self.w[feature] = x[feature]
                predict_right += 1
        return predict_right

    def correct_prediction(self, x):
        x_keys = list(x.keys())
        for feature in x_keys:
                self.w[feature] = self.w[feature] + x[feature]

    def predict_score(self, x):
        summary = 0
        keys_x = list(x.keys())
        keys_w = list(self.w.keys())
        for key in keys_x:
            if key in keys_w:  # if not in w than it's 0
                summary += x[key]*self.w[key]
        return summary

    def predict(self, x):
        if self.predict_score(x) > 0:
            return True
        return False


class MulticlassStructuredPerceptron(object):
    """ here we'll have a dictionary where key is a possible label
    and the value it's vector wights (a binary perceptron) """
    def __init__(self, examples, iterations):
        self.total_w = {}
        possible_labels = set([x[1] for x in examples])
        self.labels = list(possible_labels)
        num_of_labels = len(possible_labels)
        for i in range(num_of_labels):
            self.total_w[self.labels[i]] = {}
        for iter in range(iterations):
            for example in examples:
                # iterating over the example #iteration times and update each wrong prediction in the w's dictionary
                predicted_label = self.compute_predicted_label(example[0])
                if predicted_label != example[1]:
                    # making the update
                    self.update_ws(example[1], predicted_label, example[0])

    def update_ws(self, correct_label, incorrect_label, example):
        self.add_to_w(example, correct_label)
        self.sub_from_w(example, incorrect_label)

    def add_to_w(self, x, label):
        keys = list(self.total_w[label].keys())
        x_keys = list(x.keys())
        for feature in x_keys:
            # making the update per feature
            if feature in keys:
                self.total_w[label][feature] += x[feature]
            else:
                self.total_w[label][feature] = x[feature]

    def sub_from_w(self, x, label):
        keys = list(self.total_w[label].keys())
        x_keys = list(x.keys())
        for feature in x_keys:
            # making the update per feature
            if feature in keys:
                self.total_w[label][feature] -= x[feature]
            else:
                self.total_w[label][feature] = -x[feature]

    def compute_predicted_label(self, example):
        max = None
        selected_label = None
        for i in range(len(self.labels)):
            w = self.total_w[self.labels[i]]
            # searching the argmax perceptron's label that the multiclass yield
            if max is None:
                max = self.predict_score(example, w)
                selected_label = self.labels[i]
                continue
            tempMax = self.predict_score(example, w)
            if (tempMax > max):
                max = tempMax
                selected_label = self.labels[i]
        return selected_label

    @staticmethod
    def predict_score(x, w):
        summary = 0
        keys_x = list(x.keys())
        keys_w = list(w.keys())
        for key in keys_x:
            if key in keys_w:  # if not in w than it's 0
                summary += x[key]*w[key]
        return summary

    def predict(self, x):
        return self.compute_predicted_label(x)

############################################################
# Section 2: Applications
############################################################



#
#
# class IrisClassifier(object):
#
#     def __init__(self, data):
#         dictData = []
#         for example in data:
#             tupleData = example[0]
#             tempDict = {}
#             tempDict['x1'] = tupleData[0]
#             tempDict['x2'] = tupleData[1]
#             tempDict['x3'] = tupleData[2]
#             tempDict['x4'] = tupleData[3]
#             temp = tupleData[2]
#             if temp < 2:
#                 tempDict['x5'] = -1
#             elif 2 <= temp <= 4.5:
#                 tempDict['x5'] = 0
#             else:
#                 tempDict['x5'] = 1
#
#             dictData.append((tempDict, example[1]))
#         self.cls = MulticlassStructuredPerceptron(dictData, 135)
#
#     def classify(self, instance):
#         newDict = {}
#         for i in range(len(instance)):
#             newDict['x' + str(i+1)] = instance[i]
#         x = newDict
#         return self.cls.predict(x)
#
#
# class DigitClassifier(object):
#
#     def __init__(self, data):
#         dictData = []
#         for example in data:
#             tupleData = example[0]
#             tempDict = {}
#             for i in range(len(example[0])):
#                 tempDict['x' + str(i+1)] = tupleData[i]
#             dictData.append((tempDict, example[1]))
#         self.cls = MulticlassStructuredPerceptron(dictData, 38)
#
#     def classify(self, instance):
#         newDict = {}
#         for i in range(len(instance)):
#             newDict['x' + str(i + 1)] = instance[i]
#         x = newDict
#         return self.cls.predict(x)
#
#
# class BiasClassifier(object):
#
#     def __init__(self, data):
#         dictData = []
#         for example in data:
#             tupleData = example[0]
#             tempDict = {}
#             tempDict['x1'] = tupleData
#             # additional feature from observation on the data set
#             if (tupleData >= 1):
#                 tempDict['x2'] = 1
#             else:
#                 tempDict['x2'] = -1
#             dictData.append((tempDict, example[1]))
#         self.cls = BinaryPerceptron(dictData, 10)
#
#     def classify(self, instance):
#         newDict = {}
#         newDict['x1'] = instance
#         if (instance >= 1):
#             newDict['x2'] = 1
#         else:
#             newDict['x2'] = -1
#         x = newDict
#         return self.cls.predict(x)
#
#
# class MysteryClassifier1(object):
#
#     def __init__(self, data):
#         dictData = []
#         for example in data:
#             tupleData = example[0]
#             tempDict = {}
#             # tempDict['x1'] = tupleData[0]
#             # tempDict['x2'] = tupleData[1]
#             # tempDict['x3'] = tupleData[0]*tupleData[1]
#             # tempDict['x4'] = tupleData[0] + tupleData[1]
#             # tempDict['x5'] = tupleData[0] - tupleData[1]
#             if abs(tupleData[0]) > 2:
#                 tempDict['x2'] = 1
#             else:
#                 tempDict['x3'] = 0
#             dictData.append((tempDict, example[1]))
#         self.cls = BinaryPerceptron(dictData, 10)
#
#     def classify(self, instance):
#         newDict = {}
#         newDict['x1'] = instance[0]
#         newDict['x2'] = instance[1]
#         newDict['x3'] = instance[0]*instance[1]
#         newDict['x4'] = instance[0]+instance[1]
#         newDict['x5'] = instance[0] - instance[1]
#         x = newDict
#         return self.cls.predict(x)
#
#
# class MysteryClassifier2(object):
#
#     def __init__(self, data):
#         dictData = []
#         for example in data:
#             tupleData = example[0]
#             tempDict = {}
#             tempDict['x1'] = tupleData[0]
#             tempDict['x2'] = tupleData[1]
#             tempDict['x3'] = tupleData[2]
#             if tupleData[0]*tupleData[1]*tupleData[2] > 0:
#                 tempDict['x4'] = 1
#             else:
#                 tempDict['x4'] = -1
#             dictData.append((tempDict, example[1]))
#         self.cls = BinaryPerceptron(dictData, 10)
#
#     def classify(self, instance):
#         newDict = {}
#         newDict['x1'] = instance[0]
#         newDict['x2'] = instance[1]
#         newDict['x3'] = instance[2]
#         # additional feature from observation on the data set
#         if instance[0] * instance[1] * instance[2] > 0:
#             newDict['x4'] = 1
#         else:
#             newDict['x4'] = -1
#         x = newDict
#         return self.cls.predict(x)
