"""
scrub.py
v1.0 2015-05-02
v1.1 2015-11-21 active property and stop word handling added
scott.kleinman@csun.edu

1.  Requires configuration in config.py file in same folder as scrub.py
2.  Stop word files must be .txt files with comma, space, or line-separated words.
"""

__author__ = "Scott Kleinman"
__copyright__ = "copyright 2015, The WE1S Project"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "scott.kleinman@csun.edu"

import os, re
from config import *
iterations = len(options)

# Read and scrub files in input directory	
def readFiles(input_file_path, output_file_path):
    fileList = os.listdir(input_file_path)
	# Open individual files
    for file in fileList:
        file_path = os.path.join(input_file_path, file)
        with open(file_path) as f:
            text = f.read()
            # Call the scrub function
            output = scrub(text)
            # Write the scrubbed text to a new file
            output_path = os.path.join(output_file_path, file)
            fh = open(output_path,'w')
            fh.write(output)
            fh.close

def scrub(text):
    # Cycle iterations
    for i in range(0,iterations):
            values = options[i]["values"]
            # If the iteration is for stop words...
            if values == "stopwords":
                fh = open(stopwords_location, 'r')
                stoplist = fh.read()
                fh.close()
                stoplist = re.sub("\s+", ",", stoplist)
                stoplist = stoplist.split(",")
                replace = ""
                print(stoplist)
                for item in stoplist:
                    find = r"\b(?=\w)" + re.escape(item) + r"\b(?!\w)"
                    text = re.sub(find, "", text)
            # Otherwise...
            else:
                # Delete inactive values
                for item in values:
                    if "active" in item.keys() and item["active"] == False:
                        values.remove(item)
                num_values = len(values)
                # Apply each value in iteration
                for j in range(0, num_values):
                    find = values[j]["find"]
                    replace = values[j]["replace"]
                    text = re.sub(find, replace, text)
    return text

# Initiate
print("Processing...\n")

# Read and Scrub Files
readFiles(input_file_path, output_file_path)

# Generate Log String
out = "Number of iterations: " + str(iterations) + "\n\n"
for i, item in enumerate(options):
    values = options[i]["values"]
    if values == "stopwords":
        fh = open(stopwords_location, 'r')
        stoplist = fh.read()
        fh.close()
        stoplist = re.sub("\s+", ", ", stoplist)
        out += "Stopwords Removed: " + stoplist + "\n"
    else:
        out += "Iteration: " + str(i+1) + "\n"
        out += "Find\tReplace\n"
        for j, value in enumerate(values):
            out += value["find"] + "\t-->\t" + value["replace"] + "\n"
    	# Retrieve metadata
        if len(item) > 1:
            out += "Metadata:\n"	
            for k in item:
                if k != "values":
                    out += str(k) + ": " + str(options[i][k]) + "\n"
        out += "\n"

# Print Log
print(out)

# Save Log File
if save_log == True:
    log_file = os.path.join(output_file_path, "log.txt")
    f = open(log_file,'w')
    out = out
    f.write(out)
    f.close

# Success
print("Done!\n")