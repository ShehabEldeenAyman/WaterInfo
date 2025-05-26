import argparse
from rdflib import Graph, URIRef, Namespace
import pandas as pd
from collections import defaultdict

def load_graph(path: str) -> Graph:
    g = Graph()
    try:
        print("Started loading graph...")
        g.parse(path, format="turtle")
        print("Graph loaded successfully.")
    except Exception as e:
        print(f"Invalid RDF: {e}")
    return g

def build_triple_maps(graph: Graph):
    triples_map = {}
    triples_with_observation_map = defaultdict(list)
    triples_with_no_observation = []
    observation_subjects = set()
    observation_type = URIRef("http://www.w3.org/ns/sosa/Observation")
    rdf_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

    for s, p, o in graph:
        if s not in triples_map:
            triples_map[s] = []
        triples_map[s].append((p, o))

    for s, _, o in graph.triples((None, rdf_type, observation_type)):
        observation_subjects.add(s)

    for s in observation_subjects:
        for p, o in graph.predicate_objects(subject=s):
            triples_with_observation_map[s].append((p, o))

    for s, p, o in graph:
        if s not in triples_with_observation_map:
            triples_with_no_observation.append((s, p, o))

    return triples_map, triples_with_observation_map, triples_with_no_observation, observation_subjects

def load_prefixes(prefix_file: str) -> dict:
    df = pd.read_csv(prefix_file)
    prefix_dict = {row["Prefix"]: Namespace(str(row["URI"])) for _, row in df.iterrows()}
    return prefix_dict

def create_new_graph(prefixes: dict, observation_subjects: set, 
                     triples_with_no_observation: list,
                     triples_with_observation_map: dict) -> Graph:
    g = Graph()

    for prefix, uri in prefixes.items():
        g.bind(prefix, uri)

    base = prefixes.get("base", Namespace("http://example.com/"))
    LDES = prefixes.get("ldes", Namespace("https://w3id.org/ldes#"))
    sosa = prefixes.get("sosa", Namespace("http://www.w3.org/ns/sosa/"))
    tree = prefixes.get("tree", Namespace("https://w3id.org/tree#"))
    shapes = prefixes.get("shapes", Namespace("http://example.com/shapes/"))
    type_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

    g.add((base.EventStream, URIRef(type_ns), LDES.EventStream))
    g.add((base.EventStream, LDES.timestampPath, sosa.resultTime))
    g.add((base.EventStream, tree.shape, shapes.memberShape))

    for subj in observation_subjects:
        g.add((base.EventStream, tree.member, subj))

    for triple in triples_with_no_observation:
        g.add(triple)

    for subject, predicates in triples_with_observation_map.items():
        for predicate, obj in predicates:
            g.add((subject, predicate, obj))

    return g

def main():
    parser = argparse.ArgumentParser(description="Transform RDF and bind prefixes.")
    parser.add_argument("-input", required=True, help="Path to the input TTL file.")
    parser.add_argument("-prefix", required=True, help="Path to the CSV file with prefixes.")
    parser.add_argument("-output", required=True, help="Path to save the output TTL file.")
    
    args = parser.parse_args()

    graph = load_graph(args.input)
    triples_map, obs_map, no_obs, obs_subjects = build_triple_maps(graph)
    prefixes = load_prefixes(args.prefix)
    new_graph = create_new_graph(prefixes, obs_subjects, no_obs, obs_map)

    print("Started writing graph...")
    new_graph.serialize(destination=args.output, format="turtle")
    print("Graph written successfully.")

if __name__ == "__main__":
    main()
