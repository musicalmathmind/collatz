import math
import random 
from utils.orbit_info import OrbitInfo
from typing import Callable, Dict, List, Tuple

# List of option names that are fully supported for orbit operations
fully_supported_option_names = ['m3a1']

class OrbitOptions:
    """
    Represents a configuration for generating an orbit based on specific rules.

    Attributes:
        name (str): The name of the orbit rule set, used for identification or labeling.
        min_n (int): The minimum starting value allowed for the orbit.
        should_halt (Callable): A function that takes an integer as input and returns a boolean.
            Determines whether the orbit generation process should stop.
        should_decrease (Callable): A function that takes an integer as input and returns a boolean.
            Determines whether the current value should trigger a decrease operation.
        should_increase (Callable): A function that takes an integer as input and returns a boolean.
            Determines whether the current value should trigger an increase operation.
        decrease (Callable): A function that takes an integer as input and returns a tuple of:
            - The new integer value after the decrease operation.
            - A string identifier describing the decrease operation.
        increase (Callable): A function that takes an integer as input and returns a tuple of:
            - The new integer value after the increase operation.
            - A string identifier describing the increase operation.
        append_to_orbit (Callable): A function that appends the current value to the orbit.
            Accepts two arguments:
            - The current value (int).
            - The list representing the orbit (List[int]).
        max_iterations (int): The maximum number of iterations allowed for the orbit generation process.
    """
    def __init__(
        self,
        name: str,
        min_n: int,
        should_halt: Callable[[int], bool],
        should_decrease: Callable[[int], bool],
        should_increase: Callable[[int], bool],
        decrease: Callable[[int], Tuple[int, str]],
        increase: Callable[[int], Tuple[int, str]],
        append_to_orbit: Callable[[int, List[int]], None],
        max_iterations: int = None
    ):
        self.name: str = name
        self.min_n: int = min_n
        self.should_halt: Callable[[int], bool] = should_halt
        self.should_decrease: Callable[[int], bool] = should_decrease
        self.should_increase: Callable[[int], bool] = should_increase
        self.decrease: Callable[[int], Tuple[int, str]] = decrease
        self.increase: Callable[[int], Tuple[int, str]] = increase
        self.append_to_orbit: Callable[[int, List[int]], None] = append_to_orbit
        self.max_iterations: int = max_iterations


def create_m3a1_options() -> OrbitOptions:
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

    def decrease(n: int) -> Tuple[int, str]:
        return n // 2, 'd2'

    def increase(n: int) -> Tuple[int, str]:
        return 3 * n + 1, 'm3a1'

    def append_to_orbit(n: int, orbit: List[int]):
        orbit.append(n)

    return OrbitOptions('m3a1', 1, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)

def create_m3a3_options() -> OrbitOptions:
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

    def decrease(n: int) -> Tuple[int, str]:
        return n // 2, 'd2'

    def increase(n: int) -> Tuple[int, str]:
        return 3 * n + 3, 'm3a3'

    def append_to_orbit(n: int, orbit: List[int]):
        orbit.append(n)

    return OrbitOptions('m3a3', 3, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)

def create_m3a5_options(max_iterations: int = 100) -> OrbitOptions:
    """
    Creates an OrbitOptions instance for a modified 3x+5 Collatz rule set.

    Returns:
        OrbitOptions: Configuration for the 3x+5 orbit generation.
    """
    def should_halt(n: int) -> bool:
        return n == 5

    def should_decrease(n: int) -> bool:
        return n % 2 == 0

    def should_increase(n: int) -> bool:
        return n % 2 != 0

    def decrease(n: int) -> Tuple[int, str]:
        return n // 2, 'd2'

    def increase(n: int) -> Tuple[int, str]:
        return 3 * n + 5, 'm3a5'

    def append_to_orbit(n: int, orbit: List[int]):
        orbit.append(n)

    return OrbitOptions('m3a5', 5, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit, max_iterations)
    
    
