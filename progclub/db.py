from flask import current_app
from google.cloud import datastore

datastore_client = datastore.Client()


def from_datastore(entity):
    """Converts a datastore entity into a dictionary format."""
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity


def get_client():
    """Returns the application's DataStore client."""
    return datastore.Client(current_app.config["PROJECT_ID"])


def entry(kind, key, properties):
    """Inserts a DataStore entity of a given kind, ID,
    and properties into the database."""
    ds = get_client()
    entity = datastore.Entity(ds.key(kind, key))
    entity.update(properties)
    ds.put(entity)
    return entity


def get_entry(kind, key):
    ds = get_client()
    return from_datastore(ds.get(ds.key(kind, key)))


def update_entry(kind, key, properties):
    ds = get_client()
    entity = ds.get(ds.key(kind, key))
    entity.update(properties)
    ds.put(entity)


def get_entries(kind, order=None):
    ds = get_client()
    query = ds.query(kind=kind)

    if order is not None:
        query.order = order

    # We should probably implement filtering later.
    return list(query.fetch())
