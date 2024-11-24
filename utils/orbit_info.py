class OrbitInfo:
    """
    Represents the detailed orbit information of a number in the Collatz sequence.

    The Collatz sequence describes the iterative process starting from a positive integer n:
    - If n is even, divide it by 2.
    - If n is odd, multiply it by 3 and add 1.

    This class captures key theoretical aspects and computational properties of the sequence, 
    providing a structured representation of its behavior.

    Attributes:
    ----------
    n : int
        The starting number of the Collatz sequence.
    
    first_drop : int
        The First Drop value, representing the number of steps required for the sequence to 
        first reach a value smaller than the starting number, n. This aligns with the FirstDrop(n) 
        concept in Collatz theory.

    first_orbit : list[int]
        The sequence of numbers (orbit) in the Collatz sequence from n to the First Drop value. 
        These numbers define the "First Drop Orbit," encapsulating the initial behavior of the sequence.

    total_orbit : list[int]
        The complete sequence of numbers (orbit) in the Collatz sequence starting at n and 
        terminating at 1. This sequence represents the full traversal of the Collatz process.

    stop_mod : int
        The Stopping Modulus, representing the modular group in which the starting number resides 
        based on its First Drop value. It reflects the periodic structure of numbers with the same First Drop.

    stop_index : int
        The Stopping Index, uniquely identifying the number's position within its modular group 
        as determined by the Stopping Modulus. It combines group-level modularity with local offsets 
        to specify a unique location in modular space.

    Methods:
    --------
    __repr__():
        Provides a string representation of the OrbitInfo object, including all key attributes 
        for easy inspection and debugging.
    """
    def __init__(self, n: int, first_drop: int, first_orbit: list[int], total_orbit: list[int], stop_mod: int, stop_index: int):
        """
        Initializes the OrbitInfo instance.

        Parameters:
        ----------
        n : int
            The starting number of the Collatz sequence.
        first_drop : int
            The First Drop value for the sequence.
        first_orbit : list[int]
            The sequence of numbers in the First Drop Orbit.
        total_orbit : list[int]
            The full sequence of numbers in the Total Orbit.
        stop_mod : int
            The Stopping Modulus for the First Drop value.
        stop_index : int
            The Stopping Index within the modular group.
        """
        self.n: int = n
        self.first_drop: int = first_drop
        self.first_orbit: list[int] = first_orbit
        self.total_orbit: list[int] = total_orbit
        self.stop_mod: int = stop_mod
        self.stop_index: int = stop_index

    def __repr__(self):
        """
        Returns a string representation of the OrbitInfo instance.

        This includes all key attributes for inspection or debugging.
        """
        return (f"OrbitInfo("
                f"n={self.n}, "
                f"first_drop={self.first_drop}, "
                f"first_orbit={self.first_orbit}, "
                f"total_orbit={self.total_orbit}, "
                f"stop_mod={self.stop_mod}, "
                f"stop_index={self.stop_index})")
