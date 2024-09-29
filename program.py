import json
import tkinter as tk
from tkinter import ttk
from functions import *

with open("_internal/importantfiles/seeds.json", "r", encoding = "utf-8") as sfpr:
    seeds = json.load(sfpr)

root = tk.Tk()
root.geometry("1000x750")
root.title("FF14 Seed/Crossbreeding Tool")

notebook = ttk.Notebook(root)

# Start Screen

start = ttk.Frame(notebook)

label1 = ttk.Label(start, text="Hey there!") 
label1.pack()
label2 = ttk.Label(start, text="My name is Nick (aka nick75) and I'm the person who made this app!")
label2.pack()
label3 = ttk.Label(start, text="None of this would be possible without the work and research of everyone at ffxivgardening.com <3")
label3.pack()
label4 = ttk.Label(start, text="REMEMBER: This is just a Python script. The more complex the operation, the longer the runtime!")
label4.pack()
label5 = ttk.Label(start, text="Especially with the 'Shortest Path' Function, the larger the inventory and the more complex the target seed(s), you might get runtimes of over 2 minutes!")
label5.pack()
label6 = ttk.Label(start, text="This is why I limited the step number in that function. If the shortest path is longer than the limit, the program will refuse to calculate it.")
label6.pack()
label7 = ttk.Label(start, text="Maybe someday I will rewrite the code in Rust or C++, and more complex operations will be faster, but this has only been a hobby project :p")
label7.pack()
label8 = ttk.Label(start, text="If you find any bugs, feel free to open an issue on GitHub or contact me directly!")
label8.pack()
label9 = ttk.Label(start, text="Have fun <3 - nick75")
label9.pack()

# Screen for Function 1

shortestpathframe = ttk.Frame(notebook)

# Instructions for Shortest Path

sh_instructions = ttk.Label(shortestpathframe, text="On the left side, select all seeds you currently have. On the right side, select the seeds you want to make.")
sh_instructions.pack()
sh_instructions2 = ttk.Label(shortestpathframe, text = "The program will give you up to 10 different possibilities to get from the seeds in your inventory to the seeds you want to make, provided the path exists and is less than 9 steps long.")
sh_instructions2.pack()

# Elements of UI: Selectbox contains all elements that can be selected, Inventory is the lefthandside with all the seeds from your inventory

sh_selectbox = ttk.Frame(shortestpathframe)
sh_inventory = ttk.Frame(sh_selectbox)
sh_inventorylabel = ttk.Label(sh_inventory, text="Inventory")
sh_inventorylabel.pack()
sh_buttons = ttk.Frame(sh_inventory) # Box for Buttons to add/remove seeds from Inventory

global sh_listofseeds

sh_listofseeds = {}

keystring = "combobox1"
sh_listofseeds[keystring] = ttk.Combobox(sh_inventory)
sh_listofseeds[keystring]['values'] = list(seeds.keys())

def increaseinventorysize(): # Function for the Plus Button
    global sh_listofseeds
    length = len(list(sh_listofseeds.keys()))
    keystring = "combobox" + str(length + 1)
    sh_listofseeds[keystring] = ttk.Combobox(sh_inventory)
    sh_listofseeds[keystring]['values'] = list(seeds.keys())
    sh_listofseeds[keystring].pack(side='top')


def decreaseinventorysize(): # Function for the Minus Button
    global sh_listofseeds
    length = len(list(sh_listofseeds.keys()))
    if length > 1:
        keystring = "combobox" + str(length)
        sh_listofseeds[keystring].pack_forget()
        del sh_listofseeds[keystring]

sh_plusbutton = ttk.Button(sh_buttons, text="+", command=increaseinventorysize)
sh_plusbutton.pack(side='left')
sh_minusbutton = ttk.Button(sh_buttons, text="-", command=decreaseinventorysize)
sh_minusbutton.pack(side='left')
sh_buttons.pack(side='top') # Buttons to increase/decrease size of Inventory
sh_listofseeds[keystring].pack(side='top')


sh_inventory.pack(side='left')

