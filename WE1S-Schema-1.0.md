#WhatEvery1Says Schema
**v1.0**
_Last Update: November 17, 2016_

## Contents
* [Introduction](#introduction)
* [WE1S Manifests](#we1s-manifests)
* [Manifests Types, the WE1S Superstructure, and the MongoDB Data Model](#manifests-types-the-we1s-superstructure-and-the-mongodb-data-model)
* [Required Properties for All Manifests](#required-properties-for-all-manifests)
* [Global Properties](#global-properties)
* [_Ad Hoc_ Properties](#ad-hoc-properties)
* [Root-Level Manifests](#root-level-manifests)
* [Publications](#publications)
* [Corpus and Collection Nodes](#corpus-and-collection-nodes)
* [Data Nodes](#data-nodes)
* [RawData](#rawdata)
* [ProcessedData](#processeddata)
* [Metadata](#metadata)
* [Outputs](#outputs)
* [Related](#related)
* [Processes](#processes)
* [Step Manifests](#step-manifests)
* [Scripts](#scripts)
* [API](#api)


##Introduction
The WhatEvery1Says Schema (hereafter "WE1S Schema") is a set of recommendations for the construction of JSON-formatted manifest documents for the WE1S project. These JSON documents can be used as data storage and configuration files for a variety of scripted processes and tools that read the JSON format.

The schema is based on [JSON Schema](http://json-schema.org/), a vocabulary that allows you to annotate and validate JSON documents. The basis for JSON schema is as follows. Each JSON document contain a JSON object `{}` to which you can apply constraints by adding validation keywords to the schema. For instance, the `type` keyword can be used to restrict an instance to a string: `{ "type": "string" }`. In JSON schema parlance, `type` is referred to as a "keyword" or "property" and "string is its **value**. An excellent overview is provided in Michael Droettboom's [Understanding JSON Schema tutorial](https://spacetelescope.github.io/understanding-json-schema/). WE1S manifests follow the syntax of JSON Schema so that they always have a valid (i.e. predictable) format. This ensures maximum interoperability for a variety of uses.

A JSON document can have an unlimited number of key/value pairs, which are separated by commas:

```javascript
{ "keyword": "value",
  "keyword": "value"
}
```

These pairs are inherently unordered so, to give them sequence, they may be placed in a list, designated by square brackets:

```javascript
{[
  {"keyword": "value"},
  {"keyword": "value"}
]}
```

For multiple properties, it may be useful to construct a more elaborate structure employing a keyword for sequence:

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

This documentation provides project-specific recommendations for the how to encode types of information that requires sequence. 

##WE1S Manifests
A WE1S manifest is a JSON document that includes metadata describing a publication, process, set of data, or output of some procedure. Manifests can be used for a variety of purposes, but their primary intent is to help humans document and keep track of their workflow.

Manifests are designed to be read easily by humans but parsed just as easily by any programming language that can read JSON. Manifests may be standalone files ("JSON files"), or they may be stored in a database. They may also contain data themselves. In a database like MongoDB, data records have a JSON-like format so a record like `{"_id": "articleName", "content": "articleText"}` would contain the data within the manifest. A manifest can also serve as an empty node in a tree-like structure, used primarily to indicate a hierarchical relationship between two sub-brances. For instance, a manifest describing a collection of texts from the _New York Times_ might be used to indicate a common relationship of sub-collections of articles from different years. In a file storage system, a manifest file could be placed in each folder to describe the purpose and relationships of the files in that folder. In a database like MongoDB, and empty node of this sort documents a "materialized path" that organizes records in a human-intuitive way that mirrors a file storage system.

##Manifests Types, the WE1S Superstructure, and the MongoDB Data Model
Manifests can take a variety of forms, depending on their purpose. Broadly, manifests may describe publications, data, processes, or scripts. This generalization imposes a hierarchical "superstructure" on the WE1S project in which information is organized under one of these categories. Individual manifests are considered to be children of nodes corresponding to these four manifest types. Because the data type contains the project corpus of texts, it is known as the `Corpus` node. Thus four types of manifest are:

+ `Publications`: Information about the provenance of primary data.
+ `Corpus`: The data store for primary and generated data.
+ `Processes`: Metadata about workflow processes used to collect and generate data.
+ `Scripts`: The data store for scripts meta data about tools used to implement workflow processes.

Other record types may be possible at the root level, but they are not anticipated in v1.0 of the schema.

Manifests do not require a database storage system and can be used independently in flat file format. However, the WE1S project is building a workflow management system which stores manifests in a MongoDB database. The appeal of MongoDB, as has been stated above, is that it stores its records in a JSON-like format. This allows WE1S manifests to be imported and exported from the database easily.

WE1S uses MongoDB's ["materialized path"](https://docs.mongodb.com/v3.2/tutorial/model-tree-structures-with-materialized-paths/) data model to mirror the characteristics of the superstructure. Each manifest is given a `path` property that shows its relationship to one of the root nodes. For instance, a raw data file would have a `path` value like `Corpus/RawData/filename.txt`. The similarity to an actual file path is deliberate; it allows human readers to see directly from the manifest where the file lives within the project superstructure. **Important:** MongoDB searches `path` properties using regular expressions. Since the forward slash forms part of the regular expression syntax, it is standard practice to use commas. This is not required by the the WE1S manifest schema, but it is required for storage in a MongoDB database. Importing manifests to and exporting them from the database may therefore require a scripted replacement of slashes with commas, or vice versa.

Note also that in MongoDB each JSON object is called a "collection" and each keyword-value pair is called a "document". In order to avoid confusion with terminology employed to describe WE1S manifests, this document refers to MongoDB "collections" as a **records** and MongoDB "documents" as a **fields**.

##Required Properties for All Manifests
The WE1S schema defines what properties are required or optional in different types of manifests. In all the examples given in this documentation, properties required for a particular manifest type are preceded by an asterisk.

###_id
A string value to be used in the creation of `path` values. Ideally, the `_id` should be meaningful to a human rather than, say, an ID number. An `_id` value need not be unique, but it should be highly improbable to get the same `_id` value along the same path. The `_id` property with the underscore is required by MongoDB, so, for convenience, it is adopted in that form in the WE1S schema.

###namespace
This is a string formed from the WE1S namespace and version number (something like `WE1Sv1.0`). It should be auto-generated. Hence, for brevity, `namespace` fields are not shown in the examples below.

###path
The `path` property implements MongoDB's ["materialized path"](https://docs.mongodb.com/v3.2/tutorial/model-tree-structures-with-materialized-paths/) data model, which allows records to be related to each other within the WE1S superstructure. Path values are strings constructed by listing nodes in the tree structure delimited by slashes or commas (the latter are required for the manifest to be stored in MongoDB). Each node is represented by its `_id` value: e.g. `,Corpus,NewYorkTimes,2014,`. Some root nodes (like Corpus) have pre-defined values. The value of path within a manifest is typically relative to its parent node. Some other manifest properties require a path string as their value. In these cases, the path is a reference to another manifest.

##Global Properties
Global properties are properties that can occur in any type of manifest. For this reason, they are not listed amongst the options for specific manifest types unless they are required by that manifest type.

###title
This is an optional string value providing a "pretty" title for the manifest. Since `_id` values are used to construct paths, they may not take a form that can be used in this manner, and the `title` property fills this gap.See also the `label` field.

###label
A string value similar to the `title` field but intended for use in graph labels or other outputs where a shortened identifier may be useful.

###description
A text string that can contain an extended prose description of the manifest's content.

###notes
A list of text strings that can contain an extended prose commentary about the record’s content. Each item in the list is a separate `note`. Here are two examples, one containing a single note and one containing two notes:

```javascript
{"notes": ["This is some commentary about the record"]}

{"notes": [
  {"note": "This is the first note." },
  {"note": "This is the second note." }
]}
```

*Question: Should we require the keyword `note` or just allow a list of strings (which implies sequence)?* 

###group
In some cases, it may be necessary to designate group responsibility for authorship, processing steps, and the like. In these cases the keyword `group` can be used. For example:

```javascript
{"editors": [ {"group": "UCSB"} ]}
```

##_Ad Hoc_ Properties
WE1S manifests can contain any number of _ad hoc_ properties, as long as they are formatted in valid JSON format and do not have names that conflict with keywords in the WE1S namespace. For instance, an entire Jupyter notebook could be stored in a WE1S manifest simply by adding a `notebook` property and giving it the entire Jupyter notebook JSON object as its value. However, because such properties are not part of the WE1S schema, they will only be acessible to tools and scripts designed to exploit their presence in the manifest.

##Root-Level Manifests
The WE1S superstructure requires manifests at root level called `Publications`, `Corpus`, `Processes`, and `Scripts`. These designations are the `_id` values of the manifests (and are case sensitive). The `namespace` value for these manifests should be auto-generated, and their `path` values should be `null`. Other properties are optional for these nodes. Hence a `Publications` manifest has a form like this:

```javascript
{
  {*"_id": "Publications"},
  {*"namespace": "we1sv1.0"},
  {*"path": null},
  {"description": "The root node for Publications manifests."}
}
```

##Publications
Information about primary source material in the corpus is maintained along the path of the `Publications` node. Each separate publication is a separate `publication` record (with "publication" defined broadly). For instance, the example below represents the online publication of _The New York Times_.

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

`publication` manifests have the following properties:

####date (required)
A list containing a string value (e.g. `"date": ["2013"]`) or two objects containing `start` and `end` values, as shown in the example.

####language (optional)
A string value taken from the the [ISO 639-2 list](http://www.loc.gov/standards/iso639-2/php/code_list.php) language codes. If multiple languages are required, a list of string of strings can be supplied.

####country (optional)
A string value taken from the [ISO 3166-1 ALPHA-2](https://en.wikipedia.org/wiki/ISO_3166-1)] country codes.

####authors (optional)
A list value. Some publications (e.g. monographs) may have authors; otherwise, this information is best supplied in the records of individual newspaper articles and the like.

##Corpus and Collection Nodes
The `Corpus` node serves as a data store for all primary and generated data housed by the WE1S project. It is composed of `collection` manifests which represent a variety of types of data sets. These may be subsets or suprasets of publications; they may be data and metadata records generated by WE1S staff; or they may be related files stored for reference. The following example represents a collection derived from a publication.

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

`collection` manifests have the following properties:

####collectors (required)
A list containing the names of the WE1S staff who collected the data or creted the collection. Currently, the schema does not specify a format for names.

####date (required)
A list containing a string value (e.g. `"date": ["2013"]`) or two objects containing `start` and `end` values, as shown in the example. The date here refers to the dates on which the data was collected by WE1S staff.

*Question: Fields which take multiple values in lists are here representing as requiring a list, rather than a string, even if there is only a single value. Is there any reason not to do this?*

####workstation (optional)
A string value providing information about the environment in which the data was collected.

####queryTerms (optional)
A list providing keywords used to define the scope of the collection. The value can be used to query the `Corpus` for data matching a particular description.

####processes (optional)
A list containing embedded processes or paths to separate process manifests. Both types follow the same schema, described under [`Processes`](#processes).

Note that there is no need to reference outputs of the collection since they will be found along a standard path within the collection, described below.

Here is an example of a `collection` manifest which combines materials from two publications:

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
Collection data is stored along different branches of the `collection` node, depending on the type of data. The WE1S schema requires the use of standard node `_id` values for each of the data types:

+ `RawData`: Primary source data.
+ `ProcessedData`: Source data transformed by WE1S staff in preparation for analysis.
+ `Metadata`: Metadata records accompanying the primary source data.
+ `Outputs`: Data and metadata records generated by WE1S analytic processes.
+ `Related`: Records associated with the collection, such as documentation, often kept for reference.

The name given for each of the above node types is also the `_id` for its manifest. Its `namespace` should be auto-generated, and its `path` should be `,Corpus,collection_id,`. Other fields are optional.

Each type of data is described in detail below.

##RawData
RawData manifests are path nodes for documents containing the primary data collected by WE1S staff. They should have the `path` value `,Corpus,collection_id,RawData,`. Along this path will be found individual data documents. A RawData record may have some additional metadata shown in the schema below:

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

`RawData` manifests have the following optional properties. The values of `relationships`, `OCR`, and `rights` are inherited by all data along the path `,Corpus,New_York_Times,RawData,`.

####Relationships
A list of strings or objects. The schema above uses the `relationships` property to describe the data as being a part of another collection ("CollectionA") combined with material from a third collection ("CollectionB"). Terms from Dublin Core are used in the example above, but it is possible to use other terms from any controlled vocabulary.

####OCR (optional)
A boolean to indicate whether the data has been digitized using Optical Character Recognition. If omitted, the default value is `false`.

####rights (optional)
A text string statement of licensing rights or intellectual property restrictions. `Free culture` is assumed by default.

##Data Documents
Data documents along a Data node path contain the binary or plain text content of the data. They have the following schema (this example below assumes the `RawData` path).

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

**Note:** Since records of this type will typically consist of or be derived from files, it makes sense to use the file name (minus the file extension) as the `_id`.

Data manifests have the following optional properties.

####authors (optional)
A list of names. For items like newspaper articles, the author(s) can be supplied for each article.

####mimetype (optional)
The `mimeType` property indicates the original file format. A list of common media formats can be found at [http://en.wikipedia.org/wiki/Internet_media_type#List_of_common_media_types](http://en.wikipedia.org/wiki/Internet_media_type#List_of_common_media_types).

####documentType (optional)
A string value. `documentType` is added (tentatively) to the schema in case the content of individual documents (as opposed to publications or collections) needs a controlled vocabulary.

##ProcessedData
ProcessedData manifests are path nodes for documents containing data transformed by WE1S non-analytic processes (e.g. text scrubbing). They should have the path value `,Corpus,collection_id,ProcessedData,`. Along this path will be found individual data documents. A `ProcessedData` node may have some additional metadata shown in the schema below:

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
In the above example each step in the processing refers to a separate record describing the processes applied to the data in the `RawData` path. In place of the `reference` field, it is also possible to embed the description of the process directly in the `ProcessedData` record. This is most appropriate for simple processes that are applied only to the specific data in the collection. See [Processes](#processes) for a description of the properties.

##Metadata
Metadata manifests are path nodes for documents containing metadata that may have been acquired along with the raw data. They should have the `path` value `,Corpus,collection_id,Metadata,`. Along this path will be found individual metadata documents. A `Metadata` node will have a schema like the one below:

```javascript
{
  *"_id": "Metadata",
  *"path": ",Corpus,New_York_Times,"
}
```

Metadata nodes and/or records are similar to raw data records in allowing an optional `mimeType` field.

##Outputs
`Outputs` records are path nodes for data and metadata generated through WE1S analytic processes. They should have the `path` value `,Corpus,collection_id,Outputs,`. Along this path may be found a variety of ad hoc child nodes (`data`, `metadata`, `visualizations`, `documentation`, and so on), which are not standardized in the WE1S schema:

```javascript
{
  *"_id": "Outputs",
  *"path": ",Corpus,New_York_Times,"
}
```

Outputs nodes and/or records are similar to `RawData` manifests in allowing an optional `mimeType` field.

##Related
`Related` manifests are path nodes for documents (typically files) such as documentation which are archived for reference.

```javascript
{
  *"_id": "Related",
  *"path": ",Corpus,New_York_Times,"
}
```

`Related` nodes and/or manifests are similar to `RawData` manifests in allowing a `mimeType` field.

##Processes
`Process` records are path nodes for documents (typically files) such as documentation which are archived for reference.

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

In the example above, the `description` field for each step stands in for the entire step schema, which is described under `Step Manifests` below.

`Processes` manifests have the following properties.

####editors (required)
A list of WE1S staff members who were responsible for implementing the processes.

####steps (required)
A list of JSON objects providing each step in the process. See `Step Manifests`. Since processing steps are sequential, they need to be given an sequencing number using the `seq` keyword, as in the example above. Alternatively, a step may provide a `reference` to a "package" (that is, a re-usable process that is not specific to a single data set).

####date (required)
A list containing a string value (e.g. `"date": ["2013"]`) or two objects containing `start` and `end` values, as shown in the example. The date here refers to the dates on which the process was implemented by WE1S staff.

####source (optional)
If the process is not embedded in the collection record, this property contains the record `_id` or `path` to the input data. The `path` property is better since it will contain the collection. Otherwise, the collection should be mentioned in the description or an optional `collection` keyword can be added to reference it.

*Question: Given multiple ways to handle this, which is the best?*

##Step Manifests
Step manifests describe the workflow parameters of a single step in a process. They may be embedded within or referenced from a process record.

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

In the above example, `_id` and `_path` would be required if the record were an independent node. They would not be required if the step is embedded in a process record.

`step` manifests have the following properties:

####reference (optional)
A string containing a reference to the tool or script. If it is a tool, this can be a URL to the tool's website. If the step involves a script, the reference should be a path to the script's record, which will contain the script's version number. The `reference` field can also be used to identify a path to a package (independent reusable process) that is a step in the process.

####label (optional)
A string containing a keyword for the name of the tool or script (useful for external resources).

####version (optional)
A string containing a keyword for the version of the tool or script. This is useful for external resources. WE1S scripts will have the version number embedded in their own manifests.

####options (optional)
A list containing information about the configuration of the tool or script used in the step. The option name should be given as the "argument" and the "value" should be the option setting. This structure is ideally suited for command-line tools, but the JSON object can contain fields like `{"settings.cfg": "Sample config file:..."}` to record a sample configuration file. Likewise, you might have `{"api": "http://api.nytimes.com/svc/search/v2/articlesearch"}` for an API query with further arguments for the query terms.

####output (optional)
A list of paths to the root node where all the script's outputs are stored.

####instructions (optional)
A string containing instructions for implementing the process. Although instructions can be put in the `notes` and `description` fields, an explicit `instructions` field is perhaps helpful, especially for packages.

##Scripts
The `Scripts` node includes information about external software and tools, as well as scripts authored by WE1S staff. The general architecture consists of branching structures for standard types of processes:

+ `Collecting`
+ `Preprocessing`
+ `Analysis`
+ `Visualization`

Each of these branches may have child branches for different tools. However, the standard paths will divide scripts by language (Python and R in the examples below). Hence a possible path would be `Scripts,Preprocessing,Python,stripTags`. If the record is for a tool or external program, the terminal node record will contain manifest information about the tool or program. If it is a WE1S script, the manifest may additionally contain the code of the script itself.

A typical script manifest will look like the following:

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

A typical tool manifest will look like this:

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

##API

The following is an incomplete alphabetical listing of the WE1S schema. It is a work in progress, but it may be useful for easy reference.

###`_id`
**Description:** The identifier of the manifest.
**Type**: String
**Scope:** Global (required)
**Example:**
```json
{
    "_id": "new_york_times"
}
```
**Comments:**
* `_id` values should be human readable wherever possible.
* Although it is often desirable to have unique `_id` values, this is not required since the `_id` value is appended to the manifest's `path`. This allows for multiple manifests with the same `_id` to exist along different paths.
**Related:**
`path`

###`altTitle`
**Description:** Used when the publication is commonly known by a title other than the one given as the value of the `publication` property.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "altTitle": "The Times"
}
```
**Comments:**
**Related:**
`title`, `label`

###`author`
**Description:** An individual author of a publication.
**Type**: Object
**Scope:** `authors`
**Example:**
```json
{
    "authors": [
        "author": {
            "firstName": "Jane",
            "lastName": "Doe"
        }
    ]
}
```
**Comments:**
* The `author` object contains a group of key-value pairs representing individual parts of a name for use in more precise queries. At present, the schema does not supply a controlled vocabulary to be used as keys.
**Related:**
`authors`, `group`

###`authors`
**Description:** A list of authors of a publication.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "authors": ["Jane Doe", "John Smith"]
}

{
    "authors": [
        "author": {
            "firstName": "Jane",
            "lastName": "Doe"
        }
    ]
}
```
**Comments:**
* The list can consists of string values or objects containing the `author` or `group` properties.
* In general, string values should be standard full representations of the name. It is expected that this information will be queried by regex. If more specific information is required for querying parts of names, an `author` object can be added.
**Related:**
`author`, `group`

###`Collection`
**Description:** A top-level node manifest describing a single collection.
**Type**: Object
**Scope:** n/a
**Parameters:**
| Name           | Type          | Optional |
|----------------|---------------|----------|
| `_id`          | String        | No       |
| `collectors`   | Array         | No       |
| `date`         | Array         | No       |
| `description`  | String        | No       |
| `namespace`    | String        | No       |
| `path`         | String        | No       |
| `publications` | Array         | No       |
| `notes`        | Array         | Yes      |
| `processes`    | Array         | Yes      |
| `queryTerms`   | Array         | Yes      |
| `workstation`  | String        | Yes      |

**Example:**
```json
{
   "_id": "new_york_times",
   "title": "New York Times 2013 humanities query",
   "label": "NYT_hum_2013",
   "publications": [",Publications,new_york_times,"],
   "path": ",Corpus,new_york_times",
   "description": "Some content from the New York Times in 2013",
   "collectors": ["John Smith"],
   "date": [{"start": "2013-01-01"}, {"end": "2013-12-31"}],
   "workstation": "Windows 8.1", 
   "queryTerms": ["humanities"],
   "processes": [",Processes,remove_stopwords.py"],
   "notes": ["This was the first Collection created."]
}
```
**Comments:**
**Related:**

###`collector`
**Description:** An individual collector responsible for assembling a `Collection`.
**Type**: Object
**Scope:** `collectors`
**Example:**
```json
{
    "collectors": [
        "collector": {
            "firstName": "Jane",
            "lastName": "Doe"
        }
    ]
}
```
**Comments:**
* The `collector` object contains a group of key-value pairs representing individual parts of a name for use in more precise queries. At present, the schema does not supply a controlled vocabulary to be used as keys.
**Related:**
`collectors`, `group`

###`collectors`
**Description:** A list of collectors responsible for assembling the `Collection`.
**Type**: String
**Scope:** `Collection`
**Example:**
```json
{
    "collectors": ["Jane Doe", "John Smith"]
}

{
    "collectors": [
        "collector": {
            "firstName": "Jane",
            "lastName": "Doe"
        }
    ]
}
```
**Comments:**
* The list can consists of string values or objects containing the `collector` or `group` properties.
* In general, string values should be standard full representations of the name. It is expected that this information will be queried by regex. If more specific information is required for querying parts of names, an `collector` object can be added.
**Related:**
`collector`, `group`

###`contentType`
**Description:** A tag representing the nature or genre of the data.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "contentType": "newspaper"
}
```
**Comments:**
* There is currently no controlled vocabulary for `contentType` values.
**Related:**
`Publications`

###`country`
**Description:** A string value taken from the [ISO 3166-1 ALPHA-2](https://en.wikipedia.org/wiki/ISO_3166-1) country codes.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "country": "usa"
}
```
**Comments:**
**Related:**
`Publications`

###`date`
**Description:** A list of date strings or objects.
**Type**: List
**Scope:** Global
**Example:**
```json
{
    "date": ["2013"]
}

{
    "date": [{"startDate": "2014-01-01", "endDate": "2014-12-31"}]
}
```
**Comments:**
* Dates should be given in `DATETIME` format `YYYY-MM-DD` wherever this information is known.
* Multiple dates can be listed as the value of `date`.
* Date ranges can be given as the value of `date` by supplying an object with `startDate` and `endDate` properties.
**Related:**
`endDate`, `startDate`

###`description`
**Description:** A prose description of the manifest's content or purpose.
**Type**: String
**Scope:** Global, `Publications` (required)
**Example:**
```json
{
    "description": "An extract of five years of New York Times data."
}
```
**Comments:**
* The description property is generally optional but is required for `Publications` manifests.
**Related:**
`Publications`

###`edition`
**Description:** The edition number of a publication.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "edition": "1st"
}
```
**Comments:**
* There is currently no controlled vocabulary for `edition` values.
**Related:**
`Publications`

###`endDate`
**Description:** The end date of a date range.
**Type**: String
**Scope:** date
**Example:**
```json
{
    "date": [{"startDate": "2014-01-01", "endDate": "2014-12-31"}]
}
```
**Comments:**
* Dates should be given in `DATETIME` format `YYYY-MM-DD` wherever this information is known.
* An `endDate` must have an accompanying `startDate`.
**Related:**
`date`, `startDate`

###`group`
**Description:** An object that may replace `author` or `collector` values to indicate group responsibility.
**Type**: Object
**Scope:** `authors`, `collectors`
**Example:**
```json
{
    "collector": [{"group": "UCSB"}]
}
```
**Comments:**
**Related:**
`author`, `authors`, `collector`, `collectors`

###`label`
**Description:** A short title for that may be used as a label in graphs and charts.
**Type**: String
**Scope:** Global
**Example:**
```json
{
    "label": "NYT"
}
```
**Comments:**
**Related:**
`altTitle`, `title`

###`language`
**Description:** A string value taken from the the [ISO 639-2](http://www.loc.gov/standards/iso639-2/php/code_list.php) list language codes. If multiple languages are required, an array of strings can be supplied.
**Type**: String, Array
**Scope:** `Publications`
**Example:**
```json
{
    "language": "en"
}

{
    "language": ["en", "fr"]
}
```
**Comments:**
**Related:**
`Publications`

###`namespace`
**Description:** An identifier for the project schema and schema version number.
**Type**: String
**Scope:** Global (required)
**Example:**
```json
{
    "namespace": "WE1Sv1.0"
}
```
**Comments:**
* Currently, the default value is **WE1Sv1.0**.
**Related:**

###`note`
**Description:** An individual note supplied by the creator or editor of the manifest.
**Type**: Object
**Scope:** `notes`
**Example:**
```json
{
    "notes": [
        {"note": "This data should be double checked."}
    ]
}
```
**Comments:**
**Related:**
`description`, `notes`

###`notes`
**Description:** A list of notes supplied by the creator or editor of the manifest.
**Type**: String, Object
**Scope:** Global
**Example:**
```json
{
    "notes": [
        "This data should be double checked."
    ]
}

{
    "notes": [
        {"note": "This data should be double checked."}
    ]
}
```
**Comments:**
* Multiple notes can be supplied as a list of strings or a list of `note` objects.
**Related:**
`description`, `note`

###`path`
**Description:** The unique identifier of the manifest.
**Type**: String
**Scope:** Global (required)
**Example:**
```json
{
    "path": ",Publications,new_york_times,"
}
```
**Comments:**
* The `path` value is effectively a human readable unique identifier of the manifest. It is formatted like a file path with the manifest's `_id` value as the terminal node.
* The typical `/` delimiter of a file path is by default replaced with a comma to enable regex searching in MongoDB since `/` is part of the regex syntax.
**Related:**
`_id`

###`processes`
**Description:** List of processes applied to the data documented in the manifest. Must be a valid path to a `Processes` manifest.
**Type**: Array
**Scope:** `Collection`, `Processes`
**Example:**
```json
{
    "process": [",Processes,remove_stopwords.py,"]
}
```
**Comments:**
**Related:**
`Collection`, `Processes`

###`publication`
**Description:** The full title of a publication.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "publication": "The New York Times"
}
```
**Comments:**
**Related:**
`altTitle`, `label`, `Publications`

###`publications`
**Description:** A list of publications used to create a `Collection`. The publications must be valid paths to `Publications` manifests.
**Type**: String
**Scope:** `Collection`
**Example:**
```json
{
    "publications": [",Publications,new_york_times,"]
}
```
**Comments:**
**Related:**
`Collection`, `path`, `Publications`

###`Publications`
**Description:** A top-level node manifest describing a single publication.
**Type**: Object
**Scope:** n/a
**Parameters:**
| Name          | Type          | Optional |
|---------------|---------------|----------|
| `_id`         | String        | No       |
| `date`        | Array         | No       |
| `description` | String        | No       |
| `namespace`   | String        | No       |
| `path`        | String        | No       |
| `publication` | String        | No       |
| `publisher`   | String        | No       |
| `authors`     | Array         | Yes      |
| `altTitle`    | String        | Yes      |
| `contentType` | String        | Yes      |
| `country`     | String        | Yes      |
| `edition`     | String        | Yes      |
| `language`    | String, Array | Yes      |
| `notes`       | Array         | Yes      |

**Example:**
```json
{
   "_id": "new_york_times",
   "namespace": "WE1Sv.10",
   "title": "The New York Times",
   "publication": "The New York Times",
   "label": "NYT",
   "path": ",Publications,",
   "description": "All the news that’s fit to download",
   "publisher": "The New York Times",
   "date": [{"start": "2013-01-01"}, {"end": "2013-01-01"}],
   "edition": "online", 
   "altTitle": "New York Times",
   "contentType": "newspaper",
   "language": "en",
   "country": "USA",
   "authors": ["John Smith"],
   "notes": ["This was the first publication collected."]
}
```
**Comments:**
**Related:**

###`publisher`
**Description:** The full title of a publication.
**Type**: String
**Scope:** `Publications`
**Example:**
```json
{
    "publisher": "Conde Nast"
}
```
**Comments:**
**Related:**
`Publications`

###`queryTerms`
**Description:** List of processes applied to the data documented in the manifest. Must be a valid path to a `Processes` manifest.
**Type**: Array
**Scope:** `Collection`, `Processes`
**Example:**
```json
{
    "queryTerms": ["humanities", "liberal arts"]
}
```
**Comments:**
**Related:**
`Collection`, `Processes`

###`startDate`
**Description:** The start date of a date range.
**Type**: String
**Scope:** date
**Example:**
```json
{
    "date": [{"startDate": "2014-01-01", "endDate": "2014-12-31"}]
}
```
**Comments:**
* Dates should be given in `DATETIME` format `YYYY-MM-DD` wherever this information is known.
* A `startDate` is not required to have an accompanying `endDate`.
**Related:**
`date`, `endDate`

###`title`
**Description:** The formal or natural language title of the manifest.
**Type**: String
**Scope:** Global
**Example:**
```json
{
    "title": "The New York Times"
}
```
**Comments:**
**Related:**
`altTitle`, `label`

###`workstation`
**Description:** A description of the type of workstation used to collect the data documented in the manifest.
**Type**: String
**Scope:** `Collection`
**Example:**
```json
{
    "workstation": "Windows 10"
}
```
**Comments:**
* The `workstation` property does not currently possess a controlled vocabulary.
**Related:**
`Collection`
