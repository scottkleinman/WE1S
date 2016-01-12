################
'''
Instructions:
1. Make a copy of your articles-not-deduped folder and 
change the name to articles-deduped.

2. Paste the list of files to remove from corpus_compare.py
between the square brackets below, as shown. Adjust the path 
as needed so that the files can be accessed by delete_duplicates.py.

3. Use search and replace to add quotation marks at the beginning 
of each line and add a comma at the end of each line except the last.

4. From a terminal or command prompt, run the following command:

python delete_duplicates.py

All the files in the list will be removed from the articles-deduped folder.
'''
################

files = [
"../1/articles-deduped/guardian-2013-a-133.txt",
"../1/articles-deduped/guardian-2013-h-47.txt"
]

import os
for file in files:
	if os.path.isfile(file):
		os.remove(file)