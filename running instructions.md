Use waterinfo data scrapper:
python waterinfo-scrap.py

Use yarrrml-parser (a Node.js tool):
yarrrml-parser -i yarrrml/timeseries.yml -o generated-rdf/timeseries.rml.ttl 


Run RMLMapper to generate RDF:
java -jar rmlmapper.jar -m generated-rdf/yarrrml-mapping.rml.ttl -o generated-rdf/yarrrmlmapping.ttl

java -Xmx4g -jar rmlmapper.jar -m generated-rdf/timeseries.rml.ttl  -o generated-rdf/timeseriesmapping.ttl

Run RMLStreamer to generate LDES:
java -jar rmlstreamer.jar toFile -m generated-rdf/timeseries_ldes-mapping.rml.ttl -o generated-rdf/timeseriesmappingLDES.ttl

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
python data-postprocessing/prefixSuffix.py --graph generated-rdf/timeseriesmapping.ttl --prefix data-postprocessing/prefixes/prefix.csv --output generated-rdf/timeseries_with_prefixes.ttl

##################################################





