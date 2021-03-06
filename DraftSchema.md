#Draft for New Schema Using MongoDB for Storage

##Syntax
`MongoDB` stores data as JSON objects populated with keyword-value pairs. Each JSON object is called a "collection", and the keyword-value pairs are called "documents". In order to avoid confusion, I avoid these terms and refer to a "collection" as a **record** and a "document" as a **field**.

A database record can have an unlimited number of fields, which are enclosed in curly brackets:

```javascript
{ "keyword": "value",
  "keyword": "value"
}
```

Fields are inherently unordered so, to give them sequence, they may be placed in a list, designated by square brackets:

```javascript
{[
  {"keyword": "value"},
  {"keyword": "value"}
]}
```

For multiple fields it may be useful to construct a more elaborate structure employing a keyword for sequence:

```javascript
{"keyword": [
              {"seq": 1 },
              {"keyword": "value"}
            ],
 "keyword": [
              {"seq": 2 },
              {"keyword": "value"}
            ]
}
```

This last example demonstrates how fields can be embedded within fields (MongoDB refers to these as "embedded documents"). In this case, the value of they `keyword` field is a list of fields, one of which identifies the sequence and one of which defines some other content.

##Required Fields for All Records
The WE1S schema defines what fields are required or optional in different types of records.

###_id
This is required by MongoDB, which will generate a value based on the date if no value is supplied. Ideally, WE1S staff should create the `_id` value to be used in the creation of path values. An `_id` need not be unique, but it should be highly improbable to get the same `_id` along the same path.

###namespace
This is the WE1S namespace and version number (something like `WE1Sv1.0`). It should be auto-generated. Hence, for brevity, `namespace` fields are not shown in the examples below.

###path
This is the path in the tree structure that defines hierarchical relationships between database records. Path values are constructed by listing nodes in the tree structure delimited by commas. Each node is represented by its `_id` value: e.g. `,Corpus,NewYorkTimes,2014,`. Some root nodes (like Corpus) have pre-defined values. The value of path within a record is typically to its parent node. In other fields, a path including a record `_id` will reference another individual record.

##Global Fields
Global fields are fields that can occur in any record. For this reason, they are not listed in the options for specific record types unless they are required.

###title
This is substantially the same as `_id`, but it is not required. Since `_id` is used to construct paths, it may not take a form that can be used as a "pretty" title. A suitable value can be placed in a title field for this purpose. See also the `label` field.

###label
Similar to the `title` field, but this can be used to supply a value that can be used in creating a graph or other output where a shortened identifier may be useful.

###description
A text string that can contain an extended prose description of the record’s content.

###notes
A list of fields that can contain an extended prose commentary about the record’s content. Each item in the list is a separate `note`. Here are two examples, one containing a single note and one containing two notes:

```javascript
{"notes": ["This is some commentary about the record"]}

{"notes": [
  {"note": "This is the first note." },
  {"note": "This is the second note." }
]}
```

*Question: Should we require the keyword `note` or just allow a list of strings?* 

###group
In some cases, it may be necessary to designate group responsibility for authorship, processing steps, and the like. In these cases the keyword `group` can be used. For example:

```javascript
{"editors": [ {"group": "UCSB"} ]}
```

##Required Fields by Record Type
Whilst a MongoDB record can have any number of ad hoc fields, WE1S certain fields in some record types and not in others. In other words, the WE1S database should follow a consistent schema. In all the examples given in this documentation, fields required for a particular record type are preceded by an asterisk.

##Record Types
The WE1S schema does not strictly define the types of records stored in the database, but there are some common record types which have standardized requirements. The WE1S database model is based on a hierarchical tree structure which locates records as children of one of the following types of root nodes:

+ `Publications`: Information about the provenance of primary data
+ `Corpus`: The data store for primary and generated data
+ `Processes`: Metadata about workflow processes used to collect and generate data
+ `Scripts`: The data store for scripts meta data about tools used to implement workflow processes 

