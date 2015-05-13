#Report on MongoDB

##Introduction

This document serves as something of a report on MongoDB, a thought experiment, and a proposal for modeling our data. 
It assumes that our requirements are:

1. A data storage system
2. A system for storing metadata that helps us keep track of the relationships between stored data and workflow (hereafter, the manifest system)
3. A web-based interface for creating, updating, and deleting information from the above systems.

Here are some further considerations. The data storage system should ideally be a database, rather than a file storage system so that we do not have to maintain a complex hierarchy of directory structures and file paths. If we need to maintain files in a physical location outside the database, we should point to a GitHub repository form a manifest. It is also ideal for each database record to function as a manifest In other words, each database record is a node in which either data or metadata, or both, can be embedded. Lastly, it would be best if the system were compatible with the YAML schema or its JSON subset in order to facilitate human readability, parsing, and interoperability with a variety of tools.

##Data Modelling with MongoDB
MongoDB is very well suited to these considerations. A MongoDB record is a single JSON object called a “collection”. Each collection consists of a set of keyword-value pairs called “documents”. These terms are confusing in the context of WE1S, so, in the discussion below, I will use the term “record” for MongoDB’s “collection”, and I will refer to keywords and their values, or sometimes “fields”, rather than “documents”. A MongoDB record looks like the following:

###Example 1:

```Javascript
{ "_id": "10-ways-to-explore-and-express-what-makes-your-community-unique",
  "description": "This field stands in for all the possible fields
                  typically found in a manifest.",
  "data": "Questions about issues in the news for students 13 and older.
          We’ve posted a fresh Student Opinion question nearly every weekday
          for the last five academic years..."
}
```

In the above example, the `_id` field’s value is derived from the file name of a *New York Times* article. The article itself (of which only the beginning is shown above) is the value of the data field. Hence there is no separate file storage. Data and metadata are treated exactly the same. Here is the same record displayed in the more readable YAML indented style (further examples below will be given in YAML format for easy reading):

###Example 2:

```YAML
Manifest:
  _id: 10-ways-to-explore-and-express-what-makes-your-community-unique
  description: This field stands in for all the possible fields typically 
               found in a manifest.
  data: | Questions about issues in the news for students 13 and older. We’ve 
          posted a fresh Student Opinion question nearly every weekday for 
          the last five academic years...
```

Data and metadata are treated exactly the same. To add a full manifest, you just keep adding appropriate fields from the WE1S manifest schema. There is no limit on the number of keywords you can add to a record. The data field can take a text string up to 16MB in size. That will be more than enough for most records in our collection. MongoDB has a system for chunking and storing larger files, and the same system is used for non-text files like images or PDFs.

MongoDB allows you to store data in this open-ended way without the impositions of a schema required for a relational database. MongoDB are very upfront about the advantages and disadvantages of this approach. Providing information embedded in a record can deliver performance improvements (unlikely to be a great benefit to us given the size of our data set). At the same time, this can cause the database to contain duplicate information, which can be a problem if it needs to be updated. Additionally, MongoDB does not do database joins, so complex queries may have to be partially implemented by the application’s code, rather than that of the database.

In practice, records can be modeled using a combination of denormalized data and references normalized data housed in separate records. For instance, a record of a collection may reference another record containing information about a publication from which the data was collected. If that information ever needs to change, it only needs to be changed in one place. The modeling challenge, then, is to decide what to information to normalize and what to embed.

MongoDB also seems to have an elegant solution to our need for manifest information to work seamlessly with a human-intuitive file storage system. A keyword can contain the string value of a path, which can then be matched by regex in a query. The path does not store the physical location of the item but instead provides a human-readable way of matching its container object, from which we can get the object’s `_id`, if necessary. This effectively allows us to implement a hierarchical tree structure similar to that normally used to store files. MongoDB provides several methods of doing this; the one I think best suited to our purposes is the tree structures with materialized paths. Here is the above record according to this system:
 

###Example 3:
```YAML
Manifest:
  _id: 10-ways-to-explore-and-express-what-makes-your-community-unique
  path: ,Corpus,NewYorkTimes,HumanitiesQuery,RawData,
  description: This field stands in for all the possible fields typically 
               found in a manifest.
  data: | Questions about issues in the news for students 13 and older. We’ve 
          posted a fresh Student Opinion question nearly every weekday for 
          the last five academic years...
```
		  
