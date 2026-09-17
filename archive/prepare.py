import pathlib,json,time,subprocess
manifest=json.load(open('sources/sample_listing.json'))
while True:
    ready=all((pathlib.Path('data')/x['name'].removeprefix('robotics/')).exists() and (pathlib.Path('data')/x['name'].removeprefix('robotics/')).stat().st_size==int(x['size']) for x in manifest['items'] if int(x.get('size',0)))
    if ready:break
    time.sleep(3)
time.sleep(2)
subprocess.run(['.venv/bin/python','repair_ledger.py'],check=True)
p=subprocess.Popen(['.venv/bin/python','inspect_sample.py'],stdout=open('screening.log','w'),stderr=subprocess.STDOUT)
subprocess.run(['.venv/bin/python','fetch_models.py'],check=True)
subprocess.run(['.venv/bin/python','fetch_calibration.py'],check=True)
print('screening exit:',p.wait())
