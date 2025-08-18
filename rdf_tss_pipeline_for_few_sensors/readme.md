yarrrml-parser -i pipeline_for_few_sensors/rml_mapper.yml -o pipeline_for_few_sensors/rml_mapping.rml.ttl

java -Xmx4g -jar rmlmapper.jar -m pipeline_for_few_sensors/rml_mapping.rml.ttl  -o pipeline_for_few_sensors/rdf_generated_data.ttl

python RDF2TSS.py -i ../pipeline_for_few_sensors/rdf_generated_data.ttl -o ../pipeline_for_few_sensors/rdf2tss.ttl