from thefuzz.process import extractOne


def best_match(s, los, thresh=80):
    """
    str, iterable(str) -> int | None
    Return the best matching string index in 'los' that
    matches given string 's', only return the
    best match if the matching score is higher than thresh
    else return None 
    """
    if s == "":
        return None

    res = extractOne(s, los, score_cutoff=thresh)

    if res is None:
        return res
    else:
        return res[0]
