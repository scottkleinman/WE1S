#The WhatEvery1Says (WE1S) Research Ecosystem

##The WE1S Workspace
The [WE1S Workspace](https://github.com/jeremydouglass/WE1S-virtual-workspace) is a virtual server with Python and R installed, along with addition tools used by WE1S project. Many analysis procedures are performed in the workspace by calling scripts from [Jupyter Notebooks](http://jupyter.org/). The WE1S Workspace can be downloaded and installed from a [Docker](https://www.docker.com/) container archived in the [WE1S Docker containers repository](https://github.com/jeremydouglass/WE1S-containers).

##The WE1S Manifest System
WE1S manifests are files containing sets of key-value pairs containing metadata and data related to the project. Manifests are used to document information about the provenance of data, the processes applied to it, or the results of analysis, as well as to store data. A minimal example of a manifest is given below:

```yaml
id: 0
author: John Smith
```

This simple manifest is in the highly readable [YAML](https://en.wikipedia.org/wiki/YAML) serialiation format. More typically, manifests are maintained in the compatible [JSON](https://en.wikipedia.org/wiki/JSON) format (a subset of YAML) as in the example below:

```json
{
	"id": 0,
	"author": "John Smith"
}
```

Manifests can be created and edited in any text editor. Plain text data can be stored in a manifest as the value of the `content` property:

```JSON
{
	"id": 0,
	"content": "When in the course of human events..."
}
```

This means that a manifest can serve as a self-documenting data file. Binary data like image or PDF files can also be stored in manifests, although the result is not as human-readable and requires additional resources to create and process. However, it is also possible to have a manifest containing metadata about the data and a property listing the location of a separate binary file.

Manifests may have any number of keyword properties. However, the WE1S project employs a schema recommending required and optional properties based on its model of the research project. This schema specifies not only what properties belong in WE1S manifests but how different types of manifests relate to each other. The [WE1S Schema](https://github.com/scottkleinman/WE1S/blob/master/WE1S-Schema-1.0.md) is defined in the [JSON schema](http://json-schema.org/) format and may be easily customized for adoption in other types of projects. Users familiar with the schema may author manifests by hand; others may need helper tools such as the Workflow Management System discussed below. Manifests created by any means can be validated against the WE1S Schema to ensure that they are error free. 

The content of a manifest may be accessed by scripts such as those used in the WE1S Workspace. For instance, a user performing a Jupyter Notebook procedure in in the workspace may provide the script with a process manifest, which would act like a configuration file for the script, pointing to the locations of data files and other information used by the script. Similarly, a script could programmatically create a WE1S manifest as part of its output, thus documenting what was done to produce the results. WE1S manifests could also be used by compatible tools. For instance, the [Lexos](http://lexos.wheatoncollege.edu/) text analysis software could save a users current session properties and data as a set of manifests and allow the information to be used by other scripts and tools, or reloaded to Lexos at a later date. We anticipate the manifests will primarily be used for scripting in the earliest stages, but more tools will be developed to make use of WE1S manifests once the are commonly adopted. Until then, Lexos will be used as a proof of concept.

## The Workflow Management System (WMS)
WE1S implements an optional [Workflow Management System (WMS)](https://github.com/scottkleinman/WE1S/tree/master/we1s-web) which overlays a web-based tool for editing and creating manifests, as well as a [MongoDB](https://www.mongodb.com/)-based manifest storage system. The web-based tool provides user-friendly form fields for entering information that follows the WE1S schema, ensuring that manifests are valid. The WMS uses the [Alpaca Forms](http://www.alpacajs.org/) Javascript library to generate the forms directly from the WE1S Schema. MongoDB, a NoSQL database, stores records in a JSON-like format (including a native binary format called [BSON](http://bsonspec.org/)), making each record effectively a manifest document. This architecture allows for easy customization for other research projects. A change to the single JSON schema document has cascading effects on the web forms and database, automatically updating them for the needs of the project. The WMS, as a form of content management system, allows users to create, edit, delete, and search records in the database.

## The WE1S Public Platform
WE1S manifests allow users to specify what content is open access and what content is restricted. Furthermore, since manifests in the WMS database can be queried, the WMS will form the basis for an eventual public platform for querying the data and analyses produced by the WE1S project. The platform might also run with an installation of the WE1S Workspace to allow users to run a limited number of processes similar to those performed by the WE1S team.