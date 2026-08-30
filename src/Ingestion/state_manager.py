import json
import os



STATE_FILE = "data/state/ingestion_state.json"


def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_state(state):

    os.makedirs(
        os.path.dirname(STATE_FILE),
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            indent=4
        )


def get_last_date(source):

    state = load_state()

    return state.get(source)


def update_last_date(source, date):

    state = load_state()

    state[source] = date

    save_state(state)