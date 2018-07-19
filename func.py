def floor(value, dignum):
    return int(value / dignum) * dignum

def ceil(value, dignum):
    return (int(value / dignum) + 1 ) * dignum

def crosscorr(vec0, vec1):
    value = np.dot(vec0, vec1) / (np.linalg.norm(vec0) * np.linalg.norm(vec1))
    return value