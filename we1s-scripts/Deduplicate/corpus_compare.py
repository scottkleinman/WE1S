#!/usr/bin/env python
"""
corpus_compare.py
v1.0 2015-10-10
v1.1 2015-11-11 argument parsing
v1.2 2015-11-15 parsing defaults and bug fixes
v1.3 2016-07-19 refactor, lint
v1.3 2016-07-20 refactor

jeremydouglass@english.ucsb.edu

1.  Take a list of file paths containing .txt files (may be in subdirectories).
2.  All .txt files are described within the set using tf-idf
      (term frequency--inverse document frequency)
3.  The set of files are self-compared
4.  Files with any similarity pair above threshhold are noted
      (along with top matching file) in csv outputfile
"""

## IMPORT

## Python 2-3 compatible code
from __future__ import print_function

## argument parsing
import argparse
from argparse import RawDescriptionHelpFormatter
## time the script
from datetime import datetime
# from timeit import default_timer as timer ## http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
## file handling, matching, writing
import os
# import errno
import fnmatch
import csv
## working with lists and indexes
# import itertools
import operator
# from operator import itemgetter
## comparing files and strings
import difflib
import filecmp
## comparing document sets
from sklearn.feature_extraction.text import TfidfVectorizer
## working with matrices / arrays
import numpy as np

## INFO

__author__ = "Jeremy Douglass"
__copyright__ = "copyright 2016, The WE1S Project"
__license__ = "GPL"
__version__ = "1.4"
__email__ = "jeremydouglass@english.ucsb.edu"

## FUNCTIONS

def fp_lister(fpath, fnpattern):
    """
    Take a directory and pattern, return a list of file paths.
    """
    return [os.path.join(dirpath, f)
            for dirpath, _dirnames, files in os.walk(fpath)
            for f in fnmatch.filter(files, fnpattern)]

def fn_to_str(fname, linebreaks=0, whitespace=0):
    """
    Take file name, return text contents as string (sans line breaks).
    """
    with open(fname, "r") as fhandle:
        if linebreaks == 0 and whitespace == 0:
            contents = " ".join(fhandle.read().split())   ## remove linebreaks and reduce whitespace
        elif linebreaks == 0:
            contents = fhandle.read().replace('\n', ' ')  ## remove linebreaks only
        elif whitespace == 0:
            contents = fhandle.read().translate(None, ' \n\t\r')
        else:
            contents = fhandle.read()
    fhandle.close()
    return contents

def str_diff_inspect(str1, str2, verbose=0):
    """
    Sequence match ratio score and summary for two strings.
    NOTE: This can be **really** slow.
    """
    seqcomp = difflib.SequenceMatcher(lambda x: x == " ", str1, str2)  ## run on partial files (e.g. [0:512]) for increased speed
    seqdiffstring = ''
    codes = 0
    for tag, istart, istop, jstart, jstop in seqcomp.get_opcodes():
        istop = min(istop, istart+20)
        jstop = min(jstop, jstart+20)
        if tag == 'replace':
            seqdiffstring += (str1[istart:istop] + '>' + str2[jstart:jstop] + ' || ')
            codes += 1
        elif tag == 'insert':
            seqdiffstring += ('+' + str2[jstart:jstop] + ' || ')
            codes += 1
        elif tag == 'delete':
            seqdiffstring += ('-' + str1[istart:istop] + ' || ')
            codes += 1
        if codes > 10:
            break

    if verbose == 1:
        print('  file1:    ', '{0}'.format(str1[0:50]+' ... '+str1[-50:]))
        print('  file2:    ', '{0}'.format(str2[0:50]+' ... '+str2[-50:]))
        print('  seqdiff:  ', '{0}'.format(seqdiffstring))

    return seqdiffstring

def s_seq_similarity(str1, str2, verbose=0):
    """
    Sequence match ratio score and summary string for two files.
    NOTE: This is **really** slow for paragraph text -- much better for line splits
    """
    str1 = str1.split()  ## difflib struggles with paragraphs -- works better on lines
    str2 = str2.split()
    seqcomp = difflib.SequenceMatcher(lambda x: x == " ", str1, str2)  ## run on partial files for greatly increased speed e.g. str1[0:512], str2[0:512] -- this will impact ratio for boilerplate-heavy openings.
    seqratio = round(seqcomp.quick_ratio(), 2)  ## .quick_ratio() and .real_quick_ratio() are **much** faster than .ratio(), but unusably imprecise on paragraph text, e.g. 0.08 ratio = 0.98 quick_ratio similarity. Much better with line splits.
    if verbose == 1:
        print('  seqratio: ', '{0}'.format(seqratio))
    return seqratio

