import json
from os import listdir
from os.path import isfile, join

import numpy
results = []
for filename in listdir('.') :
    if isfile(join('.', filename)) and not filename.endswith('.py'):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            rates = data.get('rates')
            volatility_lists = {}
            if rates:
                for date, currencies in rates.items():
                    for currency, rate in currencies.items():
                        if volatility_lists.get(currency):
                            volatility_lists[currency].append(rate)
                        else:
                            volatility_lists[currency] = [rate]
                score = 0
                for list in volatility_lists.values():
                    score += numpy.std(list)
                results.append((filename, score))
results = sorted(results, key=lambda x: x[1])
for result in results:
    print(result)