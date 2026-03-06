


def analyze_replay_stability(record):
    #analyze if a endpoint behave consistently across replayss..

    replays = record.replays.all()

    if not replays.exists():
        return {
            "stability" : "UNKNOWN",
            "observed_statuses": [],
        }
    
    statuses = [r.status_after for r in replays]

    unique_statuses =  set(statuses)

    if len(unique_statuses) == 1:
        stability = "STABLE"
    else:
        stability = "FLAKY"

    return {
        "stability": stability,
        "observed_statuses" : list(unique_statuses)
    }