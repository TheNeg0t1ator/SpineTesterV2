from gui import *
from outputdataclass import *
from sensorCalc import *
import serial.tools.list_ports

app = userInterface()
app.showWindow()

set = ArrowSet(arrowcount=2, amountOfMeasurements=6)

sensors = SensorSet()

sensors.measureWeights()

spinetester = spineClass()


print("spine is: ")
spine = spinetester.forceToASTM(sensors)
print(spine)
print("Center of Gravity is: ")
cog = spinetester.forceToCoG(sensors)
print(cog)



# savestr = set.outputJson()
# with open('output.json', 'w') as f:
#     f.write(savestr)
