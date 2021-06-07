class Price:
    def __init__(self, item):
        self.item = item
        self.values = {}
        self.source = "None"
        self.total = 0

        
        
        self.enchants_value = 0

    def __init__(self):
        total = 0
        for key, value in self.values.items():
            total += value
        return total

    def __str__(self):
        list_of_elems = []
        if self.item.stack_size > 1:
            list_of_elems.append(f"{self.converted_name}, (x{self.item.stack_size})")
        else:
            list_of_elems.append(f"{self.converted_name}")

        list_of_elems.append(f"Total: {int(self)}, Base: {self.base_price}, Source: {self.source}")
        if self.values.recombobulated_value > 0:
            list_of_elems.append(f"+ Recombobulated")
        if self.values.star_value > 0:
            list_of_elems.append(f"Stars: {self.star_value}")
        if self.values.reforge_bonus > 0:
            self
            
        '''
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        list_of_elems.append(f"")
        '''
        


