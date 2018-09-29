import movie_dialogs_parser
import time

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
                self.w[feature] += 0.2*x[feature]
            else:
                self.w[feature] = x[feature]

    def sub_from_w(self, x):
        keys = list(self.w.keys())
        x_keys = list(x.keys())
        for feature in x_keys:
            if feature in keys:
                # correcting each feature in w
                self.w[feature] -= 0.2*x[feature]
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
                summary += movie_dialogs_parser.weight_calculator(x[key], w[key])
        return summary

    def predict(self, x):
        return self.compute_predicted_label(x)

############################################################
# Section 2: Applications
############################################################


class MovieClassifier(object):
    """
    data: the actual corpus_dictionary itself.
    aka: movie_dialogs_parser.MovieDialogParser.corpus_dictionary
    """
    def __init__(self, iterations):
        self.data = movie_dialogs_parser.MovieDialogParser().corpus_dictionary
        dict_data = []
        for example_id, example in self.data.items():
            # TODO: comment out for movie classifier - leave untouched for dialog
            # TODO: change dialog -> example for iterate the learning algorithm
            movie_id_rating = example['metadata']['IMDB rating']
            # for movie_dialog in example['conversation_dic'].values():
            iterate = example
            feature_dict = {'bag_size': sum(iterate['bag_of_words'].values()),
                            'set_size': len(iterate['set_of_words'])}
            if 'total_lines' in iterate.keys():
                feature_dict['total_lines'] = iterate['total_lines']
            if 'total_conversations' in iterate.keys():
                feature_dict['total_conversations'] = iterate['total_conversations']

            # for consistency tuple of (features, label)
            dict_data.append((feature_dict, movie_id_rating))

        self.cls = MulticlassStructuredPerceptron(dict_data, iterations)

    def classify(self, instance):
        feature_dict = {'bag_size': sum(instance['bag_of_words'].values()),
                        'set_size': len(instance['set_of_words'])}
        if 'total_lines' in instance.keys():
            feature_dict['total_lines'] = instance['total_lines']
        if 'total_conversations' in instance.keys():
            feature_dict['total_conversations'] = instance['total_conversations']
        return self.cls.predict(feature_dict)


def movie_perceptron_classifier():
    start_time = time.time()
    file = open("perceptron_result.txt", 'w')
    mc = MovieClassifier(35)
    total_score = 0
    progress = 0
    total_classified = 0
    for movie_id, movie_id_dict in mc.data.items():
        # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
        progress += 1
        progress_print = progress/617
        print("progress %.4f" % progress_print)

        # for dialog_id, dialog in NB.totalData.corpus_dictionary[movie_id]['conversation_dic'].items():
        total_classified += 1

        predicted_rating = mc.classify(movie_id_dict)
        movie_rating = movie_id_dict['metadata']['IMDB rating']
        score = movie_dialogs_parser.weight_calculator(float(movie_rating), float(predicted_rating))
        write_line = movie_id + ' | ' + movie_rating + ' | ' + predicted_rating + ' | ' + str(score) + '\n'
        file.write(write_line)

        total_score += score

    final_line = "Total entire corpus score is: " + str(total_score/total_classified) + '\n'
    file.write(final_line)
    file.close()
    print("--- %s seconds ---" % (time.time() - start_time))

def movie_dialog_perceptron_classifier():
    start_time = time.time()
    file = open("perceptron_dialog_result2.txt", 'w')
    mc = MovieClassifier(35)
    total_score = 0
    progress = 0
    total_classified = 0
    for movie_id, movie_id_dict in mc.data.items():
        # if int(movie_id[1:]) == 493:  # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
        progress += 1
        progress_print = progress/617
        print("progress %.4f" % progress_print)
        movie_score = 0
        for dialog_id, dialog in mc.data[movie_id]['conversation_dic'].items():
            total_classified += 1
            predicted_rating = mc.classify(dialog)
            movie_rating = movie_id_dict['metadata']['IMDB rating']
            score = movie_dialogs_parser.weight_calculator(float(movie_rating), float(predicted_rating))
            write_line = movie_id + ' | ' + str(dialog_id) + ' | ' + movie_rating + ' | ' + \
                         predicted_rating + ' | ' + str(score) + '\n'

            file.write(write_line)
            total_score += score
            movie_score += score
        # sum up movie score
        num_conver = mc.data[movie_id]['total_conversations']
        write_line = '\nTotal: ' + movie_id + ' | ' + str(num_conver) + ' | ' + movie_rating + ' | ' + \
                     str(movie_score/float(num_conver)) + '\n\n'

        file.write(write_line)
    final_line = "Total entire corpus score is: " + str(total_score/total_classified) + '\n'
    file.write(final_line)
    file.close()
    print('\n\n' + str(total_score/total_classified) + '\n\n')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    movie_perceptron_classifier()
