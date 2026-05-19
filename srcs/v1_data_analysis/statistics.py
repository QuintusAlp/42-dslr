import math
from typing import Union
from .exceptions import DataProcessingError

def compute_count(values: list) -> int:
    return (len(values))

def compute_mean(values: list, count: int) -> float:
    return (sum(values) / count)

def compute_variance(values: list, mean: float, count: int) -> float:
    if (count < 2):
        return float('nan')
        
    variance = sum((x - mean) ** 2 for x in values) / (count - 1)
    if variance < 0:
        raise DataProcessingError("Negative variance.")
    
    return (variance)

def compute_standard_deviation(values: list, mean: float, count: int, variance: float) -> float:
    return (math.sqrt(variance))

def compute_extrema(values: list) -> dict[str, Union[int, float]]:
    return {
        "min": values[0],
        "max": values[len(values) - 1]
    }

def compute_percentiles(values: list, count: int) -> dict[str, Union[int, float]]:
    def get_percentile(p):
        index = p / 100 * (count - 1)
        lower = int(index) # if float values take the index just below the result
        if (lower + 1 < count):
            upper = lower + 1
        else:
            upper = lower
        fraction = index - lower # how far is the index value from the closest smallest int value
        return (values[lower] + fraction * (values[upper] - values[lower])) # interpolating
            
    return {
        "q1": get_percentile(25),
        "q2": get_percentile(50),
        "q3": get_percentile(75)
    }

def compute_range(min: Union[int, float], max: Union[int, float]) -> Union[int, float]:
    return (max - min)

def compute_stats(values: list, bonus: bool = False) -> dict[str, Union[int, float]]:
    if not values:
        raise DataProcessingError("Cannot compute statistics on empty dataset")
    
    count = compute_count(values)
    mean = compute_mean(values, count)
    sorted_values = sorted(values)
    min_max = compute_extrema(sorted_values)
    percentiles = compute_percentiles(sorted_values, count)
    variance = compute_variance(values, mean, count)

    stats = {
        "count": count,
        "mean": mean,
        "std": compute_standard_deviation(values, mean, count, variance),
        "min": min_max["min"],
        "25%": percentiles["q1"],
        "50%": percentiles["q2"],
        "75%": percentiles["q3"],
        "max": min_max["max"],
    }

    if bonus:
        stats.update({
            "variance": variance,
            "range": compute_range(min_max["min"], min_max["max"])
        })

    return (stats)
