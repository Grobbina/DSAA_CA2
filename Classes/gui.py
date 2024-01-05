def starty():
    input("""
    ******************************************************
    * ST1507 DSAA: Welcomme to:                          *
    *       ~Evaluating and sorting assignment statements ~  *
    *----------------------------------------------------*
    *                                                    *
    * - Done by: Sean See(2214311),Cai Ruizhe                       *
    * - Class: DAAA/2B01                                 *
    ******************************************************

    Press Enter to continue...
    """)
starty()

#Main Gui
class Gui:
    while True:
        print(f"Please select your choice (1,2,3,4,5,6):\n \t1. Add/Modify assignment statement\n \t2. Display Current Assignment Statement\n \t3. Evaluate a Single Variable\n \t4. Read Assignment statements from file\n \t5. Sort assignment statemnets\n \t6. Exit")
    
        num = int(input("Enter choice:"))

        if num <= 0 or num > 6:
            print("Please choose a valid option\n")
        elif num == 1:
           print(1)
        elif num == 2:
            print(2)
        elif num == 3:
            print(3)
        elif num == 4:
            print(4)
        elif num == 5:
            print(5)
        elif num == 6:
            print('\nBye, thanks for using ST150/DSAA Assignment Statements Evaluation & Sorter')
            break