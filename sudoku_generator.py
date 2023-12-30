
import math, random, pygame

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        for i in range(row_length):
            row = []
            for j in range(row_length):
                row.append(0)
            self.board.append(row)
        self.box_length = int(math.sqrt(row_length))
    
    def get_board(self):
        return self.board

    def print_board(self):
        for i in range(len(self.board)):
            for j in self.board[i]:
                print(j, end = " ")
            print()
   
    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        return True
   
    def valid_in_col(self, col, num):
        for i in range(len(self.board)):
            if self.board[i][col] == num:
                return False
        return True
  
    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if self.board[i][j] == num:
                    return False
        return True
    
    def is_valid(self, row, col, num):
        if self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row // 3 * 3, col // 3 * 3, num):
            return True
        return False
                                                                                            
    def fill_box(self, row_start, col_start):
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                random_int = random.randint(1,9)
                while not self.valid_in_box(row_start, col_start, random_int):
                    random_int = random.randint(1,9)
                self.board[i][j] = random_int
       
    def fill_diagonal(self):
        self.fill_box(0,0)
        self.fill_box(3,3)
        self.fill_box(6,6)
  
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True       
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False
   
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)
  
    def remove_cells(self):
        for i in range(self.removed_cells):
            random_row = random.randint(0,8)
            random_col = random.randint(0,8)
            while self.board[random_row][random_col] == 0:
                random_row = random.randint(0,8)
                random_col = random.randint(0,8)
            self.board[random_row][random_col] = 0

