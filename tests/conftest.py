import datetime

import pytest

NUM_ROWS = 50_000


@pytest.fixture(scope="session")
def user_rows():
    base_date = datetime.date(1990, 1, 1)
    genders = ["M", "F", "NB", "Other", None]
    ethnicities = ["Hispanic", "White", "Black", "Asian", "Other", None]
    return [
        {
            "FirstName": f"First{i}",
            "LastName": f"Last{i}",
            "Birthday": base_date + datetime.timedelta(days=i % 3650),
            "Gender": genders[i % len(genders)],
            "Ethnicity": ethnicities[i % len(ethnicities)],
        }
        for i in range(NUM_ROWS)
    ]
