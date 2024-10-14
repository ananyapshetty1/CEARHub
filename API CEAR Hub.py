

from datetime import *
import calendar
import requests as r


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
        yest = (now - timedelta(days = 1)).strftime('%Y-%m-%d')
        now = now.strftime('%Y-%m-%d')
        ind = 0
        for i in range(len(datastream_data['value'])):
            if datastream_data['value'][i]['name'] == "Water Level":
                ind = i
        water_level_url = datastream_data['value'][ind]["Observations@iot.navigationLink"] + "?$filter=phenomenonTime%20ge%20" + yest + "T00:00:00.000Z%20and%20phenomenonTime%20le%20" + now + "T00:00:00.000Z"
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
            # print(name_of_thing)
            # print(last_data_point)
print(f"weird: {weird_sensors_within_past_day}")
print(f"active: {active_sensors_within_past_day}")

'''

#assuming that the timing gap is meant to be every day
def timingTest(name, data):
    string_data_time = data['resultTime']
    string_data_time = string_data_time.replace("Z", "+00:00")  # Replace Z with +00:00 for UTC
    datetime_obj = datetime.fromisoformat(string_data_time)
    now = datetime.now(timezone.utc)
    yesterday = (now - timedelta(days = 1))
    print(yesterday)
    if datetime_obj < yesterday:
        print(f"Timing Test Failed for {name}")
    else:
        print(f"Timing Test Passed for {name}")

timingTest(name_of_thing, first_sensor_data)

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

