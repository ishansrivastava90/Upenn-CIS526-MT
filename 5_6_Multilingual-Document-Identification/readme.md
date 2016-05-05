# Multilingual Document Identification

Task Description:
The objective of this task is, given a document containing text from 1-5 languages picked
from a set of 44 possible languages, to determine which language(s) are present and the 
proportion of the document written in each. 

## Code in this Directory

## default

Usage:  

		# for predicting dev data:
        ./default > predict.txt
        
        # for predicting test data:
        ./default -t 'data-test' > predict.txt	
        
Options:	

	-t 'testdata_directory' 	(Run predictions for documents in this directory)
	-n 3						(Choose length of n-grams)
	-k 500						(Choose size of language dictionaries)
			
This is the default model. It uses a 44-dimensional vector representation of each document where
the i-th element of the vector gives the proportion of the doc (in bytes) in the i-th language.
Languages are ordered alphabetically. The set of all possible languages is given in wiki-multi/selected_langs.

The model works like this:

1) For each of the 44 possible languages, create a byte n-gram dictionary from the monolingual training
files (ngram size can be specified by -n option and dictionaries can be pruned by -v option)

2) For each file in the training data, tokenize into byte n-grams. For each n-gram, perform a match
against each dictionary. For each language where there's a match, add 1 to the vector representation of
the document.

3) Normalize the vector by dividing each element by the total number of n-gram matches.

## baseline

Usage:  

		# for predicting dev data:
		./baseline > predict.txt 

		# for predicting test data:
		./baseline -t 'data-test' > predict.txt

Options:	

	-t 'testdata_directory' 	(Run predictions for documents in this directory)
	-n 3						(Choose length of n-grams)
	-b							(Flag to use byte n-grams instead of character n-grams)		
				
This is the shell of a baseline solution. Similarly to the default, it uses a 44-dimensional
vector representation of each document. 

The objective of the baseline system is to create a character n-gram dictionary for each
language, and to use this dictionary to determine the proportion of the document
written in each language. There are two places for student input:

1) Creating a character n-gram dictionary for each language
2) Generating the test document feature vectors by counting the n-grams that match each 
language dictionary. The student should implement a threshold to eliminate languages
with low scores. 

## grade-dev

Usage:  
		# for scoring training data:
		./default | ./grade-dev

Options:	

	-g 'goldfile'	(Use 'goldfile' as metadata. The 'goldfile' should match the directory that the predictions were run on.)

This module will score the output of default using the metadata file specified by the -g flag. By default
it uses the 'data-dev/hidden/dev-meta' solution file, since the default program predicts the documents 
in the 'data-dev' directory. 

The scoring function calculates the average cosine similarity of the predicted document vectors with the actual
document vectors calculated from the meta file.
