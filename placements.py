
def build_placements(shoes: list[str]) -> dict[str, list[int]]:
    """Return a dictionary where each key is a company and each value is a
    list of placements by people wearing shoes made by that company.
    
    >>> build_placements(['Saucony', 'Asics', 'Asics', 'NB', 'Saucony', \
    'Nike', 'Asics', 'Adidas', 'Saucony', 'Asics'])
    {'Saucony': [1, 5, 9], 'Asics': [2, 3, 7, 10], 'NB': [4], 'Nike': [6], 'Adidas': [8]}
    """
    new_d = {}
    
    for i in range(len(shoes)):
        if shoes[i] in new_d:
            new_d[shoes[i]].append(i+1)
        else:
            new_d[shoes[i]] = [i+1]
    return new_d