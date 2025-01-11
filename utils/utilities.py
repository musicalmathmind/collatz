def count_common_elements(*lists):
    """
    Count the number of elements that exist in all the given lists.
    
    :param lists: Variable number of lists to check for common elements.
    :return: The count of elements common to all lists.
    """
    if not lists:
        return 0  # If no lists are provided, return 0

    # Use set intersection to find common elements
    common_elements = set(lists[0])
    for lst in lists[1:]:
        common_elements.intersection_update(lst)

    return len(common_elements)


def count_matching_indexes(*lists):
    """
    Count the number of indexes where all the given lists have equal elements.
    
    :param lists: Variable number of lists to check for matching indexes.
    :return: The count of indexes where elements are equal across all lists.
    """
    if not lists:
        return 0  # If no lists are provided, return 0

    # Ensure all lists are of the same length
    min_length = min(len(lst) for lst in lists)
    if any(len(lst) != min_length for lst in lists):
        raise ValueError("All lists must have the same length.")

    # Count matching indexes
    count = 0
    for i in range(min_length):
        if all(lst[i] == lists[0][i] for lst in lists):
            count += 1

    return count