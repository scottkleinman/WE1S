#Draft for New Schema Using MongoDB for Storage

##Syntax
A database record can have an unlimited number of keyword-value pairs, hereafter referred to as “fields”, which are enclosed in curly brackets:

```javascript
{ "keyword": "value",
  "keyword": "value"
}
```

Fields are inherently unordered so, to give them sequence, they may be placed in a list, designated by curly brackets:

```javascript
{[
  {"keyword": "value"},
  {"keyword": "value"}
]}
```

For multiple fields it may be useful to construct a more elaborate structure:

```javascript
{"keyword": [
  {"seq": 1 },
  {"keyword": "value"}
],
 "keyword": [
  {"seq": 2 },
  {"keyword": "value"}
]}
```

This last example demonstrates how fields can be embedded in fields. In this case, the value of they “keyword” field is a list of fields, one of which identifies the sequence and one of which defines some other content.

##Required Fields for All Records
The WE1S schema defines what fields are required or optional in different types of records.

###_id
This is required by MongoDB, which will generate a value based on the date if no value is supplied. Ideally, WE1S staff should create the _id value to be used in the creation of path values. An _id need not be unique, but it should be highly improbable to get the same _id along the same path.

###namespace
This is the WE1S namespace and version number (something like “WE1Sv1.0”). It should be auto-generated.

###path
This is the path in the tree structure that defines hierarchical relationships between database records. Path values are constructed by listing nodes in the tree structure delimited by commas. Each node is represented by its _id value: e.g. ,Corpus,NewYorkTimes,2014,. Some root nodes (like Corpus) have pre-defined values. The value of path within a record is typically to its parent node. In other fields, a path including a record _id will reference another individual record.

##Global Fields
Global fields are fields that can occur in any record. For this reason, they are not listed in the options for specific record types unless they are required.

###title
This is substantially the same as _id, but it is not required. Since _id is used to construct paths, it may not take a form that can be used as a “pretty” title. A suitable value can be placed in a title field for this purpose. See also the label field.

###label
Similar to the title field, but this can be used to supply a value that can be used in creating a graph or other output where a shortened identifier may be useful.

###description
A text string that can contain an extended prose description of the record’s content.

###notes
A list of fields that can contain an extended prose commentary about the record’s content. Each item in the list is a separate note. Here are two examples, one containing a single note and one containing two notes:

```javascript
{"notes": ["This is some commentary about the record"]}
{"notes": [
  {"note": "This is the first note." },
  {"note": "This is the second note." }
]}
```

###group
In some cases, it may be necessary to designate group responsibility for authorship, processing steps, and the like. In these cases the keyword group can be used. For example:

```javascript
{"editors": {"group": "UCSB"}}
```

###Record Types
The WE1S schema does not strictly define the types of records stored in the database, but there are some common record types which have standardized requirements. The WE1S database model is based on a hierarchical tree structure which locates records as children of one of the following types of root nodes:
+ Publications: Information about the provenance of primary data
+ Corpus: The data store for primary and generated data
+ Processes: Metadata about workflow processes used to collect and generate data
+ Scripts: The data store for scripts meta data about tools used to implement workflow processes 

Other record types may be possible at the root level, but they are not anticipated in this document.

The names given for each of the above record types is also the _id for its database record. Its namespace should be auto-generated, and its path should be null. Other fields are optional.

