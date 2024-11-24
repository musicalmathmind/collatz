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
    op_list : list[id]
        The list of operation ids performed (in order) to generate the orbit.
    
        -------
        str
            A string representation of the OrbitInfo instance.
        """
    def __init__(self, n: int, first_drop: int, first_orbit: list[int], total_orbit: list[int], stop_mod: int, stop_index: int, first_op_list: list[str], first_op_map: dict[str, int],total_op_list: list[str], total_op_map: dict[str, int]):
        self.n: int = n
        self.first_drop: int = first_drop
        self.first_orbit: list[int] = first_orbit
        self.total_orbit: list[int] = total_orbit
        self.stop_mod: int = stop_mod
        self.stop_index: int = stop_index
        self.first_op_list: list[str] = first_op_list
        self.first_op_map: dict[str, int] = first_op_map
        self.total_op_list: list[str] = total_op_list
        self.total_op_map: dict[str, int] = total_op_map

    def __repr__(self):
        return (f"OrbitInfo("
                f"first_drop={self.first_drop}, "
                f"first_orbit={self.first_orbit}, "
                f"total_orbit={self.total_orbit}, "
                f"stop_mod={self.stop_mod}, "
                f"stop_index={self.stop_index}, "
                f"n={self.n})")
    
    def get_first_op_count(self, op: str) -> int:
        """
        Get the count of a specific operation in the first orbit.
        Parameters:
        ----------
        op : str
            The operation to count.
        Returns:
        -------
        int
            The count of the operation in the first orbit.
        """
        return self.first_op_map.get(op, 0)
    
    def get_total_op_count(self, op: str) -> int:
        """
        Get the count of a specific operation in the orbit.
        Parameters:
        ----------
        op : str
            The operation to count.
        Returns:
        -------
        int
            The count of the operation in the orbit.
        """
        return self.total_op_map.get(op, 0)