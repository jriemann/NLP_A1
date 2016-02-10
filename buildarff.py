import sys
import re
from functools import partial

CLASSES = ['0', '4']

def init_arff(f):
    '''
    Initialize the .arff file f. That is, write the relation name
    and enumerate the attributes.
    '''
    f.write('@relation {}\n\n'.format(RELATION_NAME))
    for feature in FEATURES:
        f.write('@attribute {} numeric\n'.format(feature))
    f.write('@attribute emotion {' + ','.join(CLASSES) + '}\n\n')
    f.write('@data\n')

def all_data_to_arff(f, data):
    '''
    Write all of data to f in accordance with .arff specifications.
    '''
    for d in data:
        write_arff_data_point(f, d)

def write_arff_data_point(f, d):
    '''
    Write the single datapoint d to f in .arff format.
    '''
    res = []
    for feature in FEATURES:
        func = FEATURE_FUNCS[feature]
        res += [str(func(d))]
    res += [str(get_class(d))]
    f.write(','.join(res) + '\n')

def load_tweets(input_file_name, max_per_class):
    '''
    Return a list of at most max_per_class normalized tweets
    for every class in CLASSES, all of which are stored in
    the file named input_file_name.
    If max_per_class is -1, return all tweets for each class in CLASSES.
    '''
    if max_per_class == -1:
        data = load_all_tweets(input_file_name)
    else:
        data = load_n_tweets(input_file_name, max_per_class)
    return data

def load_n_tweets(input_file_name, n):
    '''
    Return n normalized tweets per class in a list.
    '''
    data = []
    for cls in CLASSES:
        f = open(input_file_name, 'r')
        data += load_n_class_tweets(f, n, cls)
        f.close()
    return data

def load_n_class_tweets(f, n, cls):
    '''
    Return n normalized tweets - stored in file f - of class cls.
    '''
    data = []
    L = f.readlines()
    curr, new = (L[0], False) if is_demarcation(L[0], cls) else ('', True)
    for line in L[1:]:
        if is_demarcation(line, cls):
            curr = line
            new = False
        elif not new and not is_demarcation(line):
            curr += line
        elif is_demarcation(line) and curr:
            data += [curr]
            curr = ''
            new = True
        if len(data) == n:
            break
    return data

def load_all_tweets(input_file_name):
    '''
    Return every normalized tweet stored in the file
    input_file_name in a list.
    '''
    data = []
    f = open(input_file_name, 'r')
    L = f.readlines()
    curr = L[0]
    for line in L[1:]:
        if is_demarcation(line):
            data += [curr]
            curr = line
        else:
            curr += line
    data += [curr]
    f.close()
    return data

def is_demarcation(s, c=''.join(CLASSES)):
    '''
    Return True iff s is a tweet demarcation of the form
    <A=c>, where c is the class of that tweet.
    By default, we check for any class.
    '''
    return True if re.match('<A=[{}]>'.format(c), s.rstrip('\n')) else False

def is_punctuation(s):
    '''
    Return True iff s is a punctuation token.
    '''
    return True if re.match('[,:;]|[\.!?()$"`' + "']", s) else False

def get_class(tweet):
    '''
    Return the class of tweet.
    '''
# as follows:
    demarcation = tweet.split('\n')[0]
    cls = [int(i) for i in demarcation if i.isdigit()][0]
    return cls

def as_sentences(tweet):
    '''
    Return the input tweet as a list of sentences,
    omitting the demarcation.
    '''
    # Upon splitting on newlines, the first element
    # of the resulting list will be the tweet's
    # demarcation and the last element will be the
    # empty string. All other elements are sentences.
    return tweet.split('\n')[1:-1]

def sentence_to_tags(sentence):
    '''
    Return a list of tags corresponding to the tagged tokens
    in sentence.
    '''
    split_tags = map(lambda s: s.split('/')[1], sentence.split(' '))
    return filter(None, split_tags)

