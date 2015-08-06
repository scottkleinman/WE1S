#Revision of Processes Schema
##DRAFT

`ProcessedData` is a contentless node along the path of the collection, equivalent to the storage folder in a file path. If the processing of the data forks into different directions, extra nodes can be added to the path, and the guidelines below will apply to those nodes.

The manifest for the `ProcessedData` node contains metadata about how the data has been processed. Here is a simple example (asterisks indicate required properties):

###Example 1:
```json
{
  *"_id": "ProcessedData",
  *"path": ",Corpus,New_York_Times,",
  *"processes": [
                  {*"description": "Removed stopwords and punctuation."},
                  {"editors": []},                  
                  {"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}]},
                  {"related": "path"},
                  {"workstation": "workstation"},
                  {"scripts": [{"name": "path"}]}
                ]
}
```
Some quick explanations. The `description` for the process here will be the full prose discussion. It should probably be plain text or serialised html or markdown. If for some reason more formatting is needed (e.g. in a PDF or Word document), the `description` can be a short summary and the path to the related document given for `related`. The `editors` property is the list of editors responsible for the processing, and `date` tells when the processing took place. The reason these properties are not required will become apparent below. The `workstation` allows information about the workstation used to be queried. Finally, if the `description` mentions the use of specific scripts (shorthand for scripts and other software tools), the `scripts` property lists the paths to location of the manifest for each script. The `name` is the name of the script found in the discussion in `description`. 

The above re-working of the processes schema does not eliminate the possibility of sub-dividing processes into steps. Here is an example.

###Example 2:
```json
{
  *"_id": "ProcessedData",
  *"path": ",Corpus,New_York_Times,",
  *"processes": [
                  {*"process": [
                    {"seq": 1},
                    {*"description": "Removed stopwords."},
                    {"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}]},
                    {"editors": []},                  
                    {"related": "path"},
                    {"workstation": "workstation"},
                    {"scripts": [{"name": "path"}]}
                  },
                  {*"process": [
                    {"seq": 2},
                    {*"description": "Removed punctuation."},
                    {"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}]},
                    {"editors": []},                  
                    {"related": "path"},
                    {"workstation": "workstation"},
                    {"scripts": [{"name": "path"}]}
                  }
                ]
}
```

However, this is not a necessary part of the schema and will be more trouble than its worth in most cases.

The examples above are for processes *applied* to the collected data. For processes used in *collecting* the data, it makes sense to embed the process in the `Collection` manifest itself. Here is an example of a `Collection` with an embedded process.

###Example 3:
```json
{
  *"_id": "New_York_Times",
  *"publications": [",Publications,New_York_Times,"],
  *"path": ",Corpus,",
  *"description": "Some content from the New York Times",
  *"collectors": ["John Smith"],
  *"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
  *"processes": [
                  {*"description": "Removed stopwords and punctuation."},
                  {"related": "path"},
                  {"workstation": "workstation"},
                  {"scripts": [{"name": "path"}]}
                ]
}
```
The `editors` and `date` of the process are left out because they are implicitly the `collectors` and `date` of the `Collection`, but those properties can be added if desired.

What if you use the same process for multiple Collections? In this case, you will want to refer to an independent `Process` manifest which will also leave out the editors and dates. The path to this manifest will be along the `Processes` branch, not along the  path of the `Collection`. So your `Collection` manifest will look something like this:

###Example 4:
```json
{
  *"_id": "New_York_Times",
  *"publications": [",Publications,New_York_Times,"],
  *"path": ",Corpus,",
  *"description": "Some content from the New York Times",
  *"collectors": ["John Smith"],
  *"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
  *"processes": [",Processes,Remove_Stopwords,", ",Processes,Remove_Punctuation,"]
}
```
If you really needed to state that the processes were applied sequentially, you could encode that as

###Example 5:
```json
  *"processes": [
        { "seq": 1,
          "path": ",Processes,Remove_Stopwords,"
        },
        {
          "seq": 2,
          "path": ",Processes,Remove_Punctuation,"
        }
      ]
```
Regardless, the manifest for the first process would then look like this:

###Example 6:
```json
{
  *"_id": "Remove_Stopwords,",
  *"path": ",Processes,",
  *"processes": [
                  {*"description": "Stopword removal."},
                  {*"authors": []},
                  {"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}]},                  
                  {"related": "path"},
                  {"scripts": [{"name": "path"}]}
                ]
}
```
Note that a process independent of a specific `Collection` must have an `authors` field. It also seems reasonable to me to require the date of authorship.

If these seems a little complicated, most likely, the relatively simple descriptions found in examples 1, 4, and 6 will be used.