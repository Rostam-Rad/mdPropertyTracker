from django.shortcuts import render
import requests

md_response = requests.get('https://geodata.md.gov/imap/rest/services/PlanningCadastre/MD_PropertyData/MapServer/0/query?where=1%3D1&outFields=nfmimpvl,nfmlndvl,zipcode,mdpvdate&outSR=4326&f=json')
if md_response.status_code != 200: print('could not reach URL')

md_json = md_response.json()

avg_values = {} #holds avg values of property by zipcode
num_valuations = {} #holds num of properties by zipcode
just_zips = []
just_vals = []

#getting avg valuation by zip codes
for line in md_json['features']:

    # add to existing sum of valuations
    if dict.__contains__(avg_values, line['attributes']['zipcode'])\
            and not line['attributes']['nfmimpvl'] is None:
        avg_values[line['attributes']['zipcode']] += line['attributes']['nfmimpvl']
        num_valuations[line['attributes']['zipcode']] += 1

    #add new zip:valuation pair to dict
    elif not line['attributes']['zipcode'] is None\
            and not line['attributes']['nfmimpvl'] is None:
        avg_values[line['attributes']['zipcode']] = line['attributes']['nfmimpvl']
        num_valuations[line['attributes']['zipcode']] = 1

# Calculating averages
i = 0
for zip in num_valuations:
    avg_values[zip] = int(avg_values[zip] / num_valuations[zip])
    just_zips.insert(i, zip)
    just_vals.insert(i, avg_values[zip])
    i += 1

# Create your views here.
def home(request):
    context = {
        'avg_values': avg_values,
        'just_vals': just_vals,
        'just_zips': just_zips
    }
    return render(request, 'avgs/home.html', context)

def about(request):
    return render(request, 'avgs/about.html')
