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


class Price:
    def __init__(self, item):
        self.item = item
        self.value = {}  # need this
        self.total = 0

    def __int__(self):
        print_output = False
        
        if "stars" in self.value:
            print_output = True
                 
        if print_output:
            print(self.item.internal_name)
        price = print_tree(self.value, "  ", print_output)
        if print_output:
            print(f"Total: {price}")
        
        if isinstance(self.item, dict):
            return price
        else:
            return price * self.item.stack_size            
