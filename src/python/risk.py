"""Final presentation's headcount stages + the original fixed-area density formula.

The 2023 final PPT states 안전 1-2, 경고 3-4, 위험 5+ people.
The historical main.py calculated crowd_density = people_count / total_area
using a configured constant. These are separate outputs; the old source's
thresholds on density (<=2, <4) conflict with the final presentation.
"""

SAFE_MAX_PEOPLE = 2
DANGER_MIN_PEOPLE = 5


def calculate_density(people_count, total_area):
    if people_count < 0:
        raise ValueError('people_count must not be negative')
    if total_area <= 0:
        raise ValueError('fixed total_area must be greater than zero')
    return people_count / total_area


def danger_level(people_count):
    """Demonstration stages from the 2023 final PPT, 0 people is safe."""
    if people_count < 0:
        raise ValueError('people_count must not be negative')
    if people_count <= SAFE_MAX_PEOPLE:
        return '안전'
    if people_count < DANGER_MIN_PEOPLE:
        return '경고'
    return '위험'


def evaluate(people_count, total_area):
    """Return (fixed-area density, final-presentation risk level)."""
    return calculate_density(people_count, total_area), danger_level(people_count)
