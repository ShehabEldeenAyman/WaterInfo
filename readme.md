Use yarrrml-parser (a Node.js tool):
yarrrml-parser -i yarrrml/timeseries.yml -o generated-rdf/timeseriesmapping.rml.ttl

run RMLMapper to generate RDF:
java -jar rmlmapper.jar -m generated-rdf/timeseriesmapping.rml.ttl -o generated-rdf/timeseriesmapping.ttl

PySHACL for shacl shape evaluation:
pyshacl -s Shacl-shapes/shapes.ttl -d generated-rdf/timeseriesmapping.ttl 