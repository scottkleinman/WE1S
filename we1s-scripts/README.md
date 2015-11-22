#WES1-SCRIPTS
The `we1s-scripts` folder contains copies of scripts, configuration files, and stop word lists. Each subfolder should have a `README.md` file containing a description of the contents of the folder. Subfolders or individual files may optionally have a json manifest following the WE1S schema.

##Structure
*Deduplicate: Contains the script for de-duplicating files in a collection of texts.
*Scrub: Contains scripts and configuration files for preprocessing, including consolidation and stop word removal.

##Accessing Files
The `we1s-scripts` folder can be downloaded most easily using GitZip. Copying this url:

```
https://github.com/scottkleinman/WE1S/tree/master
```

Then click [here](http://kinolien.github.io/gitzip/) and paste the url in the search bar at the top right. Click the Download Zip File link in the `we1s-scripts` row to download the folder as a zip archive. Click on the `we1s-link` to drill down through the file tree, which will allow you to download individual files.

##Creating Temporary Working Folders
Temporary working folders contain configuration files and stop word lists used for individual projects. They may be shared on GitHub but are merged with the main WE1S project files in the Scrub directory.

Working Folders should be named with the creator's last name followed by first initial (i.e. `SmithJ`). If this leads to duplication, the first name may be expanded. If a user has multiple subsets of configuration files, each one may go in a separate folder named in date format (i.e. `YYYY-MM-DD`), expanded with other identifying information if necessary. When using files in working directories locally, keep in mind that `scrub.py` will not be able to read them unless it is placed in the same folder.

Working folders to be shared on GitHub should be placed in the `we1s-scripts/Scrub/Working` directory.

