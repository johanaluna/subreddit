import pymongo
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd



def transform_get(text, loadcv, loaddf):
    """Function written by Matthew/Johana"""
    transform = loadcv.transform([text])
    inputdata = transform.todense()
    dist_matrix = cosine_similarity(loaddf, inputdata)
    results = pd.DataFrame(dist_matrix)

    return results[0].sort_values(ascending=False)[:3].index.tolist()