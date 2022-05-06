from words import wordList, letterWeight
import urllib3
import string

lowercaseLetters = list(string.ascii_lowercase)
newLetterWeight = {}
for letter in lowercaseLetters:
    newLetterWeight.update({letter : 0})

url = "https://www.nytimes.com/games/wordle/main.af610646.js"

http = urllib3.PoolManager()
response = http.request('GET', url)
wordString = response.data.decode('utf-8').split('ko=[')[1].split(']')[0]
disallowedCharacters = " \""
for character in disallowedCharacters:
    wordString = wordString.replace(character, "")
wordList = wordString.split(",")

for word in wordList:
    for letter in word:
        newLetterWeight[letter] = newLetterWeight[letter] + 1

totalNewLetters = 0
for letter in newLetterWeight:
    totalNewLetters += newLetterWeight[letter]

for letter in newLetterWeight:
    newLetterWeight[letter] = newLetterWeight[letter]/totalNewLetters

with open("words.py", "r") as f:
    wordsFile = f.readlines()
newWordsFile = "letterWeight = " + str(newLetterWeight) + "\n" + "wordList = " + str(wordList) + "\n" + wordsFile[2]

with open("words.py", "w") as f:
    f.write(newWordsFile)