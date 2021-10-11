from nltk.tokenize import sent_tokenize, word_tokenize
import random
import json
from flask import jsonify
import json

from util.Document import Document
from util.Sentence import Sentence
from util.data import parse_doc
from util.data import extract_arguments
from util.data import extract_entities

test_sens = """We should abandon Youtube. Toolassisted speedruns uploaded to video sites like Nico Nico Douga, YouTube or 
TASVideos may be described as a new world record by TASsan , who is said to have the superhuman memory and reflexes
"""

def do_label_arg(marks):
    # print("marks:" + str(marks))
    marks_new = []
    for i, item in enumerate(marks):
        # for (var i = 0; i < marks.length; i++):
        if i > 0 and i + 1 < len(marks):
            # Start Label
            if marks[i]['type'][0] == "P" and marks[i - 1]['type'][0] != marks[i]['type'][0]:
                mark = {'type': "PREMISE", 'start': marks[i]['start']}
                marks_new.append(mark)
            elif marks[i]['type'][0] == "C" and marks[i - 1]['type'][0] != marks[i]['type'][0]:
                mark = {'type': "CLAIM", 'start': marks[i]['start']}
                marks_new.append(mark)
                # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                if marks[i]['type'][0] != marks[i + 1]['type'][0]:
                    mark = marks_new.pop()
                    mark['end'] = marks[i]['end']
                    marks_new.append(mark)
        elif i == 0 and i + 1 < len(marks):
            # Start Label
            if marks[i]['type'][0] == "P":
                mark = {'type': "PREMISE", 'start': marks[i]['start']}
                marks_new.append(mark)
            elif (marks[i]['type'][0] == "C"):
                mark = {'type': "CLAIM", 'start': marks[i]['start']}
                marks_new.append(mark)
            # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                if marks[i]['type'][0] != marks[i + 1]['type'][0]:
                    mark = marks_new.pop()
                    mark['end'] = marks[i]['end']
                    marks_new.append(mark)
        elif i == 0 and i + 1 == len(marks):
            # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                mark['end'] = marks[i]['end']
                marks_new.append(mark)
    return marks_new


"""Models"""

from Model import Model


modelIBM = Model("IBM.h5")




print(modelIBM.label(test_sens))

print("*" *10)

doc = modelIBM.label_with_probs(test_sens)
print("test results: ", doc)

text= test_sens

currentPos = 0
data = []
for sentence in doc:
    for token in sentence:
        start = text.find(token["token"], currentPos)
        end = start + len(token["token"])
        currentPos = end
        currentWord = {}
        currentWord['start'] = start
        currentWord['end'] = end
        currentWord['type'] = token["label"]
        data.append(currentWord)

data = do_label_arg(data)
print("data: ", data)