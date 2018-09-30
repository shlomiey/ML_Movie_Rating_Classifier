""""
parsing the corpus to iterable, useful & readable (mostly) dictionaries.

"""

import time

from collections import Counter
from typing import Set
from statistics import mean


def line_parser(keys, line):
    internal_dictionary = {}
    line_parse = line.split()

    index = 0
    key = keys[index]
    value = ""
    for token in line_parse:
        if token != "+++$+++":
            if value != "":
                value += " "
            value += token
        else:
            internal_dictionary[key] = value
            value = ""
            index += 1
            key = keys[index]

    # adding the last one for dictionary
    internal_dictionary[key] = value

    return internal_dictionary


def database_to_dict(exterior_key, file_keys, file_extension):
    database_dict = {}
    file_to_parse = open(".\\cornell movie-dialogs corpus\\" + file_extension)
    line_to_parse = file_to_parse.readline()
    line_counter = 1
    while line_to_parse != "":
        in_dictionary = line_parser(file_keys, line_to_parse)
        in_dict_without_ext_key = dict(in_dictionary)
        if type(exterior_key) is tuple:
            # means we parsing movie_conversations.txt - the key is tuple
            # adding the line twice for consistency - doesn't matter which character is the first one
            # added line_counter for unique key - as two character can have several conversation in the same movie
            del in_dict_without_ext_key[exterior_key[0]]
            del in_dict_without_ext_key[exterior_key[1]]

            database_dict[(line_counter, in_dictionary[exterior_key[0]], in_dictionary[exterior_key[1]])] = \
                in_dict_without_ext_key
        else:
            del in_dict_without_ext_key[exterior_key]
            database_dict[in_dictionary[exterior_key]] = in_dict_without_ext_key

        line_counter += 1
        line_to_parse = file_to_parse.readline()

    file_to_parse.close()

    return database_dict


def movie_characters_metadata_to_dict():
    file_name = "movie_characters_metadata.txt"
    keys_movie_characters_metadata = ['characterID', 'character name', 'movieID', 'movie title', 'gender', 'position']

    return database_to_dict('characterID', keys_movie_characters_metadata, file_name)


def movie_conversations_to_dict():
    file_name = "movie_conversations.txt"
    keys_movie_conversations = ['characterID1', 'characterID2', 'movieID', 'chronological_order']
    return database_to_dict(('characterID1', 'characterID2'), keys_movie_conversations, file_name)


def movie_lines_to_dict():
    file_name = "movie_lines.txt"
    keys_movie_lines = ['lineID', 'characterID', 'movieID', 'character name', 'text']

    return database_to_dict('lineID', keys_movie_lines, file_name)


def movie_titles_metadata_to_dict():
    file_name = "movie_titles_metadata.txt"
    keys_movie_titles_metadata = ['movieID', 'movie title', 'movie year', 'IMDB rating', 'IMDB votes', 'genres']

    return database_to_dict('movieID', keys_movie_titles_metadata, file_name)


def bag_of_words(text):
    b_o_w = Counter()
    for word in text.split():
        b_o_w[word] += 1
    return b_o_w


def set_of_words(text):
    s_o_w = set()
    for word in text.split():
        s_o_w.add(word)
    return s_o_w


def weight_calculator(value_1, value_2):
    # means we arrived for the new genre feature for NB
    if type(value_1) == list or type(value_2) == list:
        ret = 0
        for value in value_1:
            if value in value_2:
                ret += 1
        return ret

    max_value = max(value_1, value_2)
    min_value = min(value_1, value_2)
    if max_value == 0:
        return 1
    return 1 - (max_value - min_value) / max_value


def object_similarity(obj_1, obj_2):
    """
    calculate similarity between two objects
    :param obj_1: can be line/ conversation/ movie
    :param obj_2: can be line/ conversation/ movie
    :return: the similarity value between 0 - 1
    """
    w_list = []
    obj_1_bag_size = sum(obj_1['bag_of_words'].values())
    obj_2_bag_size = sum(obj_2['bag_of_words'].values())
    obj_1_set = obj_1['set_of_words']
    obj_2_set = obj_2['set_of_words']
    obj_1_diff_2_set = obj_1_set - obj_2_set
    obj_2_diff_1_set = obj_2_set - obj_1_set
    w_list.append(weight_calculator(obj_1_bag_size, obj_2_bag_size))
    w_list.append(weight_calculator(len(obj_1_set), len(obj_2_set)))
    w_list.append(weight_calculator(len(obj_1_diff_2_set),
                                    len(obj_2_diff_1_set)))
    if 'total_lines' in obj_1.keys() and 'total_lines' in obj_2.keys():
        w_list.append(weight_calculator(obj_1['total_lines'],
                                        obj_2['total_lines']))
    if 'total_conversations' in obj_1.keys() and 'total_conversations' in obj_2.keys():
        w_list.append(weight_calculator(obj_1['total_conversations'],
                                        obj_2['total_conversations']))
    # Added as observations of genre -> rating relations
    if 'metadata' in obj_1.keys() and 'metadata' in obj_2.keys():
        w_list.append(weight_calculator(eval(obj_1['metadata']['genres']),
                                        eval(obj_2['metadata']['genres'])))
    return mean(w_list)


