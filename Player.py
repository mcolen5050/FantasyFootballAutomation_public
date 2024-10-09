class Player:
    def __init__(self, player_id, full_name, lineup_slot, projected_points, eligible_slots, injury_status):
        self.player_id = player_id
        self.full_name = full_name
        self.lineup_slot = lineup_slot
        self.projected_points = projected_points
        self.eligible_slots = eligible_slots
        self.injury_status = injury_status
        self.new_lineup_slot = 20  # Initially bench until specified otherwise in main

    def compare(self, other_player):
        """
        Compare players by projected points.
        Return True if self has higher projected points than other_player.
        """
        return self.projected_points > other_player.projected_points
    
    def check_eligible_switch(self, other_player):
        if self.on_ir() and self.lineup_slot == 21:
            return False
        return self.lineup_slot in other_player.eligible_slots
    
    def on_ir(self):
        """Check if player is on Injury Reserve"""
        return self.injury_status == "INJURY_RESERVE"

    def set_new_lineup_slot(self, new_slot):
        """Set the new lineup slot for the player when being moved."""
        self.new_lineup_slot = new_slot

    def to_lineup_change_dict(self):
        """
        Convert player data to a dictionary for the lineup change request.
        Only include if the player is moved (has a new lineup slot).
        """
        if self.new_lineup_slot == self.lineup_slot:
            return None
        return {
            "playerId": self.player_id,
            "type": "LINEUP",
            "fromLineupSlotId": self.lineup_slot,
            "toLineupSlotId": self.new_lineup_slot
        }
        
    def __lt__(self, other):
        # Compare based on projected_points
        return self.projected_points < other.projected_points
