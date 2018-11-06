class BSTreeNode:
    #index is the index of the term in searchTerms
    def __init__(self, data, index):
        self.l_child = None
        self.r_child = None
        self.data = data
        self.index = index
        self.height = 0
    
    def insert(self, node):
        if self.data == node.data:
            self.index = node.index
        elif self.data < node.data:
            if self.r_child is None:
                self.r_child = node
            else:
                self.r_child.insert(node)
        else:
            if self.l_child is None:
                self.l_child = node
            else:
                self.l_child.insert(node)
                
    #returns index of data in document array if found
    #otherwise return -1
    def search(self, data):
        if self.data == data:
            return self.index
        if self.data > data:
            if self.l_child is not None:
                return self.l_child.search(data)
            else:
                return -1
        else:
            if self.r_child is not None:
                return self.r_child.search(data)
            else:
                return -1
    
class LinkedListNode:
    #data is the string
    #docArrIndex is the index of the string in the docArr
    #docIndex is the index of the string in the document
    def __init__(self, data, searchIndex, docArrIndex, docIndex):
        self.data = data
        self.dataLen = len(data)
        self.searchIndex = searchIndex
        self.docArrIndex = docArrIndex
        self.docIndex = docIndex
        self.next = None
        self.prev = None

        
#The shortest Substring has two conditions
#-all searchTerms are in the string
#-the count of the terms at each end is 1
#-shortest among the entire set of complete substrings
def answer(document, searchTerms):
    #parse the document
    docArr = document.split()
    docArrLen = len(docArr)
    docIter = 0
    
    #Array of searchTerms that contains their index in docArray
    searchLen = len(searchTerms)
    searchTermsCounter = [0] * searchLen
    numSearchTermsFound = 0
    
    if searchLen == 1:
        return searchTerms[0]
    
     #linked list of found searchTerms
    foundList = []
    currentBest = [0,0]
    currentBestLen = 0
    
    #I assume the searchTerms list is sorted so the best way to pick the root
    #is to choose the middle
    root = BSTreeNode(searchTerms[searchLen//2], searchLen//2)
    
    #Put the serach terms in BST for easier search O(d)
    for i in range(0, searchLen):
        root.insert(BSTreeNode(searchTerms[i], i))
        
    #find all search terms and store their indices O(d*log(s))
    #this makes it easier by having a list of only searchTerms in order
    #with indices 
    for i in range(0, docArrLen):
        #if word is in searchTerms
        #searchIndex is the index of the found word 
        #in the searchTerms array
        searchIndex = root.search(docArr[i])
        if searchIndex > -1:
            #save all indices in list
            foundList.append(LinkedListNode(docArr[i], searchIndex, i, docIter))
        docIter += len(docArr[i]) + 1
        
    #Iterators for finding the string
    head = 0
    tail = 0
    while numSearchTermsFound < searchLen:
        if searchTermsCounter[foundList[tail].searchIndex] == 0:
            numSearchTermsFound += 1
        searchTermsCounter[foundList[tail].searchIndex] += 1
        tail += 1
    #At this point, temp now holds a complete string
    #the end will always have a term counter of 1 
    #but the front may have a termCounter greater than 1.
    #So we shorten, by moving the front up.
    #Remember to keep track of term counts.
    #As the string shortens terms will be lost.
    while searchTermsCounter[foundList[head].searchIndex] > 1:
        searchTermsCounter[foundList[head].searchIndex] -= 1
        head += 1
        
    #At this point the head and tail point to the first best complete
    #string
    foundListLen = len(foundList)
    currentBest[0] = head
    currentBest[1] = tail - 1
    end =foundList[tail-1].docArrIndex
    front =foundList[head].docArrIndex
    currentBestLen = end - front
    #Look for another complete string
    #First, move the head forward once,
    #-this will remove one term with one count (update counters)
    #Then, move the tail until you find a replacement term
    #-this will provide a complete string
    #-but it can be shorter as the head term count can be greater than 1
    #Then, shorten by moving the head up until term count is 1
    #-this will give a complete short string
    #-compare this string to the current best, update if it is
    #Then, repeat
    while tail < foundListLen:
        searchTermsCounter[foundList[head].searchIndex] -= 1
        numSearchTermsFound -= 1
        head += 1
        
        while numSearchTermsFound < searchLen and tail < foundListLen:
            if searchTermsCounter[foundList[tail].searchIndex] == 0:
                numSearchTermsFound += 1
            searchTermsCounter[foundList[tail].searchIndex] += 1
            tail += 1
            
        while searchTermsCounter[foundList[head].searchIndex] > 1:
            searchTermsCounter[foundList[head].searchIndex] -= 1
            head += 1
            
        #Candidate short string found, compare with current best
        if currentBestLen > foundList[tail - 1].docArrIndex - foundList[head].docArrIndex:
            currentBest[0] = head
            currentBest[1] = tail - 1
            currentBestLen = foundList[tail - 1].docArrIndex - foundList[head].docArrIndex
    
    return document[foundList[currentBest[0]].docIndex : foundList[currentBest[1]].docIndex + foundList[currentBest[1]].dataLen]
