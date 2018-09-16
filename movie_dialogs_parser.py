from collections import Counter
import time

""""
parsing the corpus to iterable, useful & readable (mostly) dictionaries.

"""


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
    internal_dictionary[key] = value  # literal_eval(value)  # eval extract list from string

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


class MovieDialogParser:
    """
    class that contain all the dictionary in one place
    Bonus: added a CORPUS_DICTIONARY for easy iterable of the conversations
        key: movie_id
        features:
            - movie_metadata features
            - total_conversations
            - movie_bag\set_of_words
            - total_movie_lines
            - conversation_dic - a dictionary for the conversations
                - key: generated counter for each conversation starts from 1
                - lines - dictionary for the lines that constructing the conversation
                    - line_metadata features
                    - line_bag\set_of_words
                - total_lines
                - conversation_bag\set_of_words
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
                    # print(conversation)
                    # print(conversation_number, "conversation['chronological_order']")
                    lines_dic = {}
                    conversation_bag_of_words = Counter()
                    conversation_set_of_words = set()
                    for lines in eval(conversation['chronological_order']):
                        # print(lines, movie_lines_dic[lines], movie_lines_dic[lines]['text'])
                        lines_dic[lines] = movie_lines_dic[lines]
                        # bag_of_words returns a Counter object NOT dictionary
                        line_bag_of_words = bag_of_words(movie_lines_dic[lines]['text'])
                        line_set_of_words = set_of_words(movie_lines_dic[lines]['text'])
                        lines_dic[lines].update({'line_bag_of_words': dict(line_bag_of_words)})
                        lines_dic[lines].update({'line_set_of_words': line_set_of_words})
                        conversation_bag_of_words += line_bag_of_words
                        conversation_set_of_words.update(line_set_of_words)

                    lines_dic['total_lines'] = len(eval(conversation['chronological_order']))
                    total_movie_lines += len(eval(conversation['chronological_order']))
                    conversation_dic[conversation_number] = lines_dic
                    conversation_dic[conversation_number].update(
                        {'conversation_bag_of_words': dict(conversation_bag_of_words)})

                    conversation_dic[conversation_number].update(
                        {'conversation_set_of_words': conversation_set_of_words})
                    movie_bag_of_words += conversation_bag_of_words
                    movie_set_of_words.update(conversation_set_of_words)
                    inner_dict['conversation_dic'] = conversation_dic
                    inner_dict['metadata'] = movie_metadata_dic[movie_id]
                    inner_dict['movie_bag_of_words'] = movie_bag_of_words
                    inner_dict['movie_set_of_words'] = movie_set_of_words
                    inner_dict['total_movie_lines'] = total_movie_lines
            inner_dict['total_conversations'] = len(conversation_dic)
            self.corpus_dictionary[movie_id] = inner_dict
            
            # updating the rating2ID dictionary
            movie_rating = movie_metadata_dic[movie_id]['IMDB rating']
            if movie_rating in self.rating2ID_dictionary.keys():
	            self.rating2ID_dictionary[movie_rating].append(movie_id)
            else:
	            self.rating2ID_dictionary[movie_rating] = [movie_id]


# for debugging purposes
if __name__ == "__main__":
    start_time = time.time()
    c = MovieDialogParser()
    # print(c.corpus_dictionary['m2']['total_movie_lines'])
    # print(c.corpus_dictionary['m2']['total_conversations'])
    print("--- %s seconds ---" % (time.time() - start_time))
