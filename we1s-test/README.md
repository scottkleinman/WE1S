# Setting Up and Testing A WE1S Local Workspace
This is a guide for preparing your computer for work with data from the WE1S data set. It tells you how to download and install the necessary software, how to set up a file system, and how to acquire the data from the WE1S file store.

The WE1S workflow uses the Python programming language for preparing and analyzing data files. Therefore, you must have Python installed on your system. In addition, the Mallet machine learning toolkit is used for topic modeling. The instructions here provide guidance for installing this software.

It is valuable to have a good text editor on your system. Many such editors are available (you can even use Word in a pinch), but, in the interest of simplification, we will recommend [Sublime Text 3](http://www.sublimetext.com/3) and refer to that in subsequent instruction.

##Python
The Python programming language comes with a set of core functions which can be supplemented by the installation of additional "packages". There are numerous ways to install Python on your system, but the easiest is to use a pre-made Python distribution. This typically includes an auto-installer you can double-click to perform the installation, as well as many of the important Python packages already installed. The WE1S project recommends the Anaconda distribution. Anaconda is produced by Continuum Analytics for use in their data analytics products and services. The distribution itself is free. Anaconda also comes with a very good Python editor called Spyder which can be used to edit and run Python scripts. This is an option if you do not wish to use Sublime.

###Installing Anaconda
Download either the [Windows 64-Bit Graphical Installer](https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.0-Windows-x86_64.exe) or the [Mac OS X 64-Bit Graphical Installer](https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.0-MacOSX-x86_64.pkg). If one of these links does not work, go to [https://www.continuum.io/downloads](https://www.continuum.io/downloads). Make sure that you click the Graphical Installer and that you are downloading Python version 2.7.

Double-click the Graphical Installer and let Anaconda install. For the most part, the process is simple. The Mac OS X provides prompts along the way, but you can simply instruct the process to continue when these appear. When the installation is finished, a Launcher icon will appear on your desktop. You do not need to use this, but you may find it convenient.

###Testing your Python Installation
Before proceeding, it is useful to test whether Python works. To do this, you will need to open a command prompt (Windows) or terminal (Mac). If you do not know how to do this on your system, Google "open command prompt windows 8" (replace the Windows version number with whatever version you are running) or "open terminal Mac OSX". Type python and hit enter. You should see something like this:

![The Python Command Prompt](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/python-command.png?raw=true "The Python Command Prompt")

Next to the `>>>` prompt, type `print("hello")` and hit `enter`. You should see this:

![The Python Print Response](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/python-hello.png?raw=true "The Python Print Response")

If this works, Python is running. Type `exit()` to exit Python.

Next download and the WE1S test resources here. Unzip the file to your system's desktop. Once that is done, return to the command prompt or terminal. The prompt should display your current location on your computer. In the example above, this is `C:\Users\Scott`. On a Mac, it will be something like `/Users/Scott`. Note the username for your system. Now navigate to the WE1S test folder using the following command:

Windows: `cd C:\Users\USERNAME\Desktop\wes1s-test`

Mac: `cd /Users/USERNAME/Desktop/we1s-test`

`cd` means "change directory`. You can go up a level by typing `cd ..`, and you can find your current location by typing `pwd`. Type `dir` (Windows) or `ls` (Mac) to see a list of files in the directory.

Once you are in the test folder, type `python hello.py` followed by `enter` to run the "hello" test script. You should see something like this:

![The Python Hello Script Response](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/python-hello-script.png?raw=true "The Python Hello Script Response")

You have now confirmed that you can run a Python script. Note that you must `cd` to the directory containing the script in order to run it.

Anaconda comes with a package called Jupyter notebooks (formerly iPython notebooks) that allows you to run Python in your browser. We'll test this next, using the old name "iPython" for simplicity. From the command or terminal prompt, type `ipython notebook` and hit `enter` (you can also use the desktop launcher). There will be a short delay after which a browser window will open.

You should see this:

![The iPython/Jupyter Home Screen](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/ipython-1.png?raw=true "The iPython/Jupyter Home Screen")

Here the `we1s-test` folder is renamed `a-we1s-test` just to get it to display at the top of the screen. You can keep the original name. Click the `New` button and select `Python 2`. A new window will open that looks like this:

![Empty iPython/Jupyter Notebook](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/ipython-2.png?raw=true "Empty iPython/Jupyter Notebook")

The selection highlighted in green is called a cell. You can enter Python code in it and then execute the code by typing `Shift+Enter`. Let's try it. Type `print("hello")`. Then type `Shift+Enter`. You should see this:

![iPython/Jupyter Output](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/ipython-3.png?raw=true "iPython/Jupyter Output")
 
Now let's try something more complicated. In the `we1s-test` folder, you will see subfolders called `input` and `output`. The input folder contains a text file called `file.txt`. If you open it in Sublime, you will see that it just says, "THIS IS SOME SAMPLE TEXT". Go back into your jupyter notebook and paste the following into a cell:

```python
##### Configuration #####

# Configure the filename
filename = "file.txt"

# Configure the path to input directory
input_path = "C:\Users\USERNAME\Desktop\we1s-test\input"
# input_path = "/Users/USERNAME/Desktop/we1s-test/input"

# Configure the path to output directory
output_path = "C:\Users\USERNAME\Desktop\we1s-test\output"
# output_path = "/Users/USERNAME/Desktop/we1s-test/output"

##### End of Configuration #####

# Import the os package to manage file paths
import os

# Create input and out file paths
input_file = os.path.join(input_path, filename)
output_file = os.path.join(output_path, filename)

# Open the input file and read it
f = open(input_file)
text = f.read()
f.close()
print("The input file says: " + text)

# Convert the text to lower case
text = lower(text)

# Open the output file for writing and save the new text to it
f = open(output_file, "w")
f.write(text)
f.close()
print("I've just written a new file to your output folder. Check it out!")
```

Note the comments preceded by `#` which describe what each block of code is doing. At the top of the file is the configuration section. The name of the file is already configured for you, but you will need to change the input and output file paths. In the code above, these are set to Windows file paths. If you have a Mac, type `#` at the beginning of the lines that have `C:\\` and remove the `#` from the lines that have `/Users/`. Next replace `USERNAME` with your username. Now you are ready to run the code. Type `Shift+Enter`. You should see this:

![iPython/Jupyter Script Output](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/ipython-4.png?raw=true "iPython/Jupyter Script Output")

If you get an error, go back and check your configuration settings. If the code works, go to the output folder and open the `file.txt` file in Sublime. You will see that it contains the same text converted to lower case.

Now we will perform one last test. We'll now try the same thing from an iPython notebook that has been pre-prepared. Make sure that you were in the `we1s-test` folder when you launched iPython. If not, go to the command or terminal and type `Control+C` or `Command+C` one or more times until iPython exits stops. You should get a normal prompt again. Use it to `cd` to the `we1s-test` directory and then type `ipython notebook` followed by `enter`. iPython notebooks should restart, and you should be able to see a file called `ipython-notebook-test.ipynb`. Click on it, and a new browser window will open. Follow the instructions from there.

If you do not receive an error after following the instructions, you have successfully run the iPython notebook test. To exit, close the iPython notebooks windows in your browser and return to the command or terminal prompt. Type `Control+C` or `Command+C` to interrupt the iPython process. You may have to do this several times. Once the process is interrupted, you can type `exit` to exit from the command prompt or terminal.

You have now successfully tested your Python installation, and you are ready to use it for work on the WE1S project.

##MALLET
Mallet is a machine learning tool written in Java. To run it, you must first have the Java Developers Toolkit (JDK) installed on your system. This is different from the Java plugin that is used for browsers, so you probably don’t already have it.

###Installing Java Developers Kit (JDK)
Go to [http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html) and click the Java download image at the top. On the next page, you will see a list of download links near the top with the header (at the time of writing) "Java SE Development Kit 8u65". Click the **Accept License Agreement** radio button underneath and then click the download link appropriate to your system. This will likely be "Windows x64" or "Mac OS X x64". When the download finishes, double-click the downloaded file to install JDK. You are now ready to install Mallet.

###Installing Mallet
Download Mallet by clicking [this link](http://mallet.cs.umass.edu/dist/mallet-2.0.8RC3.zip). When the download is finished, unzip the archive. Double-click on the `mallet-2.0.8RC3` folder and you'll find another folder with the same name inside. Change the name to `mallet`. Make sure it is all lower case, or you'll run into trouble below. Drag the mallet `folder` to your root directory. `C:\` (Windows) or `/Users/` (Mac). This is very important.

The instructions in this paragraph apply only to Windows users. You next need to set the Windows environment variable. Type `Windows Key+Q` to get a search bar and search for "environment variables". Click the `Edit the system environment variables` link. When the System Properties dialog appears, click `Environment Variables…`. Click the `New...` button at the top of the dialog and type `MALLET_HOME` (all caps) for the variable name and `C:\mallet\` for the variable path. Click `OK` for each of the dialogs until the System Properties dialog is closed.

Mac users may now re-join us. Open a command prompt or terminal. Type `cd C:\mallet` (Windows) or `cd /Users/mallet` (Mac) to go to the `mallet` folder. Then type `\bin\mallet` (Windows) or `./bin/mallet` and hit `enter`. If Mallet is working, you should see a list of commands. If you get an error, there is a problem with your installation. See the detailed instructions in the [Program Historian Mallet tutorial](http://programminghistorian.org/lessons/topic-modeling-and-mallet) for further help.

###Testing Mallet
You are now ready to test Mallet. For the test, we will use Mallet's sample data. Open a Windows command prompt or Mac terminal and navigate to the `mallet` directory. We'll start by importing Mallet's sample data set. Copy the following command into Sublime:

```
bin\mallet import-dir --input sample-data\web\en --output C:\Users\USERNAME\Desktop\we1s-test\mallet-test.mallet --keep-sequence --remove-stopwords
```

For the Mac, this would be

```
./bin/mallet import-dir --input sample-data/web/en --output /Users/USERNAME/we1s-test/mallet-test.
mallet --keep-sequence --remove-stopwords
```

Replace `USERNAME` with your username.

Now let's look at what this command is doing. It is setting the input directory for your data to `sample-data/web/en`. This folder contains a small number of texts in English. Since `sample-data` is inside the `mallet` directory, we can simply give the path relative to that directory.

Next the command sets the path to the output file, which we'll call `mallet-test.mallet`. We want to save it to the `we1s-test` directory, so we'll give it the complete path there.

Finally, the command contains a couple of “arguments” (options) telling Mallet to keep the sequence of the words but to remove stop words (Mallet has a small list of default stop words).

When we run this command, Mallet will import the texts and save it to a mallet data file called `mallet-test.mallet`. To run the command, copy the version you have in Sublime and paste it into the command prompt or terminal (you can normally do this by right-clicking). There will be a pause and then you should get another prompt without any errors.

So far, you have just imported the data. Now you can run the topic model with a second command:

```
bin\mallet train-topics  --input C:\Users\USERNAME\Desktop\we1s-test\mallet-test.mallet --num-topics 10 --output-state C:\Users\USERNAME\Desktop\we1s-test\output-state.gz --output-topic-keys C:\Users\USERNAME\Desktop\we1s-test\keys.txt
```

For the Mac, this would be

```
./bin/mallet train-topics  --input /Users/USERNAME/Desktop/we1s-test/mallet-test.mallet --num-topics 10 --output-state /Users/USERNAME/Desktop/we1s-test/output-state.gz --output-topic-keys /Users/USERNAME/Desktop/we1s-test/we1s-test/keys.txt
```

Paste this command into Sublime. As you can see, you'll need to configure your username.
Now let's pick this command apart. We're asking Mallet to train itself to recognize topics and feeding it our `mallet-test.mallet` data file as input by providing it the complete path to that file. Then we are telling it to generate 10 topics and send two types of output (output-state and output-topic-keys) to a file called `output-state.gz` and a file called `keys.txt`. Paste this command into the command prompt or terminal window and hit enter. If there are no errors (and be careful, it is easy to make typos), a bunch of data should flash down the screen, rather like the Matrix. After a minute or less, you should receive a new command prompt when the process is complete.

Navigate to the `we1s-test folder` and look for the `keys.txt` file. Open it in Sublime, and you should see something like this:

![Mallet keys.txt file](https://github.com/scottkleinman/WE1S/blob/master/we1s-test/images/mallet-keys.png?raw=true "Mallet keys.txt file")

If you got that, you have successfully tested Mallet, and you are ready to do topic modeling on WE1S data. Just one warning. When working with bigger data sets, you may encounter the following error:

```
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
```

If this happens, see the section on **Issues with Big Data** in the [Programming Historian tutorial](
http://programminghistorian.org/lessons/topic-modeling-and-mallet).
