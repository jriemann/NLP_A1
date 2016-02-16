# ibmTrain.py
# 
# This file produces 11 classifiers using the NLClassifier IBM Service
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#

###IMPORTS###################################
#TODO: add necessary imports
from itertools import islice
import csv
import re
from twtt import partition_by_class, strip_html, html_char_to_ascii, strip_urls, strip_twitter_chars
import subprocess
import requests
import json

GROUP_ID = 90
CLASSES = [0, 4]
CLASS_INDICES = {0: 0, 4: 800000}

###HELPER FUNCTIONS##########################

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
	# Converts an existing training csv file. The output file should
	# contain only the 11,000 lines of your group's specific training set.
	#
	# Inputs:
	#	input_csv - a string containing the name of the original csv file
	#		ex. "my_file.csv"
	#
	#	output_csv - a string containing the name of the output csv file
	#		ex. "my_output_file.csv"
	#
	# Returns:
	#	None
	
	#TODO: Fill in this function
        # So need to open the file, read the right lines, and write only our lines out.
        # The lines we want are [90x5500, 90x5501, ... , 90x(5500 + 5499)]
        #                  and  [(800,00 + 90x5500), (800,000 + 90x5501), ... , (800000 + 90x(5500 + 5499))]
        #f_in = open(input_csv_name, 'r')
        #reader = list(csv.reader(f_in, delimiter=','))
        f_out = open(output_csv_name, 'r+')
        with open(input_csv_name, "r") as f_in:
            reader = list(csv.reader(f_in, delimiter=','))
            data = partition_by_class(reader, GROUP_ID, 11000)
            for line in data:
                f_out.write(process(line))
        f_out.close()
        # done
	return

def process(line):
    # Convert the given line into the corrent two field csv format.
    tweet_text = line[-1]
    tweet_class = line[0]
    formatted_tweet = strip_html(tweet_text)
    formatted_tweet = html_char_to_ascii(formatted_tweet)
    formatted_tweet = strip_urls(formatted_tweet)
    formatted_tweet = strip_twitter_chars(formatted_tweet)
    formatted_tweet = formatted_tweet.replace('"', ' ""')
    formatted_tweet = formatted_tweet.replace('\n', '')
    formatted_tweet = formatted_tweet.replace('\t', '')
    #if '"' in formatted_tweet:
    #    print(formatted_tweet)
    if "," in formatted_tweet:
        formatted_tweet = '" ' + formatted_tweet + ' "'
    formatted_line = formatted_tweet + ',' + tweet_class + '\n'
    if "Progress" in formatted_line:
        print(formatted_line)
    return formatted_line
	
def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
	# Extracts n_lines_to_extract lines from a given csv file and writes them to 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	#	input_csv - a string containing the name of the original csv file from which
	#		a subset of lines will be extracted
	#		ex. "my_file.csv"
	#	
	#	n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
	#		ex. 500
	#
	#	output_file_prefix - a prefix for the output csv file. If unspecified, output files 
	#		are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
	#		The csv must be in the "watson" 2-column format.
	#		
	# Returns:
	#	None
	
	#TODO: Fill in this function
        print(input_csv_file)
	f_out = open(output_file_prefix + str(n_lines_to_extract) + '.csv', 'w+')
        with open(input_csv_file, "r") as f_in:
            # We just want 0 - n_lines_to_extract, and then 5501 - n_lines_to_extract.
            for line in islice(f_in, 0, n_lines_to_extract, 1):
                f_out.write(line)
            for line in islice(f_in, 5501, 5501 + n_lines_to_extract, 1):
                f_out.write(line)
            
	return
	
def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
	# Creates a classifier using the NLClassifier service specified with username and password.
	# Training_data for the classifier provided using an existing csv file named
	# ibmTrain#.csv, where # is the input parameter n.
	#
	# Inputs:
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	n - identification number for the input_file, as an integer
	#		ex. 500
	#
	#	input_file_prefix - a prefix for the input csv file, as a string.
	#		If unspecified data will be collected from an existing csv file 
	#		named 'ibmTrain#.csv', where # is the input parameter n.
	#		The csv must be in the "watson" 2-column format.
	#
	# Returns:
	# 	A dictionary containing the response code of the classifier call, will all the fields 
	#	specified at
	#	http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
	#   
	#
	# Error Handling:
	#	This function should throw an exception if the create classifier call fails for any reason
	#	or if the input csv file does not exist or cannot be read.
	#
	
	#TODO: Fill in this function
        input_file = input_file_prefix + str(n) + '.csv'
        url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"

        try:
            f_open = open(input_file, 'rb')
        except IOError:
            print("Could not open input file. ")
            raise Exception

        files = {'training_data':f_open, 'training_metadata' : json.dumps({'language':'en', 'name':'Classifier ' + str(n)})}
        r = requests.post(url, auth=(username, password), files=files)

        if r.status_code != 200:
            print("Bad response.")
            raise Exception

	return {r.status_code:r.json}
	
if __name__ == "__main__":
	
	### STEP 1: Convert csv file into two-field watson format
	input_csv_name = '/u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv'
	
	#DO NOT CHANGE THE NAME OF THIS FILE
	output_csv_name = 'training_11000_watson_style.csv'
	
	#convert_training_csv_to_watson_csv_format(input_csv_name,GROUP_ID, output_csv_name)
	
	
	### STEP 2: Save 3 subsets in the new format into ibmTrain#.csv files
	
	#TODO: extract all 3 subsets and write the 3 new ibmTrain#.csv files
	#
	# you should make use of the following function call:
	#
	# n_lines_to_extract = 500
	# extract_subset_from_csv_file(input_csv,n_lines_to_extract)
        #print(output_csv_name)
        #for n in [500, 2500, 5000]:
        #    extract_subset_from_csv_file(output_csv_name, n)
	
	### STEP 3: Create the classifiers using Watson
	
	#TODO: Create all 3 classifiers using the csv files of the subsets produced in 
	# STEP 2
	# 
	#
	# you should make use of the following function call
	# n = 500
	# username = '<ADD USERNAME>'
	# password = '<ADD PASSWORD>'
	# create_classifier(username, password, n, input_file_prefix='ibmTrain')
        username = '2c838912-7ede-42ba-98f4-9f6d1e435429'
	password = "WhGGasijcgJu"
        for n in [500, 2500, 5000]:
	    create_classifier(username, password, n, input_file_prefix='ibmTrain')
	
	
	
