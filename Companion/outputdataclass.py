import json

class ArrowMeasurement:
    forces:list[float] = [0.0,0.0]
    angle:float = 0.0
    mode23:bool = False
    def __str__(self) -> str:
        return f"force: {self.forces}, Angle: {self.angle} 23 inch: {self.mode23}"
    def getAverageforce(self)->float:
        return (self.forces[0] + self.forces[1]) / 2

class Arrow:
    measurements: list[ArrowMeasurement]
    id: int  # Add an id attribute to Arrow
    CoG: float
    weight: float
    def __init__(self, id: int, amountOfMeasurements: int = 0) -> None:
        self.CoG = 0.0
        self.weight = 0.0
        self.id = id  # Assign an id when creating an Arrow
        if amountOfMeasurements > 0:
            self.measurements = [ArrowMeasurement() for _ in range(amountOfMeasurements)]
            angle_increment = 360 / amountOfMeasurements
            for i in range(amountOfMeasurements):
                self.measurements[i].angle = i * angle_increment
        else:
            self.measurements = [ArrowMeasurement() for _ in range(6)]
            angle_increment = 360 / 6
            for i in range(6):
                self.measurements[i].angle = i * angle_increment
    
    def __str__(self) -> str:
        output = f"Arrow {self.id} measurements: "
        for i in range(len(self.measurements)):
            output += f"\n{i}: {self.measurements[i]}"
        return output
    
    def addMeasurement(self, force:list[float], angle:float):
        self.measurements.append(ArrowMeasurement())
        self.measurements[-1].forces = force
        self.measurements[-1].angle = angle
    
    def removeMeasurement(self, index:int):
        self.measurements.pop(index)
    
    def getMeasurement(self, index:int):
        return self.measurements[index]	
    def getAllMeasurements(self):
        return self.measurements
    def getMeasurementCount(self):
        return len(self.measurements)
    def clearMeasurements(self):
        self.measurements.clear()
    def modifyMeasurement(self, index:int, force:list[float], angle:float):
        self.measurements[index].forces = force
        self.measurements[index].angle = angle
    def getforce(self, index:int):
        return self.measurements[index].forces
    def getAverageforce(self):
        sum = 0
        for i in range(len(self.measurements)):
            sum += self.measurements[i].getAverageforce()
        return sum / len(self.measurements)


class ArrowSet:
    arrows: list[Arrow]

    def __init__(self, arrowcount: int = 1, amountOfMeasurements: int = 1) -> None:
        self.arrows = [Arrow(id=i + 1, amountOfMeasurements=amountOfMeasurements) for i in range(arrowcount)]
    
    def addArrow(self):
        new_id = len(self.arrows) + 1  # Assign a new id for the arrow
        self.arrows.append(Arrow(id=new_id))
    
    def removeArrow(self, index: int):
        self.arrows.pop(index)
    
    def getArrow(self, index: int):
        return self.arrows[index]
    
    def getAllArrows(self):
        return self.arrows
    
    def getArrowCount(self):
        return len(self.arrows)
    
    def clearArrows(self):
        self.arrows.clear()
    
    def modifyArrow(self, index: int, arrow: Arrow):
        self.arrows[index] = arrow
    
    def getAverageforce(self, index: int):
        return self.arrows[index].getAverageforce()

    def outputJson(self):
        # Creating a dictionary to represent all arrows and their measurements
        arrow_data = []
        for arrow in self.arrows:
            measurements = []
            for measurement in arrow.getAllMeasurements():
                measurements.append({
                    'force_1': measurement.forces[0],
                    'force_2': measurement.forces[1],
                    'angle': measurement.angle,
                    'mode23': measurement.mode23
                })
            arrow_data.append({
                'arrow-id': arrow.id,  # Include the arrow ID in the JSON output
                'cog': arrow.CoG,
                'weight': arrow.weight,
                'measurements': measurements
            })
        
        # Serializing the arrow_data list into a JSON formatted string
        return json.dumps(arrow_data, indent=4)
