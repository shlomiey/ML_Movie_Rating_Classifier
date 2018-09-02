""""
parsing the corpus to iterable, useful & readable dictionaries.

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

    while line_to_parse != "":
        in_dictionary = line_parser(file_keys, line_to_parse)
        in_dict_without_ext_key = dict(in_dictionary)
        del in_dict_without_ext_key[exterior_key]
        database_dict[in_dictionary[exterior_key]] = in_dict_without_ext_key
        line_to_parse = file_to_parse.readline()

    file_to_parse.close()

    return database_dict


def movie_characters_to_dict():
    file_name = "movie_characters_metadata.txt"
    keys_movie_characters_metadata = ['characterID', 'character name', 'movieID', 'movie title', 'gender', 'position']

    return database_to_dict('characterID', keys_movie_characters_metadata, file_name)


def movie_conversations_to_dict():
    file_name = "movie_conversations.txt"
    keys_movie_conversations = ['characterID1', 'characterID2', 'movieID', 'chronological_order']

    return database_to_dict('characterID1', keys_movie_conversations, file_name)


def movie_lines_to_dict():
    file_name = "movie_lines.txt"
    keys_movie_lines = ['lineID', 'characterID', 'movieID', 'character name', 'text']

    return database_to_dict('lineID', keys_movie_lines, file_name)


def movie_titles_metadata_to_dict():
    file_name = "movie_titles_metadata.txt"
    keys_movie_titles_metadata = ['movieID', 'movie title', 'movie year', 'IMDB rating', 'IMDB votes', 'genres']

    return database_to_dict('movieID', keys_movie_titles_metadata, file_name)


# for debugging purposes
# if __name__ == "__main__":
#     d = database_to_dict('movieID', keys_movie_titles_metadata, file_name)
#     for check1 in d:
#         print(check1, d[check1])
