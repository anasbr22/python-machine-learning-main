import tkinter as tk
import numpy as np
from tkinter import ttk





test_matrice = [
    [1, 2, 3, 0, 0, 4, 0, 5, 0],
    [6, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 8, 4, 0],
    [2, 0, 0, 0, 9, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 8, 0, 2, 9],
    [0, 0, 4, 3, 0, 0, 0, 0, 1],
    [0, 0, 0, 6, 0, 5, 0, 0, 0]
]
test_matrice2=[[4, 5, 0, 2, 6, 0, 9, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 4],
    [8, 1, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 3, 5, 8, 0, 4, 0, 7],
    [7, 0, 0, 3, 0, 0, 1, 6, 8],
    [9, 8, 0, 7, 4, 6, 0, 5, 0],
    [6, 7, 2, 8, 0, 0, 3, 0, 0],
    [0, 0, 0, 1, 9, 2, 0, 0, 6],
    [0, 9, 8, 6, 7, 3, 5, 0, 2]]




win=tk.Tk()
win.title("sudoku")
win.geometry("700x600+300+20")



label1=tk.Label(win,text="* SUDOKU *",fg="gray",font=('Courier New', 23))
label1.grid(column=0,row=0,columnspan=11)



num = np.zeros((9,9), dtype=tk.Entry)
num = [[ttk.Combobox(win, values=[n for n in range(10)], width=3, font=('Arial', 17)) for _ in range(9)] for _ in range(9)]


# separators
for col in (3,7):
                for ir in range(11):
                        tk.Label(win,text="¤",font=('Courier New', 14),fg="gray",padx=6,pady=6).grid(column=col,row=ir+1)
                for ic in range(11):
                        tk.Label(win,text="¤",font=('Courier New', 14),fg="gray",padx=6,pady=6).grid(column=ic,row=col+1)


# num grid 
for i in range(9):
    for j in range(9):
        
            c=j
            r=i+1            

            if (c in (3,4,5)):
                c += 1
            elif (c in (6,7,8)):
                c += 2

            if (r in (4,5,6)):
                r += 1
            elif (r in (7,8,9)):
                r += 2


            num[i][j].grid(row=r, column=c,padx=5,pady=5)
            num[i][j].set("0")


# Functions
            
def example():
    global test_matrice
    global test_matrice2
    for i in range(9):
        for j in range(9):
            num[i][j].set(test_matrice2[i][j])
            num[i][j].configure(foreground="black")


def reset():
    global Lconfirm

    for i in range(9):
        for j in range(9):
            num[i][j].set("0")
            num[i][j].configure(foreground="black")
    
    Lconfirm.configure(text="")


def findEmpty(matrice):
    emptyTab = []
    for i in range(9):
        for j in range(9):
            if matrice[i][j] == 0:
                emptyTab.append([i, j, 0])
    return emptyTab


matrice = np.zeros((9, 9), dtype=int)
empty = []


def get_matrice():
    global matrice
    global num
    global empty

    for i in range(9):
        for j in range(9):
            matrice[i][j] = np.int32(num[i][j].get())

    empty = findEmpty(matrice)


def update_disp():
    global empty
    global num
    global matrice

    for emp_cel in empty:
        l, c, _ = emp_cel
        num[l][c].set(matrice[l][c])
        num[l][c].configure(foreground="green")
    


def checkExist(number, matrice, a, b):
    # row
    for i in range(9):
        if b != i and matrice[a][i] == number  :
            return False
    # col
    for i in range(9):
        if  a != i and matrice[i][b] == number:
            return False
    # box
    bx = a // 3
    by = b // 3

    xstart=bx * 3
    xstop=xstart+3

    ystart=by * 3
    ystop=ystart+3

    for i in range(xstart, xstop):
        for j in range(ystart, ystop):
            if matrice[i][j] == number and i !=a and  j!=b:
                return False
    return True

def checkValidSudoku():
    global matrice
    global Lconfirm
    global num
    get_matrice()

    for i in range(9):
        for j in range(9):
            if matrice[i][j] != 0:
                if not checkExist(matrice[i][j],matrice,i,j):
                     Lconfirm.configure(text=("Error in the index : ",i,"x",j),fg="red")
                     num[i][j].configure(foreground="red")
                     return (True,i,j)
                else:
                      num[i][j].configure(foreground="black")
            else:
                 num[i][j].configure(foreground="black")        
                     
    Lconfirm.configure(text="matrix valid",fg="green")
    return (True,-1,-1)
    
    

def solve(matrice, empty, cnt):
    
    if cnt > len(empty) - 1:
        return True
    else:
        empty_cel = empty[cnt]
        row, col, _ = empty_cel

    for n in range(1, 10):
        if checkExist(n, matrice, row, col):
            matrice[row][col] = n
                
            if solve(matrice, empty, cnt + 1):
                return True
            matrice[row][col] = 0

    return False


def get_solve():
    global matrice
    global empty
    global Lconfirm

    get_matrice()

    if checkValidSudoku()==(True,-1,-1):

        if solve(matrice, empty, 0):
            Lconfirm.configure(text="Solution found")
            update_disp()
        else:
            print("No solution found")
            Lconfirm.configure(text="No solution found")
            return 0
    

# Buttons
Breset = tk.Button(win, text="Reset", font=('Arial', 13), fg="red",bg="#C8C6C6", command=reset)
Breset.grid(column=0, row=16, columnspan=3, padx=10, pady=14)

Bsolve = tk.Button(win, text="Solve", font=('Arial', 13), fg="green",bg="#C8C6C6", command=get_solve)
Bsolve.grid(column=4, row=16, columnspan=3, padx=10, pady=14)

Bexample = tk.Button(win, text="Example", font=('Arial', 13),bg="#C8C6C6", command=example)
Bexample.grid(column=8, row=16, columnspan=3, padx=10, pady=14)

Bconfirm = tk.Button(win, text="Confirm",fg="#747264", font=('Arial', 13),bg="#C8C6C6", command=checkValidSudoku)
Bconfirm.grid(column=0, row=17, columnspan=3, padx=10, pady=5)

Lconfirm=tk.Label(win,font=('Courier New', 14),bg="#C8C6C6",width=30)
Lconfirm.grid(column=4, row=17, columnspan=6, padx=3, pady=5)

win.mainloop()
