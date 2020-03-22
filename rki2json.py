#!/usr/bin/env python

import json
import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="input file")
    args = parser.parse_args()
    return args.input

ToDo = 4

def rki2json(jdata):
    converted = []
    for ds in jdata['features']:
        a = ds['attributes']

        pat = re.compile("A(\d*)\-A(\d*)")
        m = pat.search(a['Altersgruppe'])

        fall = a['AnzahlFall']
        todesfall = a['AnzahlTodesfall']

        infected = fall - todesfall
        dead = todesfall

        adm = ["DE"]
        if a['IdBundesland'] < 10:
            adm.append('0' + str(a['IdBundesland']))
        else:
            adm.append(str(a['IdBundesland']))
        lk = int(a['IdBundesland']) % 100
        if lk < 10:
            lk = '00' + str(lk)
        elif lk < 100:
            lk = '0' + str(lk)
        adm.append(lk)

        nd = {
            'date': int(a['Meldedatum'] / 1000), # The ts in the RKI is is ms
            'adm': [ 'DE', a['IdBundesland'], a['IdLandkreis'] ],
            'gender': 'm' if a['Geschlecht'] == 'M' else 'f',
            'infected': infected,
            'deaths': dead,
            'source': 'RKI'
            }

        if m:
            nd['ageRange'] =  {
                'lower': int(m.group(1)),
                'upper': int(m.group(2)),
            }

        converted.append(nd)
    return converted

def main():
    input_filename = parse_args()
    with open(input_filename, "r") as fd:
        jdata = json.load(fd)
    cd = rki2json(jdata)
    print(json.dumps(cd))

if __name__ == '__main__':
    main()
