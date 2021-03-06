"""
Text preprocessing module
v0.2 April 22, 2020

Provides the following functions for pre-processing text data in string format
text_preprocess:  Makes text lower case, strips punctuation and 
                  optionally preprocesses digits
text_tokenize:  Tokenizes and optionally removes stopwords
text_normalize:  Lemmatizes or stems a list of tokens and optionally rejoins into a strong
"""

import re
import inflect
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer 
from nltk.stem import WordNetLemmatizer 
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def text_preprocess(text, lower=True, remove_punctuation=True, digits=None):
    """
    text_preprocess:  makes text lower case, strips punctuation and optionally
                      preprocesses digits
    args:   text                the text string to modify
            lower               whether to make the text lower case
            remove_punctation   whether to remove punctuation
            digits              (optional) "remove" or "convert" to text
    return: text        the processed text
    """
    # make lower case
    if lower:
        text = text.lower()
    
    # remove punctuation
    if remove_punctuation:
        punct_space = str.maketrans('-/_&', '    ')  # replaces '-', '_', '&', '/' with ' '
        punct_strip = str.maketrans('', '', '!"#$%\()*+,.:;<=>?@[\\]^`{|}~')  # all string.punctuation except _'-/&
        text = text.translate(punct_space).translate(punct_strip)

    # convert digits to text
    if digits == "convert":
        text = __convert_digits(text)
    elif digits == "remove":
        text = __remove_digits(text)
    elif digits:
        raise ValueError

    return text

  
def text_tokenize(text, remove_stopwords=False):
    tokens = word_tokenize(text) 
    if remove_stopwords:
        tokens = __remove_stopwords(tokens)
    return tokens

  
def text_normalize(tokens, normalize='lemmatize', rejoin=False):
    """
    text_normalize:  normalizes a list of tokens
    args:   text        list of word tokens
            normalize   (optional) 'lemmatize' or 'stem'
    return:             the processed list of tokens or rejoined string
    """
    if normalize == 'lemmatize':
        tokens = __lemmatize_tokens(tokens)
    elif normalize == 'stem':
        tokens = __stem_tokens(tokens)
    elif normalize:
        raise NotImplementedError
    
    return ' '.join(tokens) if rejoin else tokens


# ==================== Helper functions ==================== #

## remove numbers
def __remove_digits(text): 
    result = re.sub(r'\s*\d+\s*', ' ', text) 
    return result


## convert numbers into words 
def __convert_digits(text): 
    infl = inflect.engine() 
    
    split = text.split()
    
    elements = []
    for ele in split: 
        # if word is a digit, convert the digit 
        # to numbers and append into the new_string list 
        converted = infl.number_to_words(ele) if ele.isdigit() else ele
        elements.append(converted)
  
    # join the words of new_string to form a string 
    joined = ' '.join(elements)
    return joined 


# remove stopwords function 
def __remove_stopwords(tokens): 
    stop_words = set(stopwords.words("english")) 
    filtered_tokens = [word for word in tokens if word not in stop_words] 
    return filtered_tokens

  
# stem words in a list of tokenized words 
def __stem_tokens(tokens): 
    stemmer = PorterStemmer() 
    stems = [stemmer.stem(token) for token in tokens] 
    return stems 
  

# lemmatize words in a list of tokenized words 
def __lemmatize_tokens(tokens): 
    lemmatizer = WordNetLemmatizer() 
    lemmas = [lemmatizer.lemmatize(token) for token in tokens] 
    return lemmas 
  
