import pickle

output_path = "posting"


def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    name = output_path+"\\"+name if output_path != '' else name

    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    name = output_path+"\\"+name if output_path != '' else name

    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def load_inverted_index(path=None):
    if path:
        path = path + "\\inverted_index"
    else:
        path = "inverted_index"
    return load_obj(path)
