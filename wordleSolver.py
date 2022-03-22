from words import wordList, letterWeight, vowelList

def add_values_in_dict(sample_dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

def remove_underscores(inputString):
    outputString = ""
    for inputChar in inputString:
        if inputChar != "_":
            outputString = outputString + inputChar
    return outputString

wordNumber = 0
notLetters = ""
containsLetters = ""
#dictionary of what letters can't be in a certain spot but are in the word
containsLettersDict = {}
while wordNumber < 6:
    #lists what word to open with
    if wordNumber < 1:
        print("Open with \"AUDIO\"")
        wordNumber += 1
    #asks for user to input their current guess
    print("Enter your results for word " + str(wordNumber + 1) + ":")
    wordString = input("Type what letters are guaranteed (green) using \"_\" to denote uncertainty (yellow or gray): ")
    wordDict = {}
    for idx, letter in enumerate(wordString):
        if letter != "_":
            wordDict[idx] = letter.lower()
    wordString = remove_underscores(wordString)
    containsInput = input("Type what letters are contained in the word (yellow) using \"_\" for other letters (green or gray): ")
    containsLetters = containsLetters + remove_underscores(containsInput).lower()
    for idx, letter in enumerate(containsInput):
        if letter != "_":
            containsLettersDict = add_values_in_dict(containsLettersDict, idx, letter.lower())
    notLettersInput = input("Type what letters are not contained in the word (gray) without using spaces: ").lower()
    for letter in notLettersInput:
        if letter not in notLetters:
            if letter not in containsLetters:
                if len(wordDict) > 0:
                    for idx in wordDict:
                        if letter not in wordDict[idx]:
                            notLetters = notLetters + letter
                            break
                else:
                    notLetters = notLetters + letter

    #check to see which words are valid
    words = ""
    wordsList = []
    for i in wordList:
        knownLettersLen = len(wordDict)
        #checks if the word has a known letter at the index of the known letter
        for idx in wordDict:
            if i[idx] == wordDict[idx]:
                knownLettersLen -= 1
        if knownLettersLen == 0:
            notLettersLen = len(notLetters)
            #checks if the word has a letter that is not in the word
            for notLetter in notLetters:
                if notLetter in i:
                    notLettersLen -= 1
            if notLettersLen == len(notLetters):
                containsLettersLen = len(containsLetters)
                #checks if the word has all of the known letters
                for letter in containsLetters:
                    if letter in i:
                        containsLettersLen -= 1
                if containsLettersLen == 0:
                    #checks if the known letters are in a spot that is incorrect
                    if len(containsLettersDict.keys()) == 0:
                        wordsList.append(i)
                    else:
                        for key in containsLettersDict.keys():
                            if i[key] not in containsLettersDict[key]:
                                wordsList.append(i)

    #score each word based on the commonality weight of their letters
    scoredWords = {}
    for word in wordsList:
        scoredWords[word] = 0
        for letter in word:
            scoredWords[word] = scoredWords.get(word) + letterWeight.get(letter)
            #subtract .5 for each duplicate letter
            if word.count(letter) > 1:
                scoredWords[word] = scoredWords.get(word) - 0.5
            #add .2 for each vowel
            if letter in vowelList:
                scoredWords[word] = scoredWords.get(word) + 0.2

    #sort the scored words from best to worst
    sortScoredWords = []
    for word in scoredWords:
        sortScoredWords.append([word, scoredWords[word]])
    sortScoredWords.sort(key = lambda sortScoredWords: sortScoredWords[1], reverse=True)

    #print the words in score order
    print("Here are words to try:")
    wordsDisplayed = 0
    while wordsDisplayed < 3:
        for word, weight in sortScoredWords:
            if wordsDisplayed < 3:
                print(word)
                wordsDisplayed += 1
    wordNumber += 1