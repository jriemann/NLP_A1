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

def tag_counts(tweet):
    '''
    Return a dictionary of token tags to the number of their 
    occurences in tweet.
    '''
    pass

def count_pronouns(tweet):
    '''
    Return the number of occurences in tweet of first, second,
    and third person pronouns in the form of a tuple
        (first_person, second_person, third_person)
    '''
    pronouns = ['First', 'Second', 'Third']
    count = 0
    for i in range(len(pronouns)):
        pronouns[i] = count_pronoun(tweet, pronouns[i])
    return pronouns[0], pronouns[1], pronouns[2]

def count_pronoun(tweet, nth_person):
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

def count_verbs(tweet):
    '''
    Return the number of occurences in tweet of past and
    future tense verbs in tweet. 
    '''
    past_tags = "(/PRP\$?|/VBD|/VBG|/VBN)"
    future_tags = "(/PRP\$|/VB|/VBP|/VBZ|/MD)"
    past_fixes = "(has|had|have|were|was|did)?"
    future_fixes = "('nt|'ll|will|won't|gonna|going\sto)?"
    past_regex = past_fixes + past_tags + '\s?[a-z]*' + past_tags
    future_regex = future_fixes + future_tags + '\s?[a-z]*' + future_tags
    past_count, future_count = 0, 0
    for sentence in as_sentences(tweet):
        print sentence
        past_count += regex_count(sentence, past_regex)
        future_count += regex_count(sentence, future_regex)
    return past_count, future_count

def regex_count(sentence, regex):
    '''
    Return the number of times regex is found in sentence.
    '''
    r = re.compile(regex, re.IGNORECASE)
    return len(r.findall(sentence))

def count_nouns(tweet):
    '''
    Return the number of occurences in tweet of common nouns
    and proper nouns.
    '''
    common_count, proper_count = 0, 0
    for sentence in as_sentences(tweet):
        tags = sentence_to_tags(sentence)
        common_count += tags.count('NN') + tags.count('NNS')
        proper_count += tags.count('NNP'), + tags.count('NNPS')
    return common_count, proper_count

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
        ,    (commas)
        :    (colons)
        ;    (semi-colons)
        -    (dashes)
        (    (right parenthesis)
        )    (left parenthesis)
        ...  (ellipses)
    '''
    punctuations = [',', ':', ';', '-', '(', ')', '...']
    punc_to_count = {}
    for punc in punctuations:
        punc_to_count[punc] = count_punctuation(tweet, punc)
    return punc_to_count

def count_punctuation(tweet, punc):
    '''
    Return the number of occurences in tweet of punc.
    Multiple punctuations are considered single tokens,
    so we count how many matches of the regular expression
    punc+ we find in tweet.
    '''
    count = 0
    for sentence in as_sentences(tweet):
        tokens_no_tags = sentence_no_tags(sentence) 
        count += len(re.findall('\{}+'.format(punc), tokens__no_tags))
    return count

if __name__ == "__main__":
    args = sys.argv
    input_file_name = args[1] # eg train.twt
    output_file_name = args[2]  # eg train.arff

    if len(args) == 4:
        max_per_class = int(args[3])
    else:
        max_per_class = -1

    data = load_tweets(input_file_name, max_per_class)
