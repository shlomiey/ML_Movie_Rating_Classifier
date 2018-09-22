from movie_dialogs_parser import MovieDialogParser
from movie_dialogs_parser import object_similarity

class NaiveBayesClassifier:
    BagOfWords = {}
    allRatings = [ '0.0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9', '1.0','1.1','1.2','1.3','1.4','1.5','1.6','1.7','1.8','1.9',
                   '2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '3.0','3.1','3.2','3.3','3.4','3.5','3.6','3.7','3.8','3.9',
                   '4.0', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '5.0','5.1','5.2','5.3','5.4','5.5','5.6','5.7','5.8','5.9',
                   '6.0', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7.0','7.1','7.2','7.3','7.4','7.5','7.6','7.7','7.8','7.9',
                   '8.0', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '9.0','9.1','9.2','9.3','9.4','9.5','9.6','9.7','9.8','9.9', '10.0' ]

## Assumptions: linesDict and conversationDict are dictionries inside dictrioneries
# #the list of lineIDs should be numbers
    def __init__(self, linesDict, conversationDict, titlesDict):
        for movieConvDict in conversationDict.values():
            list = movieConvDict['list']
            movieID = movieConvDict['movieID']
            rating = titlesDict[movieID]['IMDB rating']
            for i in list:
                movieLineDict = linesDict[i]
                text = movieLineDict['text']
                sepText = text.split(' ')
                for word in sepText:
                    tupleKey = tuple(word, rating)
                    count = self.BagOfWords.get(tupleKey)
                    if count is None:
                        self.BagOfWords[tupleKey] = 1
                    else:
                        self.BagOfWords[tupleKey] = count + 1

        self.totalExamples = 0
        histogram = [0] * 100
        for movieID, movieDict in titlesDict.items():
            self.totalExamples += 1
            movieRating = movieDict['IMDB rating']
            index = int(float(movieRating) * 10 - 1)  ################## may need to subtract 1 here if the indexes start at 0
            histogram[index] += 1

        for i in range(100):
            histogram[i] /= self.totalExamples

        self.probArr = histogram
        self.totalData = MovieDialogParser()


    def Classify(self, x):
        maxSum = None
        maxRating = None
        for rating in self.totalData.rating2ID_dictionary.keys():
            sum = 0
            for ids in self.totalData.rating2ID_dictionary[rating]:
                totalDialogs = self.totalData.corpus_dictionary[ids]['total_conversations']
                for conversations in self.totalData.corpus_dictionary[ids]['conversation_dic']:
                    for dialog in conversations.values():
                        sum += object_similarity(x, dialog)
            prob = sum / totalDialogs
            if maxSum is None or maxSum < prob:
                maxSum = prob
                maxRating = rating

        return maxRating