The path field contains a sequence of nodes indicating that this record belongs in the *New York Times* section of the entire Corpus, that it is a subset involving a Humanities query (the exact nature of which will be in the manifest information, and that this record belongs to the raw data from that subset. Commas are used instead of the traditional slashes for a file path because slashes are often used as delimiters in regex pattern matching and would therefore need to be escaped. With the above information, a query can be limited only to those objects matching this path value. Since it is a string, there are no formatting restrictions (other than the issue with slashes) as there would be for a file path.

##A WhatEvery1Says Data Model in MongoDB
With this in mind, the following tree structure represents the organization of nodes for the Corpus portion of the database:

###Figure 1:

![Figure 1](https://github.com/scottkleinman/WE1S/blob/master/figure1.JPG?raw=true "Figure 1")

Each node is a manifest giving parent/child relationships at a bare minimum. The Corpus is simply the root node of the tree structure containing (it has path: null) primary and secondary data. It does not contain any other information. Typically, a Publication record would consist only of an _id (from which the path is constructed), a path to the root, and a reference to another manifest containing information about the publication. Here is an example:

###Example 4:

```YAML
Manifest:
  _id: 10-ways-to-explore-and-express-what-makes-your-community-unique
  path: ,Corpus, 
  description: This contains collections from the New York Times 
  publication: ,Publications,NewYorkTimes,
```

The `publication` field can alternatively refer to the `_id` of a manifest, but a path works just as well. Since many collections will derive from the same publication, it is appropriate to represent information about the publication as normalized data in its own record.

A collection refers to a section or slice of the data present in the Corpus. Since information about how data was collected is particular to an individual collection, it makes sense to embed that information in the collection record itself. Hence there is no need in this system for separate Corpus and Collecting manifests. As the diagram shows, the path system allows multiple collections to be children of a single publication, but it also allows collections to be constructed on their own. These collections might derive from multiple publications, in which case the collection record would contain a publication link with the paths to the manifests of publications from which the data was derived and the processes by which this took place. Example 3 represents a record that might occupy one of the file nodes in the diagram. Collection nodes may be the products of individual API queries, for instance. Data resulting from two different queries should generate separate collection nodes.

Manifest information about Publications and Processes can be embedded in nodes on the Corpus path, but, in most cases, it will be best to normalize this data by placing it on a separate path and using that as a reference. Figure 2: represents a model Publications hierarchy.

###Figure 2:

![Figure 2](https://github.com/scottkleinman/WE1S/blob/master/figure2.JPG?raw=true "Figure 2")

This is a fairly simple structure. In most cases, there will only be a manifesto with metadata about the Publication. For the sake of illustration, a Related Files path is given for the storage of documentation related to the publication. However, this is probably an appropriate place to exploit MongoDB’s “embedded documents” feature and simply embed these files in the Publication record. Processes and Packages will also likely need only a single hierarchical level. If a Process relates only to a single Collection or Publication, it can be embedded in that record.

Hence it is likely that only Scripts will require a more elaborate tree structure, for which the following diagram provides a model.

###Figure 3:

![Figure 3](https://github.com/scottkleinman/WE1S/blob/master/figure3.JPG?raw=true "Figure 3")

The Analysis and Visualization nodes will have children like the Collecting and Preprocessing nodes. The Script nodes are individual script manifests in which the script file itself is embedded as a JSON object. I am assuming that encoding as JSON/BSON will not break the scripts.

##Further Comments about MongoDB
MongoDB does present some challenges. Most of the examples in the documentation are geared towards using the built-in Javascript shell, which quickly grows tiresome. Running MongoDB in an iPython notebook involves importing Pymongo. That itself is easy, but issuing database queries can be tricky at first. Many of the examples in the documentation don’t work properly if you cut and paste since Pymongo, unlike the MongoDB shell, seems to require strict JSON formatting (keywords must be in quotation marks). The documentation of these sorts of differences is not very good, and I had to do a lot of Googling to discover, for instance, that the Pymongo equivalent of null is “none”. 

But I did get there in the end, so, presumably, using Pymongo will get easier once you become familiar with the procedures and presumably define some functions to automate common procedures. As a test, I stuck my code in a function in Lexos, which runs of the Python Flask framework. It read my manifest data and piped it into the Lexos interface without a hitch. Since Django is very similar to Flask, I don’t anticipate any difficulties. Note that I am not talking about running a CMS off of MongoDB, just having the CMS query information from the MongoDB database for display.

I am primarily thinking of the proposed system as a means of keeping track of data and workflow for research purposes, not as a means of making data and provenance queryable by the public. In general, MongoDB is not the best system for complex data queries because it lacks the database joins of which most relational databases are capable. How much of a problem this would be depends on the data and the type of queries you expect to run. Aggregating data in the application’s code, rather than in the database query, can have an impact on performance, but in most cases it is possible to achieve the same result. There is a body of thought that a document storage system like MongoDB can be a stepping stone to eventually move the data into a relational database with a more rigid schema.

##Recording WhatEvery1Says Manifests in MongoDB

Since MongoDB is effectively schema-less, any manifest field can be inserted in any record. In practice, we have a need to restrict fields to certain types of records and to prompt WhatEvery1Says editors with what type of information is required or optional in a given record. Hence, although our database does not need a schema (other than the general model outlined above), our manifests do. Since YAML does not have a schema language, and MongoDB stores data as JSON objects, it makes sense to use JSON Schema.

An additional challenge is the creation of a web form that validates against this schema. I have found a number of tools that will do this and that also aid in the construction of the HTML form from the schema. These are:

+ [Jeremy Dorn's JSON Editor](http://jeremydorn.com/json-editor/)
+ [Alpaca](http://www.alpacajs.org/)
+ [Angular Schema Form](http://schemaform.io/)

As yet, I have been unable to evaluate the strengths and weaknesses of these tools.

It should be stated that MongoDB records can be created by scripts. An easy-to-implement system would be to create an `insert_record()` function and pass it an `_id value`. In the above examples, it would look like this:

```Javascript
insert_record("10-ways-to-explore-and-express-what-makes-your-community-unique")
```

Then another `upsert_field()` function would allow you to add keyword-value pairs to the existing record:

```Javascript
 upsert_record({"path": ",Corpus,NewYorkTimes,HumanitiesQuery,RawData,"})
```

The `upsert_record()` function could be repeated indefinitely to add new fields to the record’s manifest whenever needed. The information is not validated, and there is no prompt for what fields may be required or optional, but these functions would make constructing records with manifest information relatively painless.

If you've made it this far, check out the [draft schema documentation](https://github.com/scottkleinman/WE1S/blob/master/DraftSchema.md) next.