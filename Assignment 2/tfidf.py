# For this problem, you are given a set of documents (text files) on which you will perform some 
    # preprocessing tasks, and then compute what is called the TF-IDF score for each word. 
    # The TF-IDF score for a word is measure of its importance within the entire set of documents: 
    # the higher the score, the more important is the word.

# The input set of documents must be read from a file named "tfidf_docs.txt". This file will list all 
    # the documents (one per line) you will need to work with. For instance, if you need to work with 
    # the set "doc1.txt", "doc2.txt", and "doc2.txt", the input file "tfidf_docs.txt" contents 
    # will look like this:
        # doc1.txt
        # doc2.txt
        # doc2.txt
import csv
import re
from collections import Counter
from collections import defaultdict
import math

#     Part 1: Preprocessing (30 pts)
#     For each document in the input set, clean and preprocess it as follows:
def main():
    doclist = []
    with open("tfidf_docs.txt") as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                doclist.extend(row)
    stopwords = []
    with open("stopwords.txt") as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                stopwords.append(row[0])
    pdoclist = []
    for item in doclist:
        with open(item) as csvfile:
            reader = csv.reader(csvfile)
            newfilen = 'preproc_' + item
            pdoclist.append(newfilen)
            with open(newfilen,'w',newline='') as csvout:
                newrow = ''
                for row in reader:
                    for string in row:
                        rowwords = string.split(' ')
                        for word in rowwords:
                        
# Clean.
    # Remove all characters that are not words or whitespaces. Words are sequences of letters 
        # (upper and lower case), digits, and underscores.
    #AKA remove all punctuation that is not an underscore
    # Remove extra whitespaces between words. e.g., “Hello World! Let’s   learn    Python!”, so that 
        # there is exactly one whitespace between any pair of words.
    # Remove all website links. A website link is a sequence of non-whitespace characters that starts with 
        # either "http://" or "https://".
                            if word == '':
                                continue
                            if re.search(r'^http://.*', word) or re.search(r'^https://.*', word):
                                continue
                            res = re.sub(r'[^\w\s_]', '', word)
    # Convert all the words to lowercase.
                            res = res.lower()
    # The resulting document should only contain lowercase words separated by a single whitespace.

# Remove stopwords.
    # From the document that results after #1 above, remove "stopwords". These are the non-essential 
        # (or "noise") words listed in the file stopwords.txt
                            if res in stopwords:
                                continue
# Stemming and Lemmatization.
    # This is a process of reducing words to their root forms. For example, look at the following reductions: 
        # run, running, runs → run. All three words capture the same idea ‘run’ and hence their suffixes 
        # are not as important.
    # Use the following rules to reduce the words to their root form:
        # Words ending with "ing": "flying" becomes "fly"
        # Words ending with "ly": "successfully" becomes "successful"
        # Words ending with "ment": "punishment" becomes "punish"
                            ending = re.compile(r'(.*)(ing$)')
                            test = ending.search(res)
                            if test != None:
                                res = test.groups()[0]
                            ending = re.compile(r'(.*)(ly$)')
                            test = ending.search(res)
                            if test != None:
                                res = test.groups()[0]
                            ending = re.compile(r'(.*)(ment$)')
                            test = ending.search(res)
                            if test != None:
                                res = test.groups()[0]

        # These rules are not expected to capture all the edge cases of Stemming in the English language 
            # but are intended to give you a general idea of the preprocessing steps in NLP 
            # (Natural Language Processing) tasks. 

# After performing #1, #2, and #3 above for each input document, write the modified data to 
    # another text file with the prefix "preproc_". For instance, if the input document is "doc1.txt", 
    # the output should be "preproc_doc1.txt".
                            newrow = newrow + res + ' '
                newrow = re.sub(r' $', "", newrow)
                csvout.write(newrow)
# If you do not print to a file, or your output file name is not exactly as required, you will get 0 points.




# Part 2: Computing TF-IDF Scores (30 pts)
# Once preprocessing is performed on all the documents, you need to compute the Term Frequency(TF) — 
    # Inverse Document Frequency(IDF) score for each word.

