# Information Retrieval HW4
### Mirko Mantovani, 10 November 2018

Homework 4 for the CS 582 Information Retrieval course at University of Illinois at Chicago

---
## Running the program
---
To run the program from terminal just use the command:
> python hw4.py ./stopwords.txt ./www/abstracts/ ./www/gold/

replacing the 3 arguments with the paths to your files to:

* Stop words
* Documents
* Gold standards

---
## Scripts
---
### hw4.py
The main program which controls the workflow of the scripts

### document.py

Document class which stores the word graph, tf-idf and page rank scores and ngrams

### graph.py

Graph class, an implementation of an undirected graph

### page_rank.py

Runs the page rank algorithm on a word graph

### preprocess.py

Contains custom tokenizer and functions to tokenize docs and golds

### statistics.py

Computes MRR and tf-idf

---
## Implementation choices
---

* Documents that do not have gold standards are not considered.
* Two words which are separated by a comma or a dot are not considered adjacent
* The tf-idf for ngrams are calculated by summing up the tf-idf scores of each single word belonging to the ngram


---
## Results
---
The obtained results are: 

MRR with page rank:

Using top-1 ngrams, MRR: 0.061654135338345864  
Using top-2 ngrams, MRR: 0.08984962406015037  
Using top-3 ngrams, MRR: 0.11040100250626562  
Using top-4 ngrams, MRR: 0.13088972431077694  
Using top-5 ngrams, MRR: 0.14728070175438573  
Using top-6 ngrams, MRR: 0.15680451127819517  
Using top-7 ngrams, MRR: 0.1634640171858212  
Using top-8 ngrams, MRR: 0.168821160042964  
Using top-9 ngrams, MRR: 0.1730818116720367  
Using top-10 ngrams, MRR: 0.17631489437880352  

MRR with tf-idf:

Using top-1 words, MRR using TF-IDF: 0.07819548872180451  
Using top-2 words, MRR using TF-IDF: 0.11842105263157894  
Using top-3 words, MRR using TF-IDF: 0.14448621553884727  
Using top-4 words, MRR using TF-IDF: 0.16647869674185486  
Using top-5 words, MRR using TF-IDF: 0.18016290726817044  
Using top-6 words, MRR using TF-IDF: 0.18868421052631562  
Using top-7 words, MRR using TF-IDF: 0.19502148227712104  
Using top-8 words, MRR using TF-IDF: 0.2015064446831361  
Using top-9 words, MRR using TF-IDF: 0.205349385368182  
Using top-10 words, MRR using TF-IDF: 0.20850728010502406