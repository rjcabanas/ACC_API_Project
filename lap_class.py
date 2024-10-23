
class Laps:

    def __init__(self, session_details: str, lap_number: int, carModel: str):
        self.session_details = session_details
        self.lap_number = lap_number
        self.gas = []
        self.brake = []
        self.fuel = []
        self.gear = []
        self.steerAngle = []
        self.speed_kph = []
        self.carDamage = []
        self.brakeTemp = []
        self.tyre_coordinates = []
        self.current_lap_time = []
        self.carModel = carModel
