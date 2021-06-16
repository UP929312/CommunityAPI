import json

def print_tree(info_dict, current_indent, print_output):
    branch_value = 0
    if isinstance(info_dict, dict):
        if len(list(info_dict.keys())) == 0:
            return 0
        for key, value in info_dict.items():
            if isinstance(value, dict):
                if print_output:
                    print(f"{current_indent}{key}")
                branch_value += print_tree(value, current_indent+"  ", print_output)
            else:
                if not isinstance(value, str):
                    branch_value += value
                if print_output:
                    print(f"{current_indent}{key}: {value}")
    return branch_value


class Price(object):
    def __init__(self, item):
        self.item = item
        self.value = {}  # need this
        self.total = 0

    def display_output(self):
        print(self.item.internal_name)
        print_tree(self.value, "  ", True)
        print(f"Total: {price}")

    def calculate_total(self):
        self.total = print_tree(self.value, "  ", False)
            
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
        return json.dumps({"total": self.total,
                           "value": self.value,
                           "item":  self.item.to_dict(),
                         })

