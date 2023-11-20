import sbol3
import tyto

sbol3.set_namespace('http://sbolstandard.org/testfiles')

doc = sbol3.Document()

# ecoRI_comp = sbol3.Component('EcoRI_comp', 'http://purl.obolibrary.org/obo/PR_P00642', description='EcoRI restriction enzyme', name='EcoRI')
# xbaI_comp = sbol3.Component('XbaI_comp', 'http://purl.obolibrary.org/obo/PR_O68567', description='XbaI restriction enzyme', name='XbaI')

ecoRI_subcomp = sbol3.SubComponent('http://purl.obolibrary.org/obo/PR_P00642', description='EcoRI restriction enzyme', identity='EcoRI_subcomp')
xbaI_subcomp = sbol3.SubComponent('http://purl.obolibrary.org/obo/PR_O68567', description='XbaI restriction enzyme', identity='XbaI_subcomp')

sequence = sbol3.Sequence('seq' , elements='atgnnntaa', encoding=sbol3.IUPAC_DNA_ENCODING)
ecoRI_cutsite = sbol3.SequenceFeature(sbol3.Range(sequence, 2, 5), roles=[tyto.SO.restriction_enzyme_recognition_site], name='EcoRI_recognition_site')
xbaI_cutsite = sbol3.SequenceFeature(sbol3.Range(sequence, 7, 9), roles=[tyto.SO.restriction_enzyme_recognition_site], name='XbaI_recognition_site')

parent_sequence = sbol3.Component('parent', sbol3.SBO_DNA, features=[ecoRI_cutsite, xbaI_cutsite], sequences=[sequence], description='Parent sequence')

ecoRI_participation = sbol3.Participation(tyto.SBO.modifier, ecoRI_subcomp)
xbaI_participation = sbol3.Participation(tyto.SBO.modifier, xbaI_subcomp)
ecoRI_participation.cut_position = sbol3.ReferencedObject(ecoRI_participation, 'http://example.org/my_vis#cut_position', 0, 1, )
xbaI_participation.cut_position = sbol3.ReferencedObject(xbaI_participation, 'http://example.org/my_vis#cut_position', 0, 1, )
ecoRI_participation.cut_position = ecoRI_cutsite
xbaI_participation.cut_position = xbaI_cutsite

digestion = sbol3.Interaction(tyto.SBO.cleavage, name='digestion', participations=[
    sbol3.Participation(parent_sequence.identity, tyto.SBO.reactant),
    ecoRI_participation,
    xbaI_participation
])

# OPTION 1: Digestion as a component

digestion_component = sbol3.Component('digestion', sbol3.SBOL_COMPONENT, interactions=[digestion])

activity_usage = sbol3.Usage(digestion_component.identity, roles=[sbol3.SBOL_DESIGN])
in_silico_restriction = sbol3.Activity('restriction', types=sbol3.SBOL_DESIGN, usage=[activity_usage], description='Restriction digestion')
child_sequence = sbol3.Component('child', sbol3.SBO_DNA, derived_from=[parent_sequence.identity], generated_by=in_silico_restriction.identity)

doc.add(child_sequence)
doc.add(parent_sequence)
doc.add(in_silico_restriction)
doc.add(sequence)
doc.add(digestion_component)

doc.write('example2.ttl')
doc.write('example2.xml')

# OPTION 1: Digestion as a plan

doc2 = sbol3.Document()

cloning_strategy = sbol3.Plan('plan', description='Will contain fields describing position of cut')
cloning_strategy.activity = sbol3.ReferencedObject(cloning_strategy, 'http://example.org/my_vis#plan_activity', 0, 1, )
cloning_strategy.activity = digestion


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

doc2.add(child_sequence)
doc2.add(parent_sequence)
doc2.add(in_silico_restriction)
doc2.add(sequence)
doc2.add(api)
doc2.add(cloning_strategy)
doc2.add(digestion_component)

doc2.write('example2_alt.ttl')
doc2.write('example2_alt.xml')