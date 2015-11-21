#!/usr/bin/env python
"""
corpus_compare.py
v1.0 2015-10-10
v1.1 2015-11-11 argument parsing
v1.2 2015-11-15 parsing defaults and bug fixes
jeremydouglass@english.ucsb.edu

1.  Takes a list of file paths containing .txt files (may be in subdirectories).
2.  All .txt files are described within the set using tf-idf (term frequency--inverse document frequency)
3.  The set of files are self-compared
"""

__author__ = "Jeremy Douglass"
__copyright__ = "copyright 2015, The WE1S Project"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "jeremydouglass@english.ucsb.edu"

## IMPORT

## file handling, matching, writing
import os
import fnmatch
import csv
## working with lists and indexes
import itertools
import operator
from operator import itemgetter
## comparing files and strings
import difflib
import filecmp
## nltk tools
from sklearn.feature_extraction.text import TfidfVectorizer
## working with matrices / arrays
import numpy as np
## time the script
from datetime import datetime

## argument parsing
import argparse

parser = argparse.ArgumentParser(description='Duplicate file scanner and report generator.')
parser.add_argument('-i', '--inputpaths', nargs='*', default=['./'], help='input source paths for files to compare, default is current directory')
parser.add_argument('-f', '--filepattern', default="*.txt", help='input source path for files to compare')
parser.add_argument('-o', '--outputfile', default='./corpus_compare.csv', help='results output file')
parser.add_argument('-t', '--threshold', type=float, default=0.85, help='threshold for matching')
args = parser.parse_args()

# parser.parse_args('--inputpaths'.split())
# parser.parse_args('--filepattern'.split())
# parser.parse_args('--outputfile'.split())
# parser.parse_args('--threshold'.split())


## VARIABLES

# corpus_compare.py -i /mytemp/doc-compare-test/2015-11-16-workshop/data/ -f "*.txt" -t 0.85 -o /mytemp/doc-compare-test/2015-11-16-workshop/corpus_compare-args.csv

# myfilepattern = '*.txt'
myfilepattern = args.filepattern
print myfilepattern
# mythreshold = 0.85
mythreshold = args.threshold
print mythreshold
## mypaths = ['/mytemp/doc-compare-test/']
# mypaths = [
#   '/mytemp/doc-compare-test/2015-11-16-workshop/data/'
#   ]	
mypaths = args.inputpaths
print mypaths
# myresultsfile = '/mytemp/doc-compare-test/2015-11-16-workshop/corpus_compare.csv'
# myresultsfile_unique = '/mytemp/doc-compare-test/2015-11-16-workshop/corpus_unique.csv'
myresultsfile = args.outputfile
print myresultsfile

## FUNCTIONS

def f_lister(fpath, fnpattern):
  """
  Take a directory and pattern, return a list of file paths.
  """
  return [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(fpath)
    for f in fnmatch.filter(files, fnpattern)]

def f_str(fname):
  """
  Take file name, return text contents as string (sans line breaks).
  """
  with open(fname, "r") as fhandle:
    contents=fhandle.read().replace('\n', ' ')
  fhandle.close()
  return contents

def f_seq_compare(fname1,fname2):
  """
  DEPRECATED
  Sequence match ratio score for two files 
  ...this is *really* slow.
  """
  seqcomp = difflib.SequenceMatcher(lambda x: x==" ", f_str(fname1), f_str(fname2))
  seqcomp = round(seqcomp.ratio(), 2)
  ## print '    seqcomp:', seqcomp
  return seqcomp

def f_jaccard_compare(file1, file2):
  """
  Jaccard similarity score for two files.

  NOTE: in the future, could try to speed up an implementation
  -  http://www.nltk.org/_modules/nltk/metrics/distance.html
  ... or could compute in direct relation to the tf-idf matrix, rather than as pairs.  
  -  http://stackoverflow.com/questions/32805916/compute-jaccard-distances-on-sparse-matrix
  """
  a = set(f_str(file1).split())
  b = set(f_str(file2).split())
  similarity = float(len(a.intersection(b))*1.0/len(a.union(b))) # similarity [0,1], 1 = exact replica.
  similarity = round(similarity, 2)
  ## print '    jaccard:', similarity
  return similarity

def f_file_compare(file1, file2):
  """
  check equality with filecmp / md5
  http://stackoverflow.com/questions/4283639/check-files-for-equality
  """
  return filecmp.cmp(file1, file2)

