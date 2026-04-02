# import labraries
import math
from datetime import datetime

history = []
memory = 0.0
last_result = 0.0

while True:
    try:
        # Get the input 
        print ("\n Welcome to the Python Calculator!")
        print ("\n Available operations: +, -, *, /^(power), %(modulo), sqrt, sin, cos, tan, log, abs.")
        print ("\n Type 'History' to see past calculations or 'Exit' to quit.")
        print ("\n Commands: history, exit, mc (Clear), ms (Store), m+ (Add), mr (Recall)")

        User_input = input ("\n Enter the first number (or command): ").lower()

        # Handle History and Exit commands 
        if User_input =='history':
            if not history:
                print ("\n Histoy is empty.")
            else:
                print ("\n ----Calculator History---")
                for entry in history:
                    print (f"{entry['expression']} = {entry['result']}")
                continue
        elif User_input == 'exit':
            print ("\n Goodbye!")
            break
        elif User_input == 'mc':
            memory = 0.0
            print ("🧹 Memory cleared.")
            continue
        elif User_input == 'ms':
            memory = last_result
            print (f"💾 Stored {last_result} to memory.")
            continue
        elif User_input == 'm+':
            memory += last_result
            print(f"➕ Added {last_result} to memory. New Memory: {memory}")
            continue

        # Process first number (allowing 'mr'as a valid number input)  
        if User_input == 'mr':
            num1 = memory
            print(f"> Using recalled memory value: {num1}")
        else:
            num1 = float(User_input)

        op = input ("Enter the operation: ").lower()

        # Check if unary or binary
        uniary_op = ["sqrt", "sin", "cos", "tan", "log", "abs"]
        num2 = None
        expression = ""

        if op not in uniary_op:
            num2 = float(input ("Enter the second numer: "))
            expression = f"{num1}{op}{num2}"
        else:
            expression = f"{op}{num1}"

        result = None # initialize the result to none 

        # Basic Operations
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result  = num1 - num2 
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 != 0:
                result = abs(num1 / num2)
            else:
                print ("\n 🧨 Error: Cannot devide by 0!" )
        elif op == "^":
            result = num1 ** num2
        elif op == "%":
            if num2 == 0:
                print ("Error!")
            else:
                result = num1 % num2   

        # Unary Operations
        elif op == "sqrt":
            if num1 >= 0:
                result = math.sqrt(num1)
            else:
                print ("Error: Cannot sqrt a negative number!")
        elif op == "sin":
            result = math.sin(math.radians(num1))
        elif op == "cos":
            result = math.cos(math.radians(num1))
        elif op == "tan":
            result = math.tan(math.radians(num1))
        elif op == "log":
            if num1 >= 0:
                print (f"The result is {math.log10(num1)}")
            else:
                print ("Error")
        elif op == "abs":
            result = abs(num1)
        else:
            print ("\n Invalid operation selected. try again!")

        # Save to the history
        if result is not None:
            print (f"The result is: {result}")

            # Create the dictionary and append to histoy
            calc_entry = {
                "expression": expression,
                "result": result,
            }
            history.append(calc_entry)

        # Ask user for further choice    
        choice = input ("Exit (y/n): ").lower()
        if choice == "y":
            print ("\n Goodbye!")
            break 

    # if user enter the wrong datatype
    except ValueError:
        print("\n Invalid input! Please enter a nmeric value.")
        