sh_targetseeds = ttk.Frame(sh_selectbox) # Righthandside box for Target seeds
sh_targetseedslabel = ttk.Label(sh_targetseeds, text="Target Seeds")
sh_targetseedslabel.pack()
sh_seedbuttons = ttk.Frame(sh_targetseeds)

global listoftargets

listoftargets = {}

keystring = "combobox1"
listoftargets[keystring] = ttk.Combobox(sh_targetseeds)
listoftargets[keystring]['values'] = list(seeds.keys())

def increasetargetsize(): # Function for Plus Targets
    global listoftargets
    length = len(list(listoftargets.keys()))
    keystring = "combobox" + str(length + 1)
    listoftargets[keystring] = ttk.Combobox(sh_targetseeds)
    listoftargets[keystring]['values'] = list(seeds.keys())
    listoftargets[keystring].pack(side='top')

def decreasetargetsize(): # Function for Minnus Targets
    global listoftargets
    length = len(list(listoftargets.keys()))
    if length > 1:
        keystring = "combobox" + str(length)
        listoftargets[keystring].pack_forget()
        del listoftargets[keystring]

sh_targetplusbutton = ttk.Button(sh_seedbuttons, text="+", command=increasetargetsize)
sh_targetplusbutton.pack(side='left')
sh_targetminusbutton = ttk.Button(sh_seedbuttons, text="-", command=decreasetargetsize)
sh_targetminusbutton.pack(side='left')
sh_seedbuttons.pack(side='top') # Buttons for Plus/Minus Targets

listoftargets[keystring].pack(side='top')

sh_targetseeds.pack(side='right')

def calculateseeds(): # Function for "Calculate Output" button
    global sh_listofseeds
    global listoftargets
    global sh_mapofresults
    global sh_resulttext


    inventory = []

    result = []

    for key in sh_listofseeds:
        seed = str(sh_listofseeds[key].get())
        if seed != '':
            inventory.append(seed)
    for key in listoftargets:
        seed = str(listoftargets[key].get())
        if seed != '':
            result.append(seed)
    
    if not inventory or not result:
        print("Invalid Input!")
        sh_resulttext.set("Invalid Input! Either the Input or the Target is empty!")

    elif len(inventory) < 2:
        print("Not enough seeds in inventory!")
        sh_resulttext.set("Not enough seeds in your inventory!")
    else:
        output = programcalcsteps(inventory, result)
        for item in sh_mapofresults:
            sh_mapofresults[item].pack_forget()
        for key in output:
            keystring = "resulttree" + str(len(list(output.keys())) + 1)
            sh_mapofresults[keystring] = ttk.Treeview(sh_resultframe, columns = ("steps"), show = 'headings')
            sh_mapofresults[keystring].heading("steps", text = key)
            sh_mapofresults[keystring].pack(fill = 'both', expand = True)
            option = 1
            for steps in output[key]:
                sh_mapofresults[keystring].insert(parent = '', index = tk.END, values = (str(option) + ":",))
                for step in steps:
                    sh_mapofresults[keystring].insert(parent = '', index = tk.END, values = (step,))
                option = option + 1

    
sh_resulttext = tk.StringVar()

def programcalcsteps(inputlist, resultlist): # Calculate Seeds, but for the tkinter program (with progress text variable)

    global sh_gather

    output = {}

    gather = sh_gather.get()

    for item in resultlist:
        depth = 1
        found = False
        while depth < 11 and not found:
            possibles = allpossibles(inputlist, depth, gather)
            for key in possibles:
                if item in possibles[key]:
                    found = True
            depth = depth + 1
        
        outputtemp = {}
        
        if not found:
            print("Seed too complicated")
            outputtemp.update({item + " takes over 10 steps and is a bit too complicated for this silly little program...":[]})
        else:
            sh_resulttext.set("Calculating shortest path for " + item + "...")
            outputtemp = shortestpath(inputlist, [item], gather)
            sh_resulttext.set("Calculating amount of steps needed...")
            outputtemp = stepamount(outputtemp)
            sh_resulttext.set("Cleaning up the steps...")
            outputtemp = cleanstep(outputtemp)
            sh_resulttext.set("Creating the steplist...")
            outputtemp = steplist(outputtemp)
        output.update(outputtemp)

    return output

