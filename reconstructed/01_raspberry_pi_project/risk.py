"""2023 코드의 단계 경계값과 사람수/설정면적 산식을 보존한 순수 계산부."""
def calculate_density(people_count, total_area):
    if total_area <= 0:
        raise ValueError('total_area must be greater than 0')
    if people_count < 0:
        raise ValueError('people_count must not be negative')
    return people_count / total_area

def danger_level(density, safe_max=2.0, danger_min=4.0):
    if safe_max >= danger_min:
        raise ValueError('safe_max must be less than danger_min')
    if density <= safe_max:
        return '안전'
    if density < danger_min:
        return '경고'
    return '위험'

def evaluate(people_count, total_area, safe_max=2.0, danger_min=4.0):
    density = calculate_density(people_count, total_area)
    return density, danger_level(density, safe_max, danger_min)