def f_jaccard_similarity(str1, str2, verbose=0):
    """
    Jaccard similarity score for two files.

    NOTE: in the future, could try to speed up an implementation
    -  http://www.nltk.org/_modules/nltk/metrics/distance.html
    ... or could compute in direct relation to the tf-idf matrix, rather than as pairs.
    -  http://stackoverflow.com/questions/32805916/compute-jaccard-distances-on-sparse-matrix
    """
    set1 = set(str1.split())
    set2 = set(str2.split())
    similarity = float(len(set1.intersection(set2))*1.0/len(set1.union(set2))) # similarity [0,1], 1 = exact replica.
    similarity = round(similarity, 2)
    if verbose == 1:
        print('jaccard: '.rjust(12), '{0}'.format(similarity))
    return similarity

def f_file_equality(fname1, fname2, verbose=0):
    """
    Equality of two files with filecmp / md5 (True/False).

    http://stackoverflow.com/questions/4283639/check-files-for-equality
    """
    equality = filecmp.cmp(fname1, fname2)
    if verbose == 1:
        print('  equality: ', '{0}'.format(equality))
    return equality

def make_corpus(fname_list):
    """
    Take a list of file names, return a generator of file content strings which will load on-demand.

    Memory-efficient generator to yield file contents on-demand rather than loading them all at once.
    http://stackoverflow.com/questions/16453855/tfidfvectorizer-for-corpus-that-cannot-fit-in-memory
    """
    for fname in fname_list:
        yield fn_to_str(fname)

def f_tfidf_compare(corpus, verbose=1):
    """
    Take a generator of file contents, return a 2D array of tf-idf file comparisons [0-1] (one per file pair):

    1. take a generator of file contents
    2. generate a self-comparison matrix of tf-idf vectors
    3. convert to an array and filter to upper-triangle only (one comparison per file pair)
    4. return array
    """

    if verbose == 1:
        print('  Computing TF/IDF pairs...')
        start_time = datetime.now().replace(microsecond=0)

    tfv = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01, stop_words='english')
    tfidf_matrix = tfv.fit_transform(corpus)
    pairwise_similarity_matrix = tfidf_matrix * tfidf_matrix.T

    ## Zero out everything except upper triangle (also zeros out identity diagonal)
    ## NOTE: np.triu takes an array, so this changes the matrix to an array
    pairwise_similarity_upperarray = np.triu(pairwise_similarity_matrix.toarray(), 1) #pylint: disable=maybe-no-member

    if verbose == 1:
        print('  ...elapsed time: {}'.format(datetime.now().replace(microsecond=0) - start_time.replace(microsecond=0)))

    return pairwise_similarity_upperarray

def f_sample_string(fstr, scount=2, swidth=20, verbose=0):
    """
    Return a concatonated series of n samples from a long string.
    """
    result = []
    if verbose == 1:
        print('len: {}  scount*swidth: {}  scount:  {}  swidth: {}'.format(str(len(fstr)), str(scount*swidth), str(scount), str(swidth)))
    if scount*swidth > len(fstr): ## If sample size is greater than whole (or even almost), just return whole string. NOTE: consider adding the amount taken up by separators -- e.g. why omit 15 chars and print 15 chars of separators when you could print the original?
        return str
    else:  ## Concatonate a series of string samples (scount) of the same width (swidth) -- calculate the spacing
        step = (len(fstr)-(swidth))/float(scount-1)  ## Space samples such that the first is 0-aligned and the last (>1) is always end-aligned. Step is a float to avoid accumulating offset errors
        for i in np.arange(0, len(fstr), step): ## range over floats
            if verbose == 1:
                print(i, i+swidth, step)
            result += [fstr[int(np.ceil(i)):int((np.ceil(i))+swidth)]]  ## round up i to next character. e.g. for 3, 20, len(fstr)=100, loop produces a string of samples ~fstr[0:20]+'[...]'+fstr[40:60]+'[...]'+fstr[80:100]
        return '[...]'.join(result)

