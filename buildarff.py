import sys
import re

CLASSES = ['0', '4']
WORDLISTS_DIR = '/u/cs401/Wordlists'

def load_tweets(input_file_name, max_per_class):
    '''
    Return a list of at most max_per_class normalized tweets
    for every class in CLASSES, all of which are stored in
    the file named input_file_name.
    If max_per_class is -1, return all tweets for each class in CLASSES.
    '''
    if max_per_class == -1:
        data = load_all_tweets(input_file_name)

    return data

def load_all_tweets(input_file_name):
    '''
    Return every normalized tweet stored in the file
    input_file_name in a list.
    '''
    data = []
    f = open(input_file_name, 'r')
    lines = f.readlines()
    curr = lines[0]
    for line in lines[1:]:
        if is_demarcation(line.rstrip('\n')):
            data += [curr]
            curr = line
        else:
            curr += line
    data += [curr]
    return data

def count_sentences(tweet):
    '''
    Return the number of sentences in tweet.
    '''
    return len(tweet.split('\n')) - 2

def avg_token_length(tweet):
    '''
    Return the average length of tokens in tweet,
    measured by number of characters.
    '''
    pass
    
def avg_sentence_length(tweet):
    '''
    Return the average length of sentences in tweet,
    measured by number of tokens 
    '''
    pass

def tag_counts(tweet):
    '''
    Return a dictionary of token tags to the number of their 
    occurences in tweet.
    '''
    pass

def count_pronouns(tweet):
    '''
    Return the number of occurences in tweet of first, second,
    and third person pronouns.
    '''
    pass

def count_conjunctions(tweet):
    '''
    Return the number of occurences in tweet of the following: 
     'and', 'but', 'for', 'nor', 'or', 'so', 'yet'
    '''
    pass

def count_verbs(tweet):
    '''
    Return the number of occurences in tweet of past and
    future tense verbs in tweet. 
    '''
    pass

def count_nouns(tweet):
    '''
    Return the number of occurences in tweet of common nouns
    and proper nouns.
    '''
    pass

def count_adverbs(tweet):
    '''
    Return the number of occurences in tweet of adverbs.
    '''
    pass

def count_wh_words(tweet):
    '''
    Return the number of occurences in tweet of wh-words,
    i.e. words tagged with WDT / WP / WP$ / WRB.
    '''
    pass

def count_slang(tweet):
    '''
    Return the number of occurences in tweet of slang words.
    '''
    pass

def count_uppercase(tweet): 
    '''
    Return the number of occurences of uppercase words of
    length greater than or equal to 2.
    '''
    pass

def count_punctuation(tweet):
    '''
    Return the number of occurences of the following
    characters:
        ,    (commas)
        :    (colons)
        ;    (semi-colons)
        -    (dashes)
        (    (right parenthesis)
        )    (left parenthesis)
        ...  (ellipses)
    '''
    pass

def is_demarcation(s):
    '''
    Return True iff s is a tweet demarcation of the form
    <A=#>, where # is the class of that tweet.
    '''
    c = ''.join(CLASSES)
    return True if re.match('<A=[{}]>'.format(c), s) else False

if __name__ == "__main__":
    args = sys.argv
    input_file_name = args[1] # eg train.twt
    output_file_name = args[2]  # eg train.arff

    if len(args) == 4:
        max_per_class = int(args[3])
    else:
        max_per_class = -1

    data = load_tweets('very_small_test.twt', -1)
    for d in data:
        print count_sentences(d)
