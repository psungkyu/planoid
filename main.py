import spidev, requests, json
import time
from sensors import SoilMoistureSensor

delay = 1 
edgexip = "blueshift.xslab.co.kr"
edgexport = "56382"

name = "Carnation"
name2 = "Basil"
name3 = "Rosemary"
name4 = "Begonia"

# Open Spi Bus
spi = spidev.SpiDev()
spi.open(0,0) # open(bus, device)
spi.max_speed_hz = 1000000 # set transfer speed

# To read SPI data from MCP3008 chip
# Channel must be 0~7 integer
def readChannel(channel): 
  val = spi.xfer2([1, (8+channel)<<4, 0])
  data = ((val[1]&3) << 8) + val[2]
  return data
  # return 1023 - data


def sendSensorData(humidity_value, humidity_percentage):
  if humidity_value is None or humidity_percentage is None:
    print('Read Error!')
    time.sleep(100)
  else:
    url_humidity_value = 'http://%s:%s/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/temperature' % (edgexip, edgexport)
    url_humidity_percentage = 'http://%s:%s/api/v1/resource/Temp_and_humidity_sensor_cluster_01/humidity' % (edgexip, edgexport)

    #hum_val = str(humidity_value)
    #hum_percentage_val = str(humidity_percentage)

    headers = {'content-type' : 'application/json'}
    response = requests.post(url_humidity_value, data=json.dumps(int(humidity_value)), headers=headers, verify=False)
    response = requests.post(url_humidity_percentage, data=json.dumps(int(humidity_percentage)), headers=headers, verify=False)


def convertPercent(data, sensor, flag):
  if flag:
    return 100.0 - round((((data - sensor.get_lower_bound_score) * 100) / float(sensor.get_upper_bound_score - sensor.get_lower_bound_score)), 1)
  
  else:
    return round((((data - sensor.get_lower_bound_score) * 100) / float(sensor.get_upper_bound_score - sensor.get_lower_bound_score)), 1)


def main():
	sensor = SoilMoistureSensor(0, name, 0, 555)
	sensor2 = SoilMoistureSensor(1, name2, 275, 910)
	sensor3 = SoilMoistureSensor(2, name3, 325, 908)
	sensor4 = SoilMoistureSensor(3, name4, 330, 920)
	
	try:
		while True:
			val = readChannel(sensor.get_channel_number)
			converted_percent_score = convertPercent(val, sensor, False)

			val2 = readChannel(sensor2.get_channel_number)
			converted_percent_score = convertPercent(val, sensor, False)
			
			val3 = readChannel(sensor3.get_channel_number)
			converted_percent_score = convertPercent(val, sensor, False)
			
			val4 = readChannel(sensor4.get_channel_number)
			converted_percent_score = convertPercent(val, sensor, False)

			print(name, " | lower_bound : ", sensor.get_lower_bound_score, " | cur_val : ", val, " | upper_bound : ", sensor.get_upper_bound_score, " | Percentage : ", convertPercent(val, sensor, False),"%")
			print(name2, " | lower_bound : ", sensor2.get_lower_bound_score, " | cur_val : ", val2, " | upper_bound : ", sensor2.get_upper_bound_score, " | Percentage : ", convertPercent(val2, sensor2, True),"%")
			print(name3, " | lower_bound : ", sensor3.get_lower_bound_score, " | cur_val : ", val3, " | upper_bound : ", sensor3.get_upper_bound_score, " | Percentage : ", convertPercent(val3, sensor3, True),"%")
			print(name4, " | lower_bound : ", sensor4.get_lower_bound_score, " | cur_val : ", val4, " | upper_bound : ", sensor4.get_upper_bound_score, " | Percentage : ", convertPercent(val4, sensor4, True),"%")
			
			sendSensorData(val, converted_percent_score)
			print()
			
			
			time.sleep(delay)
	
	except KeyboardInterrupt:
		spi.close()
		print("Keyboard Interrupt!!!!")

if __name__=="__main__":
	main()
