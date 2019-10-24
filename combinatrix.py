
import hashlib
import itertools

def subtract_string(op1, op2):
    res = op1 # Possibly more thourough copy?
    for char in op2:
        idx = res.index(char)
        res = res[:idx] + res[idx+1:]
    return res

def mk_dict_dict(wordlist):
    output = {}
    for word in wordlist:
        sword = "".join(sorted(word))
        if not sword in output:
            output[sword] = []
        output[sword].append(word)
    return output

def word_in(sentence, word):
    try:
        subtract_string(sentence, word)
    except:
        return False
    return True

def prune_dict(sentence, dictionary):
    return { key:value for key,value in dictionary.items()
            if word_in(sentence, key) }

def iter_match_words(dictionary, char):
    #for key in dictionary:
    #    if key[0] == char:
    #        yield key
    return (key for key in dictionary if key[0] == char)

def seek_anagrams(sentence, dictionary):
    # Assume pruned dict
    # Assume sentence is sorted
    for key in iter_match_words(dictionary, sentence[0]):
        new_sentence = subtract_string(sentence, key)
        new_dictionary = prune_dict(new_sentence, dictionary)

        words = dictionary[key]
        if len(new_dictionary) == 0:
            for word in words:
                yield [word]
        else:
            rest = seek_anagrams(new_sentence, new_dictionary)
            for word in words:
                for sent in rest:
                    yield ([word] + sent)

def get_long_words(dictionary, limit):
    return sorted([ key for key in dictionary if len(key) >= limit ],
            key=lambda x: len(x), reverse=True)

def heuristic_start(sentence, dictionary):
    # Assume pruned dict
    # Assume sentence is sorted
    candidates = list( get_long_words(dictionary, 7) )
    print("Seed candidates: {}, {}".format(len(candidates), candidates[0]))
    for key in candidates:
        new_sentence = subtract_string(sentence, key)
        new_dictionary = prune_dict(new_sentence, dictionary)

        # print("Seeding with {}, dictionary pruned to {}".format(
        #     key, len(new_dictionary) ))
        
        words = dictionary[key]
        rest = list( seek_anagrams(new_sentence, new_dictionary) )
        for word in words:
            for sent in rest:
                if len( subtract_string(sentence, (word+"".join(sent))) ) > 0:
                    continue
                yield ([word] + sent)

def check_hashes(anagrams, hashes):
    for anagram in anagrams:
        for sentence in itertools.permutations(anagram):
            actual = " ".join(sentence).encode()
            checksum = hashlib.md5(actual).hexdigest()
            
            if checksum in hashes:
                print("Found \"{}\" for {}".format(
                    actual, checksum))

def main():
    in_sentence = "poultry outwits ants"
    wordlist = (x.strip() for x in open("wordlist") if len(x.strip()) > 1)
    print(next(wordlist))
    dd = mk_dict_dict(wordlist)
    
    base_sentence = "".join(sorted(in_sentence)).strip()
    pdd = prune_dict(base_sentence, dd)
    print(len(pdd))
    anagrams = list( heuristic_start(base_sentence, pdd) )
    print(len(anagrams))

    print( [ x for x in anagrams 
        if ("statutory" in x) and ("lisp" in x) ])

    check_hashes(anagrams, [
        "e4820b45d2277f3844eac66c903e84be",
        "23170acc097c24edb98fc5488ab033fe",
        "665e5bcb0c20062fe8abaaf4628bb154"
        ])

def tests():
    import timeit
    from collections import Counter

    poultry = "poultry outwits ants"
    words = ["trustpilot", "wants", "you", "zitcom", "poultry", "ant", "awnts"]

    print("Subtract_string, test cases:")
    print("sub({}, {}) = {}".format("abe", "ab", subtract_string("abe", "ab")))
    print("sub({}, {}) = {}".format(
        "poultry outwits ants", "trustpilot", 
        subtract_string("poultry outwits ants", "trustpilot")))

    print("mk_dict_dict({}) = {}".format(
        ["abe", "eba", "ab", "zitcom"],
        mk_dict_dict(["abe", "eba", "ab", "zitcom"])))

    word_dict = mk_dict_dict(words)
    pword_dict = prune_dict("".join(sorted(poultry)), mk_dict_dict(words))
    print(mk_dict_dict(words))
    print(prune_dict("".join(sorted(poultry)), mk_dict_dict(words)))

    t0 = timeit.timeit(lambda: subtract_string("poultry outwits ants", "trustpilot"), number=10000)
    print(t0)

    print("get_long_words(dict, lim) = {}".format(
        get_long_words(word_dict,7) ))

    # Do something with real things
    base_sentence = "".join(sorted(poultry)).strip()
    fp = (x.strip() for x in open("wordlist"))
    dd = mk_dict_dict(fp)
    pdd = prune_dict(base_sentence, dd)

    print(len(pdd))
    
    xs = Counter([ str(len(k)) for k in pdd ])
    print(xs)

    print(list( iter_match_words(word_dict, 'c')))
    print("======================================")
    print(list( heuristic_start(base_sentence, pword_dict) ))

if __name__ == "__main__":
    # tests()
    main()
