# Draft Instructions for Installing and Using Serendip

Serendip includes both a command-line tool and a browser interface, each of which has different functions. The command-line tool performs the topic modelling using Mallet and prepare the html files necessary for the browser interface.

The following instructions have not been extensively tested and, at this stage, have been tried only in Windows.

##Requirements
Both Python 2.7 (preferably Ananconda) and Mallet should be already installed on your system. For help, see [Setting up and Testing a WE1S Local Workspace](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/README.md).

##Installation
Following the instructions given on the [Serendip website](), which are repeated here for convenience.

1. Download [this file](https://bootstrap.pypa.io/ez_setup.py). From a command prompt, `cd` to the folder containing the file and then type `python ez_setup.py`. This will install the necessary installation scripts.

2. Finally, download [this .egg file](https://www.dropbox.com/s/md0iuheonf4ryiu/VEP_Core-1.01-py2.7.egg?dl=0), which contains the latest version of Serendip (along with a few built-in topic models). From the command prompt, run the command `easy_install VEP_Core-1.01-py2.7.egg`.

This will install Serendip in the `Anaconda\Lib\site-packages\VEP_Core-1.01-py2.7.egg` folder (assuming that you are running Anaconda). From here, you will need to perform a few modifications to make Serendip work on your system.

3. Install the Python raven module by typing `pip install raven` from the command prompt.

4. Search your sytem for a file called `gzip.exe` and note its file location. If you do not have gzip.exe on your system, you can download it [here](http://gnuwin32.sourceforge.net/packages/gzip.htm). If you have to download a copy move it to a desired location and note the file path.

5. In a text editor, open `C:\Users\Scott\Anaconda2\Lib\site-packages\VEP_Core-1.01-py2.7.egg\vep_core\Apps\SaliencyTopicModelerApp.py`. Search for "gzip.exe" and, at each location, replace it with the full path to `gzip.exe` on your system.

6. Next search for "import-dir". The line will probably begin with `callStr = 'mallet import-dir`. Change "mallet" to the full path to Mallet on your system (e.g. `C:/mallet/bin/mallet`). Note that the path should end in `bin\mallet`.

7. Search for "train-topics". The line will probably begin with `callStr = 'mallet train-topics`. As above, change "mallet" to the full path to Mallet on your system ending in `bin\mallet`.

8. In an editor, `C:\Users\Scott\Anaconda2\Lib\site-packages\VEP_Core-1.01-py2.7.egg\vep_core\Serendip\templates\text.html`. Search for "GET_TOPIC_NAMES_URL". In the line `$GET_TOPIC_NAMES_URL = "{{ url_for('corpus_get_topic_names', corpus_name=corpus_name) }}";` change `corpus_topic_names` to `corpus_get_topic_names`. This fixes a bug in the templating system for Serendip's Text Viewer.

This should make Serendip mostly functional. A few features probably need additional tweaking, but I haven't looked into this yet.

##Using Serendip
To use Serendip, you must first run the command line tool to topic model your data. Start by preparing your data as described below:

1. Place your text files in a folder (called `example` here) and then place the folder in  `C:\Users\Scott\Anaconda2\Lib\site-packages\VEP_Core-1.01-py2.7.egg\vep_core\Data\Corpora`. Although it is possible to provide Serendip's command-line tool with a path to input data, I found that it did not work unless I placed my data in the Corpora folder.

2. Create a stop words file, if desired. It can be located anywhere, as the command-line tool does will accept the file path you specify.

###Building the Topic Model from the Command Line
You are now ready to perform the topic modelling routine. From the command line type something like the following:

`vep_tmbuilder --corpus_name WorksOfShakespeare --corpus_path C:\Users\Scott\Anaconda2\Lib\site-packages\VEP_Core-1.01-py2.7.egg\vep_core\Data\Corpora\example\ --model_name Shakespeare_50 -mS -eS C:\Users\Scott\WE1S\shakespeareanStops.txt --chunkSize 1000 -n 50 -i 1000 --outputAll`

The precise command will vary depending on the options you desire. A complete list of options is available [here](http://vep.cs.wisc.edu/serendip/#gettingStarted). The important points to note are that the command must supply the path to your data folder inside Serendip's Corpora folder and that, if you are using stopwords, you must give the full path to that file.

The process of building the topic model takes less time than the process of creating the html files for Serendip's browser interface. In a test with approximately 3300 documents, the topic modelling took 5 minutes and the rest of the process took 25 minutes.

###Using the Browser Interface
To start the browser interface, type `serendip` at the command prompt. You should see the following:

```
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

When you are finished with Serendip, you will want to return to the command prompt and type `Control+C` to exit from Serendip. Note that you cannot run Serendip at the same time as Lexos because they both use port 5000.

Next, open a browser and enter `http://127.0.0.1:5000/` in the address bar. Serendip will automatically load the `ShakespeareChunked_50` corpus. However, if all went well, you should see your own corpus in the dropdown menu in the title bar. Select it, and your corpus should load shortly.

Note that some changes you make to the view can take a substantial amount of time, often freezing your browser. Be patient. Also, some features such as "Graph" and "Count" in the documents pane will probably not work. These are the functions mentioned above where further tweaking of the code is probably required.