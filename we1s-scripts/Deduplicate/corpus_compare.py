#!/usr/bin/env python
"""
corpus_compare.py
Generate a document similarity report.

1.  Accepts a list of one or more file paths. Within those paths (recursive):
2.  All text files matching pattern (*.txt by default) are described within the set using tf-idf
      (term frequency--inverse document frequency)
3.  The set of files are self-compared
4.  Files with any similarity pair above threshhold are noted
      (along with top matching file) in csv outputfile

jeremydouglass@english.ucsb.edu

v1.0 2015-10-10
v1.1 2015-11-11 argument parsing
v1.2 2015-11-15 parsing defaults and bug fixes
v1.3 2016-07-20 rework sequence similarity, refactor
v1.4 2016-07-21 generator without passing resultwriter, renaming
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
__email__ = "jeremydouglass@gmail.com"

## FUNCTIONS

def comp_fnames_file_equality(fname1, fname2):
    """
    Compare filenames: file equality.
    Check if contents of files are identical.

    Equality = True/False.
    Uses filecmp md5 hash.

    NOTES:
    http://stackoverflow.com/questions/4283639/check-files-for-equality
    """
    equality = filecmp.cmp(fname1, fname2)
    return equality

def strs_diff_summary(str1, str2, diffitems=5, itemlength=10, joinstr='  '):
    """
    Strings diff summary.
    Summarizes 'replace' 'insert' and 'delete' differences in a compact single-string format.

    By default, limits string to 5 items 10 chars long.
    Uses difflib.SequenceMatcher.get_opcodes.

    NOTES:
    -  Extremely slow for long line lengths / no linebreaks.
    -  Default return = 63 chars: 5 items * (1 marker + 10 chars) + (4 separaters * 2 chars)
    """
    seqcomp = difflib.SequenceMatcher(lambda x: x == " ", str1, str2)  ## run on partial files (e.g. [0:512]) for increased speed
    seqdiff = []
    # seqlen = diffitems*(1+itemlength) + (diffitems-1)*len(joinstr)
    codes = 0
    for tag, istart, istop, jstart, jstop in seqcomp.get_opcodes():
        if itemlength > 0: ## crop overlong items
            istop = min(istop, istart+itemlength)
            jstop = min(jstop, jstart+itemlength)
        if tag == 'replace':
            seqdiff += ['>' + str2[jstart:jstop]]
            codes += 1
        elif tag == 'insert':
            seqdiff += ['+' + str2[jstart:jstop]]
            codes += 1
        elif tag == 'delete':
            seqdiff += ['-' + str1[istart:istop]]
            codes += 1
        if codes > diffitems:
            break
    return joinstr.join(seqdiff)

def comp_strs_jaccard_similarity(str1, str2):
    """
    Compare strings: Jaccard similarity.
    Return set similarity metric [0-1] for two sets of unique terms.

    Similarity = shared terms / all terms.

    NOTES:
    -  Could speed up an implementation? http://www.nltk.org/_modules/nltk/metrics/distance.html
    -  Could compute on tf-idf matrix, rather than as pairs? http://stackoverflow.com/questions/32805916/compute-jaccard-distances-on-sparse-matrix
    """
    set1 = set(str1.split())
    set2 = set(str2.split())
    similarity = float(len(set1.intersection(set2))*1.0/len(set1.union(set2))) # similarity [0,1], 1 = exact replica.
    similarity = round(similarity, 2)
    return similarity

def comp_strs_diff_similarity(str1, str2):
    """
    Compare strings: Diff similarity.
    Return a diff sequence similarity metric [0-1] for two strings.

    Similarity = 2 * matches / total elements.
    Uses difflib.SequenceMatcher.ratio.

    NOTES:
    -  The ratio calculation is influenced by difflib's junk and autojunk settings, which by default filters whitespace and supresses excessive duplicates.
    -  Calculating ratios is very slow for unsplit paragraph text. It performs much better for line splits or word splits.
    """
    str1 = str1.split()  ## difflib struggles with paragraphs -- works better on lines
    str2 = str2.split()
    seqcomp = difflib.SequenceMatcher(lambda x: x == " ", str1, str2)  ## run on partial files for greatly increased speed e.g. str1[0:512], str2[0:512] -- this will impact ratio for boilerplate-heavy openings.
    seqratio = round(seqcomp.quick_ratio(), 2)  ## .quick_ratio() and .real_quick_ratio() are **much** faster than .ratio(), but unusably imprecise on paragraph text, e.g. 0.08 ratio = 0.98 quick_ratio similarity. Much better with line splits.
    return seqratio

def fname_to_fstr(fname, linebreaks=0, whitespace=0):
    """
    Filename to filestring:
    Take file name, return text contents as string.

    By default filters linebreaks and whitespace.
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