# Steps:
# For each preprocessed document that results from the preprocessing in Part 1, compute frequencies 
    # of all the distinct words in that document only. So if you had 3 documents in the input set, 
    # you will compute 3 sets of word frequencies, one per document.
    tflists = defaultdict(list)      # doc to tuple list (word, tf)
    idfdict = defaultdict(int)       # word to idf
    for index in range(0, len(pdoclist)):
        with open(pdoclist[index]) as csvfile:
            reader = csv.reader(csvfile)
        
#  Compute the Term Frequency (TF) of each distinct word for each of the preprocessed documents:
    # TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
    # Note: The denominator, total number of terms, is the sum total of all the words, not just 
        # unique instances. So if a word occurs 5 times, and the total number of words in a document is 100,
        # then TF for that word is 5/100.
# Compute the Inverse Document Frequency (IDF) of each distinct word for each of the preprocessed documents.
    # IDF(t) = log((Total number of documents) / (Number of documents the word is found in)) + 1
    # Note: The log here uses base e. And 1 is added after the log is taken, so that the IDF score is 
        # guaranteed to be non-zero.
            for row in reader:   #each doc only has 1 row, so row[0] = whole doc string
                wordlist = row[0].split(' ')
                wordcount = Counter(wordlist)
                for key in wordcount:
                    tf = wordcount[key]/len(wordlist)
                    tftuple = (key, tf)
                    tflists[doclist[index]].append(tftuple)
                    idfdict[key] += 1        
    for key in idfdict:
        idfdict[key] = math.log(len(pdoclist)/idfdict[key]) + 1
# Calculate TF-IDF score: TF * IDF for each distinct word in each preprocessed document. 
    # Round the score to 2 decimal places.

# Print the top 5 most important words in each preprocessed document according to their TF-IDF scores. 
    # The higher the TF-IDF score, the more important the word. In case of ties in score, pick words 
    # in alphabetical order. You should print the result as a list of (word,TF-IDF score) tuples sorted 
    # in descending TF-IDF scores. See the Testing section below, in files tfidf_test1.txt and 
    # tfidf_test2.txt, for the exact output format.

    # Print to a file prefixed with "tfidf_". So if the initial input document was "doc1.txt", 
        # you should print the TF-IDF results to "tfidf_doc1.txt".
    # If you do not print to a file, or your output file name is not exactly as required, 
        # you will get 0 points. 
    for index in range(0, len(doclist)):
        newfilen = 'tfidf_' + doclist[index]
        with open(newfilen,'w',newline='') as csvout:
            tfidflist = []   #tuple list (word,tfidf)
            for tup in tflists[doclist[index]]:
                (word, tf) = tup
                tfidf = round(tf * idfdict[word], 2)
                tfidfTup = (word, tfidf)
                tfidflist.append(tfidfTup)
            tfidflist = sorted(tfidflist, key=lambda x: (x[1] * -1, x[0].lower()))
            tfidflist = tfidflist[0:5]
            tuplistStr = '['
            for tup in tfidflist:
                (word, tfidf) = tup
                tuplistStr = tuplistStr + f"('{word}', {str(tfidf)}), "
            tuplistStr = re.sub(r', $', "", tuplistStr) + ']'
            csvout.write(tuplistStr)

# Testing:
# You can begin with the following three sentences as separate documents against which to test your code:
    # #d1 = "It is going to rain today."
    # #d2 = "Today I am not going outside."
    # #d3 = "I am going to watch the season premiere."
 
    # You can match values computed by your code with this same example in the 
        # TF-IDF/Term Frequency Technique page referenced above. Look for it under 
        # "Let's cover an example of 3 documents" on this page. (Note: We are adding 1 to the log 
        # for our IDF computation.)

# Next, you can test your code against test1.txt and test2.txt. Compare your resulting preprocessed documents
    # with our results in preproc_test1.txt and preproc_test2.txt, and your TF-IDF results 
    # with our results in tfidf_test1.txt and tfidf_test2.txt.

# Finally, you can try your code on these files: covid_doc1.txt, and covid_doc2.txt, and covid_doc3.txt. 
    # Results for these are not provided, however the files are small enough that you can identify the words 
    # that make the cut and manually compute TF-IDF. 

# Note: When we test your submissionn, the input test file will be named tfidf_docs.txt, as stated 
    # at the start of Part 3. However, the file names contained in this file may be different than 
    # the samples given above (i.e. "doc1.txt", "doc2.txt", ..) so make sure that your code can read 
    # whatever file names appear in the tfidf_docs.txt file and work on them. 
    
main()