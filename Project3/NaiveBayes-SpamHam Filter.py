#William Fu
#Project 3: Spam/ham filter
#AI

import math

def main():
    print("Type in train file 1")
    train1 = input()
    print("Type in train file 2")
    train2 = input()
    print("Type in test file 1")
    test1 = input()
    print("Type in test file 2")
    test2 = input()       
    
    vocab, spam, ham, spam_ectr, ham_ectr, spam_wctr, ham_wctr = train(train1, train2)

    total, test_ectr = test(test1, test2, vocab, spam, ham, spam_ectr, ham_ectr)

    #print total correct out of total email
    print("Total: {0}/{1} emails classified correctly".format(total, test_ectr))

def train(train1, train2):
    vocab={}
    spam={}
    ham={}
    spam_emailctr = 0
    ham_emailctr = 0
    spam_wordctr = 0
    ham_wordctr = 0
    #run through both files and collect every word
    line = [line.lower().rstrip('\n').split(" ") for line in open(train1)]
    for l in line:
        for x in l:
            if "<" not in x and x != "":
                if x not in vocab:
                    vocab[x]=0
    line = [line.lower().rstrip('\n').split(" ") for line in open(train2)]
    for l in line:
        for x in l:
            if "<" not in x and x != "":
                if x not in vocab:
                    vocab[x]=0

    #copy the entire dictionary of train words to a spam and ham dict
    spam = vocab.copy()
    ham = vocab.copy()
    #for current email reading
    curr_email = {}
    line = [line.lower().rstrip('\n').split(" ") for line in open(train1)]
    for l in line:
        for x in l:
            #if at the end of the email indicated by </body> any word in the current email
            #is increased in the coresponding dict spam/ham
            if x == '</body>':
                for k in curr_email:
                    if k in spam:
                        temp = spam[k]
                        temp += 1
                        spam[k] = temp
                curr_email.clear()
                spam_emailctr += 1
            if "<" not in x and x != "":
                if x not in curr_email:
                    curr_email[x] = 1
                
    line = [line.lower().rstrip('\n').split(" ") for line in open(train2)]
    for l in line:
        for x in l:
            if x == '</body>':
                for k in curr_email:
                    if k in ham:
                        temp = ham[k]
                        temp += 1
                        ham[k] = temp
                curr_email.clear()
                ham_emailctr += 1
            if "<" not in x and x!= "":
                if x not in curr_email:
                    curr_email[x] = 1
                    
    #returns a whole bunch of hopefully usefull stats                    
    return vocab, spam, ham, spam_emailctr, ham_emailctr, spam_wordctr, ham_wordctr

def test(test1, test2, vocab, spam, ham, spam_ectr, ham_ectr):
    #priors are given to us - .6/.4 for small and
    #0.7866966480154788/0.21330335198452124 for the big files
    totalcorrect = 0
    priorSpam = 0
    priorHam = 0
    #set priors depending on files
    if (test1 == "test-spam-small.txt" or test1 == "test-ham.txt"):
        priorSpam = .6
        priorHam = .4
    else:
        priorSpam = .7866966480154788
        priorHam = .21330335198452124

    #testdict for current email again
    testdict = {}
    test_ectr = 1 #email ctr for file 1
    test2_ectr = 1 #email ctr for file 2

    #at end of email run the classifier
    line = [line.lower().rstrip('\n').split(" ") for line in open(test1)]
    if test1 == "test-spam.txt" or test1=="test-spam-small.txt":
        currtxt = "spam"
    else:
        currtxt = "ham"
    for l in line:
        for x in l:
            if x == '</body>':
                temp = sh(vocab, spam, ham, testdict, spam_ectr, ham_ectr, priorSpam, priorHam, currtxt, test_ectr)
                #keeps track of # correct
                totalcorrect = totalcorrect + temp
                testdict.clear()
                test_ectr += 1
            if "<" not in x and x != "":
                if x in vocab:
                    testdict[x] = 1
    print("{0} out of {1} classified correctly".format(totalcorrect, test_ectr-1))
    totalcorrect1 = totalcorrect

    test2_ectr = 1
    line = [line.lower().rstrip('\n').split(" ") for line in open(test2)]
    if test2 == "test-spam.txt" or test2=="test-spam-small.txt":
        currtxt = "spam"
    else:
        currtxt = "ham"
    for l in line:
        for x in l:
            if x== '</body>':
                temp = sh(vocab, spam, ham, testdict, spam_ectr, ham_ectr, priorSpam, priorHam, currtxt, test2_ectr)
                totalcorrect = totalcorrect + temp
                testdict.clear()
                test2_ectr += 1
            if "<" not in x and x != "":
                if x in vocab:
                    testdict[x] = 1
    print("{0} out of {1} classified correctly".format(totalcorrect - totalcorrect1, test2_ectr-1))
    test_ectr = test_ectr + test2_ectr
    test_ectr = test_ectr - 2

    return totalcorrect, test_ectr


def sh(vocab, spam, ham, testdict, spam_ectr, ham_ectr, priorSpam, priorHam, currtxt, test_ectr):
    #spam
    result = " "
    ctr = 0
    sumSpam = 0
    for x in spam:
        if (x in testdict):
            probSpam = math.log((spam[x]+1)/(spam_ectr+2))
            sumSpam = sumSpam + probSpam
        elif (x not in testdict):
            sumSpam = sumSpam + math.log(((spam_ectr - spam[x])+1)/(spam_ectr+2))
    endSpam = sumSpam + math.log(priorSpam)

    #ham
    sumHam = 0
    for x in ham:
        if (x in testdict):
            probHam = math.log((ham[x]+1)/(ham_ectr+2))
            sumHam = sumHam + probHam
        elif (x not in testdict):
            sumHam = sumHam + math.log(((ham_ectr - ham[x])+1)/(ham_ectr+2))
    endHam = sumHam + math.log(priorHam)

    #if classified as spam/ham and whether the classifier was right/wrong
    if endHam>endSpam:
        if currtxt == "ham":
            result = "right"
            ctr = 1
        else:
            result = "wrong"
        print("TEST {0} {1}/{2} features true {3:.3f} {4:.3f}".format(test_ectr, len(testdict), len(vocab), endSpam, endHam)," {0} {1}".format("ham", result))

    if endHam<endSpam:
        if currtxt == "spam":
            result = "right"
            ctr = 1
        else:
            result = "wrong"
        print("TEST {0} {1}/{2} features true {3:.3f} {4:.3f}".format(test_ectr, len(testdict), len(vocab), endSpam, endHam)," {0} {1}".format("spam", result))

    return ctr


main()

    