def sentence_to_tokens(sentence):
    '''
    Return a list of tokens corresponding to the tagged tokens
    in sentence.
    '''
    split_tokens = map(lambda s: s.split('/')[0], sentence.split(' '))
    return filter(None, split_tokens)

def sentence_no_tags(sentence):
    '''
    Return a string of the input sentence with tags stripped
    from tokens.
    '''
    return ' '.join(sentence_to_tokens(sentence))

def count_sentences(tweet):
    '''
    Return the number of sentences in tweet.
    '''
    return len(as_sentences(tweet))

def avg_token_length(tweet):
    '''
    Return the average length of tokens in tweet,
    measured by number of characters.
    '''
    num_tokens = 0
    total = 0
    for sentence in as_sentences(tweet):
        tokens = sentence_to_tokens(sentence)
        lengths = map(lambda s: 0 if is_punctuation(s) else len(s), tokens)
        num_tokens += len(lengths)
        total += sum(lengths)
    return total / num_tokens

def avg_sentence_length(tweet):
    '''
    Return the average length of sentences in tweet,
    measured by number of tokens 
    '''
    num_sentences = count_sentences(tweet)
    total = 0
    for sentence in as_sentences(tweet):
        tokens = sentence_to_tokens(sentence)
        total += len(tokens)
    return total / num_sentences

def count_pronoun(nth_person, tweet):
    '''
    Return the number of occurences in tweet of nth_person
    pronouns.
    '''
    f = open(WORDLISTS_DIR + '/{}-person'.format(nth_person), 'r')
    pronouns = [s.rstrip('\n') for s in f.readlines()]
    f.close()
    count = 0
    for sentence in as_sentences(tweet):
        tokens = sentence_to_tokens(sentence)
        token_to_pronoun = map(lambda s: 1 
                                         if s.lower() in pronouns 
                                         else 0, tokens)
        count += sum(token_to_pronoun)
    return count

def count_conjunctions(tweet):
    '''
    Return the number of occurences in tweet of the following: 
     'and', 'but', 'for', 'nor', 'or', 'so', 'yet'
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tags = sentence_to_tags(sentence)
        count += tags.count('CC')
    return count

def count_verbs(tense, tweet):
    '''
    Return the number of occurences in tweet of
    tense-tense verbs in tweet. 
    '''
    tense_regex = VERB_TENSE_REGEX[tense]
    count = 0
    for sentence in as_sentences(tweet):
        count += regex_count(sentence, tense_regex)
    return count

def regex_count(sentence, regex):
    '''
    Return the number of times regex is found in sentence.
    '''
    r = re.compile(regex, re.IGNORECASE)
    return len(r.findall(sentence))

def count_p_nouns(tweet):
    '''
    Return the number of occurences in tweet of proper nouns.
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tags = sentence_to_tags(sentence)
        count += tags.count('NNP') + tags.count('NNPS')
    return count

def count_c_nouns(tweet):
    '''
    Return the number of occurences in tweet of common nouns
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tags = sentence_to_tags(sentence)
        count += tags.count('NN') + tags.count('NNS')
    return count

def count_adverbs(tweet):
    '''
    Return the number of occurences in tweet of adverbs.
    Adverbs are tagged RB, RBR, or RBS.
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tags = sentence_to_tags(sentence)
        count += tags.count('RB') + tags.count('RBR') + tags.count('RBS')
    return count

def count_wh_words(tweet):
    '''
    Return the number of occurences in tweet of wh-words,
    i.e. words tagged with WDT / WP / WP$ / WRB.
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tags = sentence_to_tags(sentence)
        count += tags.count('WDT') + tags.count('WP')
        count += tags.count('WP$') + tags.count('WRB')
    return count

def count_slang(tweet):
    '''
    Return the number of occurences in tweet of slang words.
    '''
    count = 0
    f = open(WORDLISTS_DIR + '/Slang', 'r')
    slang_words = [s.rstrip('\n') for s in f.readlines()]
    f.close()
    for sentence in as_sentences(tweet):
        tokens = sentence_to_tokens(sentence)
        token_to_slang = map(lambda s: 1 
                                       if s.lower() in slang_words 
                                       else 0, tokens)
        count += sum(token_to_slang)
    return count

def count_uppercase(tweet): 
    '''
    Return the number of occurences of uppercase words of
    length greater than or equal to 2.
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tokens = sentence_to_tokens(sentence)
        token_to_upper = map(lambda s: 1 
                                    if len(s) > 1 and s.isupper() 
                                    else 0, tokens)
        count += sum(token_to_upper)
    return count

