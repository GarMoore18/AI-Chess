from game_display import Chess

games = ['1','2','3','4']
chose = input('Enter 1 for minimax AI\nEnter 2 for alpha-beta AI\nEnter 3 for alpha-beta looking more moves ahead\nEnter 4 to see invalid game tests\nWhat is your choice? ')
while chose not in games:
    print('Please enter an integer value of 1, 2, 3, or 4.')
    chose = input('Enter 1 for minimax AI\nEnter 2 for alpha-beta AI\nEnter 3 for alpha-beta AI looking more moves ahead\nEnter 4 to see invalid game tests\nWhat is your choice? ')

if chose == '1':
    print('\n')
    #Showing minimax
    print('Test 1:\n\tminimax\n\t3 moves ahead\n\twhite goes first\n\t500ms delay')
    game_1 = Chess()
    game_1.chess_game(1, 3)
    print('\n')

elif chose == '2':
    print('\n')
    #Showing alpha-beta pruning improvement
    print('Test 2:\n\talpha-beta\n\t3 moves ahead\n\twhite goes first\n\t500ms delay')
    game_2 = Chess()
    game_2.chess_game(2, 3)
    print('\n')

elif chose == '3':
    print('\n')
    #Showing alpha-beta allows for extra look ahead and Black turn first
    print('Test 3:\n\talpha-beta\n\t4 moves ahead\n\tblack goes first\n\t500ms delay')
    game_3 = Chess()
    game_3.chess_game(2, 4, False)
    print('\n')

else:
    print('\n')
    #Testing invalid AI
    print('Test 4:\n\tunknown\n\t5 moves ahead\n\twhite goes first\n\t500ms delay')
    game_4 = Chess()
    game_4.chess_game(3, 5)
    print('\n')

    #Testing invalid moves
    print('Test 5:\n\tminimax\n\t4 moves ahead\n\twhite goes first\n\t500ms delay')
    game_5 = Chess()
    game_5.chess_game(1, 4)
    