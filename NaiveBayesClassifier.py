from movie_dialogs_parser import *
import time


class NaiveBayesClassifier:
    num_movies = 493

    def __init__(self):

        titlesDict = movie_titles_metadata_to_dict()
        self.totalExamples = 0
        histogram = [0] * 101
        for movieID, movieDict in titlesDict.items():
            self.totalExamples += 1
            movieRating = movieDict['IMDB rating']
            index = int(float(movieRating) * 10)
            histogram[index] += 1

        for i in range(101):
            histogram[i] /= self.totalExamples

        self.probArr = histogram
        self.totalData = MovieDialogParser()
        # HMM purposes
        self.classified = {}

    def Classify(self, x):
        maxSum = None
        maxRating = None
        for rating in self.totalData.rating2ID_dictionary.keys():
            sum = 0
            for ids in self.totalData.rating2ID_dictionary[rating]:
                if int(ids[1:]) <= 493:  # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
                    totalDialogs = self.totalData.corpus_dictionary[ids]['total_conversations']
                    for conver_dic in self.totalData.corpus_dictionary[ids]['conversation_dic'].values():
                        #   for dialog in conversations.values():
                        sum += object_similarity(x, conver_dic)
            prob = self.probArr[int(float(rating) * 10)]*(sum / totalDialogs)
            if maxSum is None or maxSum < prob:
                maxSum = prob
                maxRating = rating

        return maxRating

    def classify_movie(self, x):
        maxSum = None
        maxRating = None
        for rating in self.totalData.rating2ID_dictionary.keys():
            sum = 0
            for ids in self.totalData.rating2ID_dictionary[rating]:
                if int(ids[1:]) <= NaiveBayesClassifier.num_movies:
                    # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
                    movie_dic = self.totalData.corpus_dictionary[ids]
                    sum += object_similarity(x, movie_dic)

            prob = self.probArr[int(float(rating) * 10)] * (sum / NaiveBayesClassifier.num_movies)
            if maxSum is None or maxSum < prob:
                maxSum = prob
                maxRating = rating

        return maxRating

    def classify_hmm_movie(self, x_id, x):
        maxSum = None
        maxRating = None
        for rating in self.totalData.rating2ID_dictionary.keys():
            sum = 0
            for ids in self.totalData.rating2ID_dictionary[rating]:
                if int(ids[1:]) <= NaiveBayesClassifier.num_movies:  # TODO: comment out for using k_fold_CV
                    # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
                    movie_dic = self.totalData.corpus_dictionary[ids]
                    sum += object_similarity(x, movie_dic)

            # HMM
            if rating in self.classified.keys():
                for ids in self.classified[rating]:
                    movie_dic = self.totalData.corpus_dictionary[ids]
                    movie_actual_rating = x['metadata']['IMDB rating']
                    sum += weight_calculator(float(movie_actual_rating), float(rating))*object_similarity(x, movie_dic)

            prob = self.probArr[int(float(rating) * 10)]*(sum / NaiveBayesClassifier.num_movies)
            if maxSum is None or maxSum < prob:
                maxSum = prob
                maxRating = rating

        # HMM update
        if maxRating not in self.classified.keys():
            self.classified[maxRating] = []
        self.classified[maxRating].append(x_id)

        return maxRating


def nb_dialog_k_fold_cv_test():
    start_time = time.time()
    file = open("naive_bayes_dialog_result.txt", 'w')
    NB = NaiveBayesClassifier()
    total_score = 0
    progress = 0
    total_classified = 0
    for movie_id, movie_id_dict in NB.totalData.movie_titles.items():
        if int(movie_id[1:]) > 493:  # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
            progress += 1
            progress_print = progress/123
            print("progress %.4f" % progress_print)
            movie_score = 0
            for dialog_id, dialog in NB.totalData.corpus_dictionary[movie_id]['conversation_dic'].items():
                total_classified += 1
                predicted_rating = NB.Classify(dialog)
                movie_rating = movie_id_dict['IMDB rating']
                score = weight_calculator(float(movie_rating), float(predicted_rating))
                write_line = movie_id + ' | ' + str(dialog_id) + ' | ' + movie_rating + ' | ' + \
                             predicted_rating + ' | ' + str(score) + '\n'

                file.write(write_line)
                total_score += score
                movie_score += score
            # sum up movie score
            num_conver = NB.totalData.corpus_dictionary[movie_id]['total_conversations']
            write_line = '\nTotal: ' + movie_id + ' | ' + str(num_conver) + ' | ' + movie_rating + ' | ' + \
                         str(movie_score/float(num_conver)) + '\n\n'

            file.write(write_line)
    final_line = "Total entire corpus score is: " + str(total_score/total_classified) + '\n'
    file.write(final_line)
    file.close()
    print("-- %s seconds ---" % (time.time() - start_time))


