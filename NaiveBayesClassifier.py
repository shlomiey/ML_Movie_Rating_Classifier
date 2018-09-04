class NaiveBayesClassifier:
    BagOfWords = {}


## Assumptions: linesDict and conversationDict at dictionries inside dictrioneries
# #the list of lineIDs should be numbers
    def __init__(self, linesDict, conversationDict):
        for movieConvDict in conversationDict.values():
            list = movieConvDict['list']
            for i in list:
                movieLineDict = linesDict[i]
                text = movieLineDict['text']
                sepText = text.split(' ')
                for word in sepText:
                    count = self.BagOfWords.get(word)
                    if count is None:
                        self.BagOfWords[word] = 1
                    else:
                        self.BagOfWords[word] = count + 1