class Cell:
    def __init__(self,value,row,col,screen,width,height, CONSTANT):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.width = width
        self.height = height
        self.selected = False
        self.CONSTANT = CONSTANT
        self.sketched_value = 0

    def set_cell_value(self,value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        number_font = pygame.font.SysFont(None, 64)
        if self.value != 0 and self.CONSTANT:           
            number_image = number_font.render(str(self.value),True,(0,0,0), (220,255,255))
            self.screen.blit(number_image, (self.row * 70 + 25, self.col * 70 + 17))
        elif self.value != 0 and not self.CONSTANT:
            number_image = number_font.render(str(self.value),True,(255,0,0), (220,255,255))
            self.screen.blit(number_image, (self.row * 70 + 25, self.col * 70 + 17))
        if self.selected:
            pygame.draw.line(self.screen,(255,0,0), (self.row * 70, self.col * 70), (self.row * 70 + 70, self.col * 70), 4)
            pygame.draw.line(self.screen,(255,0,0), (self.row * 70, self.col * 70 + 70), (self.row * 70 + 70, self.col * 70 + 70), 4)
            pygame.draw.line(self.screen,(255,0,0), (self.row * 70, self.col * 70), (self.row * 70, self.col * 70 + 70), 4)
            pygame.draw.line(self.screen,(255,0,0), (self.row * 70 + 70, self.col * 70), (self.row * 70 + 70, self.col * 70 + 70), 4)
        if self.sketched_value != 0:
            number_font = pygame.font.SysFont(None, 32)
            number_image = number_font.render(str(self.sketched_value),True,(135,135,135), (220,255,255))
            self.screen.blit(number_image, (self.row * 70 + 10, self.col * 70 + 10))
     
class Board:
    def __init__(self, rows, cols, width, height, screen, difficulty,sudoku):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = []
        self.sudoku, self.full_board = sudoku
        for i in range(len(self.sudoku)):
            row = []
            for j in range(len(self.sudoku[i])):
                if self.sudoku[i][j] != 0:
                    c = Cell(self.sudoku[i][j], i, j, screen, 0,0, True)
                else:
                   c = Cell(self.sudoku[i][j], i, j, screen, 0,0, False) 
                row.append(c)
            self.cells.append(row)
        
    def draw(self):
        self.screen.fill((220,255,255))
        draw_lines(self.screen)
        for i in range(4):
            pygame.draw.line(self.screen,(0,0,0), (self.width // 3 * i, 0), (self.width // 3 * i, 630), 10)
            pygame.draw.line(self.screen,(0,0,0), (0 , self.width // 3 * i), (630, self.width // 3 * i), 10)
            for i in range(len(self.cells)):
                for j in self.cells[i]:
                    j.draw()
        #Buttons
        number_font = pygame.font.SysFont(None, 40)
        reset_button = number_font.render("Reset",True,(255,255,255), (220,0,0))
        self.screen.blit(reset_button, (150, 650))
        restart_button = number_font.render("Restart",True,(255,255,255), (220,0,0))
        self.screen.blit(restart_button, (240, 650))
        exit_button = number_font.render("Exit",True,(255,255,255), (220,0,0))
        self.screen.blit(exit_button, (350, 650))

    def select(self, row, col):
        if self.cells[row][col].selected:
            self.cells[row][col].selected = False
        else:
            for i in range(len(self.cells)):
                for j in self.cells[i]:
                    j.selected = False
            if not self.cells[row][col].CONSTANT:
                self.cells[row][col].selected = True
            
    def click(self,x,y):
        if x > 0 and x < self.width and y > 0 and y < self.height:
            return (x,y)
        return None
    
    def clear(self, row, col):
        if not self.cells[row][col].CONSTANT:
            self.cells[row][col].value = 0
            self.cells[row][col].sketched_value = 0

    def sketch(self, value, row, col):
        if not self.cells[row][col].CONSTANT and self.cells[row][col].value == 0:
            self.cells[row][col].sketched_value = value

    def place_numbers(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j].sketched_value != 0:
                    self.cells[i][j].value = self.cells[i][j].sketched_value
                    self.cells[i][j].sketched_value = 0

    def reset_to_original(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if not self.cells[i][j].CONSTANT:
                    self.cells[i][j].value = 0
                    self.cells[i][j].sketched_value = 0

    def check_win(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if self.cells[i][j].value != self.full_board[i][j]:
                    return False
        return True

    def check_if_full(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if self.cells[i][j].value == 0:
                    return False
        return True

#functions outside class
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    full_board = []
    for i in range(len(board)):
        row = []
        for j in board[i]:
            row.append(j)
        full_board.append(row)
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board, full_board

def draw_lines(screen):
    for i in range(10):
        pygame.draw.line(screen, [0,0,0], (i * 70, 0), (i * 70, 630), 2)
        pygame.draw.line(screen, [0,0,0], (0, i * 70), (630, i * 70), 2)

def game_start(difficulty):
    pygame.init()
    screen = pygame.display.set_mode((630, 700)) #10x9 grid, 1 box length saved at buttom for buttons, each box is 70x70 pixels
    pygame.display.set_caption('Sudoku')
    board = Board(9,9,630,700,screen,0, generate_sudoku(9,difficulty))
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                row, col = x // 70, y // 70
                if (row < 9 and col < 9):
                    board.select(row, col)
                if (x >= 350 and x <= 403 and y >= 650 and y <= 677):   #Exit button
                    game_running = False
                if (x >= 240 and x <= 335 and y >= 650 and y <= 677):   #New board
                    board = Board(9,9,630,700,screen,0, generate_sudoku(9,difficulty))
                if (x >= 150 and x <= 224 and y >= 650 and y <= 677):   #Reset to original
                    board.reset_to_original()
                    for i in range(len(board.cells)):
                        for j in board.cells[i]:
                            j.selected = False
            if event.type == pygame.KEYDOWN and board.cells[row][col].selected: #Place sketched numbers
                if event.key == pygame.K_1:
                    board.sketch(1, row, col)
                if event.key == pygame.K_2:
                    board.sketch(2, row, col)
                if event.key == pygame.K_3:
                    board.sketch(3, row, col)
                if event.key == pygame.K_4:
                    board.sketch(4, row, col)
                if event.key == pygame.K_5:
                    board.sketch(5, row, col)
                if event.key == pygame.K_6:
                    board.sketch(6, row, col)
                if event.key == pygame.K_7:
                    board.sketch(7, row, col)
                if event.key == pygame.K_8:
                    board.sketch(8, row, col)
                if event.key == pygame.K_9:
                    board.sketch(9, row, col)
                if event.key == pygame.K_BACKSPACE:
                    board.clear(row, col)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    #Enter sketched numbers as normal numbers
                    board.place_numbers()                  
        board.draw()
        pygame.display.update()
        if board.check_win() and board.check_if_full():
            game_running = False
            WinningWindow()
        if board.check_if_full() and not board.check_win():
            game_running = False
            GameOver(difficulty)
    pygame.quit()

def WelcomeWindow():
    pygame.init()
    screen = pygame.display.set_mode((630, 700)) #10x9 grid, 1 box length saved at buttom for buttons, each box is 70x70 pixels
    pygame.display.set_caption('Welcome Window')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if (x >= 130 and x <= 226 and y >= 400 and y <= 442): # Easy
                    running = False
                    game_start(2)
                elif (x >= 240 and x <= 397 and y >= 400 and y <= 442): #Medium
                    running = False
                    game_start(40)
                elif (x >= 410 and x <= 509 and y >= 400 and y <= 442): #Hard
                    running = False
                    game_start(50)
        screen.fill((255,255,255))
        number_font = pygame.font.SysFont(None, 80)
        welcome = number_font.render("Welcome To Sudoku!",True,(0,0,0), (255,255,255))
        screen.blit(welcome, (30, 120))
        select_font = pygame.font.SysFont(None, 60)
        select = select_font.render("Select Game Mode:", True, (0,0,0), (255,255,255))
        screen.blit(select, (120, 300))
        number_font = pygame.font.SysFont(None, 60)
        easy_button = number_font.render("Easy",True,(255,255,255), (220,0,0))
        screen.blit(easy_button, (130, 400))       
        med_button = number_font.render("Medium",True,(255,255,255), (220,0,0))
        screen.blit(med_button, (240, 400))
        hard_button = number_font.render("Hard",True,(255,255,255), (220,0,0))
        screen.blit(hard_button, (410, 400))
        pygame.display.update()
    pygame.quit()

def WinningWindow():
    pygame.init()
    screen = pygame.display.set_mode((630, 700)) 
    pygame.display.set_caption('Winning Window')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if (x >= 270 and x <= 365 and y >= 300 and y <= 348):
                    running = False
        screen.fill((255,255,255))
        number_font = pygame.font.SysFont(None, 80)
        win = number_font.render("Game Won!",True,(0,0,0), (255,255,255))
        screen.blit(win, (170, 120))
        number_font = pygame.font.SysFont(None, 70)
        exit_button = number_font.render("Exit",True,(255,255,255), (220,0,0))
        screen.blit(exit_button, (270, 300))               
        pygame.display.update()
    pygame.quit()

def GameOver(difficulty):
    pygame.init()
    screen = pygame.display.set_mode((630, 700)) 
    pygame.display.set_caption('Lost Window')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if (x >= 220 and x <= 390 and y >= 300 and y <= 348):
                    running = False
                    game_start(difficulty)
        screen.fill((255,255,255))
        number_font = pygame.font.SysFont(None, 80)
        win = number_font.render("Game Lost!",True,(0,0,0), (255,255,255))
        screen.blit(win, (170, 120))
        number_font = pygame.font.SysFont(None, 70)
        exit_button = number_font.render("Restart",True,(255,255,255), (220,0,0))
        screen.blit(exit_button, (220, 300))    
        pygame.display.update()
    pygame.quit()
