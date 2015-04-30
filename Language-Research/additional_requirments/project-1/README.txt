bhojpuri_data.json :
The JSON file has three fields 
* doc_id : Document Id
* url : Url of the webpage
* content : Bhojpuri  Content of the webpage (in unicode)

crawler.py :
Crawls the websites and downloads the webpages

extract_bhojpuri.py :
Extracts bhojpuri data based on unicode ranges. It also creates a list of all unique words in the data. 
