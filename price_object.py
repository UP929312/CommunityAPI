def print_tree(info_dict, current_indent):
    branch_value = 0
    if isinstance(info_dict, dict):
        if len(list(info_dict.keys())) == 0:
            return 0
        for key, value in info_dict.items():
            if isinstance(value, dict):
                print(f"{current_indent}{key}")
                branch_value += print_tree(value, current_indent+"  ")
            else:
                if not isinstance(value, str):
                    branch_value += value
                print(f"{current_indent}{key}: {value}")
    return branch_value


class Price:
    def __init__(self, item):
        self.item = item
        self.value = {}
        self.total = 0

    def __int__(self):
        if self.item.type == "DRILL":
            print(self.item.internal_name)
            price = print_tree(self.value, "  ")        
            return price * self.item.stack_size
        return 0