##Publications
Information about primary source material in the corpus is maintained along the path of the Publications node. Each separate publication (broadly defined) is a separate publication record which looks like the following example. Required fields are in bold.
{
 "_id": "New_York_Times",
 "publication": "The New York Times",
 "path": ",Publications,",
 "description": "All the news that’s fit to download",
 "publisher": "The New York Times",
 "date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
 "edition": "online", 
 "altTitle": "New York Times",
 "contentType": "newspaper",
 "language": "en",
 "country": "USA",
 "authors": []
}
date
If there are not start and end dates, the date can be given as a single value, e.g. "date": ["2013"].
language
Language codes should be taken from the ISO 639-2 list.
country
Country codes should be taken from some controlled vocabulary list.
authors
Some publications (e.g. monographs) may have authors; otherwise, this information is best supplied in the records of individual newspaper articles and the like.
Collections
The Corpus serves as a data store for all primary and generated data housed by the project. It is composed of Collections which represent a variety of types of data sets. These may be subsets or suprasets of publications, or they may be data and metadata records generated by WE1S staff, or related files stored for reference. The following example represents a Collection derived from a Publication.
{
 "_id": "New_York_Times",
 "publications": [",Publications,New_York_Times,"],
 "path": ",Corpus,",
 "description": "Some content from the New York Times",
 "collectors": [],
 "date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
 "workstation": "Windows 8.1", 
 "queryTerms": [],
 "processes": []
}
date
The date here refers to the dates on which the data was collected. If there are not start and end dates, the date can be given as a single value, e.g. "date": ["2013"].
workstation
This provides optional information about the environment in which the data was collected.
queryTerms
Provides keywords used to define the scope of the collection (possibly better referred to as “keywords” or “facets”). The value can be used to query the Corpus for data matching a particular description.
processes
This field may contain embedded processes or paths to separate process records. Regardless, they follow the same schema, described under Processes.
Note that there is no need to reference outputs of the Collection since they will be found along a standard path within the collection, described below.
Here is an example of a record which combines materials from two publications:
{
 "_id": "New_York_Times_Wall_Street_Journal",
 "publications": [
                   ",Publications,New_York_Times,",
                   ",Publications,Wall_Street_Journal,"
                 ],
 "path": ",Corpus,",
 "description": "Some content from the New York Times and the Wall 
                 Street Journal",
 "collectors": [],
 "date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}]
}
Data Nodes
Collection data is stored under different parent nodes, depending on the type of data. The WE1S schema requires the use of standard node _id values for each of the data types:
•	RawData: Primary source data
•	ProcessedData: Source data transformed by WE1S staff in preparation for analysis
•	Metadata: Metadata records accompanying the primary source data
•	Outputs: Data and metadata records generated by WE1S analytic processes 
•	Related: Records associated with the Collection, such as documentation, often kept for reference
These nodes have minimal information in their database records. The names given for each of the above record types is also the _id for its database record. Its namespace should be auto-generated, and its path should be ,Corpus,collection_id,. Other fields are optional. Each of the child records will be described next.
RawData
RawData records are path nodes for documents containing the data They should have the path value ,Corpus,collection_id,RawData,. Along this path will be found individual data documents. A RawData node may have some additional metadata shown in the schema below:
{
 "_id": "RawData",
 "path": ",Corpus,New_York_Times,",
 "relationships": [
                   {"isPartOf",",Corpus,CollectionA,"},
                   {"hasPart",",Corpus,CollectionB"}
                  ]
 "OCR": true,
 "rights": "Creative Commons License"
}
These schema uses the relationships field to describe the data as being a part of another Collection (CollectionA) combined with material from a third Collection (CollectionB). The values of relationships, OCR, and rights are inherited by all data along the path ,Corpus,New_York_Times,RawData,.
OCR
Indicates whether the data has been digitized using Optical Character Recognition. If omitted, the default value is false.
rights
A statement of licensing rights or intellectual property restrictions. Free culture is assumed by default.
RawData Records
Data records along the RawData path have the following schema.
{
 "_id": "Some_id",
 "path": ",Corpus,New_York_Times,RawData,",
 "authors": [],
 "mimeType": "",
 "documentType": ""
}
Since records of this type will typically be derived from files, it makes sense to use the file name (minus the file extension) as the _id.
For items like newspaper articles, the author(s) can be supplied for each article.
The mimeType field will indicate the original file format. A list of common media formats can be found at http://en.wikipedia.org/wiki/Internet_media_type#List_of_common_media_types.
Tentatively, documentType is added (tentatively) here in case the content of individual documents (as opposed to publications or collections) needs a controlled vocabulary.
ProcessedData
ProcessedData records are path nodes for documents containing data transformed by WE1S non-analytic processe. They should have the path value ,Corpus,collection_id,ProcessedData,. Along this path will be found individual data documents. A ProcessedData node may have some additional metadata shown in the schema below:
{
 "_id": "ProcessedData",
 "path": ",Corpus,New_York_Times,",
 "processes": [
                {"step": [
                           {"seq": 1},
                           {"reference": ",Processes,process_id,"}
                        ]
                },
                {"step": [
                           {"seq": 2},
                           {"reference": ",Processes,process_id,"}
                        ]
                }
}
In the above example each step in the processing refers to a separate record describing the processes applied to the data in the RawData path. In place of the reference field, it is also impossible to embed the description of the process directly in the ProcessedData record. This is most appropriate for simple processes that are applied only to the specific data in the Collection.
Metadata
Metadata records are path nodes for documents containing metadata that may have been acquired along with the raw data. They should have the path value ,Corpus,collection_id,Metadata,. Along this path will be found individual metadata documents. A Metadata node will have a schema like the one below:
{
 "_id": "Metadata",
 "path": ",Corpus,New_York_Times,"
}
Metadata nodes and/or records are similar to raw data records in allowing a mimeType field.
Outputs
Metadata records are path nodes for data and metadated generated through WE1S analytic processes. They should have the path value ,Corpus,collection_id,Outputs,. Along this path may be found a variety of child nodes (data, metadata, visualizations, documentation, and so on):
{
 "_id": "Outputs",
 "path": ",Corpus,New_York_Times,"
}
Outputs nodes and/or records are similar to raw data records in allowing a mimeType field.
The Outputs branch in the hierarchy can have further ad hoc branches (e.g. CSVs, visualizations, etc.), depending on the nature of the content.
Related
Related records are path nodes for documents (typically files) such as documentation which are archived for reference.
{
 "_id": "Related",
 "path": ",Corpus,New_York_Times,"
}
Related nodes and/or records are similar to raw data records in allowing a mimeType field.
Processes
Related records are path nodes for documents (typically files) such as documentation which are archived for reference.
{
 "_id": "Process_id",
 "path": ",Processes,Process_id,",
 "description": "A process to remove stop words.",
 "editors": [],
 "source": [],
 "steps": [
            {
             "step": 1,
             "description": ""
            },
            {
             "step": 2,
             "description": ""
            }
          ],
 "date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
 "workstation": "workstation"

}
In the example above, the description field for each step stands in for the entire step schema shown below. Since processing steps are sequential, they need to be given an iterator. A step value may be a reference to a package (which is a re-usable process that is not specific to a single data set).
source
If the process is not embedded in a Collection record, this field contains the record _id or path to the input data. The path field is better since it will contain the collection. Otherwise, the collection should be mentioned in the description or an optional collection keyword can be added to reference it.
Step Records
Related records are path nodes for documents (typically files) such as documentation which are archived for reference.
{
 "_id": "Step_id",
 "path": ",Processes,Process_id,step_id",
 "seq": 1,
 "description": "A process to remove stop words.",
 "type": ["tool","script","API"],
 "reference": "",
 "label": "Mallet",
 "version": "2.0.7",
 "options": [
              { "argument": "value" },
              { "argument": "value" }
            ],
 "output": [],
 "instructions": ""
}
In the above example, _id and _path are required because the record is an independent node. They are not required if the step is embedded in a Process record. 
reference
Contains a reference to the tool or script. If a tool, this can be a URL to the tool's website. If the step involves a script, the reference should be a path to the script's record, which will contain the script's version number. The reference field can also be used to identify a path to a package (independent reusable process) that is a step in the Process.
label
Contains keyword for the name of the tool or script (useful for external resources).
version
Contains keyword for the version of the tool or script. This is useful for external resources. WE1S scripts will have the version number embedded in their own records.
options
Contains information about the configuration of the tool or script used in the step. The option name should be given as the “argument” and the “value” should be the option setting. This structure is ideally suited for command-line tools, but the JSON object can contain fields like {"settings.cfg": "Sample config file:..."} to record a sample configuration file. Likewise, you might have {"api": "http://api.nytimes.com/svc/search/v2/articlesearch"} for an API query with further arguments for the query terms.
output
A list of paths to the root node where all the script’s outputs are stored.
instructions
Although instructions can be put in the notes and description, an explicit instructions field is perhaps helpful, especially for packages.

Scripts
The Scripts root really includes manifests for external scripts or tools, as well as WE1S scripts. The general architecture consists of branching structures for standard types of processes:
•	Collecting
•	Preprocessing
•	Analysis
•	Visualization
Each of these branches may have child branches for different tools. However, the standard paths will divide scripts by language (Python and R in the examples below). Hence a possible path would be Scripts > Preprocessing > Python > stripTags. If the record is for a tool or external program, the terminal node record will contain manifest information about the tool or program. If it is a WE1S script, the record will additionally contain the code of the script itself. (Note: Are there security risks to storing code in this way?)
A typical script record will look like the following:
{
 "_id": "stripTags",
 "path": ",Scripts,Preprocessing,Python,",
 "authors": ["Scott Kleinman"],
 "date": "2014-01-01",
 "version": "1.0",
 "description": "A script to strip tags",
 "script": "def stripTags(str):\n etc. etc."
}
A typical tool record will look like this:
{
 "_id": "stripTags",
 "reference": "http://mallet.cs.umass.edu/topics.php",
 "authors": ["Andrew Kachites McCallum"],
 "dateAccessed": "2015-01-01",
 "version": "2.0.7",
 "description": "LDA topic modeling tool",
}
In other words, scripts stored in the database will have paths, authors, dates of authorship, and the script code. External tools will have references and dates of access. A version number may not always be available, but a value like “unknown” can be used in such cases.