def count_punctuations(tweet):
    '''
    Return the number of occurences of the following
    characters:
        ,     (commas)
        : | ; (colons or semi colons)
        -     (dashes)
        (     (right parenthesis)
        )     (left parenthesis)
        ...   (ellipses)
    '''
    punc_to_count = {}
    for punc in PUNCTUATIONS:
        punc_to_count[punc] = count_punctuation(tweet, punc)
    return punc_to_count

def count_punctuation(punc, tweet):
    '''
    Return the number of occurences in tweet of punc.
    Multiple punctuations are considered single tokens,
    so we count how many matches of the regular expression
    punc+ we find in tweet.
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tokens_no_tags = sentence_no_tags(sentence) 
        count += len(re.findall(r'{}+'.format(punc), tokens_no_tags))
    return count

RELATION_NAME = 'twit_classification'

FEATURES = ['1st_person_pro', '2nd_person_pro', '3rd_person_pro',
            'conjunctions', 'past', 'future', 'commas', '(semi)colons',
            'dashes', 'parentheses', 'ellipses', 'common_nouns',
            'proper_nouns', 'adverbs', 'wh_words', 'slang', 'uppercase',
            'avg_sentence_len', 'avg_token_len', 'num_sentences']

FEATURE_FUNCS = {'1st_person_pro': partial(count_pronoun, 'First'),
                 '2nd_person_pro': partial(count_pronoun, 'Second'),
                 '3rd_person_pro': partial(count_pronoun, 'Third'),
                 'conjunctions': count_conjunctions,
                 'past': partial(count_verbs, 'past'),
                 'future': partial(count_verbs, 'future'),
                 'commas': partial(count_punctuation, ','),
                 '(semi)colons': partial(count_punctuation, ':|;'),
                 'dashes': partial(count_punctuation, '-'),
                 'parentheses': partial(count_punctuation, '(|)'),
                 'ellipses': partial(count_punctuation, '...'),
                 'common_nouns': count_c_nouns,
                 'proper_nouns': count_p_nouns,
                 'adverbs': count_adverbs,
                 'wh_words': count_wh_words,
                 'slang': count_slang,
                 'uppercase': count_uppercase,
                 'avg_sentence_len': avg_sentence_length,
                 'avg_token_len': avg_token_length,
                 'num_sentences': count_sentences}

PAST_TAGS = "(/PRP\$?|/VBD|/VBG|/VBN)"
FUTURE_TAGS = "(/PRP\$|/VB|/VBP|/VBZ|/MD)"
PAST_FIXES = "(has|had|have|were|was|did)?"
FUTURE_FIXES = "('nt|'ll|will|won't|gonna|going\sto)?"
PAST_REGEX = PAST_FIXES + PAST_TAGS + '\s?[a-z]*' + PAST_TAGS
FUTURE_REGEX = FUTURE_FIXES + FUTURE_TAGS + '\s?[a-z]*' + FUTURE_TAGS

VERB_TENSE_REGEX = {'past': PAST_REGEX, 'future': FUTURE_REGEX}

WORDLISTS_DIR = '/u/cs401/Wordlists'

if __name__ == "__main__":
    args = sys.argv
    input_file_name = args[1] # eg train.twt
    output_file_name = args[2]  # eg train.arff

    if len(args) == 4:
        max_per_class = int(args[3])
    else:
        max_per_class = -1

    data = load_tweets(input_file_name, max_per_class)
    with open(output_file_name, 'w+') as f:
        init_arff(f)
        all_data_to_arff(f, data)
