import sbol3

sbol3.set_namespace('http://sbolstandard.org/testfiles')

doc = sbol3.Document()

comp = sbol3.Component('aComp', sbol3.SBO_DNA, description='example component')
subcomp = sbol3.SubComponent(comp.identity, description='example subcomponent', identity='aSubComp')

doc.add(comp)
doc.write('mini_example.ttl')