Other record types may be possible at the root level, but they are not anticipated in this document.

The names given for each of the above record types is also the `_id` for its database record. Its namespace should be auto-generated, and its path should be null. Other fields are optional.

##Publications
Information about primary source material in the corpus is maintained along the path of the Publications node. Each separate publication is a separate `publication` record (with a broad definitions of "publication"), which looks like the following example.

```javascript
{
  *"_id": "New_York_Times",
  *"publication": "The New York Times",
  *"path": ",Publications,",
  *"description": "All the news that’s fit to download",
  *"publisher": "The New York Times",
  *"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
   "edition": "online", 
   "altTitle": "New York Times",
   "contentType": "newspaper",
   "language": "en",
   "country": "USA",
   "authors": ["John Smith"]
}
```

###Notes:
####date
If there are not start and end dates, the date can be given as a single value, e.g. "date": ["2013"].

####language
Language codes should be taken from the [ISO 639-2 list](http://www.loc.gov/standards/iso639-2/php/code_list.php).

####country
Country codes should be taken from some controlled vocabulary list. *Question: is there a standard list we can use?*

####authors
Some publications (e.g. monographs) may have authors; otherwise, this information is best supplied in the records of individual newspaper articles and the like.

##Collections
The Corpus serves as a data store for all primary and generated data housed by the project. It is composed of collections which represent a variety of types of data sets. These may be subsets or suprasets of publications, or they may be data and metadata records generated by WE1S staff, or related files stored for reference. The following example represents a collection derived from a publication.

```javascript
{
  *"_id": "New_York_Times",
  *"publications": [",Publications,New_York_Times,"],
  *"path": ",Corpus,",
  *"description": "Some content from the New York Times",
  *"collectors": ["John Smith"],
  *"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
   "workstation": "Windows 8.1", 
   "queryTerms": ["humanities"],
   "processes": [*path to process*]
}
```
###Notes:

####date
The date here refers to the dates on which the data was collected. If there are not start and end dates, the date can be given as a single value, e.g. `"date": ["2013"]`.

*Question: Fields which take multiple values in lists are here representing as requiring a list, rather than a string, even if there is only a single value. Is there any reason not to do this?*

####workstation
This provides optional information about the environment in which the data was collected.

####queryTerms
Provides keywords used to define the scope of the collection (possibly better referred to as "keywords" or "facets"). The value can be used to query the Corpus for data matching a particular description.

####processes
This field may contain embedded processes or paths to separate process records. Regardless, they follow the same schema, described under `Processes`.

Note that there is no need to reference outputs of the collection since they will be found along a standard path within the collection, described below.

Here is an example of a record which combines materials from two publications:

```javascript
{
  *"_id": "New_York_Times_Wall_Street_Journal",
  *"publications": [
                    ",Publications,New_York_Times,",
                    ",Publications,Wall_Street_Journal,"
                   ],
  *"path": ",Corpus,",
  *"description": "Some content from the New York Times and the Wall Street Journal",
  *"collectors": [],
  *"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}]
}
```

##Data Nodes
Collection data is stored along different branches of the collection node, depending on the type of data. The WE1S schema requires the use of standard node `_id` values for each of the data types:

+ `RawData`: Primary source data
+ `ProcessedData`: Source data transformed by WE1S staff in preparation for analysis
+ `Metadata`: Metadata records accompanying the primary source data
+ `Outputs`: Data and metadata records generated by WE1S analytic processes 
+ `Related`: Records associated with the Collection, such as documentation, often kept for reference

The name given for each of the above record types is also the `_id` for its record node. Its namespace should be auto-generated, and its path should be `,Corpus,collection_id,`. Other fields are optional.

Each type of data is described in detail below.

##RawData
RawData records are path nodes for documents containing the primary data collected by WE1S staff. They should have the path value `,Corpus,collection_id,RawData,`. Along this path will be found individual data documents. A RawData record may have some additional metadata shown in the schema below:

```javascript
{
  *"_id": "RawData",
  *"path": ",Corpus,New_York_Times,",
   "relationships": [
                      {"isPartOf",",Corpus,CollectionA,"},
                      {"hasPart",",Corpus,CollectionB"}
                  ]
   "OCR": true,
   "rights": "Creative Commons License"
}
```

###Notes:

This schema uses the `relationships` field to describe the data as being a part of another collection (CollectionA) combined with material from a third collection (CollectionB). Terms from Dublin Core are used in the example above, but it is possible to use other terms from a controlled vocabulary.

The values of `relationships`, `OCR`, and `rights` are inherited by all data along the path `,Corpus,New_York_Times,RawData,`.

####OCR
A boolean to indicate whether the data has been digitized using Optical Character Recognition. If omitted, the default value is `false`.

####rights
A statement of licensing rights or intellectual property restrictions. `Free culture` is assumed by default.

##Data Documents
Data documents along a Data Record path contain the binary or plain text content of the data. They have the following schema (this example below assumes the `RawData` path).

```javascript
{
  *"_id": "Some_id",
  *"path": ",Corpus,New_York_Times,RawData,",
  *"content": "This is the text of the journal article.",  
   "authors": [],
   "mimeType": "",
   "documentType": ""
}
```

###Notes:

Since records of this type will typically consist of or be derived from files, it makes sense to use the file name (minus the file extension) as the `_id`.

For items like newspaper articles, the author(s) can be supplied for each article.

The `mimeType` field will indicate the original file format. A list of common media formats can be found at [http://en.wikipedia.org/wiki/Internet_media_type#List_of_common_media_types](http://en.wikipedia.org/wiki/Internet_media_type#List_of_common_media_types).

`documentType` is added (tentatively) here in case the content of individual documents (as opposed to publications or collections) needs a controlled vocabulary.

##ProcessedData
ProcessedData records are path nodes for documents containing data transformed by WE1S non-analytic processe. They should have the path value `,Corpus,collection_id,ProcessedData,`. Along this path will be found individual data documents. A ProcessedData node may have some additional metadata shown in the schema below:

```javascript
{
  *"_id": "ProcessedData",
  *"path": ",Corpus,New_York_Times,",
  *"processes": [
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
```

In the above example each step in the processing refers to a separate record describing the processes applied to the data in the RawData path. In place of the `reference` field, it is also impossible to embed the description of the process directly in the ProcessedData record. This is most appropriate for simple processes that are applied only to the specific data in the collection.

##Metadata
Metadata records are path nodes for documents containing metadata that may have been acquired along with the raw data. They should have the path value `,Corpus,collection_id,Metadata,`. Along this path will be found individual metadata documents. A Metadata node will have a schema like the one below:

```javascript
{
  *"_id": "Metadata",
  *"path": ",Corpus,New_York_Times,"
}
```

Metadata nodes and/or records are similar to raw data records in allowing a `mimeType` field.

###Outputs
Outputs records are path nodes for data and metadata generated through WE1S analytic processes. They should have the path value `,Corpus,collection_id,Outputs,`. Along this path may be found a variety of ad hoc child nodes (`data`, `metadata`, `visualizations`, `documentation`, and so on), which are not standardized in the WE1S schema:

```javascript
{
  *"_id": "Outputs",
  *"path": ",Corpus,New_York_Times,"
}
```

Outputs nodes and/or records are similar to raw data records in allowing a `mimeType` field.

##Related
Related records are path nodes for documents (typically files) such as documentation which are archived for reference.

```javascript
{
  *"_id": "Related",
  *"path": ",Corpus,New_York_Times,"
}
```

Related nodes and/or records are similar to raw data records in allowing a `mimeType` field.

##Processes
Process records are path nodes for documents (typically files) such as documentation which are archived for reference.

```javascript
{
  *"_id": "Process_id",
  *"path": ",Processes,Process_id,",
  *"description": "A process to remove stop words.",
  *"editors": [],
   "source": [],
  *"steps": [
              {
               "seq": 1,
               "reference": "*path to process record*",
               "description": ""
              },
              {
               "seq": 2,
               "reference": "*path to process record*",
               "description": ""
              }
            ],
  *"date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
   "workstation": "workstation"
}
```

###Notes:
In the example above, the `description` field for each step stands in for the entire step schema, which described under `Step Records` below. Since processing steps are sequential, they need to be given an sequencing number using the `seq` keyword.

Alternatively, a step may provide a `reference` to a "package" (that is, a re-usable process that is not specific to a single data set).

####source
If the process is not embedded in the collection record, this field contains the record `_id` or `path` to the input data. The `path` field is better since it will contain the collection. Otherwise, the collection should be mentioned in the description or an optional `collection` keyword can be added to reference it.

*Question: Given multiple ways to handle this, which is the best?*

##Step Records
Step records describe the workflow parameters of a single step in a process. They may be embedded within or referenced from a process record.

```javascript
{
   "_id": "Step_id",
   "path": ",Processes,Process_id,step_id",
  *"description": "A process to remove stop words.",
  *"type": ["tool","script","API"],
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
```

###Notes:
In the above example, `_id` and `_path` would be required if the record were an independent node. They would not be required if the step is embedded in a process record. 

####reference
Contains a reference to the tool or script. If it is a tool, this can be a URL to the tool's website. If the step involves a script, the reference should be a path to the script's record, which will contain the script's version number. The `reference` field can also be used to identify a path to a package (independent reusable process) that is a step in the process.

####label
Contains keyword for the name of the tool or script (useful for external resources).

####version
Contains keyword for the version of the tool or script. This is useful for external resources. WE1S scripts will have the version number embedded in their own records.

####options
Contains information about the configuration of the tool or script used in the step. The option name should be given as the "argument" and the "value" should be the option setting. This structure is ideally suited for command-line tools, but the JSON object can contain fields like `{"settings.cfg": "Sample config file:..."}` to record a sample configuration file. Likewise, you might have `{"api": "http://api.nytimes.com/svc/search/v2/articlesearch"}` for an API query with further arguments for the query terms.

####output
A list of paths to the root node where all the script's outputs are stored.

####instructions
Although instructions can be put in the `notes` and `description` fields, an explicit `instructions` field is perhaps helpful, especially for packages.

##Scripts
The Scripts node includes information about external software and tools, as well as scripts authored by WE1S staff. The general architecture consists of branching structures for standard types of processes:

+ `Collecting`
+ `Preprocessing`
+ `Analysis`
+ `Visualization`

Each of these branches may have child branches for different tools. However, the standard paths will divide scripts by language (Python and R in the examples below). Hence a possible path would be `Scripts,Preprocessing,Python,stripTags`. If the record is for a tool or external program, the terminal node record will contain manifest information about the tool or program. If it is a WE1S script, the record will additionally contain the code of the script itself.

A typical script record will look like the following:

```javascript
{
  *"_id": "stripTags",
  *"path": ",Scripts,Preprocessing,Python,",
  *"authors": ["Scott Kleinman"],
  *"date": "2014-01-01",
  *"version": "1.0",
  *"description": "A script to strip tags",
  *"script": "def stripTags(str):\n etc. etc."
}
```

A typical tool record will look like this:

```javascript
{
  *"_id": "stripTags",
  *"reference": "http://mallet.cs.umass.edu/topics.php",
  *"authors": ["Andrew Kachites McCallum"],
  *"dateAccessed": "2015-01-01",
  *"version": "2.0.7",
  *"description": "LDA topic modeling tool",
}
```

In other words, scripts stored in the database will have paths, authors, dates of authorship, and the script code. External tools will have references and dates of access. A version number may not always be available, but a value like "unknown" can be used in such cases.