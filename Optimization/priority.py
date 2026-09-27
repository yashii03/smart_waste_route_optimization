from datetime import datetime


def calculate_priority(fill_level, last_collected):
    """
    Calculate priority score for a waste bin.

    Higher score = higher collection priority.
    """

    # Fill level contribution
    fill_score = float(fill_level)

    # Days since last collection
    if last_collected is None:
        days_score = 30
    else:
        days_since_collection = (
            datetime.now() - last_collected
        ).days

        # Maximum contribution capped at 30
        days_score = min(days_since_collection * 5, 30)

    # Final priority score
    priority_score = fill_score * 0.7 + days_score * 0.3

    return round(priority_score, 2)