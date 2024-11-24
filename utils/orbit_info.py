class OrbitInfo:
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
