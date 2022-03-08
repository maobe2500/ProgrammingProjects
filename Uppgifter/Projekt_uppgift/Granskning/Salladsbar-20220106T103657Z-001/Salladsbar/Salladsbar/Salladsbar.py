from tkinter import *
from tkinter import messagebox
from Ingredient import *
from Sallad import *

root = Tk()

#------------===== INFO =====------------#

#Format på filerna:

#ingrediens-format: namn,pris:namn,pris:namn,pris:namn,,,,,
#meny-format: salladsnamn,pris,ingr1_index,ingr2_index,ingr3_index:salladsnamn,pris,,,,,


#Kort om Tkinter:

#Labels är bara info text för avnändaren
#Buttons är knappar som kan anropa funktioner när de klickas
#Radiobuttons förekommer i grupp, men endast en av dem kan vara valda åt gången (och den valda kan inte "o-väljas" utan att en annan väljs"
#I det här programmet har alla radiobutton-grupper en förvald som är "tryckt" från början som ett slag default-svar
#Checkboxes är väldigt lika radiobutton men man kan kryssa i fler av dem
#Både Radiobuttons och Checkboxes behöver "länkas" IntVar, ett av Tkinters egna påfund, för att lagra infon av användarens val
#För att knapparna och annat ska visas behöver man använda .grid(). Som parameter anger man vilken rad och kolumn elementet ska sättas in på i fönstret
#Frames är de fönster progammet öppnar och där knapparna visas
#Stänger man det tomma kommando-fönstret som öppnas med programmet stängs hela programmet av

#Av någon anledning gillar inte python att läsa bokstäverna å, ä, och ö från filer, det finns sätt att fixa det, fast de skulle ta en del arbete jag inte tycker är viktigt för uppgiften

#Jag har försökt hålla alla metoder i ordningen de körs, dock hamnade "read_" funktionerna längst ner

#========================================#


def main():

    lbl_vilken_bar = Label(text="Var vill du äta?").grid(row=1, column=1)

    sallad_bar_list = read_file("Salladsbarer.txt", "") #de olika salladsbarerna läses in från en fil
    counter = 1
    
    #knapparna som låter en välja restaurang skapas
    for b in sallad_bar_list:
        #messagebox.showinfo("sdf", "bar = " + sallad_bar_list[b])
        Button(root, text=b, command=lambda j=counter: open_bar_menu(sallad_bar_list[j-1])).grid(row=counter + 2, column=1) #lambda används för att ge parametrar till funktioner när de startas från knappar
        counter += 1

    

        #så här såg knapp-uppstarten ut innan jag flyttade över namnen till en fil, dessa är tekniskt sätt onödiga nu men de kan hjälpa till med att förstå set-uppet

    #btn_kalles = Button(root, text="Kalles på hörnet",  command=lambda: open_bar_menu("Kalles på hörnet")).grid(row=2, column=1)
    #btn_runt_jorden = Button(root, text="Runt Jorden på 80 tuggor",  command=lambda: open_bar_menu("Runt Jorden på 80 tuggor")).grid(row=3, column=1)
    #btn_italia = Button(root, text="Sallata de Italia",  command=lambda: open_bar_menu("Sallata de Italia")).grid(row=4, column=1)
    #btn_ranch = Button(root, text="RAM Ranch",  command=lambda: open_bar_menu("RAM Ranch")).grid(row=5, column=1)
    
    root.mainloop()



