Use yarrrml-parser (a Node.js tool):
yarrrml-parser -i yarrrml/timeseries.yml -o generated-rdf/timeseriesmapping.rml.ttl

Run RMLMapper to generate RDF:
java -jar rmlmapper.jar -m generated-rdf/timeseriesmapping.rml.ttl -o generated-rdf/timeseriesmapping.ttl

PySHACL for shacl shape evaluation:
pyshacl -s Shacl-shapes/shapes.ttl -d generated-rdf/timeseriesmapping.ttl 

Start a solid community server:
npx @solid/community-server

Upload data to Solid Server: 
curl -X POST -H "Slug:waterinfo" -H "Content-Type:text/turtle" --data-binary "@timeseriesmapping.ttl" http://localhost:3000/