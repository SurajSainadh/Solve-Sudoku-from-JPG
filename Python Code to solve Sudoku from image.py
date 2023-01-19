
import cv2
import pytesseract
import numpy as np
from PIL import Image


# COmmented steps are for people with Tessaract, If not upload the matric directly as shown below
# # Load the image
# image = cv2.imread("Sudoku_Picture.jpg")

# # Pre-process the image
# gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
# gray1 = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# # Run OCR on the image
# text = pytesseract.image_to_string(gray1, lang='eng', config='--psm 10')

# # Convert the text to a 9x9 matrix
# matrix = [[int(c) if c.isdigit() else 0 for c in line] for line in text.split()]

matrix = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# Solve the puzzle
def isSolvable(puzzle):
    # check if puzzle has at least 17 filled cells
    filled = 0
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                filled += 1
    if filled < 17:
        return False
    # check if puzzle has unique solution
    # (there should be no repeated numbers in rows, columns, or sub-grids)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                for x in range(9):
                    if (x != j and puzzle[i][x] == puzzle[i][j]) or (x != i and puzzle[x][j] == puzzle[i][j]):
                        return False
                sx = (i // 3) * 3
                sy = (j // 3) * 3
                for x in range(sx, sx + 3):
                    for y in range(sy, sy + 3):
                        if (x != i or y != j) and puzzle[x][y] == puzzle[i][j]:
                            return False
    return True

def findNextEmptyCell(puzzle):
    # find the empty cell with the least possibilities
    min_possibilities = 10
    empty_cell = [-1, -1]
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                possibilities = 0
                for num in range(1, 10):
                    if isValid(puzzle, i, j, num):
                        possibilities += 1
                if possibilities < min_possibilities:
                    min_possibilities = possibilities
                    empty_cell = [i, j]
    return empty_cell

def isValid(puzzle, row, col, num):
    # check if num is valid in the given cell
    for i in range(9):
        if puzzle[i][col] == num or puzzle[row][i] == num:
            return False
    sx = (row // 3) * 3
    sy = (col // 3) * 3
    for x in range(sx, sx + 3):
        for y in range(sy, sy + 3):
            if puzzle[x][y] == num:
                return False
    return True

def isempty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return False
    return True

def solveSudoku(puzzle):
    # check if puzzle is solvable
    if not isSolvable(puzzle):
        return 0
    # find the empty cell with the least possibilities
    [row, col] = findNextEmptyCell(puzzle)
    # if there are no more empty cells, the puzzle is solved

    if isempty(puzzle):
        return puzzle
    # try the possible numbers for the empty cell
    for num in range(1,10):
        if isValid(puzzle, row, col, num):
            puzzle[row][col] = num
            solution = solveSudoku(puzzle)
            # if a solution is found, return it
            if solution is not None:
                return solution
    # if no solution is found, backtrack
    puzzle[row][col] = 0
    return None


solution = solveSudoku(matrix)
if solution is not None:
    print('Solution:')
    print(solution)
else:
    print('No solution found')
    
    


# Create an empty image with a white background
solved_image = 255 * np.ones((450, 450, 3), np.uint8)

# Define the font and the font size
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1

# Define the text color
color = (0, 0, 0)

# Iterate through the matrix and add the digits to the image
height, width, channels = solved_image.shape
cell_size = (width/9,height/9)

cv2.imshow('solved sudoku',solved_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


for i in range(9):
    for j in range(9):
        text = str(solution[i][j])
        text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
        x = 50 * j + 25 - text_size[0] / 2
        y = 50 * i + 38 + text_size[1] / 2
        text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
        text_x = x + (cell_size[0] - text_size[0]) / 2
        text_y = y + (cell_size[1] + text_size[1]) / 2

        cv2.putText(solved_image, text, (int(text_x), int(text_y)), font, font_scale, color, 2, cv2.LINE_AA)

# Draw a black border around the entire puzzle
cv2.rectangle(solved_image, (0,0), (450,450), (0,0,0), thickness=10)

# Fill the background outside the puzzle with white color
cv2.rectangle(solved_image, (10,10), (440,440), (255,255,255), -1)


# Draw the lines that separate the cells
for i in range(1, 9):
    x = 50 * i
    cv2.line(solved_image, (x, 0), (x, 450), (0, 0, 0), 2)
    cv2.line(solved_image, (0, x), (450, x), (0, 0, 0), 2)

# Draw the lines that separate the sub-grids
cv2.line(solved_image, (150, 0), (150, 450), (0, 0, 0), 4)
cv2.line(solved_image, (300, 0), (300, 450), (0, 0, 0), 4)
cv2.line(solved_image, (0, 150), (450, 150), (0, 0, 0), 4)
cv2.line(solved_image, (0, 300), (450, 300), (0, 0, 0), 4)

#Save the image to a file
cv2.imwrite('solved_sudoku.jpg', solved_image)
