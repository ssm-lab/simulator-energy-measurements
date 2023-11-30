import csv
import json
import pandas as pd
import optparse

states = { "AL": "Alabama", "AK": "Alaska", "AS": "American Samoa", "AZ": "Arizona", \
   "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", \
   "DE": "Delaware", "DC": "District Of Columbia", "FL": "Florida", "GA": "Georgia", \
   "HI": "Hawaii", "ID": "Idaho",  "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", \
   "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", \
   "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", \
   "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", \
   "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", \
   "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", \
   "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", \
   "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", \
   "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", \
   "U.S.": "U.S.", "_unit":"_unit", "_define": "_define"
}

def parse_args():
    """Parse command line arguments for year."""
    parser = optparse.OptionParser(description='find year')


    parser.add_option('-y', '--year', type='string', help='year for the data')

    (opts, args) = parser.parse_args()
    mandatories = ['year',]
    for m in mandatories:
        if not opts.__dict__[m]:
            print('mandatory option ' + m + ' is missing\n')
            parser.print_help()
            sys.exit()
    return opts


# take the arg from the script
opts = parse_args()
year = opts.year

""" Converts the US EIA csv file to json """
# Definiting structure of JSON
countries = {"_define": {
      "total":"TOTAL EMISSIONS",
      "coal":"COAL",
      "naturalGas":"NATURAL GAS",
      "petroleum":"PETROLEUM + OTHER LIQUIDS",
      "lowCarbon":"NUCLEAR, RENEWABLES + OTHERS",
      "units":"Quad Btu"
      }}
categories = ["total", "coal", "naturalGas", "petroleum",  "lowCarbon"]
category_index = -1
with open("./data/raw/" + year + "/international_data.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Skipping unnecessary headers
    [next(reader) for i in range(7)]
    for row in reader:
        # Category line - increment to move on to next category
        if len(row) == 3:
            category_index += 1
        # Country line
        elif len(row) == 5:
            if row[1] in countries:
                if row[-1] == "--" or row[-1] == "(s)":
                    row[-1] = 0
                countries[row[1]][categories[category_index]] = float(row[-1])
            else:
                if row[-1] == "--" or row[-1] == "(s)":
                    row[-1] = 0
                country_dict = {}
                country_dict[categories[category_index]] = float(row[-1])
                countries[row[1]] = country_dict
json_file = json.dumps(countries)
with open("./data/json/energy-mix-intl_" + year + ".json", 'w') as jsonwriter:
    jsonwriter.write(json_file)


""" Converts eGRID xlsx file to json """
# Table 3: CO2 Emissions

egrid = pd.ExcelFile("./data/raw/" + year + "/egrid.xlsx")
emissions = egrid.parse('Table 3')
emissions.to_csv("./data/csv/egrid_emissions_" + year + ".csv", sep=',')

state_carbon = {"_unit": "lbs/MWh"}
with open("./data/csv/egrid_emissions_" + year + ".csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    [next(reader) for i in range(4)]
    for row in reader:
        if row[2] != "":
            state_carbon[row[2]] = float(row[3])

# Handling the renaming of the states
state_carbon = { states[key]:value for key, value in state_carbon.items()}
json_file = json.dumps(state_carbon)
with open("./data/json/us-emissions_" + year + ".json", 'w') as jsonwriter:
    jsonwriter.write(json_file)

# Table 4: State Resource Mix
resource_mix = egrid.parse('Table 4')
resource_mix.to_csv("./data/csv/egrid_resource_mix_" + year + ".csv", sep=',')
state_resource_mix = {"_define":{
      "nameplateCapacity":"Nameplate Capacity (MW)",
      "netGeneration":"Net Generation (MWh)",
      "mix":{
         "coal":"Coal",
         "oil":"Oil",
         "gas":"Gas",
         "otherFossil":"Other Fossil",
         "nuclear":"Nuclear",
         "hydro":"Hydro",
         "biomass":"Biomass",
         "wind":"Wind",
         "solar":"Solar",
         "geothermal":"Geo-thermal",
         "unknown":"Other unknown/purchased fuel",
         "_units":"percentage"
      }}}

with open("./data/csv/egrid_resource_mix_" + year + ".csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    [next(reader) for i in range(3)]
    for row in reader:
        if row[2] != "":
            state_resource_mix[row[2]] = {
                "nameplateCapacity": float(row[3]),
                "netGeneration": float(row[4]),
                "mix": {
                    "coal": float(row[5]),
                    "oil": float(row[6]),
                    "gas": float(row[7]),
                    "otherFossil": float(row[8]),
                    "nuclear": float(row[9]),
                    "hydro": float(row[10]),
                    "biomass": float(row[11]),
                    "wind": float(row[12]),
                    "solar": float(row[13]),
                    "geothermal": float(row[14]),
                    "unknown": float(row[15])
                }}
state_resource_mix = { states[key]:value for key, value in state_resource_mix.items()}
json_file = json.dumps(state_resource_mix)
with open("./data/json/energy-mix-us_" + year + ".json", 'w') as jsonwriter:
    jsonwriter.write(json_file)
