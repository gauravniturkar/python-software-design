"""
INHERITANCE: a new class reuses and extends an existing class.

Analogy: an electric car.
An electric car IS A car. It still drives, brakes and has a model name.
It simply adds something new (charging) and changes how refuelling works.
"""


class Car:
    def __init__(self, model: str):
        self.model = model

    def drive(self) -> str:
        return f"{self.model} is driving"

    def refuel(self) -> str:
        return f"{self.model}: filling petrol"


class ElectricCar(Car):  # "ElectricCar is a Car"
    def __init__(self, model: str, battery_kwh: int):
        super().__init__(model)  # let the parent set up the shared parts
        self.battery_kwh = battery_kwh

    # OVERRIDE: same method name, different behaviour.
    def refuel(self) -> str:
        return f"{self.model}: charging a {self.battery_kwh} kWh battery"

    # EXTEND: something only electric cars can do.
    def regenerative_braking(self) -> str:
        return f"{self.model}: recovering energy while braking"


if __name__ == "__main__":
    petrol = Car("Swift")
    electric = ElectricCar("Nexon EV", battery_kwh=40)

    print(petrol.drive())          # inherited behaviour
    print(petrol.refuel())
    print(electric.drive())        # reused from Car, no new code needed
    print(electric.refuel())       # overridden
    print(electric.regenerative_braking())  # new behaviour

    print(isinstance(electric, Car))  # True: an ElectricCar is a Car

# WHEN NOT TO USE INHERITANCE
# Ask: "Is X truly a kind of Y, in every situation?"
#   ElectricCar -> Car      yes, good fit
#   Car -> Engine           no! a car HAS an engine; use composition instead
#
# TRADE-OFFS
# + Reuses shared code with very little effort.
# - Child classes are tightly tied to the parent. Changing the parent can
#   break every child.
# - Deep chains (A -> B -> C -> D) quickly become hard to follow.
#   Keep hierarchies shallow, usually one or two levels.
