import time
from movie_dialogs_parser import movie_titles_metadata_to_dict, weight_calculator
import matplotlib.pyplot as plt


class MajorityClassifier:

    def __init__(self):
        MovieData = movie_titles_metadata_to_dict()
        self.total_movies = len(MovieData)
        self.histogram = [0] * 101
        for movieID, movieDict in MovieData.items():
            movieRating = movieDict['IMDB rating']
            index = int(float(movieRating) * 10)
            self.histogram[index] += 1

        self.max_rating = 0
        for i in range(101):
            if self.histogram[i] > self.histogram[self.max_rating]:
                self.max_rating = i

        self.max_rating_examples = self.histogram[self.max_rating]

    def Classify(self):
        return self.max_rating/10

    # def accuracy(self):
    #     return self.max_rating_examples / self.total_movies

    def plot_histogram(self):
        hist_plot = {}
        for i in range(101):
            if self.histogram[i] != 0:
                hist_plot[i/10] = self.histogram[i]

        lists = sorted(hist_plot.items())  # sorted by key, return a list of tuples
        x, y = zip(*lists)  # unpack a list of pairs into two tuples
        plt.plot(x, y)
        plt.xlabel('IMDB ratings')
        plt.ylabel('Size')
        plt.show()


if __name__ == "__main__":
    start_time = time.time()
    file = open("majority_result.txt", 'w')
    m = MajorityClassifier()
    movies = movie_titles_metadata_to_dict()
    total_score = 0
    for movie_id, movie_metadata in movies.items():
        movie_rating = movie_metadata['IMDB rating']
        score = weight_calculator(float(movie_rating), float(m.Classify()))
        write_line = movie_id + ' | ' + movie_rating + ' | ' + str(m.Classify()) + ' | ' + str(score) + '\n'
        file.write(write_line)
        total_score += score

    final_line = "Total entire corpus score is: " + str(total_score / len(movies)) + '\n'
    file.write(final_line)
    file.close()
    m.plot_histogram()
    print("--- %s seconds ---" % (time.time() - start_time))

