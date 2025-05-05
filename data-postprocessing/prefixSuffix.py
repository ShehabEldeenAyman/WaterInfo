from rdflib import Graph
import pandas as pd
import argparse

def load_graph(graph_directory):
    try:
        print("Started loading graph...")
        g = Graph()
        g.parse(graph_directory, format="turtle")
        print("Graph loaded successfully.")
        return g
    except Exception as e:
        print(f"Error loading graph: {e}")
        raise

def load_prefix(prefix_directory):
    try:
        print("Started loading prefixes...")
        df = pd.read_csv(prefix_directory)
        prefixes = df.set_index('KEY')['VALUE'].to_dict()
        print("Prefixes loaded successfully.")
        return prefixes
    except FileNotFoundError:
        print("Error: Prefix CSV file not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: Prefix CSV file is empty.")
        raise
    except Exception as e:
        print(f"Error loading prefixes: {e}")
        raise

def bind_prefix(g, prefixes,output):
    try:
        print("Started binding prefixes and writing file...")
        for prefix, namespace in prefixes.items():
            g.bind(prefix, namespace)
        g.serialize(destination=output, format="turtle")
        print("File written successfully.")
    except Exception as e:
        print(f"Error binding prefixes or writing file: {e}")
        raise

def main():

    parser = argparse.ArgumentParser(description="Bind prefixes to RDF graph and serialize.")
    parser.add_argument('--graph', required=True, help='Path to the input graph file (TTL format)')
    parser.add_argument('--prefix', required=True, help='Path to the CSV file containing prefixes')
    parser.add_argument('--output', required=True, help='Path where the output TTL file will be saved')

    args = parser.parse_args()

    try:
        g = load_graph(args.graph) #"../generated-rdf/timeseriesmapping.ttl"
        prefixes = load_prefix(args.prefix) #'prefixes/prefix.csv'
        bind_prefix(g, prefixes,args.output) #"../generated-rdf/ttimeseries_with_prefixes.ttl"
    except Exception as e:
        print(f"Fatal error in main workflow: {e}")

if __name__ == "__main__":
    main()
