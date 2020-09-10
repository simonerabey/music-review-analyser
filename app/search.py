from app import es

'''
Adds a record to the index
@param index: elasticsearch index
@param model: record to be added to the index
'''
def add(index, model):
    if es:
        fields = {}
        for field in model.__searchable__:
            fields[field] = getattr(model, field)
        es.index(index=index, id=model.id, body=fields)

'''
Deletes a record from the index
@param index: elasticsearch index
@param model: record to be deleted from the index
'''
def delete(index, model):
    if es:
        es.delete(index=index, id=model.id)

'''
Queries the index
@param index: elasticsearch index
@param query(str): a string consisting of the words to be searched for
@ret List of records resulting from the query
'''
def query(index, query):
    if not es:
        return []
    body = {"query": {"multi_match": {"query": query, "fields": ["*"]}}}
    search = es.search(index=index, body=body)
    results = [int(result["_id"]) for result in search["hits"]["hits"]]
    return results