def create_probabilistic_options(p: float) -> OrbitOptions:
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

    def decrease(n: int) -> Tuple[int, str]:
        return n // 2, 'd2'

    def increase(n: int) -> Tuple[int, str]:
        r = random.random()
        if r < p:
            return 3 * n + 1, 'm3a1'
        else:
            return 3 * n + 3, 'm3a3'

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
        - This implementation is specific to the 'm3a1' rule set.
        - Uses an iterative approach to compute admissible terms based on 
          a dynamic programming-like update of two arrays, `x` and `y`.
    """
    limit = 1000  # Limit on the number of terms to calculate
    results = []
    if options.name == 'm3a1':
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
        - Specific to the 'm3a1' rule set.
        - Computes terms based on a logarithmic formula.
    """
    results = []
    if options.name == 'm3a1':
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
) -> Tuple[int, list[int], list[int], int, int, list[str], dict[str, int], list[str], dict[str, int]]:
    """
    Generates detailed information about an orbit starting from a given number.

    Args:
        n (int): The starting number for the orbit.
        options (OrbitOptions): The configuration for the orbit generation, defining rules for 
            halting, increasing, decreasing, and appending values to the orbit.
        lookup_map (Dict[int, int], optional): A map of first drop values to their magnitudes. 
            Used for advanced orbit analysis. Defaults to None.
        wheel_map (Dict[int, int], optional): A map of first drop values to their wheel positions.
            Used to track modular relationships. Defaults to None.
        index_map (Dict[str, int], optional): A map of first drop and mod values to their occurrence counts.
            Used to maintain indexed relationships. Defaults to None.

    Returns:
        Tuple: A tuple containing:
            - first_drop (int): The step at which the first drop occurred, relative to the starting value.
            - first_orbit (list[int]): The sequence of numbers in the orbit up to the first drop.
            - orbit (list[int]): The complete sequence of numbers in the generated orbit.
            - stopping_mod (int): The modular value at which the orbit stopped.
            - stopping_index (int): The index at which the stopping condition occurred.
            - first_op_list (list[str]): A list of operation IDs for the first drop.
            - first_op_map (dict[str, int]): A map of operation IDs to their counts during the first drop.
            - total_op_list (list[str]): A list of all operation IDs encountered in the orbit.
            - total_op_map (dict[str, int]): A map of operation IDs to their total counts.

    Raises:
        Exception: If `first_drop` is not found in the provided `lookup_map` when required.

    Notes:
        - This function generates an orbit based on the rules specified in the `options`.
        - If advanced mapping (`lookup_map`, `wheel_map`, and `index_map`) is provided and valid, 
          it updates those maps during the first drop computation.
        - Special cases for orbits starting with predefined configurations are handled explicitly 
          (e.g., 'm3a1' starting at 1).

    """
    building_frome_scratch = (lookup_map != None and wheel_map != None and index_map != None)
    if options.name == 'm3a1' and n == 1:
        return [1, [1, 4, 2], [1, 4, 2], 1, 1, ['m3a1', 'd2', 'm3a1'], {'m3a1': 2, 'd2': 1}, ['m3a1', 'd2', 'm3a1'], {'m3a1': 2, 'd2': 1}]
    if options.name == 'm3a3' and n == 3:
        return [3, [3, 12, 6], [3, 12, 6], 1, 1, ['m3a3', 'd2', 'm3a3'], {'m3a3': 2, 'd2': 1}, ['m3a1', 'd2', 'm3a1'], {'m3a1': 2, 'd2': 1}]

    orbit = [n]
    orig_n = n
    first_orbit = None
    stopping_mod = None
    stopping_index = None
    first_drop = None
    first_op_list = []
    first_op_map = {}
    total_op_list = []
    total_op_map = {}

    while options.should_halt(n) is False:
        inc_op_id = None
        if (options.max_iterations is not None) and (len(orbit) >= options.max_iterations):
            break
        if options.should_decrease(n):
            n, inc_op_id = options.decrease(n)
        else:
            n, inc_op_id = options.increase(n)
            
        if (inc_op_id is not None):
            total_op_list.append(inc_op_id)
            if (inc_op_id not in total_op_map):
                total_op_map[inc_op_id] = 0
            total_op_map[inc_op_id] += 1
            
            if (first_drop is None):
                first_op_list.append(inc_op_id)
                if (inc_op_id not in first_op_map):
                    first_op_map[inc_op_id] = 0
                first_op_map[inc_op_id] += 1

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

    return first_drop, first_orbit, orbit, stopping_mod, stopping_index, first_op_list, first_op_map, total_op_list, total_op_map


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

def generate_orbit_info_batch(total: int, orbit_option: OrbitOptions) -> list[OrbitInfo]:
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
            first_drop, first_orbit, total_orbit, stopping_mod, stopping_index, first_op_list, first_op_map, total_op_list, total_op_map = generate_orbit_info(
                n, orbit_option, lookup_map, wheel_map, index_map)
            results.append(OrbitInfo(n, first_drop, first_orbit, total_orbit, stopping_mod, stopping_index, first_op_list, first_op_map, total_op_list, total_op_map))
    except Exception as e:
        print(e)
        raise e

    return results