sh_calcbutton = ttk.Button(shortestpathframe, text="Output Steps", command=calculateseeds) # Button to Calculate Seeds

sh_selectbox.pack()
sh_gather = tk.BooleanVar()
sh_gathercheck = ttk.Checkbutton(shortestpathframe, text = "I am not afraid to gather seeds!", variable = sh_gather)
sh_gathercheck.pack()

sh_calcbutton.pack()

sh_resultframe = ttk.Frame(shortestpathframe) # Frame to pack the results into

progress = ttk.Label(sh_resultframe, textvariable=sh_resulttext)

progress.pack()

sh_mapofresults = {}

sh_resultframe.pack(fill = 'x', expand = True)

allpossibilities = ttk.Frame(notebook) # Screen for Function 3

all_instructions = ttk.Label(allpossibilities, text = "On the left side, select the seeds you have. On the right, select a depth.") # Instructions for Function
all_instructions.pack()
all_instructions2 = ttk.Label(allpossibilities, text = "The program will output each seed you can make with the seeds you have in 'depth' steps.")
all_instructions2.pack()
all_instructions3 = ttk.Label(allpossibilities, text = "If the number of steps is smaller than 'depth', then there are no seeds that can be made with additional steps.")
all_instructions3.pack()

# 

all_selectbox = ttk.Frame(allpossibilities)
all_inventory = ttk.Frame(all_selectbox)
all_inventorylabel = ttk.Label(all_inventory, text="Inventory")
all_inventorylabel.pack()
all_buttons = ttk.Frame(all_inventory)

global all_listofseeds

all_listofseeds = {}

keystring = "combobox1"
all_listofseeds[keystring] = ttk.Combobox(all_inventory)
all_listofseeds[keystring]['values'] = list(seeds.keys())

def all_increaseinventorysize(): # Function for the Plus Button
    global all_listofseeds
    length = len(list(all_listofseeds.keys()))
    keystring = "combobox" + str(length + 1)
    all_listofseeds[keystring] = ttk.Combobox(all_inventory)
    all_listofseeds[keystring]['values'] = list(seeds.keys())
    all_listofseeds[keystring].pack(side='top')


def all_decreaseinventorysize(): # Function for the Minus Button
    global all_listofseeds
    length = len(list(all_listofseeds.keys()))
    if length > 1:
        keystring = "combobox" + str(length)
        all_listofseeds[keystring].pack_forget()
        del all_listofseeds[keystring]

all_plusbutton = ttk.Button(all_buttons, text="+", command=all_increaseinventorysize)
all_plusbutton.pack(side='left')
all_minusbutton = ttk.Button(all_buttons, text="-", command=all_decreaseinventorysize)
all_minusbutton.pack(side='left')
all_buttons.pack(side='top') # Buttons to increase/decrease size of Inventory
all_listofseeds[keystring].pack(side='top')

all_inventory.pack(side='left')

all_depth = ttk.Frame(all_selectbox)
all_depthlabel = ttk.Label(all_depth, text="Depth")
all_depthlabel.pack()
all_depthinput = ttk.Frame(all_depth)

all_depthint = tk.IntVar(value = 1)

all_depthspin = ttk.Spinbox(all_depthinput, from_=1, to=100, textvariable=all_depthint)
all_depthspin.pack(side='left')
all_depthspinlabel = ttk.Label(all_depthinput, text=" steps")
all_depthspinlabel.pack(side='left')
all_depthinput.pack()
all_depth.pack(side='right')
all_selectbox.pack()
all_gather = tk.BooleanVar()
all_gathercheck = ttk.Checkbutton(allpossibilities, text = "I am not afraid to gather seeds!", variable=all_gather)
all_gathercheck.pack()

all_resultframe = ttk.Frame(allpossibilities)

all_treeofresults = ttk.Treeview(all_resultframe, columns=("steps"), show='headings')

all_resulttext = tk.StringVar()

