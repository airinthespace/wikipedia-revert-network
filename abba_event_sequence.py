from datetime import timedelta

def get_event_sequence(network):
    """
    Create a dictionary of event sequences for each pair of reverter and reverted.
    
    The key of the dictionary is a tuple of reverter and reverted.
    The value of the dictionary is a list of event sequences.
    Each event sequence is a list of two events.
    Each event is a dictionary with the following keys:
        reverter: the user who reverted
        reverted: the user who was reverted
        time: the time of the event
        reverter_seniority: the log10 of the number of edits the reverter has made
        reverted_seniority: the log10 of the number of edits the reverted has made
    """
    event_sequence = {}

    for i, edge in enumerate(network):
        
        latest_revert_time = edge['time'] + timedelta(hours=24)
        # Find the next revert that is within 24 hours of the current revert

        for other_edge in network[i+1:]:
            if other_edge['time'] > latest_revert_time:
                break
            
            # If the "other_edge" is a revert of the current edge, add it to the "event_sequence"
            if other_edge['reverter'] == edge['reverted'] and other_edge['reverted'] == edge['reverter']:
                pair = (edge['reverter'], edge['reverted'])
                events = [edge , other_edge]
                if pair not in event_sequence:
                    event_sequence[pair] = []
                event_sequence[pair].append(events)
                break
    return event_sequence