## Wikidata api fetching
A proof-of-concept script that generate a JSON file containing a list of notable people who studied at University of Strasbourg. 

## Implementation
The list isextracted from Wikidata API using a pre-built SPARQL query (`wikidata-query-rd` file) and the Wikidata API.

Once obtained, the alumni list is used in a second set operation: the collection of details about each former student from Wikipedia. This additional step is needed as I am not yet able to pull some details from Wikidata: excerpt of a student's biography, pictures available in their Wikipedia article, etc.

The output data is saved in `alumni.json`

# Requirements

* [Python 3.x+](https://www.python.org/downloads/)
* [PIP (Python Dependency Manager)](https://pip.pypa.io/en/stable/installing/)

## Installing dependencies
Install application dependencies using the `pip -r requirements.txt` command

## Running the scripts
Run the following command to make trigger script.
`python generate-alumni.py`

# Contributors 
 * Samuel Guebo ([@samuelguebo](https://twitter/com/samuelguebo))
