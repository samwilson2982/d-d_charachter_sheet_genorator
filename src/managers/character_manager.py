import os


class CharacterManager(object):
    def __init__(self,json_input=""):
        if not json_input:
            character_dict = {}
        else:
            character_dict = self.gather_from_json(json_input)

        # the idea is to take in what we can from the json, and randomize the rest
        self.fill_out(character_dict)


    def gather_from_json(self,json_path):
        pass


    def local_path(self,realtive_path):
        return os.path.join(os.path.dirname(__file__), realtive_path)

    def fill_out_character(self,cd):
        if "Race" not in cd:
            cd["Race"] = self.get_random_race()

        if "Name" not in cd:
            cd["Name"] = self.get_random_name(cd["Race"])


    def get_random_name(self,race):
        pass

    def get_random_race(self):
        pass