def all_calclist():
    global all_listofseeds
    global all_treeofresults
    global all_resulttext
    global all_depthint
    global all_gather

    gather = all_gather.get()

    inventory = []

    steps = -1

    for key in all_listofseeds:
        seed = str(all_listofseeds[key].get())
        if seed != '':
            inventory.append(seed)
    
    steps = all_depthint.get()

    if steps < 1 or not inventory:
        all_resulttext.set("Invalid input!")
    elif len(inventory) == 1:
        all_resulttext.set("Not enough seeds in your inventory!")
    else:
        for item in all_treeofresults.get_children():
            all_treeofresults.delete(item)
        output = allpossibles(inventory, steps, gather)
        for key in output:
            keystring = key  
        all_treeofresults.heading("steps", text=keystring)
        all_treeofresults.pack(fill='both', expand=True)
        for seed in output[keystring]:
            all_treeofresults.insert(parent='', index = tk.END, values=(seed,))

all_calclabel = ttk.Label(allpossibilities, textvariable=all_resulttext)
all_calclabel.pack()

all_calcbutton = ttk.Button(allpossibilities, text="Calculate Output", command=all_calclist)
all_calcbutton.pack()
all_resultframe.pack(fill='x', expand=True)

gatherseeds = ttk.Frame(notebook)

gs_instructions = ttk.Label(gatherseeds, text="Select any target seed you wish.")
gs_instructions.pack()
gs_instructions2 = ttk.Label(gatherseeds, text="The program will tell you what seeds you need to get to be able to get to the target, and where to gather them.")
gs_instructions2.pack()
gs_instructions3 = ttk.Label(gatherseeds, text="DISCLAIMER: There is no way to show *all* possibilities for which seeds to gather. Even for simple seeds, the complexity rises exponentially.")
gs_instructions3.pack()
gs_instructions4 = ttk.Label(gatherseeds, text="The program will only show a highly limited amount of possibilities. ")
gs_instructions4.pack()

gs_selectbox = ttk.Frame(gatherseeds)
gs_target = ttk.Frame(gs_selectbox)
gs_targetlabel = ttk.Label(gs_target, text="Target")
gs_targetlabel.pack()
gs_targetcombobox = ttk.Combobox(gs_target, values=list(seeds.keys()))
gs_targetcombobox.pack()
gs_target.pack()
gs_selectbox.pack()

gs_resultframe = ttk.Frame(gatherseeds)

gs_treeofresults = ttk.Treeview(gs_resultframe, columns=("seeds"), show='headings')

gs_resulttext = tk.StringVar()

def gs_calclist():
    global gs_listofseeds
    global gs_treeofresults
    global gs_resulttext
    global gs_targetcombobox
    
    target = gs_targetcombobox.get()

    if target == '':
        gs_resulttext.set("Invalid input!")
    else:
        for item in gs_treeofresults.get_children():
            gs_treeofresults.delete(item)
        output = seedsources([target])
        for key in output:
            keystring = key  
        gs_treeofresults.heading("seeds", text=keystring)
        gs_treeofresults.pack(fill='both', expand=True)
        option = 1
        for seed in output[keystring]:
            if isinstance(seed, list):
                gs_treeofresults.insert(parent='', index = tk.END, values=(str(option), ))
                print(seed)
                for item in seed:
                    gs_treeofresults.insert(parent='', index = tk.END, values=(item,))
                option = option + 1
            else:
                gs_treeofresults.insert(parent='', index=tk.END, values = (seed,))

gs_calclabel = ttk.Label(gatherseeds, textvariable=gs_resulttext)
gs_calclabel.pack()

gs_calcbutton = ttk.Button(gatherseeds, text="Calculate Output", command=gs_calclist)
gs_calcbutton.pack()
gs_resultframe.pack(fill='x', expand=True)

notebook.add(start, text="Start")
notebook.add(shortestpathframe, text="Shortest path to target seed")
notebook.add(allpossibilities, text="What can you make from the seeds in your inventory?")
notebook.add(gatherseeds, text="Which seeds do you need to gather for a target seed?")

notebook.pack()

root.mainloop()