def open_bar_menu(bar_name):

    ingredient_list = read_ingredients(bar_name)
    
    #nytt fönster skapas
    frame1 = Toplevel(root)
    frame1.geometry("250x250")
    frame1.title(bar_name)

    lbl_menu_info = Label(frame1, text = "Välj innehåll:").grid(row=1, column=1)

    cbox_value_list = [] #ska innehålla alla checkbuttons för ingredienserna

    for ingredient in ingredient_list:
        cbox_value_list.append(IntVar()) #en ny IntVar() skapas för varje ingrediens, den kommer att innehålla en 0 ifall ingrediensen inte väljs och en 1 ifall den väljs
        c = Checkbutton(frame1, text = ingredient.name, variable = cbox_value_list[len(cbox_value_list)-1]) #en checkbox (för varje ingr.) skapas med namnet av en ingrediens, dess av/på status binds till en IntVar som sparas i en lista på samma index som ingrediensen
        c.grid(row=(1 + len(cbox_value_list)//2 + len(cbox_value_list)%2), column=(2 - len(cbox_value_list)%2)) #denna kod ser till att cboxarna ställs upp i två estetiska kolumner
    
    btn_search_sallad = Button(frame1, text="Sök Sallad", command=lambda: translate(bar_name, cbox_value_list)).grid(row=(2 + len(cbox_value_list)//2 + len(cbox_value_list)%2), column=1) #värdet på row borde se till att den hamnar en rad under cboxarna



def translate(bar_name, cbox_value_list, search_for_sallad = True): #denna funktion översätter listan med cbox värdena (0 eller 1) till en lista av de önskade ingrediensernas index

    ingr_index_list = []
    print('ingredients before' + str(ingr_index_list))
    #print('checkbox val list ' + str(cbox_value_list))
    for i in range(0, len(cbox_value_list)):
        if(cbox_value_list[i].get() == 1):
            ingr_index_list.append(i)
    #eftersom att translate() senare i koden även används för att returnera en sträng (och inte bara används i en knapp) kan man välja vilket den ska göra
    if search_for_sallad:
        search_sallad(bar_name, ingr_index_list)
    else:
        print('ingredients after' + str(ingr_index_list))
        return ingr_index_list


def search_sallad(bar_name, ingr_index_list):

    if len(ingr_index_list) == 0: #om det visar sig att användaren inte valde några innehåll innan de tryckte på "sök sallad" får de ett popup-meddelande som informerar om dennes inkompetens
        messagebox.showinfo("Fel", "Du måste välja något att ha i salladen")
        return #metoden avslutas innan det nästa fönstret har öppnats, vilket betyder att användaren får en till chans att välja innehåll

    sallad_list = read_sallads(bar_name)

    #här får varje sallad en lista med tillval, d.v.s. de ingredienser användaren önskade men salladen inte innehåller
    for s in sallad_list: #varje sallad kollas...
        for i in ingr_index_list: #ifall den innehåller en av alla önskade ingredienser (alla ingr. kollas)...  
            if int(i) not in s.ingr_index: #i sin ingr. lista
                s.extras.append(i) #ifall komponenten saknas läggs den till som tillval
            

    #här sorteras sallad-listan om, först efter dess pris (från lägst till högst) och sedan beroende på antalet tillval som krävs (från lägst till högst)
    sallad_list.sort(key=sort_price) #sort_price och sort_extras är korta funktioner som endast finns för att sortering ska vara smidig, allt de gör är att returnera respektive värde
    sallad_list.sort(key=sort_extras) #genom att sortera efter pris först och sedan efter antalet extraingredienser kommer kommer den sallad med minst extra alltid vara högst upp, men om 2 sallader har lika många extra kommer den med lägst pris att prioriteras

    present_sallads(bar_name, sallad_list, len(ingr_index_list))


def sort_price(sallad):

    return sallad.price

def sort_extras(sallad):

    return len(sallad.extras)


def present_sallads(bar_name, sallad_list, requested_ingr_amount):

    #kolla ifall den första salladen kräver tillval, om inte: ta bort alla som kräver tillval
    s_length = len(sallad_list) #detta värde måste hållas konstant för att de snarast förljande kodraderna ska fungera
    extras_and_price = "Minst en sallad utan tillägg hittades"
    total_extra_price = 0
    ingredient_list = []
    if len(sallad_list[0].extras) == 0: #ifall detta stämmer betyder det att det finns minst en sallad med alla önskade ingredienser, därav blir de med tillval överflödiga

        for i in range(s_length):
            if len(sallad_list[s_length-i-1].extras) != 0: #listan kollas baklänges, om en sallad kräver tillval tas den bort
                sallad_list.remove(sallad_list[s_length-i-1])

    else: #ingen sallad levde upp till kraven och därav måste listor på extraval och extrapris tas fram för varje sallad
        
        for t in range(s_length): #här tas sallader som inte innehåller någon önskad ingrediens bort
            if len(sallad_list[s_length-t-1].extras) == requested_ingr_amount:
                del sallad_list[s_length-t-1]

        extras_and_price = "Tillval: "
        ingredient_list = read_ingredients(bar_name)
        for s in sallad_list:
            extras_and_price += "\n" + s.name + ": "
            for e in s.extras: #för varje tillägg i varje sallad läggs varje tillval och dess pris till
                extras_and_price += ingredient_list[e].name + ", "
                total_extra_price += int(ingredient_list[e].price)
            extras_and_price += " tot. +" + str(total_extra_price) + " kr"
            total_extra_price = 0



    #salladerna är nu sorterade efter antalet eftersöka ingredienser och även pris

    frame2 = Toplevel(root)
    frame2.title("Välj en sallad")
    
    lbl_choice_info = Label(frame2, text = "Våra förslag:").grid(row=1, column=1)


    #en sats med radiobuttons skapas på ungefär samma sätt som checkboxarna skapades tidigare

    rbox_value = IntVar() #här sparas värdet på salladen användaren väljer
    counter = 1 #används till placeringen av "köp sallad" knappen

    for s in range(len(sallad_list)):
        c = Radiobutton(frame2, text = (sallad_list[s].name, sallad_list[s].price, "kr"), variable = rbox_value, value = s).grid(row=2 + s, column=1)
        counter += 1
    lbl_extras_info = Label(frame2, text = extras_and_price).grid(row=counter + 1, column=1)

    btn_buy_sallad = Button(frame2, text="Köp Sallad", command=lambda: buy_sallad(bar_name, sallad_list[rbox_value.get()])).grid(row=counter + 2, column=1)




def buy_sallad(bar_name, sallad):

    frame3 = Toplevel(root)
    frame3.title("Välj tillval")
    frame3.geometry("300x250")

    ingredient_list = read_ingredients(bar_name)

    #här ställs ingredienser upp precis som i menyn där man skulle önska innehåll, här presenteras dock deras pris, för kommentarer, se tidigare metod

    cbox_value_list = [] 
    for ingredient in ingredient_list:
        cbox_value_list.append(IntVar())
        c = Checkbutton(frame3, text = (ingredient.name, ingredient.price, "kr"), variable = cbox_value_list[len(cbox_value_list)-1])
        c.grid(row=(1 + len(cbox_value_list)//2 + len(cbox_value_list)%2), column=(2 - len(cbox_value_list)%2))

    btn_confirm_purchase = Button(frame3, text="Slutför köp", command=lambda: confirm_purchase(bar_name, sallad, ingredient_list, cbox_value_list)).grid(row=(2 + len(cbox_value_list)//2 + len(cbox_value_list)%2), column=1)



def confirm_purchase(bar_name, sallad, ingredient_list, cbox_value_list):

    extras_index_list = translate(bar_name, cbox_value_list, False)

    frame4 = Toplevel(root)
    frame4.title("Kvitto")

    total_price = sallad.price

    for e in sallad.extras: #kostnaderna för de nödvändiga salladstillvalen läggs på salladens baskostnad
        total_price += ingredient_list[e].price

    for i in extras_index_list: #kostnaderna för kundens egna tillval läggs till
        total_price += ingredient_list[i].price

    reciept = "---** " + bar_name + " **---\n\nKöpt:\n" + sallad.name + " " + str(sallad.price) + "\n\n"

    if len(sallad.extras) != 0: #ifall det finns tillval så radas de upp på kvittot här
        reciept += "--Kompliment:\n"
        for e in sallad.extras:
            reciept += "* " + ingredient_list[e].name + " " + str(ingredient_list[e].price) + "\n"

    if len(extras_index_list) != 0: #ifall väljaren har valt egna tillval skrivs de till på kvittot här
        reciept += "--Extra Tillval:\n"
        for e in extras_index_list:
            reciept += "* " + ingredient_list[e].name + " " + str(ingredient_list[e].price) + "\n"

    reciept += "Den totala kostnaden blir:\n" + str(total_price) + " kr\n\nTack för att du besökte " + bar_name + " och kom snart åter!"

    #strängen skrivs till en fil
    with open("kvitto.txt", "w") as file:
        file.write(reciept)
        file.close()

    lbl_reciept = Label(frame4, text=reciept).grid(row=1, column=1)
       

#eftersom att read_ingr och read_meny är rätt lika varandra skulle man kunna sätta in dem i read_file där "tag" används för att bestämma vilken av de som ska köras med en if-sats
#dock tycker jag att detta är lättare att läsa och förstå, vilket troligen väger mer än att spara 2 funktions deklarationer i det här sammanhanget
#dessutom används read_file för att läsa in vilka olika salladsbarer programmet ska arbeta med från filen "Salladsbarer"

def read_file(bar_name, tag):

    file_data = open(bar_name + tag, "r") #data läses in från relevant fil
    raw_data = file_data.readlines()[0] #data skrivs till en temporär variabel
    file_data.close() #filen stängs

    raw_data_list = raw_data.split(":") #den inlästa datan delas upp

    return raw_data_list


def read_ingredients(bar_name):

    ingredient_list = [] #en tom lista deklareras för att hålla instanserna av Ingr. klassen

    raw_data_list = read_file(bar_name, " ingredienser.txt")

    for i in raw_data_list:
        ingredient_list.append(Ingredient(i.split(",")[0], int(i.split(",")[1]))) #i delas upp i namn och pris

    return ingredient_list #en lista av Ingredient-klass instanser returneras


def read_sallads(bar_name):

    sallad_list = []
    temp_ingr_list = [] #salladens ingredienser sparas i en lista

    raw_data_list = read_file(bar_name, " meny.txt")

    for s in raw_data_list:
        temp_ingr_list = [] #listan rensas
        for t in s.split(",")[2:]:
            temp_ingr_list.append(int(t)) #salladens innehåll läggs in listan
        sallad_list.append(Sallad(s.split(",")[0], int(s.split(",")[1]), temp_ingr_list)) #salladens namn, pris och ingr. lista läggs in i klassen

    return sallad_list

main()

