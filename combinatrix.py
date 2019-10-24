
from multiprocessing import Pool, cpu_count
import functools

def word_in_sentence(sentence, word):
    try:
        remove_word(word, sentence)
    except:
        return False
    return True
    # return all( (letter in sentence for letter in word) )

def mk_true_dict(sentence, dictionary):
    return frozenset( { word for word in dictionary
            if word_in_sentence(sentence, word) } )


def remove_word(word, sentence):
    for letter in word:
        idx = sentence.index(letter)
        sentence = sentence[:idx] + sentence[idx+1:]
    return sentence

def mk_sentences(sentence, dictionary, depth=0):
    if depth % 10 == 0:
        print("Generating sentences from, depth: {}, sentence: \"{}\", dictionary size: {}".format(
            depth, sentence, len(dictionary)
        ))

    for word in dictionary:
        new_sentence = remove_word(word, sentence)
        true_dict = mk_true_dict(new_sentence, dictionary)

        if len(new_sentence) == 0:
            yield word

        new_sentencess = list( mk_sentences(new_sentence, true_dict, depth+1) )
        for new_sen in new_sentencess:
            if len(new_sen.replace(" ", "")) == len(new_sentence.replace(" ", "")):
                yield word + " " + new_sen

def get_dict():
    with open("wordlist", 'r') as f:
        for word in f:
            yield word.strip()

def main():
    dictionary = [ "a", "an", "be", "bee", "beee", "zitcom" ]
    base_sentence = "e bea"
    
    base_sentence = base_sentence.replace(" ", "")
    true_dict = mk_true_dict(base_sentence, dictionary)

    print("Reduced dictionary to: {} words".format(len(true_dict)))
    sentences = list(mk_sentences(base_sentence, true_dict))
    
    print( "Generated sentences: {},\n length: {}".format( list(sentences), len(sentences) ))


def true_main():
    base_sentence = "poultry outwits ants"

    easy_secret = "e4820b45d2277f3844eac66c903e84be"
    medium_secret = "23170acc097c24edb98fc5488ab033fe"
    hard_secret = "665e5bcb0c20062fe8abaaf4628bb154"
    
    dictionary = get_dict()
    
    base_sentence = "".join(sorted(base_sentence.replace(" ", "")))
    true_dict = mk_true_dict(base_sentence, dictionary)

    print("Reduced dictionary to: {} words".format(len(true_dict)))

    sentences = list(mk_sentences(base_sentence, true_dict))
    
    print( "Generated sentences: {},\n length: {}".format( list(sentences), len(sentences) ))

if __name__ == "__main__":
    true_main()