# rules
# cards:[1,52]
# 0 for empty

card_symbol=['']

class FreeCell(object):
    def __init__(self):
        self.cells=[0 for i in range(4)]
