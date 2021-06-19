import json

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


class Price(object):
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

    def calculate_total(self):
        self.total = search_tree(self.value)
            
        if not isinstance(self.item, dict):
            self.total *= self.item.stack_size

        return self.total

    def to_dict(self):
        if not isinstance(self.item, dict):
            item = self.item.to_dict()
        else:
            item = self.item

        return {"total": self.total,
                "value": self.value,
                "item":  item,
               }

    def __str__(self):
        if isinstance(self.item, dict):
            item = self.item
        else:
            item = self.item.to_dict()
            
        return json.dumps({"total": self.total,
                           "value": self.value,
                           "item":  item,
                          })
  