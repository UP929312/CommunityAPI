def generate_tree(info_dict, current_list, current_indent):
    if isinstance(info_dict, dict):
        if len(list(info_dict.keys())) == 0:
            return 0
        for key, value in info_dict.items():
            if isinstance(value, dict):
                current_list.append(f"{current_indent}{key}")
                generate_tree(value, current_list, current_indent+"  ")
            else:
                current_list.append(f"{current_indent}{key}: {value}")
    return current_list

def search_tree(info_dict):
    branch_value = 0
    if isinstance(info_dict, dict):
        if len(list(info_dict.keys())) == 0:
            return 0
        for key, value in info_dict.items():
            if isinstance(value, dict):
                branch_value += search_tree(value)
            else:
                if not isinstance(value, str):
                    branch_value += value
    return branch_value


class Price():
    def __init__(self, item):
        self.item = item
        self.value = {}  # need this
        self.total = 0

    def display_output(self):
        print(self.item.internal_name)
        lines = generate_tree(self.value, [], "  ")
        print("\n".join(lines))
        total = search_tree(self.value)
        print(f"Total: {total}")

    def to_dump_string(self):
        '''
        Used for the website dump (tree) to show it all.
        '''
        if isinstance(self.item, dict):
            start = f"Level {self.value['pet_level']} {self.item['type'].replace('_', ' ').title()}\n"
        else:
            start = f"{self.item.internal_name}\n"
            
        return start+"\n".join(generate_tree(self.value, [], "  "))+f"\nTotal Value: {search_tree(self.value)}"+"\n"

       
    def calculate_total(self):
        self.total = search_tree(self.value)
        if not isinstance(self.item, dict):
            self.total *= self.item.stack_size
        return self.total
    

    def to_dict(self):
        '''
        returns a dictionary with all the needed information, included the total number,
        all the attributes that make up the value, as well as the attributes that make
        up the item object itself
        '''
        item = self.item if isinstance(self.item, dict) else self.item.to_dict()

        return {"total": self.total,
                "value": self.value,
                "item":  item,
               }
