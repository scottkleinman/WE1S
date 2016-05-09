#### These are some instructions for using dfr-browser written up by Lindsay Thomas:

# Metadata requirements for dfr-browser

+ Ids and file names must match (every id in the `id` column must match a file name in the corpus being modeled); and every id must be unique. 
+ The `pubdate` column (publication date) must be in UTC format. Again, there is undoubtedly a way around this, but I haven't yet figured out how to customize the browser files so that UTC format is not required. But it might be a good idea to standardize our publication dates according to UTC formats anyway.
+ Needs to be in CSV or TSV format.
+ The first column must be the id column, but beyond that, the columns don't need to be in any particular order, as long as they are all in the same order. This means we will need to standardize column type and order across all of our metadata sheets.
+ Issues with special characters: Upon further investigation, the special characters display issue appears to be a problem with the metadata spreadsheet itself. For example, if you look at the title column of row 27, you will see the following: "The Doctorês Failure to Cut Costs." In this case, the spreadsheet has represented an apostrophe with a "ê". Dfr-browser doesn't know how to display this character. In the title column of row 43, you will see something similar: "Room for Debate: Can •Neuro Lit Critê Save the Humanities?" In this case, these are supposed to be single quotes. I believe this is happening with every apostrophe/single quote in the metadata spreadsheet, but I'm not 100% sure about that. I also don't know if this is a result of the conversion from Google spreadsheets to CSV or what.

# Instructions for creating dfr-browser files using dfr-topics in R

## R packages you need to install: 
It's not clear to me if all of these packages are required for what we are using dfr-topics for, but these are the packages Goldstone recommends installing.

+ devtools
+ dplyr
+ ggplot2
+ lubridate
+ stringr
+ readr
+ dfrtopics
  * This requires mallet and rJava packages

## To install these packages using RStudio:

Here is where things get tricky. The following are instructions for installing these packages that worked on my system. I do not know how any of this will play out on a Windows system, or even perhaps on another Mac. But here's what I did.

+ Install every package EXCEPT dfrtopics by going to the “Packages” tab in RStudio and searching for each one. Click the box to install.
+ Then type this into the RStudio console: `install_github("agoldst/dfrtopics")`
+ This may or may not work, depending on if your system is able to install the mallet and rJava R packages. Getting these packages to install in RStudio was difficult on my system. Goldstone has provided these instructions, which help, but which didn’t work for me exactly as they are written and may be out of date by now: [http://andrewgoldstone.com/blog/2015/02/03/rjava/](http://andrewgoldstone.com/blog/2015/02/03/rjava/).
+ You may have to delete and re-install several packages which dfrtopics, mallet and rJava themselves depend on, including R6, Rcpp, and RcppEigen.
+ I was not able to do this properly using Studio’s package installer interface. I would delete them, only to have the packages re-appear when I started up a new R session.
+ I finally got these packages to delete properly by deleting them manually using the command line:
  * This means navigating, via the command line, to the directory where your current version of RStudio stores the packages you install. For me, this is that path: `/Users/lindsaythomas/Library/Frameworks/R.framework/Versions/3.2/Resources/library`. 
  * You might be able to find what this path is for your machine by installing any R package, and then looking in the console to see what R has used for the `lib.loc` path.
  * Once there, use ls command to list the contents of the folder to make sure the packages you want to delete are there.
  * Then use `rm filename-of-package` command to delete the packages you need to delete.
  * Back in RStudio, the packages should no longer show up in the list of packages you have installed.
+ Now you should be able to install the dfrtopics package, which should automatically install the packages you just deleted as part of its installation process.

## To create the browser files:

+ Create topic model using MALLET from the command line
  * The output you need to save is the `topic-state` file (`.gz` extension) and the instances file (`.mallet` extension).
+ Move these files to whatever directory you will be working in to create the dfrbrowser (I have a dedicated dfr directory in my user account, for example).
+ Move whatever metadata file you are using for the browser to this directory as well.
+ Open up the we1s-dfr script (attached to this email) in RStudio and set the working directory to whatever directory you are working in (wherever the topics-state, instances, and metadata files are located).
  * Do this by going to `Session > Set Working Directory > Choose Directory`.
+ Run the first line of the script. This increases the available working memory, which you often need to do to with larger models. You must do this before you load Goldstone’s dfrtopics package.
+ Load required packages (the next block of the script).
+ Change file names as appropriate and run the rest of the script. There should now be a folder called “browser-we1s-2010h” in your working directory. This folder contains the browser files need to run dfr-browser.
  * NOTE: These files WILL NOT be customized to display our metadata correctly. This is a separate issue. We must customize the JavaScript files that the dfr-topics package outputs directly.
+ After making required changes to the browser display files (see below), use the command line to navigate to the browser directory. Once there, type `bin/server`. Then open up an internet browser and go to `http://localhost:8888/`. You should see our model.

## Notes about customizing browser files

+ The Javascript files that the dfr-topics package outputs as part of its browser files creation process must be customized to properly display our metadata. 
+ This involves customizing files located in the` src` directory of dfr-browser. But this directory IS NOT output as part of the browser file creation process in dfr-topics because it is not used by dfr-browser in the display process (this took me an embarrassingly long time to figure out). Instead, you can find these files in the MASTER version of dfr-browser, located on github: [https://github.com/agoldst/dfr-browser](https://github.com/agoldst/dfr-browser).
+ To customize these files, we must download the src directory from github and make the required changes to the necessary JavaScript files. 
+ Then, we must minify these files so that they can be used by the browser (Goldstone includes a script in the master version of dfr-browser that makes this easy). After minifying, we replace the standard .js files in the browser's data directory with our customized .js files. And voila! A customized browser display. Easy, right.......
+ For now, I've stopped tinkering with dfr-browser's JavaScript files until we figure out what our metadata files will look like. Once we settle on a standardized format that ALL of our metadata files will follow, I can then start customizing the browser files so that they are suited to our metadata. 