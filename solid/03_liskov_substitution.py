"""
L - LISKOV SUBSTITUTION PRINCIPLE (LSP)
"If code works with a parent class, it must also work with any child class."

Analogy: a substitute teacher.
When the regular teacher is away, the substitute should still take the class.
If the substitute just cancels every lesson, they are not a real substitute,
even if they have the job title.

PROBLEM
A child class "is a" parent on paper, but it breaks promises the parent made.
Code that worked fine with the parent suddenly crashes with the child.
"""


# ---------------------------------------------------------------------------
# BEFORE: a child class that breaks the parent's promise
# ---------------------------------------------------------------------------
class Bird:
    def fly(self) -> str:
        return "Flying high"


class Sparrow(Bird):
    def fly(self) -> str:
        return "Sparrow flapping quickly"


class Penguin(Bird):
    def fly(self) -> str:
        # The parent promised "every Bird can fly". Penguin breaks that.
        raise NotImplementedError("Penguins can't fly!")


def start_migration(birds: list[Bird]) -> None:
    for bird in birds:
        print(bird.fly())  # crashes when it reaches the Penguin


# ---------------------------------------------------------------------------
# AFTER: only promise what every child can actually do
# ---------------------------------------------------------------------------
class Animal:
    def move(self) -> str:
        return "Moving"


class FlyingBird(Animal):
    def move(self) -> str:
        return self.fly()

    def fly(self) -> str:
        return "Flying high"


class Eagle(FlyingBird):
    def fly(self) -> str:
        return "Eagle soaring"


class SwimmingPenguin(Animal):
    def move(self) -> str:
        return "Penguin swimming fast"


def move_everyone(animals: list[Animal]) -> None:
    # Every Animal really can `move`, so any child is a safe substitute.
    for animal in animals:
        print(animal.move())


if __name__ == "__main__":
    try:
        start_migration([Sparrow(), Penguin()])
    except NotImplementedError as error:
        print(f"[before] Crashed: {error}")

    print("[after]")
    move_everyone([Eagle(), SwimmingPenguin()])

# QUICK CHECK FOR LSP
# A child class should NOT:
#   - raise errors the parent never raises
#   - accept fewer kinds of input than the parent
#   - return something the caller wouldn't expect
#
# TRADE-OFFS
# + Code that uses the parent class never gets nasty surprises.
# - Sometimes you need to rethink the hierarchy (as we did above).
# - If a subclass keeps fighting its parent, composition is often a better fit.
