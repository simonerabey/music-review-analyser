from app import es

def add(index, model):
    if es:
        fields = {}
        for field in model.__searchable__:
            fields[field] = getattr(model, field)
        es.index(index=index, id=model.id, body=fields)

def delete(index, model):
    if es:
        es.delete(index=index, id=model.id)

def query(index, query):
    if not es:
        return []
    body = {"query": {"multi_match": {"query": query, "fields": ["*"]}}}
    search = es.search(index=index, body=body)
    results = [int(result["_id"]) for result in search["hits"]["hits"]]
    return results