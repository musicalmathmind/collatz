class OrbitInfo:
    """
    A class to represent the orbit information of a number in the Collatz sequence.
    Attributes:
    ----------
    n : int
        The starting number of the Collatz sequence.
    first_drop : int
        The first drop in the Collatz sequence.
    first_orbit : list[int]
        The first orbit of the Collatz sequence.
    total_orbit : list[int]
        The total orbit of the Collatz sequence.
    stop_mod : int
        The modulus at which the sequence stops.
    stop_index : int
        The index at which the sequence stops.
        -------
        str
            A string representation of the OrbitInfo instance.
        """
    def __init__(self, n: int, first_drop: int, first_orbit: list[int], total_orbit: list[int], stop_mod: int, stop_index: int):
        self.n: int = n
        self.first_drop: int = first_drop
        self.first_orbit: list[int] = first_orbit
        self.total_orbit: list[int] = total_orbit
        self.stop_mod: int = stop_mod
        self.stop_index: int = stop_index

    def __repr__(self):
        return (f"OrbitInfo("
                f"first_drop={self.first_drop}, "
                f"first_orbit={self.first_orbit}, "
                f"total_orbit={self.total_orbit}, "
                f"stop_mod={self.stop_mod}, "
                f"stop_index={self.stop_index}, "
                f"n={self.n})")