def fnamelist_to_strgen(fname_list):
    """
    Filename list to string generator:
    Take a list of file names, return a generator of file content strings which will load on-demand.

    NOTES:
    For processing large document collections with the tfidfvectorizer,
    a memory-efficient generator is necessary to yield file contents on-demand rather than loading them all at once.
    http://stackoverflow.com/questions/16453855/tfidfvectorizer-for-corpus-that-cannot-fit-in-memory
    """
    for fname in fname_list:
        yield fname_to_fstr(fname)

def fpath_to_fnamelist(fpath, fnpattern):
    """
    Filepath to filename list.
    Take a directory and pattern, return a list of file paths.

    fnpattern filters results use Unix shell-style wildcards: (*, ?, [abc], [!abc])
    Uses fnmatch.filter.
    """
    return [os.path.join(dirpath, f)
            for dirpath, _dirnames, files in os.walk(fpath)
            for f in fnmatch.filter(files, fnpattern)]

def str_sampler(longstr, scount=2, swidth=20, join=1, joinstr='[...]', return_shortest=1):  #pylint: disable=too-many-arguments
    """
    String sampler.
    From a string, return a series of equadistant spaced samples (scount) of the same width (swidth).

    Sampling has the following properties:

    1. Samples are all the same size (swidth).
    2. First sample is always taken from the string head
    3. Multiple samples (scount > 1) always include the both string head & tail.
    4. Samples are equidistantly spaced.
    5. Samples do not overlap, and the sampler is never longer than the original (by default).
       The original string is returned unchanged if a sampler would result in a longer string.

    NOTES:
    Spaces samples such that the first is 0-aligned and the last (>1) is always end-aligned.
    Step is a float to avoid accumulating offset errors.
    Whether a sampler would be overlong is calculated based on the total *including* join strings.
    To enable overlapping / overlong samplers, set return_shortest=0.
s    """
    result = []
    if return_shortest == 1:
        if join == 0:  ## calculate shortest correctly if not joining strings
            joinstr = ''
        if len(longstr) < (scount + len(joinstr))*swidth:  ## return original string if the sampler will be longer
            return [longstr]

    step = (len(longstr)-(swidth))/float(scount-1)  ## calculate spacing
    for i in np.arange(0, len(longstr), step):  ## range over floats to avoid a creeping offset error
        result += [longstr[int(np.ceil(i)):int((np.ceil(i))+swidth)]]  ## round up i to next character
    if join == 1:
        return [joinstr.join(result)]
    else:
        return result

def strlist_to_tfidf_pairarray(corpus, verbose=0):
    """
    Take a corpus of file contents; return an array of pairwise file comparisons based on tf-idf similarity [0-1].

    1. Take a corpus of file contents (string list or string generator).
    2. Generate a self-comparison matrix of tf-idf vectors.
    3. Convert to matrix to 2D array and filter to upper-triangle only (one comparison per file pair).
    4. Return array.
    """

    if verbose == 1:
        print('  Computing TF/IDF pairs...')
        start_time = datetime.now().replace(microsecond=0)

    tfv = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01, stop_words='english', decode_error='replace')
    tfidf_matrix = tfv.fit_transform(corpus)
    pairwise_similarity_matrix = tfidf_matrix * tfidf_matrix.T

    ## Zero out everything except upper triangle (also zeros out identity diagonal)
    ## NOTE: np.triu takes an array, so this changes the matrix to an array
    pairwise_similarity_upperarray = np.triu(pairwise_similarity_matrix.toarray(), 1) #pylint: disable=maybe-no-member

    if verbose == 1:
        print('  ...elapsed time: {}'.format(datetime.now().replace(microsecond=0) - start_time.replace(microsecond=0)))

    return pairwise_similarity_upperarray

## MAIN CODE

