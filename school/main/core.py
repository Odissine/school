
def get_purcent(score, max):
    if score is not None and max is not None:
        purcent = int(score * 100 / max)
    else:
        purcent = 0
    return purcent