class MovieDialogParser:
    """
    class that contain all the dictionary in one place
    Bonus: added a CORPUS_DICTIONARY for easy iterable of the conversations
        key: movie_id
        features:
            - metadata for movie meta features
            - total_conversations
            - bag\set_of_words
            - total_lines
            - conversation_dic - a dictionary for the conversations
                - key: generated counter for each conversation starts from 1
                - lines - dictionary for the lines that constructing the conversation
                    - line_metadata features
                    - bag\set_of_words
                - total_lines
                - bag\set_of_words
    Bonus2: added a rating2ID_dictionary for easy
                IMDB rating (float) -> [movie_id_1, movie_id_2, ...] mapping
    """

    def __init__(self):
        self.movie_lines = movie_lines_to_dict()
        self.movie_characters = movie_characters_metadata_to_dict()
        self.movie_titles = movie_titles_metadata_to_dict()
        self.movie_conversations = movie_conversations_to_dict()

        # Building up the Bonus
        self.corpus_dictionary = {}
        self.rating2ID_dictionary = {}
        movie_conversation_dic = self.movie_conversations
        movie_lines_dic = self.movie_lines
        movie_metadata_dic = self.movie_titles
        for movie_id in movie_metadata_dic.keys():
            conversation_number = 0
            conversation_dic = {}
            inner_dict = {}
            movie_bag_of_words = Counter()
            movie_set_of_words = set()
            total_movie_lines = 0
            for conversation in movie_conversation_dic.values():
                if conversation['movieID'] == movie_id:
                    conversation_number += 1
                    lines_dic = {}
                    conversation_bag_of_words = Counter()
                    conversation_set_of_words: Set[str] = set()  # added type hint because duck typing inconsistency
                    for lines in eval(conversation['chronological_order']):
                        lines_dic[lines] = movie_lines_dic[lines]
                        # bag_of_words returns a Counter object NOT dictionary
                        line_bag_of_words = bag_of_words(movie_lines_dic[lines]['text'])
                        line_set_of_words = set_of_words(movie_lines_dic[lines]['text'])
                        lines_dic[lines].update({'bag_of_words': dict(line_bag_of_words)})
                        lines_dic[lines].update({'set_of_words': line_set_of_words})
                        conversation_bag_of_words += line_bag_of_words
                        conversation_set_of_words.update(line_set_of_words)

                    lines_dic['total_lines'] = len(eval(conversation['chronological_order']))
                    total_movie_lines += len(eval(conversation['chronological_order']))
                    conversation_dic[conversation_number] = lines_dic
                    conversation_dic[conversation_number].update(
                        {'bag_of_words': dict(conversation_bag_of_words)})
                    conversation_dic[conversation_number].update(
                        dict(set_of_words=conversation_set_of_words))
                    movie_bag_of_words += conversation_bag_of_words
                    movie_set_of_words.update(conversation_set_of_words)
                    inner_dict['conversation_dic'] = conversation_dic
                    inner_dict['metadata'] = movie_metadata_dic[movie_id]
                    inner_dict['bag_of_words'] = movie_bag_of_words
                    inner_dict['set_of_words'] = movie_set_of_words
                    inner_dict['total_lines'] = total_movie_lines
            inner_dict['total_conversations'] = len(conversation_dic)
            self.corpus_dictionary[movie_id] = inner_dict

            # updating the rating2ID dictionary
            movie_rating = movie_metadata_dic[movie_id]['IMDB rating']
            if movie_rating in self.rating2ID_dictionary.keys():
                self.rating2ID_dictionary[movie_rating].append(movie_id)
            else:
                self.rating2ID_dictionary[movie_rating] = [movie_id]


def viterbi_algorithm(obs, states, start_p, trans_p, emit_p):
    vertices = [{}]
    for st in states:
        vertices[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        vertices.append({})
        for st in states:
            max_tr_prob = max(vertices[t - 1][prev_st]["prob"] * trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if vertices[t - 1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    vertices[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    for line in dict_table(vertices):
        print(line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in vertices[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in vertices[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(vertices) - 2, -1, -1):
        opt.insert(0, vertices[t + 1][previous]["prev"])
        previous = vertices[t + 1][previous]["prev"]

    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)


def dict_table(dict):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(dict)))
    for state in dict[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


# for debugging & example purposes
if __name__ == "__main__":
    start_time = time.time()
    c = MovieDialogParser()
    movie_0 = c.corpus_dictionary['m0']
    movie_1 = c.corpus_dictionary['m1']
    conversation_0 = movie_0['conversation_dic'][1]
    conversation_1 = movie_1['conversation_dic'][1]
    line_0 = conversation_0['L194']
    line_1 = conversation_1['L2170']

    print('movie similarity score: ', object_similarity(movie_0, movie_1))
    print('conversation similarity score: ', object_similarity(conversation_0, conversation_1))
    print('line similarity score: ', object_similarity(line_0, line_1))
    print(weight_calculator('0', '10'))
    print("--- %s seconds ---" % (time.time() - start_time))
