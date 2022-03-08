class Sallad(object):

    #denna klass innehåller en sallads namn, pris, en lista av dess ingredienser och en lista av krävda tillval (som genereras under körning)

    def __init__(self, name, price, ingr_index):
        self.name = name
        self.price = price
        self.ingr_index = ingr_index #istället för att ingredienserna sparas som en lista av namn sparas de som en lista av index i ingrediensfilen
        self.extras = [] #de olika tillval som krävs för att salladen ska nå kundens önskemål sparas här