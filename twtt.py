# This file parses the raw csv data into normalized form.

import NLPlib
import sys
import csv
# WARNING: Change this before submitting.
INPUT_FILE = 'testdata.manual.2009.06.14.csv'

def strip_html(tweet): # Step 1 of part 1.
     """ Remove all html tags and attributes.
     """
     pass

def html_char_to_ascii(tweet): # Step 2 of part 1.
     """
     """
     pass


def strip_urls(tweet): # Step 3 of part 1.
     """
     """
     pass

def strip_twitter_chars(tweet): # Step 4 of part 1.
     """ Remove the @ and # chars.
     """
     pass

def split_sentences(tweet): # Step 5 of part 1.
     """
     """
     pass

# Note: Step 6 just says that ellipsis and repeated punctuation (eg !!!) do NOT get split.


def space_tokens(tweet): # Step 7 of part 1.
     """
     """
     pass

def tag_tokens(tokens): # Step 8 of part 1.
    """ Use the module provided (NLPlib).
    """
    pass

def add_demarcation(tweet): # Step 9 of part 1.
    """
    """
    pass

def normalize_tweet(tweet):
    """ Apply all the steps (1-9) and return the formatted string.
    """
    tweet_class = tweet[0]
    tweet_text = tweet[-1]
    
    tweet_text = strip_html(tweet_text)
    # Apply all other filters here.


    return tweet_text + '\n'


def main(tweets, output_file):
    for tweet in tweets: # A tweet is a list of length 6, containing the various fields.
        normalized_tweet = normalize_tweet(tweet)
        # Write out the file
        output_file.write(normalized_tweet)


if __name__ == "__main__":
    args = sys.argv
    input_file_name = args[1]
    group_id = int(args[2])
    output_file_name = args[3] 
    open_input_file = open(input_file_name, 'r')
    open_output_file = open(output_file_name, 'w+')
    reader = csv.reader(open_input_file, delimiter=',')

    main(reader, open_output_file)
    print("Done")
    
