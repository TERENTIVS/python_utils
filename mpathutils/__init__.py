# __init__.py

from .funcs import (
    metapath_gen,        
    to_neo4j_path_q,
    metapath_featset_gen
)

# Optionally, define the __all__ variable
__all__ = [
    "metapath_gen", 
    "to_neo4j_path_q",
    "metapath_featset_gen"
    # ... list all exported functions
]
