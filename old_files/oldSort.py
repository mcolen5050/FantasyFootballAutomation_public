def sort_and_get_best_lineup_changes(starters, bench):
    """
    Sort players by position and find the best replacements for the lineup.
    Includes checks for IR eligibility.
    """
    changes = []

    # Sort starters by position
    starters.sort(key=lambda starter: starter.lineup_slot)

    for starter in starters:
        eligible_positions = {POSITION_MAP[starter.lineup_slot]}
        print(f"nf: {[POSITION_MAP[slot] for slot in starter.eligible_slots]}")
        if starter.lineup_slot == 23:  # Handling FLEX positions
            eligible_positions = {POSITION_MAP[2], POSITION_MAP[4], POSITION_MAP[6], POSITION_MAP[23]}
            print(f"YES FLEX: {eligible_positions}")

        best_replacement = None

        # Loop over bench players to find a better replacement
        for bench_player in bench:
            if any(pos in eligible_positions for pos in bench_player.eligible_slots):
                # Check if this bench player is better than the current starter
                if bench_player.compare(starter) and (not best_replacement or bench_player.compare(best_replacement)):
                    best_replacement = bench_player

        if best_replacement:
            best_replacement.set_new_lineup_slot(starter.lineup_slot)
            starter.set_new_lineup_slot(POSITION_MAP['BE'])

            changes.append(best_replacement.to_lineup_change_dict())
            changes.append(starter.to_lineup_change_dict())

    return changes