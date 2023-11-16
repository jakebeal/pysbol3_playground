import sbol3
import tyto

sbol3.set_namespace('http://sbolstandard.org/testfiles')

doc = sbol3.Document()


sequence = sbol3.Sequence('seq' , elements='atgnnntaa', encoding=sbol3.IUPAC_DNA_ENCODING)
cut_site = sbol3.SequenceFeature(sbol3.Range(sequence, 0, 10), type_uri=tyto.SO.restriction_enzyme_recognition_site, name='EcoRI_recognition_site')

parent_sequence = sbol3.Component('parent', sbol3.SBO_DNA, features=[cut_site], sequences=[sequence], description='Parent sequence')



cloning_strategy = sbol3.Plan('plan', description='Will contain fields describing position of cut')
cloning_strategy.enzyme_name = sbol3.TextProperty(cloning_strategy, 'http://example.org/my_vis#enzyme_name', 0, 1, )
cloning_strategy.cut_position = sbol3.ReferencedObject(cloning_strategy, 'http://example.org/my_vis#cut_position', 0, 1, )
cloning_strategy.enzyme_name = 'EcoRI'
cloning_strategy.cut_position = cut_site




api = sbol3.Agent('api', description='Receives input seq and activity and returns child')
api.api_version = sbol3.TextProperty(api, 'http://example.org/my_vis#api_version', 0, 1, )
api.api_url = sbol3.TextProperty(api, 'http://example.org/my_vis#api_url', 0, 1, )
api.request_method = sbol3.TextProperty(api, 'http://example.org/my_vis#request_method', 0, 1, )
api.api_version = '1.0'
api.api_url = 'http://example.org/api'
api.request_method = 'POST'

activity_association = sbol3.Association(agent=api, roles=[sbol3.SBOL_DESIGN], plan=cloning_strategy)

activity_usage = sbol3.Usage(parent_sequence.identity, roles=[sbol3.SBOL_DESIGN])
in_silico_restriction = sbol3.Activity('in_silico_restriction', types=sbol3.SBOL_DESIGN, usage=[activity_usage], association=activity_association, description='Simulation of restriction digestion')

child_sequence = sbol3.Component('child', sbol3.SBO_DNA, derived_from=[parent_sequence.identity], generated_by=in_silico_restriction.identity)
# child_sequence.derived_from = [parent_sequence]
doc.add(child_sequence)
doc.add(parent_sequence)
doc.add(in_silico_restriction)
doc.add(api)
doc.add(cloning_strategy)
doc.add(sequence)

doc.write('example1.ttl')
doc.write('example1.xml')


