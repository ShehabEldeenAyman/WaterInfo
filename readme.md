Use yarrrml-parser (a Node.js tool):
yarrrml-parser -i timeseries.yml -o timeseriesmapping.rml.ttl

run RMLMapper to generate RDF:
java -jar rmlmapper.jar -m timeseriesmapping.rml.ttl -o timeseriesmapping.ttl

