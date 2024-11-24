from orbit_info import OrbitInfo
import math
import random 
from typing import Callable, Dict, List, Tuple

fully_supported_option_names = ['3x_plus_1']

class OrbitOptions:
    def __init__(
        self,
        name: str,
        min_n: int, 
        should_halt: Callable[[int], bool], 
        should_decrease: Callable[[int], bool], 
        should_increase: Callable[[int], bool], 
        decrease: Callable[[int], None], 
        increase: Callable[[int], None],  
        append_to_orbit: Callable[[int, List[int]], None]
    ):
        self.name: str = name
        self.min_n: int = min_n
        self.should_halt: Callable[[int], bool] = should_halt
        self.should_decrease: Callable[[int], bool] = should_decrease
        self.should_increase: Callable[[int], bool] = should_increase
        self.decrease: Callable[[int], None] = decrease
        self.increase: Callable[[int], None] = increase
        self.append_to_orbit: Callable[[int, List[int]], None] = append_to_orbit

def create_collatz_3x_plus_1_options() -> OrbitOptions:
    def should_halt(n: int) -> bool:
        return n == 1

    def should_decrease(n: int) -> bool:
        return n % 2 == 0

    def should_increase(n: int) -> bool:
        return n % 2 != 0

    def decrease(n: int) -> int:
        return n // 2

    def increase(n: int) -> int:
        return 3 * n + 1

    def append_to_orbit(n: int, orbit: List[int]):
        orbit.append(n)
        

    return OrbitOptions('3x_plus_1', 1, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)

def create_collatz_3x_plus_3_options() -> OrbitOptions:
    def should_halt(n: int) -> bool:
        return n == 3

    def should_decrease(n: int) -> bool:
        return n % 2 == 0

    def should_increase(n: int) -> bool:
        return n % 2 != 0

    def decrease(n: int) -> int:
        return n // 2

    def increase(n: int) -> int:
        return 3 * n + 3

    def append_to_orbit(n: int, orbit: List[int]):
        orbit.append(n)

    return OrbitOptions('3x_plus_3', 3, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)

def create_collatz_probabilistic_options(p: float) -> OrbitOptions:
    def should_halt(n: int) -> bool:
        return n <= 3

    def should_decrease(n: int) -> bool:
        return n % 2 == 0

    def should_increase(n: int) -> bool:
        return n % 2 != 0

    def decrease(n: int) -> int:
        return n // 2

    def increase(n: int) -> int:
        r = random.random()
        if r < p:
            return 3 * n + 1
        else:
            return 3 * n + 3

    def append_to_orbit(n: int, orbit: List[int]):
        orbit.append(n)

    return OrbitOptions('probabilistic', 1, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)

# https://oeis.org/A100982
def get_admissible(n_terms, options: OrbitOptions) -> List[int]:
    limit = 1000  # Increase if more terms are needed
    results = []
    if (options.name == '3x_plus_1'):
        x = [0] * (limit + 2)  # x[1] to x[limit+1]
        y = [0] * (limit + 2)
        x[1] = 1  # Initial condition
        n = 1
        b = 1

        while len(results) < n_terms:
            b += 1
            # Update y[c] = x[c] + x[c-1] for c from 2 to b+1
            for c in range(2, b + 2):
                y[c] = x[c] + x[c - 1]
            # Copy y back to x
            for c in range(2, b + 2):
                x[c] = y[c]
            a_n = 0
            # Check the condition and compute a_n
            for c in range(1, b + 2):
                if (b + 1 - c) * math.log(3) < b * math.log(2):
                    a_n += x[c]
                    x[c] = 0
            if a_n != 0:
                results.append((a_n))
                n += 1
    return results

#https://oeis.org/A122437
def get_allowable_dropping_times(n_terms: int, options: OrbitOptions) -> List[int]:
    results = []
    if (options.name == '3x_plus_1'):
        for n in range(1, n_terms + 1):
            a_n_plus1 = math.floor(1 + n + n * math.log(3) / math.log(2))
            results.append(a_n_plus1)
    return results

def generate_orbit_info(
    n: int,
    lookup_map: Dict[int, int],
    wheel_map: Dict[int, int],
    index_map: Dict[str, int],
    options: OrbitOptions
) -> Tuple[int, List[int], List[int], int, int]:
    if options.name == '3x_plus_1' and n == 1:
        return [1, [1, 4, 2], [1, 4, 2], 1, 1]
    if options.name == '3x_plus_3' and n == 3:
        return [3, [3, 12, 6], [3, 12, 6], 1, 1]

    orbit = [n]
    orig_n = n
    first_orbit = None
    stopping_mod = None
    stopping_index = None
    first_drop = None

    while options.should_halt(n) is False:
        if options.should_decrease(n):
            n = options.decrease(n)
        else:
            n = options.increase(n)

        if n <= orig_n and first_orbit is None:
            first_orbit = orbit[0:]
            first_drop = len(first_orbit)

            if (options.name in fully_supported_option_names):
                if first_drop not in lookup_map:
                    raise Exception(f'First drop {first_drop} not in lookup_map')
            
                mod_magnitude = lookup_map[first_drop]
                if wheel_map[first_drop] > mod_magnitude:
                    wheel_map[first_drop] = 1

                stopping_mod = wheel_map[first_drop]
                wheel_map[first_drop] += 1

                index_key = f'{first_drop}-{stopping_mod}'
                if index_key in index_map:
                    index_map[index_key] += 1
                else:
                    index_map[index_key] = 1

                stopping_index = index_map[index_key]

        options.append_to_orbit(n, orbit)

    return first_drop, first_orbit, orbit, stopping_mod, stopping_index

def generate_maps() -> Tuple[Dict[int, int], Dict[int, int], Dict[str, int]]:
    lookup_map = { 1 : 1}
    wheel_map = { 1 : 1 }
    index_map = { 1 : 1}
    return lookup_map, wheel_map, index_map



def generate_orbit_info_batch(total: int, orbit_options: OrbitOptions) -> List[OrbitInfo]:
    admissable : List[int] = get_admissible(200, orbit_options)
    allowable_dropping_times : List[int] = get_allowable_dropping_times(200, orbit_options)
    lookup_map, wheel_map, index_map = generate_maps()
    for i, elem in enumerate(allowable_dropping_times):
        lookup_map[elem] = admissable[i]
        wheel_map[elem] = 1
        index_map[f'{elem}-1'] = 0

    results : List[OrbitInfo] = []
    try:
        for n in range(orbit_options.min_n, total):
            first_orbit, orbit, first_drop, stopping_mod, stopping_index = generate_orbit_info(n, lookup_map, wheel_map, index_map, orbit_options)
            results.append(OrbitInfo(n, first_orbit, orbit, first_drop, stopping_mod, stopping_index))
    except Exception as e:
        print(e)
    return results