def main_fnamelist_comparer(filelist, threshold):
    """
    1. Computes TF/IDF on file list
    2. Measures similarity for each top file pair
    3. Returns all results as a row list (e.g. for csv.writer)
    """
    # count_hits = 0
    resultrow_list = []
    tfidf_pairs = strlist_to_tfidf_pairarray(fnamelist_to_strgen(filelist), 1)

    for idx, row in enumerate(tfidf_pairs):  ## For each file row (one row of matrix per file)
        maxindex, maxvalue = max(enumerate(row), key=operator.itemgetter(1))  ## Get the top match (for each array row, return column index and value of max cell)
        if maxvalue > threshold:  ## Print only high-value matches -- many are low or 0, and 100,000^2 is a huge result set. Calculate additional comparisons only on high-tf-idf matches.
            resultrow_list = []
            # count_hits += 1
            ## file contents
            str1 = fname_to_fstr(filelist[idx])
            str2 = fname_to_fstr(filelist[maxindex])

            resultrow_list += [comp_fnames_file_equality(filelist[idx], filelist[maxindex])]  ## File equality is fast (True/False), and can sometimes provide additional confirmation in order to speed inspection, but will fail to detect nigh-identical contents.
            resultrow_list += [round(maxvalue, 2)] ## tfidf
            resultrow_list += [comp_strs_diff_similarity(str1, str2)]    ## Sequence is very slow, and works much better with texts split by line breaks than on paragraphs
            resultrow_list += [comp_strs_jaccard_similarity(str1, str2)]  ## Jaccard is slow to compute and sensitive; it can helpfully disagree tf-idf on false-positives but misses too much on its own.
            resultrow_list += [filelist[idx]]
            resultrow_list += [filelist[maxindex]]
            resultrow_list += [str_sampler(str1)[0]] # [str_sampler(str1, 2, 20)[0]]
            resultrow_list += [str_sampler(str2)[0]] # [str_sampler(str2, 2, 20)[0]]
            yield resultrow_list

def main(args):
    """
    Main loop through comparison filesets -- either per-path or in one merged batch.
    Manages csv file writing and timing.
    """
    print('\n###  corpus_compare.py  ###')

    ## TIMING
    start_time = datetime.now().replace(microsecond=0)
    print('Start time: {}'.format(start_time))

    ## ARGS
    if args.verbose == 1:
        print('args: {}'.format(args))
        # print('  from:     {}\n  check:    {}\n  thresh:   {}\n  results:  {}\n  copy:     {}\n'.format(args.inputpaths, args.filepattern, args.threshold, args.outputfile, args.copydir))

    csvfile = open(args.outputfile, 'w') ## a/ab = add to existing csv, w/wb = write (clobber) new csv -- https://docs.python.org/2.7/library/csv.html -- both py2 and py3 compat: http://stackoverflow.com/questions/34283178/typeerror-a-bytes-like-object-is-required-not-str-in-python-and-csv
    resultwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    resultwriter.writerow(['identical', 'tf-idf', 'sequence', 'jaccard', 'file1', 'file2', 'str1', 'str2', datetime.now()])

    count_total_hits = 0
    filelist = []
    if args.mergepaths == 1:  ## combine all filenames, run once
        for path in args.inputpaths:
            filelist = filelist + fpath_to_fnamelist(path, args.filepattern)  ## combine lists
        print('In merged paths: {}'.format(args.inputpaths))
        print('  {} {} files found'.format(str(len(filelist)), args.filepattern))
        print('  Est. batch time -- total: {} comparisons in {} minutes'.format(str(len(filelist)^2), str(round((len(filelist)**2)/float(5250000), 1))))
        for row in main_fnamelist_comparer(filelist, args.threshold):
            count_total_hits += 1
            resultwriter.writerow(row)

    else:  ## run in per-path batches of filenames
        for path in args.inputpaths:
            filelist = fpath_to_fnamelist(path, args.filepattern)
            print('In path: {}'.format(path))
            print('  {} {} files found'.format(str(len(filelist)), args.filepattern))
            print('  Est. batch time -- this path: {} comparisons in {} minutes'.format(str(len(filelist)^2), str(round((len(filelist)**2)/float(5250000), 1))))
            count_hits = 0
            for row in main_fnamelist_comparer(filelist, args.threshold):
                count_hits += 1
                resultwriter.writerow(row)
            print('  {} {} file matched pairs ( TF/IDF > {} )\n'.format(str(count_hits), args.filepattern, str(args.threshold)))
            count_total_hits += count_hits

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
    PARSER.add_argument('-v', '--verbose', help='verbose mode')
    CL_ARGS = PARSER.parse_args()

    main(CL_ARGS)
