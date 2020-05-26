

def full_search(alphabet, word):

    alphabet_list = list(alphabet)
    word_list = list(word)
    new_word = []

    for i in range(len(word_list)):
        for j in range(len(alphabet_list)):
            if word_list[i] == alphabet_list[j]:
                new_word.append(alphabet_list[j])
                print("".join(new_word))
                break