def nb_k_fold_cv_test():
    start_time = time.time()
    file = open("naive_bayes_movie_result.txt", 'w')
    NB = NaiveBayesClassifier()
    total_score = 0
    progress = 0
    total_classified = 0
    for movie_id, movie_id_dict in NB.totalData.corpus_dictionary.items():
        if int(movie_id[1:]) > NaiveBayesClassifier.num_movies:
            # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
            progress += 1
            progress_print = progress/123
            print("progress %.4f" % progress_print)

            # for dialog_id, dialog in NB.totalData.corpus_dictionary[movie_id]['conversation_dic'].items():
            total_classified += 1

            predicted_rating = NB.classify_movie(movie_id_dict)
            movie_rating = movie_id_dict['metadata']['IMDB rating']
            score = weight_calculator(float(movie_rating), float(predicted_rating))
            write_line = movie_id + ' | ' + movie_rating + ' | ' + predicted_rating + ' | ' + str(score) + '\n'
            file.write(write_line)

            total_score += score

    final_line = "Total entire corpus score is: " + str(total_score/total_classified) + '\n'
    file.write(final_line)
    file.close()
    print("--- %s seconds ---" % (time.time() - start_time))


def nb_hmm_k_fold_cv_test():
    start_time = time.time()
    file = open("naive_bayes_movie_HMM_result.txt", 'w')
    NB = NaiveBayesClassifier()
    total_score = 0
    progress = 0
    total_classified = 0
    for movie_id, movie_id_dict in NB.totalData.corpus_dictionary.items():
        if int(movie_id[1:]) > NaiveBayesClassifier.num_movies:
            # used for 5 fold-Cross-Validation 493 = 80% from 616 total movies
            progress += 1
            progress_print = progress/123
            print("progress %.4f" % progress_print)

            # for dialog_id, dialog in NB.totalData.corpus_dictionary[movie_id]['conversation_dic'].items():
            total_classified += 1

            predicted_rating = NB.classify_hmm_movie(movie_id, movie_id_dict)
            movie_rating = movie_id_dict['metadata']['IMDB rating']
            score = weight_calculator(float(movie_rating), float(predicted_rating))
            write_line = movie_id + ' | ' + movie_rating + ' | ' + predicted_rating + ' | ' + str(score) + '\n'
            file.write(write_line)

            total_score += score

    final_line = "Total entire corpus score is: " + str(total_score/total_classified) + '\n'
    file.write(final_line)
    file.close()
    print("--- %s seconds ---" % (time.time() - start_time))


def nb_hmm_test():
    start_time = time.time()
    file = open("naive_bayes_movie_HMM_result_no_CV.txt", 'w')
    NB = NaiveBayesClassifier()
    total_score = 0
    progress = 0
    total_classified = 0
    for movie_id, movie_id_dict in NB.totalData.corpus_dictionary.items():
        progress += 1
        progress_print = progress/123
        print("progress %.4f" % progress_print)

        # for dialog_id, dialog in NB.totalData.corpus_dictionary[movie_id]['conversation_dic'].items():
        total_classified += 1

        predicted_rating = NB.classify_hmm_movie(movie_id, movie_id_dict)
        movie_rating = movie_id_dict['metadata']['IMDB rating']
        score = weight_calculator(float(movie_rating), float(predicted_rating))
        write_line = movie_id + ' | ' + movie_rating + ' | ' + predicted_rating + ' | ' + str(score) + '\n'
        file.write(write_line)

        total_score += score

    final_line = "Total entire corpus score is: " + str(total_score/total_classified) + '\n'
    file.write(final_line)
    file.close()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    nb_hmm_test()