def make_corpus(doc_files):
  """
  Take a list of file names, return a generator of file content strings which will load on-demand.

  Memory-efficient generator to yield file contents on-demand rather than loading them all at once.
  http://stackoverflow.com/questions/16453855/tfidfvectorizer-for-corpus-that-cannot-fit-in-memory
  """
  for doc in doc_files:
    yield f_str(doc)


def f_tfidf_compare(corpus):
  """
  Take a generator of file contents, return a 2D array of tf-idf file comparisons [0-1] (one per file pair)

  1. take a generator of file contents
  2. generate a self-comparison matrix of tf-idf vectors
  3. convert to an array and filter to upper-triangle only (one comparison per file pair)
  4. return array
  """

  tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0.01, stop_words = 'english')
  tfidf_matrix =  tf.fit_transform(corpus)
  pairwise_similarity_matrix = tfidf_matrix * tfidf_matrix.T

  ## Zero out everything except upper triangle (also zeros out identity diagonal)
  ## NOTE: np.triu takes an array, so this changes the matrix to an array    
  pairwise_similarity_upperarray = np.triu(pairwise_similarity_matrix.toarray(), 1)
  return pairwise_similarity_upperarray


## MAIN CODE

startTime = datetime.now()
print startTime
print '\n## corpus_compare.py ##\n'

csvfile = open(myresultsfile, 'ab') ## add to existing csv
# csvfile = open(myresultsfile, 'wb') # write (clobber) new csv
## https://docs.python.org/2.7/library/csv.html
resultwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
headings = ['identical', 'tf-idf', 'jaccard', 'file1', 'file2', datetime.now()]
# print headings
resultwriter.writerow(headings)


# myresultsfile_unique
# csvfile_unique = open(myresultsfile, 'ab') ## add to existing csv



count_total_hits = 0

for path in mypaths:
  print 'Finding ' + myfilepattern + ' in ' + path
  myfilelist = f_lister(path, myfilepattern)
  print '  ' + str(len(myfilelist)) + ' ' + myfilepattern + ' files found'
  
  mycorpus = make_corpus(myfilelist)
  tfidf_pairs = f_tfidf_compare(mycorpus)

  count_path_hits = 0
  
  ## for each file row (one row of matrix per file)
  for idx, row in enumerate(tfidf_pairs):
    ## get the top match (for each array row, return column index and value of max cell)
    maxindex, maxvalue = max(enumerate(row), key=operator.itemgetter(1))
    ## print only high-value matches -- many are low or 0, and 100,000^2 is a huge result set.
    if (maxvalue > mythreshold): 
      count_path_hits += 1
      ## calculate additional comparisons only on high-tf-idf matches;
      ## these include a straight file compare (True/False) and Jaccard.
      ## Why are these additional steps instead of first-pass?
      ## File compare (fc) is fast, and can sometimes provide additional confirmation
      ## in order to speed inspection, but round-robin of 100,000 files would take
      ## a long time and not catch much -- it can fail on nigh-identical contents.
      ## Jaccard (jc) is slow to compute and sensitive; it can helpfully disagree tf-idf
      ## on false-positives but misses too much on its own.
      ## Sequence compare (sc) just isn't worth much; this isn't source code.
      fc = f_file_compare(myfilelist[idx], myfilelist[maxindex])
      jc = f_jaccard_compare(myfilelist[idx], myfilelist[maxindex])
      # sc = f_seq_compare(myfilelist[idx], myfilelist[index])
      # print idx, index, fc, jc, round(value, 2), myfilelist[idx], myfilelist[index]
      resultwriter.writerow([fc, round(maxvalue, 2), jc, myfilelist[idx], myfilelist[maxindex]]) 
    ## note unusual files separately
    # if (maxvalue < 0.06):  
    #  print '  unusual: ', myfilelist[idx], round(maxvalue, 4)

  print '  ' + str(count_path_hits) + ' matching ' + myfilepattern + ' file pairs (tf-idf > ' + str(mythreshold) + ')'
  count_total_hits = count_total_hits + count_path_hits

csvfile.close()

print '\n' + 'Done.'
print str(count_total_hits) + ' matching ' + myfilepattern + ' file pairs (tf-idf > ' + str(mythreshold) + ')'
print 'Elapsed time: ', datetime.now() - startTime
print 'Results in: ' +  myresultsfile + '\n'

