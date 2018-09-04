class MajorityClassifier:
    rating = 0.1

    def __init__(self, MovieData):
        histogram = [0] * 100
        for movieID, movieDict in MovieData.items():
            movieRating = movieDict['IMDBrating']
            index = movieRating * 10 - 1 ################## may need to subtract 1 here if the indexes start at 0
            histogram[index] += 1

        max = None
        for i in range(100):
            if max is None:
                max = i
                continue

            if (histogram[i] > histogram[max]):
                max = i

        self.rating = max/10

    def Classify(self, x):
        return self.rating


