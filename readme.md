Use yarrrml-parser (a Node.js tool):
yarrrml-parser -i yarrrml/timeseries.yml -o generated-rdf/timeseriesmapping.rml.ttl

Run RMLMapper to generate RDF:
java -jar rmlmapper.jar -m generated-rdf/timeseriesmapping.rml.ttl -o generated-rdf/timeseriesmapping.ttl

PySHACL for shacl shape evaluation:
pyshacl -s Shacl-shapes/shapes.ttl -d generated-rdf/timeseriesmapping.ttl 

Start a solid community server:
npx @solid/community-server

Install a local solid community server:
git clone https://github.com/CommunitySolidServer/CommunitySolidServer.git
cd CommunitySolidServer
npm ci
npm start 

Start Penny:
npm run dev

Upload data to Solid Server: 
curl -X POST -H "Slug:waterinfo" -H "Content-Type:text/turtle" --data-binary "@timeseriesmapping.ttl" http://localhost:3000/

Use the prefix post-prossing:
python prefixSuffix.py --graph ../generated-rdf/timeseriesmapping.ttl --prefix prefixes/prefix.csv --output ../generated-rdf/ttimeseries_with_prefixes.ttl