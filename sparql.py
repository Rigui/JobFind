import sparql

q = ('SELECT DISTINCT ?station, ?orbits WHERE { '
     '?station a <http://dbpedia.org/ontology/SpaceStation> . '
     '?station <http://dbpedia.org/property/orbits> ?orbits . '
     'FILTER(?orbits > 50000) } ORDER BY DESC(?orbits)')
result = sparql.q('http://dbpedia.org/sparql', q)

print result.variables

for row in result:
    print 'row:', row
    values = sparql.unpack_row(row)
    print values[0], "-", values[1], "orbits"