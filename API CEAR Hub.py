from datetime import *
import calendar
import requests as r


adict = {}
locDict = {}
active_sensors_within_past_day = []
weird_sensors_within_past_day = []
base_url = "https://api.sealevelsensors.org/v1.0/Things"
thing = r.get(base_url)
thing_data = thing.json()
name = ""
water_level_data = ""
for index in range(len(thing_data['value'])):
    item = thing_data['value'][index]
    name_of_thing = item['name']
    if "Water Level" in item['description'] and item["properties"]["status"] == "active":
        datastream = r.get(item["Datastreams@iot.navigationLink"])
        datastream_data = datastream.json()
        now = datetime.now(timezone.utc)
        tmrw = (now + timedelta(days = 1)).strftime('%Y-%m-%d')
        now = now.strftime('%Y-%m-%d')
        ind = 0
        for i in range(len(datastream_data['value'])):
            if datastream_data['value'][i]['name'] == "Water Level":
                ind = i
        coordinates = datastream_data['value'][ind]['observedArea']['coordinates']
        locDict[name_of_thing] = coordinates
        water_level_url = datastream_data['value'][ind]["Observations@iot.navigationLink"] + "?$filter=phenomenonTime%20ge%20" + now + "T00:00:00.000Z%20and%20phenomenonTime%20le%20" + tmrw + "T00:00:00.000Z"
        water_level = r.get(water_level_url)
        past_day_water_level_data = water_level.json()
        num = past_day_water_level_data['@iot.count']
        if num == 0:
            weird_sensors_within_past_day.append(name_of_thing)
            # print(f"Error(no data collected in the past day) for {name_of_thing}")
        else:
            active_sensors_within_past_day.append(name_of_thing)
            while num > 100:
                past_day_water_level_data = r.get(past_day_water_level_data['@iot.nextLink']).json()
                num -= 100
            last_data_point = past_day_water_level_data['value'][num - 1]
            adict[name_of_thing] = last_data_point



def timingTest(name):
    last_data_point = adict[name]
    phenomTime = last_data_point['phenomenonTime']
    date = datetime.strptime(phenomTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    now = datetime.now(timezone.utc)
    six_ago = (now - timedelta(minutes = 6))
    date_str = date.isoformat()
    six_ago_str = six_ago.isoformat()
    if six_ago_str > date_str:
        print(f"Timing Test Failed for {name}")
    else:
        print(f"Timing Test Passed for {name}")

for i in active_sensors_within_past_day:
    timingTest(i)
for i in weird_sensors_within_past_day:
    print(f"No data since midnight for {i}")

def locationTest(name):
    last_data_point = adict[name]
    coordinate_link = r.get(last_data_point['FeatureOfInterest@iot.navigationLink'])
    coords = coordinate_link.json()
    coordinates = coords['feature']['coordinates']
    if coordinates != locDict[name]:
        print(f"Location Test Failed for {name}")
    else:
        print(f"Location Test Passed for {name}")
    
'''

def grossRangeTest(name):
    last_data_point = adict[name]
    result = float(last_data_point['result'])
    if result > 1.0 or result < -1.0:
        print(f"Gross Range Test Failed for {name}")
    else:
        print(f"Gross Range Test Passed for {name}")




def climatologyTest(name):
    seasonDict = {}
    last_data_point = adict[name]
    result = float(last_data_point['result'])
    if result > 1.0 or result < -1.0:
        print(f"Gross Range Test Failed for {name}")
    else:
        print(f"Gross Range Test Passed for {name}")



def syntaxTest(name, data):
    if data['@iot.selfLink'][:32] != "https://api.sealevelsensors.org/":
        print(f"Syntax Test Failed at Self Link for {name}")
        return
    elif data["@iot.id"].isdigit() == False:
        print(f"Syntax Test Failed at ID for {name}")
        return
    elif data["result"].isfloat() == False:
        print(f"Syntax Test Failed at Result for {name}")
        return
    elif data['Datastream@iot.navigationLink'][:32] != "https://api.sealevelsensors.org/" and data['Datastream@iot.navigationLink'][-11:] != "Datastreams":
        print(f"Syntax Test Failed at Datastream Link for {name}")
        return
    elif data['FeatureOfInterest@iot.navigationLink'][:32] != "https://api.sealevelsensors.org/" and data['Datastream@iot.navigationLink'][-18:] != "FeatureOfInterest":
        print(f"Syntax Test Failed at Feature of Interest Link for {name}")
        return
    else:
        print(f"Syntax Text Passed for {name}!")
    
##            while '@iot.nextLink' in water_level_data:
##                final_data = r.get(water_level_data['@iot.nextLink'])
##                water_level_data = final_data.json()
##            for observation in water_level_data['value']:
##                phenomTime = observation['phenomenonTime'][:10]
##                date_phenom = datetime.date(int(phenomTime[:4]), int(phenomTime[5:7]), int(phenomTime[8:]))
##                if date_phenom >= one_week_ago:
##                    if abs(observation['phenomenonTime'][:10] - observation['resultTime'][:10]) <= 0.001:
##                        print(f"{thing_data['description']}:passed")



today_date = datetime.today().strftime('%Y-%m-%d')
 
recent_links = []
for link in links_list:
    # Replace the second date with today's date
    recent_url = f'https://api.sealevelsensors.org/v1.0/Datastreams({link[49]})/Observations?$filter=phenomenonTime%20ge%202024-09-15T00:00:00.000Z%20and%20phenomenonTime%20le%20{today_date}T00:00:00.000Z'
    recent_links.append(recent_url)
print(recent_url)

'''



