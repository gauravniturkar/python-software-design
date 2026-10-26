"""
COMPOSITION: build objects out of smaller objects ("has a" instead of "is a").

Analogy: building a car from parts.
A car HAS an engine and HAS a music system. If you want a different engine,
you swap the engine. You don't design a whole new kind of car.
"""


# ---------------------------------------------------------------------------
# BEFORE: inheritance used for every combination ("class explosion")
# ---------------------------------------------------------------------------
class PetrolCarWithRadio: ...
class PetrolCarWithBluetooth: ...
class ElectricCarWithRadio: ...
class ElectricCarWithBluetooth: ...
# Add one more engine type and one more music type -> 9 classes. Then 16...


# ---------------------------------------------------------------------------
# AFTER: small parts plugged into one Car class
# ---------------------------------------------------------------------------
class PetrolEngine:
    def start(self) -> str:
        return "Vroom! Petrol engine started"


class ElectricMotor:
    def start(self) -> str:
        return "Hmm... electric motor silently started"


class Radio:
    def play(self) -> str:
        return "Playing FM 93.5"


class Bluetooth:
    def play(self) -> str:
        return "Playing your phone's playlist"


class Car:
    # The car HAS an engine and HAS a music system.
    def __init__(self, engine, music_system):
        self.engine = engine
        self.music_system = music_system

    def start_trip(self) -> None:
        print(self.engine.start())
        print(self.music_system.play())


if __name__ == "__main__":
    print("--- Petrol car with radio ---")
    Car(PetrolEngine(), Radio()).start_trip()

    print("--- Electric car with Bluetooth ---")
    Car(ElectricMotor(), Bluetooth()).start_trip()

    # Swapping a part while the program runs: easy with composition.
    car = Car(PetrolEngine(), Radio())
    car.music_system = Bluetooth()
    print("--- Upgraded the music system ---")
    car.start_trip()

# TRADE-OFFS
# + 2 engines + 2 music systems = 4 small classes, not 4 combined classes.
# + Parts can be swapped or tested on their own.
# - You write a little "wiring" code to plug parts together.
# Rule of thumb: "prefer composition over inheritance".
