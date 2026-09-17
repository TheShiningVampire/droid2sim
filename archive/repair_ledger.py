import ast,json,re,pathlib
p=pathlib.Path('LOG.md')
entries=[]
for s in p.read_text().splitlines():
    if 'Download result: {' in s:
        entries.append(ast.literal_eval(s.split('Download result: ',1)[1].split('; cumulative',1)[0]))
pathlib.Path('downloads.json').write_text(json.dumps(entries,indent=2))
print('Reconciled',len(entries),'downloads:',sum(x['bytes'] for x in entries))
with p.open('a') as f:f.write('\n- Reconciled download ledger from per-transfer LOG.md entries: concurrent documentation/sample transfers could overwrite the JSON ledger; the append-only log preserved each result. Serialize future transfers.\n')
