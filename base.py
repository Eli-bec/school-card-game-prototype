

class Listener:
    def on_encounter_start(self) -> list: pass
    def on_turn_start(self, turn) -> list: pass
    def on_turn_end(self, turn) -> list: pass
    def on_encounter_end(self) -> list: pass
    def on_card_played(self, card) -> list: pass
    def on_option_selected(self, option_key, option_info) -> list: pass