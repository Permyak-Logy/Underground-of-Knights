import run


def get(name):
    '''Возвращает набор уровней с именем name'''
    return list_of_names.get(name, ([], None))


list_of_names = {}