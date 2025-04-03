from pinecone import Pinecone


def init_pinecone(PINECONE_API_KEY, INDEX_NAME):
    # Initialize Pinecone
    pc = Pinecone(
            api_key= PINECONE_API_KEY, 
            index_name = INDEX_NAME

        )
    return pc.Index(INDEX_NAME)

def delete_namespace(pinecone_index, namespace):
    """Deletes all vectors in the user's namespace after session ends."""
    stats = pinecone_index.describe_index_stats()
    if namespace in stats["namespaces"]:
        pinecone_index.delete(delete_all=True, namespace=namespace)
        print(f"Deleted namespace: {namespace}")

def namespace_exists(pinecone_index, namespace):
    namespaces = pinecone_index.describe_index_stats()['namespaces']
    return namespace in namespaces