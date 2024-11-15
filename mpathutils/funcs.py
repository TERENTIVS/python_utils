import itertools

def metapath_gen(source, target, triple_types, length):
    '''Source and target: string indicating node types in Neo4j format i.e. '(:NodeType)' 
    Triple types: list of triple types with each triple in form ['(:NodeType)','-[:RelType]->','(:NodeType)'] 
    Path length: integer.
    Relations need not be directed.
    Accumulates and prunes permutations of triple types to
    to retain only sequence of triples that matches the provided metapath parameters.'''
    paths = []
    for p in itertools.product(triple_types, repeat=length): # generate permutations
        if p[0][0] == source and p[-1][-1] == target: # check if starts and ends as desired
            # add n_source and n_target to p[0][0] and p[-1][-1]
            paths.append(p)
            for i in range(len(p)-1):
            # check if first node of next triple is always same as last node of preceding triple
                if p[i+1][0] != p[i][-1]:
                    paths.remove(p)
                    break
    return paths



def to_neo4j_path_q(source, target, triple_types, length):
    '''Converts sequence of triples into Neo4j input path'''
    paths = metapath_gen(source, target, triple_types, length)
    neo4j_paths = []
    for path in paths:
        flat = list(itertools.chain.from_iterable(path)) # flatten list
        indices_to_pop = list(range(3,len(flat),3)) # get duplicates - every 4th node in list
        for i in sorted(indices_to_pop, reverse=True): # remove indices from reverse
            flat.pop(i)
        
        flat[0] = '(n_source' + flat[0][1:]
        flat[-1] = '(n_target' + flat[-1][1:]
        
        node_counter = 0
        for i, thing in enumerate(flat):
            if i != 0 and thing != flat[-1] and thing[0] != '-' and thing[0] != '<': # replace with '==('
                node_counter += 1
                flat[i] = '(n_' + str(node_counter) + thing[1:]
        neo4j_path = ''
        for i in flat:
            neo4j_path +=i # build continuous string from flattened list
        neo4j_paths.append(neo4j_path)
    return neo4j_paths



def metapath_featset_gen(path_lengths, triple_types):
    '''Generate list of metapaths in Neo4j format.
    path_lengths: list of integers specifying lenghts of metapaths.
    triple_types: as in metapath_gen function.'''
    
    feats = []
    for length in path_lengths:
        feats.append(to_neo4j_path_q('(:Compound)', '(:Assay)', triple_types, length))

    feats_flat = list(itertools.chain.from_iterable(feats))
    
    return feats_flat
