# This file parses the raw csv data into normalized form.

import NLPlib
import sys
import csv
import re
import HTMLParser

# WARNING: Change this before submitting.
INPUT_FILE = 'testdata.manual.2009.06.14.csv'
ABBR_FILE = 'abbrev.english'

with open(ABBR_FILE) as f:
    ABBREVIATIONS = map(lambda x: x.rstrip('\n'), f.readlines())

def strip_html(tweet): # Step 1 of part 1.
     """
     Return the input tweet with all html tags and attributes
     removed.

     input:
        tweet - a string representing a tweet.
     output:
        tweet - a string representing a tweet.
     """
     mo = re.search(r"<[^>]+>" , tweet)
     while mo:
         tweet = tweet[:mo.start()] + tweet[mo.end():]
	 mo = re.search(r"<[^>]+>" , tweet)
     return tweet

def html_char_to_ascii(tweet): # Step 2 of part 1.
     """
     Return the input tweet with all HTML character codes
     replaced with their corresponding ASCII characters.

     input:
        tweet - a string representing a tweet.
     ouput:
        tweet - a string representing a tweet.
     """
     h = HTMLParser.HTMLParser()
     return h.unescape(tweet)

def strip_urls(tweet): # Step 3 of part 1.
     """
     Return the input tweet with all URLs removed.
     A URL is any substring beginning with one of
     the following:
        - 'http://'
        - 'https://'
        - 'www.'

     input:
        tweet - a string representing a tweet.
     output:
        tweet - a string representing a tweet.
     """
     mo = re.search("([Hh]ttps?|www)[^\s]*\s+", tweet)
     while mo:
         tweet = tweet[:mo.start()] + tweet[mo.end():]
         mo = re.search("([Hh]ttps?|www)[^\s]*\s+", tweet)
     return tweet

def strip_twitter_chars(tweet): # Step 4 of part 1.
     """
     Return the input tweet with Twitter-specific characters removed.
     That is, username tags (@) and hash tags (#).

     input:
        tweet - a string representing a tweet.
     output:
        tweet - a string representing a tweet.
     """
     mo = re.search(r"[#@]" , tweet)
     while mo:
         tweet = tweet[:mo.start()] + tweet[mo.end():]
         mo = re.search(r"[#@]" , tweet)
     return tweet

def split_sentences(tweet): # Step 5 of part 1.
     """
     Return the input tweet with all distinct sentences separated by
     a newline character.

     input:
        tweet - a string representing a tweet.
     ouput:
        split_tweet - a string representing a tweet, where each
                      distinct sentence is on it's own line.
     """
     split_tweet = ''
     mo = re.search("[\.!?]+", tweet)
     i = 0
     while mo:
         n = len(tweet)
         if mo.end() < n and tweet[mo.end()] in ["'", '"']:
             split_tweet += tweet[i:mo.end() + 1] + '\n'
             i = 1
         elif tweet[mo.end() - 1] in ['!', '?']:
             split_tweet += tweet[i:mo.end()] + '\n'
             i = 0
         elif tweet[mo.end() - 1] == '.':
             if is_abbreviation(tweet, mo.end() - 1):
                 split_tweet += tweet[i:mo.end()+1]
             else:
                 split_tweet += tweet[i:mo.end()] + '\n'
             i = 0
         tweet = tweet[mo.end() + 1:]
         mo = re.search("[\.!?]+", tweet)
     return (split_tweet + tweet).rstrip('\n')

def is_abbreviation(tweet, i):
    """
    Return True iff the word terminated by the period at index i is
    an abbreviation.

    input:
        tweet - a string representing a tweet.
        i - the index of a period in tweet.
    output:
        True - the word terminated at index i is an abbreviation.
        False - otherwise.
    """
    word = ''
    while i >= 0:
        word += tweet[i]
        i -= 1
        if tweet[i] == ' ':
            break
    return word[::-1] in ABBREVIATIONS

# Note: Step 6 just says that ellipsis and repeated punctuation (eg !!!) do NOT get split.

def space_tokens(tweet): # Step 7 of part 1.
     """
     Return the input tweet with all distinct token separated by a space.

     input:
        tweet - a string representing a tweet.
     output:
        tweet - a string representing a tweet.
     """
     mo = re.search("[,:;]|[\.!?]+"  , tweet) # dog... asdf -> dog ... asdf
     split_tweet = ''
     while mo:
         split_tweet += tweet[:mo.start()] + ' ' + tweet[mo.start():mo.end()]
         tweet = tweet[mo.end():]
         mo = re.search("[,:;]|[\.!?]+"  , tweet)
     return space_clitics(split_tweet + tweet)

def space_clitics(tweet):
    """
    Return the input tweet with spaces between each clitic.

    input:
        tweet - a string where each word and punctuation mark
                are separated by a space.
    output:
        split_tweet - a string where each word, punctuation mark,
                      and clitic are separated by a space.
    """
    # First we match a quote followed by zero or more characters, then a space.
    mo = re.search("'[^\s]*\s", tweet) # Will detect any quote marks and go to the end of the word.
    split_tweet = ''
    while mo:
        # If the quote is not followed by an s, we split the quote. So dogs' -> dogs '
        if tweet[mo.start()+1] == 't': # we grab the char preceding the apostrophe.
            split_tweet += tweet[:mo.start()-1] + ' ' + tweet[mo.start()-1:mo.end()]
        else: # We split from apostrophe onward to end of word (this includes cases such as dogs' -> dogs ' )
            # before mo.start() is where we want to insert a space
            split_tweet += tweet[:mo.start()] + ' ' + tweet[mo.start():mo.end()]
        tweet = tweet[mo.end():]
        mo = re.search("'[^\s]*\s", tweet) # Will detect any quote marks and go to the end of the word.
    return split_tweet + tweet

     
def tag_tokens(tokens): # Step 8 of part 1.
    """
    Return a string where space-separated tokens are each tagged
    with their part-of-speech.

    input:
       tokens - a string of space-separated tokens.
    output:
       tagged - a string of space-separated tokens, each tagged
                with their part-of-speech.
    """
    pass

def add_demarcation(tweet, n): # Step 9 of part 1.
    """
    Return the input tweet prefixed with a demarcation (on a separate line)
    representing the numeric class of the tweet.

    input:
       tweet - a string representing a tweet.
       n     - the numeric class of tweet.
    output:
       labeled_tweet - the input tweet prefixed with it's
                       numeric class n demarcated on a separate line.
    """
    demarcation = '<A={}>\n'.format(n)
    return demarcation + tweet
      
def normalize_tweet(tweet):
    """
    Return the input tweet in normalized form. That is: 
        - all HTML tags and attributes are removed 
        - all HTML characters code are replaced with their ASCII equivalents
        - all URLs are removed
        - all Twitter user tags (@) and hash tags (#) are removed
        - each sentence within a tweet is on its own line
        - each token, including punctuation and cltiics, is separated by spaces
        - ellipsis and other kinds of multiple punctuation are not split
        - each token is tagged with its part-of-speech
        - each tweet is labeled with its class in a prefixing demarcation

    input:
        tweet - a string representing a tweet.
    output:
        normalized_tweet - the input tweet in normalized form.
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
    print ABBREVIATIONS
    
