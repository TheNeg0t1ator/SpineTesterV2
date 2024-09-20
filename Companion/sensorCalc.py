from outputdataclass import *
from uartSensor import *

astmFactor:float = 440000.0
SUPPORTSPACING28 = 711.2
SUPPORTSPACING23 = 584.2

# some test data
weighttest1:float = 585.0
weighttest2:float = 582.0


class SensorClass:
    sensorid:int
    weights:list[float]
    def __init__(self, sensorid:int) -> None:
        self.sensorid = sensorid
    def getWeight(self) -> float:
        #TODO change the return values if the uart works
        if self.sensorid == 1:
            return weighttest1
            # return self.weights[0]
        if self.sensorid == 2:
            return weighttest2
            # return self.weights[1]
    def measureWeight(self, UART:uartSensor) -> None:
        self.weights = UART.getUART()
        pass
    
class SensorSet:
    sensors: list[SensorClass]
    weights: list[float] = [0.0,0.0]
    
    def __init__(self):
        self.sensors = [SensorClass(sensorid=i + 1) for i in range(2)]

    def getSensors(self):
        return self.sensors
    def getAverageForce(self)->float:
        sum = 0
        for i in range(len(self.sensors)):
            sum += self.sensors[i].getWeight()
        return sum / len(self.sensors)
    def measureWeights(self):
        for i in range(len(self.sensors)):
            #self.sensors[i].measureWeight()
            self.weights[i] = self.sensors[i].getWeight()
    def getWeights(self)->list[float]:
        self.measureWeights()
        return self.weights

class spineClass:
    
    
    def forceToASTM(self, sensors:SensorSet) -> float:
        force = sensors.getAverageForce()
        output:float = astmFactor/force 
        return output
    
    def forceToCoG(self, sensors:SensorSet) -> float:
        HalfSupportSpacing:float = SUPPORTSPACING28/2
        CoG:float = 0.0
        
        weights = sensors.getWeights()
        front_weight = weights[0]
        back_weight = weights[1]
        
        #(back - front) * half spacing / (back + front) + half spacing
        CoG = (back_weight - front_weight) * HalfSupportSpacing / (back_weight + front_weight) + HalfSupportSpacing
        
        return CoG