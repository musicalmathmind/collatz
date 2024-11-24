import math
import random 
from utils.orbit_info import OrbitInfo
from typing import Callable, Dict, List, Tuple

# List of option names that are fully supported for orbit operations
fully_supported_option_names = ['3x_plus_1']

class OrbitOptions:
    """
    Represents a configuration for orbit generation based on specific rules.

    Attributes:
        name (str): Name of the orbit rule set.
        min_n (int): Minimum starting value for the orbit.
        should_halt (Callable): Function to determine when to halt the orbit.
        should_decrease (Callable): Function to determine if the value should decrease.
        should_increase (Callable): Function to determine if the value should increase.
        decrease (Callable): Function to decrease the value.
        increase (Callable): Function to increase the value.
        append_to_orbit (Callable): Function to append the current value to the orbit list.
    """
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
    """
    Creates an OrbitOptions instance for the classic 3x+1 (Collatz) rule set.

    Returns:
        OrbitOptions: Configuration for the 3x+1 orbit generation.
    """
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
    """
    Creates an OrbitOptions instance for a modified 3x+3 Collatz rule set.

    Returns:
        OrbitOptions: Configuration for the 3x+3 orbit generation.
    """
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
    """
    Creates an OrbitOptions instance for a probabilistic Collatz-like rule set.

    Args:
        p (float): Probability of applying the 3x+1 rule instead of 3x+3.

    Returns:
        OrbitOptions: Configuration for the probabilistic orbit generation.
    """
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
    """
    Generates a list of admissible values for the specified orbit rule set.

    Args:
        n_terms (int): Number of admissible terms to generate.
        options (OrbitOptions): The orbit rule set configuration.

    Returns:
        List[int]: A list of admissible values for the specified rule set.

    Notes:
        - This implementation is specific to the '3x_plus_1' rule set.
        - Uses an iterative approach to compute admissible terms based on 
          a dynamic programming-like update of two arrays, `x` and `y`.
    """
    limit = 1000  # Limit on the number of terms to calculate
    results = []
    if options.name == '3x_plus_1':
        x = [0] * (limit + 2)  # x[1] to x[limit+1]
        y = [0] * (limit + 2)
        x[1] = 1  # Initial condition
        n = 1
        b = 1

        while len(results) < n_terms:
            b += 1
            # Update y[c] = x[c] + x[c-1] for indices 2 to b+1
            for c in range(2, b + 2):
                y[c] = x[c] + x[c - 1]
            # Copy updated values from y back to x
            for c in range(2, b + 2):
                x[c] = y[c]
            a_n = 0
            # Compute admissible value a_n based on logarithmic conditions
            for c in range(1, b + 2):
                if (b + 1 - c) * math.log(3) < b * math.log(2):
                    a_n += x[c]
                    x[c] = 0
            if a_n != 0:
                results.append(a_n)
                n += 1
    return results

# https://oeis.org/A122437
def get_allowable_dropping_times(n_terms: int, options: OrbitOptions) -> List[int]:
    """
    Computes allowable dropping times for the specified orbit rule set.

    Args:
        n_terms (int): Number of terms to compute.
        options (OrbitOptions): The orbit rule set configuration.

    Returns:
        List[int]: A list of allowable dropping times.

    Notes:
        - Specific to the '3x_plus_1' rule set.
        - Computes terms based on a logarithmic formula.
    """
    results = []
    if options.name == '3x_plus_1':
        for n in range(1, n_terms + 1):
            a_n_plus1 = math.floor(1 + n + n * math.log(3) / math.log(2))
            results.append(a_n_plus1)
    return results

def generate_orbit_info(
    n: int,
    options: OrbitOptions,
    lookup_map: Dict[int, int] = None,
    wheel_map: Dict[int, int] = None,
    index_map: Dict[str, int] = None,
) -> Tuple[int, List[int], List[int], int, int]:
    """
    Generates detailed information about an orbit starting from a given number.

    Args:
        n (int): Starting number for the orbit.
        lookup_map (Dict[int, int]): Map of first drop values to their magnitude.
        wheel_map (Dict[int, int]): Map of first drop values to wheel positions.
        index_map (Dict[str, int]): Map of first drop and mod values to counts.
        options (OrbitOptions): Configuration for the orbit rule set.

    Returns:
        Tuple[int, List[int], List[int], int, int]: A tuple containing:
            - First drop (int)
            - First orbit (List[int])
            - Full orbit (List[int])
            - Stopping modulus (int)
            - Stopping index (int)
    """
    building_frome_scratch = (lookup_map != None and wheel_map != None and index_map != None)
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

        # Check for the first drop and update related maps
        if n <= orig_n and first_orbit is None:
            first_orbit = orbit[:]
            first_drop = len(first_orbit)
            
            if (building_frome_scratch) and options.name in fully_supported_option_names:
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

        # Append the current value to the orbit
        options.append_to_orbit(n, orbit)

    return first_drop, first_orbit, orbit, stopping_mod, stopping_index

def generate_maps() -> Tuple[Dict[int, int], Dict[int, int], Dict[str, int]]:
    """
    Generates initial lookup, wheel, and index maps for orbit calculations.

    Returns:
        Tuple[Dict[int, int], Dict[int, int], Dict[str, int]]: A tuple containing:
            - lookup_map (Dict[int, int]): Maps first drops to their magnitude.
            - wheel_map (Dict[int, int]): Tracks wheel positions for first drops.
            - index_map (Dict[str, int]): Tracks counts for first drop/mod combinations.
    """
    lookup_map = {1: 1}
    wheel_map = {1: 1}
    index_map = {1: 1}
    return lookup_map, wheel_map, index_map

def generate_orbit_info_batch(total: int, orbit_option: OrbitOptions) -> List[OrbitInfo]:
    """
    Generates a batch of orbit information for numbers up to the specified total.

    Args:
        total (int): Total numbers to process.
        orbit_options (OrbitOptions): Configuration for the orbit rule set.

    Returns:
        List[OrbitInfo]: A list of OrbitInfo objects for the generated orbits.
    """
    admissible: List[int] = get_admissible(200, orbit_option)
    allowable_dropping_times: List[int] = get_allowable_dropping_times(200, orbit_option)
    lookup_map, wheel_map, index_map = generate_maps()

    # Populate maps based on allowable dropping times and admissible values
    for i, elem in enumerate(allowable_dropping_times):
        lookup_map[elem] = admissible[i]
        wheel_map[elem] = 1
        index_map[f'{elem}-1'] = 0

    results: List[OrbitInfo] = []
    try:
        for n in range(orbit_option.min_n, total):
            # Generate detailed orbit information for each number
            first_drop, first_orbit, orbit, stopping_mod, stopping_index = generate_orbit_info(
                n, orbit_option, lookup_map, wheel_map, index_map)
            results.append(OrbitInfo(n, first_drop, first_orbit, orbit, stopping_mod, stopping_index))
    except Exception as e:
        # Handle errors and log exception
        print(e)

    return results