def f_all_compare_writer(args, myfilelist, resultwriter):
    """
    1. Computes TF/IDF on file list
    2. measures similarity for each top file pair
    3. writes all results to resultwriter (open csv file).
    """
    count_hits = 0
    resultrow_list = []
    tfidf_pairs = f_tfidf_compare(make_corpus(myfilelist))

    for idx, row in enumerate(tfidf_pairs):  ## For each file row (one row of matrix per file)
        maxindex, maxvalue = max(enumerate(row), key=operator.itemgetter(1))  ## Get the top match (for each array row, return column index and value of max cell)
        if maxvalue > args.threshold:  ## Print only high-value matches -- many are low or 0, and 100,000^2 is a huge result set. Calculate additional comparisons only on high-tf-idf matches.
            resultrow_list = []
            count_hits += 1
            ## file contents
            str1 = fn_to_str(myfilelist[idx])
            str2 = fn_to_str(myfilelist[maxindex])

            resultrow_list += [f_file_equality(myfilelist[idx], myfilelist[maxindex], 0)]  ## File equality is fast (True/False), and can sometimes provide additional confirmation in order to speed inspection, but will fail to detect nigh-identical contents.
            resultrow_list += [round(maxvalue, 2)] ## tfidf
            resultrow_list += [s_seq_similarity(str1, str2, 0)]    ## Sequence is very slow, and works much better with texts split by line breaks than on paragraphs
            resultrow_list += [f_jaccard_similarity(str1, str2, 0)]  ## Jaccard is slow to compute and sensitive; it can helpfully disagree tf-idf on false-positives but misses too much on its own.
            resultrow_list += [myfilelist[idx]]
            resultrow_list += [myfilelist[maxindex]]
            resultrow_list += [f_sample_string(str1, 2, 20)]
            resultrow_list += [f_sample_string(str2, 2, 20)]

            resultwriter.writerow(resultrow_list)
            # resultwriter.writerow([fe_score, round(maxvalue, 2), ss_score, js_score, myfilelist[idx], myfilelist[maxindex], sample1, sample2])

    print('  {} {} file matched pairs ( TF/IDF > {} )\n'.format(str(count_hits), args.filepattern, str(args.threshold)))
    return count_hits

## MAIN CODE

def main(args):
    """ Main. """
    ## TIMING

    print('\n###  corpus_compare.py  ###')
    start_time = datetime.now().replace(microsecond=0)
    print(start_time)

    ## ARGS

    print('  from:     {}\n  check:    {}\n  thresh:   {}\n  results:  {}\n  copy:     {}\n'.format(args.inputpaths, args.filepattern, args.threshold, args.outputfile, args.copydir))

    csvfile = open(args.outputfile, 'w') ## a/ab = add to existing csv, w/wb = write (clobber) new csv -- https://docs.python.org/2.7/library/csv.html -- both py2 and py3 compat: http://stackoverflow.com/questions/34283178/typeerror-a-bytes-like-object-is-required-not-str-in-python-and-csv
    resultwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    resultwriter.writerow(['identical', 'tf-idf', 'sequence', 'jaccard', 'file1', 'file2', 'str1', 'str2', datetime.now()])

    count_total_hits = 0

    myfilelist = []
    if args.mergepaths == 1:  ## combine all filenames, run once
        for path in args.inputpaths:
            myfilelist = myfilelist + fp_lister(path, args.filepattern)  ## combine lists
        print('In merged paths: {}'.format(args.inputpaths))
        print('  {} {} files found'.format(str(len(myfilelist)), args.filepattern))
        count_total_hits = f_all_compare_writer(args, myfilelist, resultwriter)  ## all comparisons
    else:  ## run in per-path batches of filenames
        for path in args.inputpaths:
            myfilelist = fp_lister(path, args.filepattern)
            print('In path: {}'.format(path))
            print('  {} {} files found'.format(str(len(myfilelist)), args.filepattern))
            count_total_hits += f_all_compare_writer(args, myfilelist, resultwriter)    ## all comparisons

    csvfile.close()

    print('\n' + 'Done.')
    print('Total: ' + str(count_total_hits) + ' matching ' + args.filepattern + ' file pairs (tf-idf > ' + str(args.threshold) + ')')
    print('Elapsed time: ', datetime.now().replace(microsecond=0) - start_time)
    print('Result output in: ' +  args.outputfile + '\n')


## ENTRY POINT

if __name__ == '__main__':

    ## COMMAND LINE ARGUMENT PARSING
    PARSER = argparse.ArgumentParser(description='Duplicate file scanner. Generates an outputfile of comparisons; optionally copies unique files to a new directory. Developed for near-match newspaper articles, for the WE1S project.\nNOTE: file comparison is pairwise (quadratic), so --mergepaths may produce large arrays and long run times.', epilog='EXAMPLE:\n  corpus_compare.py -i ./data/ -f "*.txt" -t 0.90 -o ./corpus_compare-args.csv\n \n', formatter_class=RawDescriptionHelpFormatter)
    PARSER.add_argument('-i', '--inputpaths', nargs='*', default=['./'], help='input source paths for files to compare, default is current directory')   ## e.g.  ['./'] ... or ['./data1/', './data2/']
    PARSER.add_argument('-m', '--mergepaths', default=0, help='compare all files in all paths')
    PARSER.add_argument('-f', '--filepattern', default="*.txt", help='input source path for files to compare')
    PARSER.add_argument('-o', '--outputfile', default='./corpus_compare.csv', help='results output file')
    PARSER.add_argument('-t', '--threshold', type=float, default=0.90, help='threshold for matching')
    PARSER.add_argument('-c', '--copydir', help='copy unique results to directory')
    CL_ARGS = PARSER.parse_args()

    main(CL_ARGS)
