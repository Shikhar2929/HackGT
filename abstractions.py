import os


def setup(classes):
    try:
        os.mkdir('data')
    except:
        pass
    for c in classes:
        try:
            os.mkdir('data/{}'.format(c))
        except:
            pass
