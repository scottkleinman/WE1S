#Guidelines for Using Networked Corpus
The instructions below assume you are working on a Windows machine. Guidelines for the Mac will be added soon.

##Preparing to Use Networked Corpus
The GitHub repo of [Networked Corpus](https://github.com/jeffbinder/networkedcorpus) appears to make assumptions about your environment and file locations that make it difficult to run out of the box. As a result, a zipped version is provided here with some modifications to make it easier to run. [Download](https://raw.githubusercontent.com/scottkleinman/WE1S/master/networkedcorpus/networkedcorpus.zip) and extract the zipped version. Then do the following:

Open `gen-networked-corpus.py` in a text editor and scroll to line 303. Change `datadir = "/path/to/data-folder"` as appropriate to provide the location of your data.

##Using Networked Corpus

Using Networked Corpus involves two steps:

1. Run Mallet
2. Run Networked Corpus

###Step 1
Networked Corpus requires that data be imported into Mallet with the `--token-regex` flag. Assuming that you are running Mallet on a Windows machine, and that your data is in a folder called `data-folder`, that your Mallet output is stored in a folder called `output-folder`, and that both are inside your `mallet` path, the Mallet import command would look like this:

```
bin\mallet import-dir --input data-folder --output output-folder/corpus.mallet --keep-sequence --remove-stopwords --token-regex "[\p{L}\p{M}]+"
```

**Important: In Windows, the regex pattern must be enclosed in double quotes.**

Once you have imported your data, you can run Mallet's `train-topics` command as normal. However, see below for file naming conventions.

##Step 2
To run Networked Corpus, open a command prompt or terminal and `cd` to the folder containing your Mallet output. In order for Networked Corpus to read the Mallet data, you need to make sure that the data has the following file names:

1. doc_topics.txt (this the file sometimes called "composition")
2. topic_keys.txt
3. topic_state.gz

Change the file names if necessary. Type `cd ..` to go up a level and type `mkdir networkedcorpus`. This will make a folder for your Networked Corpus output. Go back into your output folder by typeing `cd output-folder`.

You are now ready to run Networked Corpus. The following command assumes that Networked Corpus is located inside a folder in a Windows user's `Documents` path:

```
python C:\Users\Scott\Documents\networkedcorpus\gen-networked-corpus.py --input-dir output-folder --output-dir networkedcorpus
```

This will populate your `networkedcorpus` folder with the necessary files. When the process is finished, navigate to that folder and look for `index.html`. Launch it in a browser to view the results.