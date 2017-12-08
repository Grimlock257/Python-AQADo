import pygame
import pickle
import Entities
import Colours
import time

# Define window properties
size = width, height = 480, 400
caption = "Adam Watson - NTU Python Programming Assignment"

# Clock variables
clock = pygame.time.Clock()
TARGET_FPS = 10

# Initialise PyGame
pygame.init()

# Fonts
title_font = pygame.font.SysFont("Source Code Pro Bold", 52)
main_font = pygame.font.SysFont("Source Code Pro", 18)
small_font = pygame.font.SysFont("Source Code Pro", 11)

# Set up the PyGame display window
display = pygame.display.set_mode(size)
pygame.display.set_caption(caption)

# Initialise renderer
renderer = Entities.Render()


def display_main_menu():
    """ Display the main menu to the users """
    # Create the main menu button/text objects
    txt_title = Entities.Text(title_font, "NTU Python Assessment", Colours.WHITE, width / 2, 38)

    btn_play = Entities.Button(main_font, "New Game", Colours.BLACK, width / 2, 125)
    btn_load = Entities.Button(main_font, "Load Game", Colours.BLACK, width / 2, 175)
    btn_rules = Entities.Button(main_font, "Rules", Colours.BLACK, width / 2, 225)
    btn_scores = Entities.Button(main_font, "Highscores", Colours.BLACK, width / 2, 275)
    btn_quit = Entities.Button(main_font, "Quit", Colours.BLACK, width / 2, 325)

    while True:
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for each button object and do necessary function call if needed
            play() if btn_play.event(e) else False
            display_saved_games("main") if btn_load.event(e) else False
            display_rules("main") if btn_rules.event(e) else False
            display_highscores() if btn_scores.event(e) else False
            quit_game() if btn_quit.event(e) else False

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add((128, 89, 224, 272))
        renderer.add(txt_title)
        renderer.add(btn_play)
        renderer.add(btn_load)
        renderer.add(btn_rules)
        renderer.add(btn_scores)
        renderer.add(btn_quit)

        renderer.draw("bg_plain")


def display_saved_games(return_to):
    """ Display the available saved games from /game_saves """
    # Create the main menu button/text objects
    txt_title = Entities.Text(title_font, "Load Game", Colours.WHITE, width / 2, 38)
    txt_hint = Entities.Text(main_font, "Select a slot to load from", Colours.WHITE, width / 2, 380)

    btn_load_1 = Entities.Button(main_font, "Load Slot 1", Colours.WHITE, width / 2, 120)
    btn_load_2 = Entities.Button(main_font, "Load Slot 2", Colours.WHITE, width / 2, 160)
    btn_load_3 = Entities.Button(main_font, "Load Slot 3", Colours.WHITE, width / 2, 200)
    btn_load_4 = Entities.Button(main_font, "Load Slot 4", Colours.WHITE, width / 2, 240)

    btn_return = Entities.Button(main_font, "Return to " + ("Main Menu" if return_to is "main" else "Game"),
                                 Colours.WHITE, width / 2, 300)

    while True:
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for the button object and do necessary function call if needed
            if return_to is "main" and btn_return.event(e):
                display_main_menu()
            elif return_to == "play" and btn_return.event(e):
                return
            elif btn_return.event(e):
                print("Invalid return_to parameter:", return_to)

            if btn_load_1.event(e):
                if load_game(1) is None:
                    txt_hint.update_text("No save under slot 1!")
            if btn_load_2.event(e):
                if load_game(2) is None:
                    txt_hint.update_text("No save under slot 2!")
            if btn_load_3.event(e):
                if load_game(3) is None:
                    txt_hint.update_text("No save under slot 3!")
            if btn_load_4.event(e):
                if load_game(4) is None:
                    txt_hint.update_text("No save under slot 4!")

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add(txt_title)
        renderer.add(txt_hint)
        renderer.add(btn_load_1)
        renderer.add(btn_load_2)
        renderer.add(btn_load_3)
        renderer.add(btn_load_4)
        renderer.add(btn_return)

        renderer.draw("bg_plain", Colours.BLACK)


def load_game(save_number):
    """ Load a saved game state into the game ready to be played """
    # Try to open the file, catch if the file is not found (i.e no save game under that slot)
    try:
        file = open("game_saves/save_game_" + str(save_number) + ".dat", "rb")
        loaded_game_data = pickle.load(file)
        file.close()
    except FileNotFoundError:
        return None

    play(True, loaded_game_data)


def display_rules(return_to=None):
    """ Display the game rules to the users """
    str_rules = \
        "Each player has 2 counters, the objective is for a player to get \n" \
        "each of their counters to the FINISH space before the other player.\n" \
        "The game uses a 5 sided dice. The result a dice throw is as follows:"

    str_die_results = \
        "+-----------+----------------------------------------------------+\n" \
        "| Dice Roll | Action                                             |\n" \
        "+-----------+----------------------------------------------------+\n" \
        "|     1     | Move a counter of choice 1 space closer to FINISH  |\n" \
        "+-----------+----------------------------------------------------+\n" \
        "|     2     | Move a counter of choice 2 spaces closer to FINISH |\n" \
        "+-----------+----------------------------------------------------+\n" \
        "|     3     | Move a counter of choice 3 spaces closer to FINISH |\n" \
        "+-----------+----------------------------------------------------+\n" \
        "|     4     | Move a counter of choice 1 space closer to START   |\n" \
        "+-----------+----------------------------------------------------+\n" \
        "|     5     | Select a counter to move to the next EMPTY row     |\n" \
        "+-----------+----------------------------------------------------+"

    # Create the main menu button/text objects
    txt_rules_title = Entities.Text(title_font, "Rules", Colours.WHITE, width / 2, 38)
    txt_goal = Entities.Text(small_font, str_rules, Colours.WHITE, width / 2, 100)
    txt_die_results = Entities.Text(small_font, str_die_results, Colours.WHITE, width / 2, 150)

    btn_return = Entities.Button(main_font, "Return to " + ("Main Menu" if return_to is "main" else "Game"),
                                 Colours.WHITE, width / 2, 300)

    while True:
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for the button object and do necessary function call if needed
            if return_to is "main" and btn_return.event(e):
                display_main_menu()
            elif return_to == "play" and btn_return.event(e):
                return

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add(txt_rules_title)
        renderer.add(txt_goal)
        renderer.add(txt_die_results)
        renderer.add(btn_return)

        renderer.draw("bg_plain")


def play(need_load_game=False, data=None):
    """ This is the main play function, the game essentially takes place here """
    # Initial game object initialisations
    if need_load_game:
        p1_c1 = data["p1_c1"]
        p1_c2 = data["p1_c2"]
        p2_c1 = data["p2_c1"]
        p2_c2 = data["p2_c2"]
        die = data["die"]

        # Update the rects for the counters and die
        p1_c1.from_load()
        p1_c2.from_load()
        p2_c1.from_load()
        p2_c2.from_load()
        die.from_load()

        # Game play variables
        names = data["names"]

        p1_c1_move = data["p1_c1_move"]
        p1_c2_move = data["p1_c2_move"]
        p2_c1_move = data["p2_c1_move"]
        p2_c2_move = data["p2_c2_move"]

        die_result = data["die_result"]
        die_rolled = data["die_rolled"]

        move_by = data["move_by"]

        turn = data["turn"]  # 1 or 2

        scores = data["scores"]
    else:
        p1_c1 = Entities.Counter(1, 1)
        p1_c2 = Entities.Counter(1, 2)
        p2_c1 = Entities.Counter(2, 1)
        p2_c2 = Entities.Counter(2, 2)
        die = Entities.Die()

        # Game play variables
        names = display_enter_player_names()

        p1_c1_move = True, None
        p1_c2_move = True, None
        p2_c1_move = True, None
        p2_c2_move = True, None

        die_result = 0
        die_rolled = False

        move_by = 0

        turn = 1  # 1 or 2

        scores = [0, 0]  # Player 1 score, Player 2 score

    # Set up text and button objects
    current_player = Entities.Text(small_font, "Current Player", Colours.WHITE, 430, 135)
    txt_player_one = Entities.Text(small_font, names[0], Colours.WHITE, 430, 150)
    txt_player_two = Entities.Text(small_font, names[1], Colours.WHITE, 430, 150)
    txt_hint = Entities.Text(small_font, "Test", Colours.WHITE, width / 2, 380)

    btn_load = Entities.Button(small_font, "Load", Colours.WHITE, 430, 214)
    btn_save = Entities.Button(small_font, "Save", Colours.WHITE, 430, 246)
    btn_rules = Entities.Button(small_font, "Rules", Colours.WHITE, 430, 278)
    btn_return = Entities.Button(small_font, "Return to\nMenu", Colours.WHITE, 430, 305)

    # Draw to the screen
    def render_board():
        renderer.update_display(display)

        renderer.add(p1_c1)
        renderer.add(p1_c2)
        renderer.add(p2_c1)
        renderer.add(p2_c2)
        renderer.add(die)
        renderer.add(current_player)
        renderer.add(txt_player_one if turn == 1 else txt_player_two)
        renderer.add(btn_load)
        renderer.add(btn_save)
        renderer.add(btn_rules)
        renderer.add(btn_return)
        renderer.add(txt_hint)

        renderer.draw("bg_play", Colours.BLACK)

    def end_turn():
        """ Handle end of turn information such as switching of turns, die image reset etc. """
        new_turn = 1 if turn == 2 else 2
        die.update_image(0)

        check_winner()

        return new_turn, False, 0, 1

    def check_winner():
        """ Check if a player has both of their counters on row 11 (FINISH) """
        if p1_c1.get_row() == 11 and p1_c2.get_row() == 11:
            display_winner(names[0], scores[0])

        if p2_c1.get_row() == 11 and p2_c2.get_row() == 11:
            display_winner(names[1], scores[1])

    def calculate_move_by(result):
        """ Calculate the move_by variable based on the die result, essentially convert the die result
        into the movement distance as specified by the rules """
        movement = 0

        if result in [1, 2, 3]:
            return result
        elif result == 4:
            movement = -1
        elif result == 5:
            movement = "available"

        return movement

    def get_move_text(movement):
        """ Return the text to display to the user based on their movement result """
        if movement == 1:
            return "select counter to move 1 space closer to FINISH!"
        elif movement in [2, 3]:
            return "select counter to move " + str(movement) + " spaces closer to FINISH!"
        elif movement == -1:
            return "select counter to move 1 space closer to START!"
        elif movement == "available":
            return "select counter to move to next EMPTY row!"

    # Main game loop
    while True:
        # Handle events (beginning of game logic - i.e clicks on the window)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            die_event = die.event(e, die_rolled)

            # Check if the die was clicked
            if die_event[0]:
                if not die_rolled:
                    die_result = die_event[1]
                    die_rolled = True
                    move_by = calculate_move_by(die_result)
                    if turn == 1:
                        p1_c1_move = p1_c1.can_move(move_by, p1_c2.get_row(), p2_c1.get_row(), p2_c2.get_row())
                        p1_c2_move = p1_c2.can_move(move_by, p1_c1.get_row(), p2_c1.get_row(), p2_c2.get_row())
                    elif turn == 2:
                        p2_c1_move = p2_c1.can_move(move_by, p2_c2.get_row(), p1_c1.get_row(), p1_c2.get_row())
                        p2_c2_move = p2_c2.can_move(move_by, p2_c1.get_row(), p1_c1.get_row(), p1_c2.get_row())
                else:
                    txt_hint.update_text("You can only roll once!", 2)

            # Game logic for each player turn
            if turn == 1:
                if p2_c1.event(e) or p2_c2.event(e):
                    txt_hint.update_text("This isn't your counter!", 2)
                elif die_rolled:
                    if not p1_c1_move[0] and p1_c1.event(e):
                        txt_hint.update_text("This counter cannot be moved!", 2)
                    elif p1_c1_move[0] and p1_c1.event(e):
                        p1_c1.move(p1_c1_move[1])
                        scores[0] += p2_c1.counter_moved(p1_c1.get_row())
                        scores[0] += p2_c2.counter_moved(p1_c1.get_row())
                        turn, die_rolled, die_result, txt_hint.get_text_manager().priority = end_turn()
                    elif not p1_c2_move[0] and p1_c2.event(e):
                        txt_hint.update_text("This counter cannot be moved!", 2)
                    elif p1_c2_move[0] and p1_c2.event(e):
                        p1_c2.move(p1_c2_move[1])
                        scores[0] += p2_c1.counter_moved(p1_c2.get_row())
                        scores[0] += p2_c2.counter_moved(p1_c2.get_row())
                        turn, die_rolled, die_result, txt_hint.get_text_manager().priority = end_turn()
                    elif not p1_c1_move[0] and not p1_c2_move[0]:
                        txt_hint.update_text("No counter can move, ending turn...", 3)
                        render_board()
                        time.sleep(5)
                        turn, die_rolled, die_result, txt_hint.get_text_manager().priority = end_turn()
                elif p1_c1.event(e) or p1_c2.event(e):
                    txt_hint.update_text(names[turn - 1] + ", you need to roll the die first!", 2)
            elif turn == 2:
                if p1_c1.event(e) or p1_c2.event(e):
                    txt_hint.update_text("This isn't your counter!", 2)
                elif die_rolled:
                    if not p2_c1_move[0] and p2_c1.event(e):
                        txt_hint.update_text("This counter cannot be moved!", 2)
                    elif p2_c1_move[0] and p2_c1.event(e):
                        p2_c1.move(p2_c1_move[1])
                        scores[1] += p1_c1.counter_moved(p2_c1.get_row())
                        scores[1] += p1_c2.counter_moved(p2_c1.get_row())
                        turn, die_rolled, die_result, txt_hint.get_text_manager().priority = end_turn()
                    if not p2_c2_move[0] and p2_c2.event(e):
                        txt_hint.update_text("This counter cannot be moved!", 2)
                    elif p2_c2_move[0] and p2_c2.event(e):
                        p2_c2.move(p2_c2_move[1])
                        scores[1] += p1_c1.counter_moved(p2_c2.get_row())
                        scores[1] += p1_c2.counter_moved(p2_c2.get_row())
                        turn, die_rolled, die_result, txt_hint.get_text_manager().priority = end_turn()
                    elif not p2_c1_move[0] and not p2_c2_move[0]:
                        txt_hint.update_text("No counter can move, ending turn...", 2)
                        render_board()
                        time.sleep(5)
                        turn, die_rolled, die_result, txt_hint.get_text_manager().priority = end_turn()
                elif p2_c1.event(e) or p2_c2.event(e):
                    txt_hint.update_text(names[turn - 1] + ", you need to roll the die first!", 2)

            # Current data - used if user clicks save from side menu
            current_data = {"p1_c1": p1_c1,
                            "p1_c2": p1_c2,
                            "p2_c1": p2_c1,
                            "p2_c2": p2_c2,
                            "die": die,
                            "names": names,
                            "p1_c1_move": p1_c1_move,
                            "p1_c2_move": p1_c2_move,
                            "p2_c1_move": p2_c1_move,
                            "p2_c2_move": p2_c2_move,
                            "die_result": die_result,
                            "die_rolled": die_rolled,
                            "move_by": move_by,
                            "turn": turn,
                            "scores": scores}

            display_saved_games("play") if btn_load.event(e) else False
            display_save_screen(current_data) if btn_save.event(e) else False
            display_rules("play") if btn_rules.event(e) else False
            display_main_menu() if btn_return.event(e) else False

        # Remaining game logic
        if not die_rolled:
            txt_hint.update_text(names[turn - 1] + ", click the die to roll!")
        elif die_result != 0:
            txt_hint.update_text(names[turn - 1] + " rolled a " + str(die_result) + ", " + get_move_text(move_by))

        # Render the game board to the screen
        render_board()

        # Pause loop for a time so that we can get the TARGET_FPS
        clock.tick(TARGET_FPS)


def display_enter_player_names():
    """ Ask the users to enter their names """
    # Create the menu button/text/field objects
    txt_title = Entities.Text(title_font, "Enter Player Names", Colours.WHITE, width / 2, 38)
    txt_user = Entities.Text(main_font, "Player 1, enter your name:", Colours.WHITE, width / 2, 150)
    txt_hint = Entities.Text(main_font, "Enter name (press enter to set)", Colours.WHITE, width / 2, 380)

    name_field = Entities.InputField(main_font, "Player 1", Colours.BLACK, width / 2, 200, 14)

    btn_return = Entities.Button(main_font, "Return to Main Menu", Colours.WHITE, width / 2, 300)

    player = 1
    player_names = ["Player 1", "Player 2"]

    while True:
        # Handle events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for the button object and do necessary function call if needed
            if btn_return.event(e):
                display_main_menu()

            if name_field.event(e):
                field_text = name_field.get_text()

                if field_text:
                    player_names[player - 1] = field_text

                player += 1
                name_field.reset("Player 2")
                txt_user.update_text("Player 2, enter your name:")

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add(txt_title)
        renderer.add(txt_user)
        renderer.add(name_field)
        renderer.add(btn_return)
        renderer.add(txt_hint)

        renderer.draw("bg_plain", Colours.BLACK)

        if player > 2:
            return player_names


def display_save_screen(game_data):
    """ Display a screen asking the user for a name to give to their save """
    # Create the main menu button/text objects
    txt_title = Entities.Text(title_font, "Save Game", Colours.WHITE, width / 2, 38)
    txt_hint = Entities.Text(main_font, "Select a slot to save to", Colours.WHITE, width / 2, 380)

    btn_save_1 = Entities.Button(main_font, "Save Slot 1", Colours.WHITE, width / 2, 120)
    btn_save_2 = Entities.Button(main_font, "Save Slot 2", Colours.WHITE, width / 2, 160)
    btn_save_3 = Entities.Button(main_font, "Save Slot 3", Colours.WHITE, width / 2, 200)
    btn_save_4 = Entities.Button(main_font, "Save Slot 4", Colours.WHITE, width / 2, 240)

    btn_return = Entities.Button(main_font, "Return to Game", Colours.WHITE, width / 2, 300)

    while True:
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for the button object and do necessary function call if needed
            if btn_return.event(e):
                return

            if btn_save_1.event(e):
                save_game(1, game_data)
                return
            if btn_save_2.event(e):
                save_game(2, game_data)
                return
            if btn_save_3.event(e):
                save_game(3, game_data)
                return
            if btn_save_4.event(e):
                save_game(4, game_data)
                return

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add(txt_title)
        renderer.add(btn_save_1)
        renderer.add(btn_save_2)
        renderer.add(btn_save_3)
        renderer.add(btn_save_4)
        renderer.add(btn_return)
        renderer.add(txt_hint)

        renderer.draw("bg_plain", Colours.BLACK)


def save_game(save_number, game_data):
    """ Save the current game state to a file with the indicated name """
    file = open("game_saves/save_game_" + str(save_number) + ".dat", "wb")
    pickle.dump(game_data, file)
    file.close()


def update_highscores(new_score, name):
    highscores = load_highscores()

    if highscores is None:
        highscores = [[new_score, name]]
    else:
        highscores.append([new_score, name])
        highscores.sort(key=lambda x: x[0])
        highscores = highscores[::-1]
        highscores = highscores[:5]

    save_highscores(highscores)


def display_highscores():
    # First, load the scores
    scores = load_highscores()
    displayable_score = ""

    if scores is None:
        displayable_score = "There are no high scores!"
    else:
        for i, score in enumerate(scores, 1):
            displayable_score += str(score[0]) + " achieved by " + score[1] + ("\n" + "-" * 40 + "\n" if i < len(scores) else "")

    # Create the main menu button/text objects
    txt_rules_title = Entities.Text(title_font, "Top 5 Scores", Colours.WHITE, width / 2, 38)
    txt_goal = Entities.Text(main_font, displayable_score, Colours.WHITE, width / 2, 125)

    btn_return = Entities.Button(main_font, "Return to Main Menu", Colours.WHITE, width / 2, 300)

    while True:
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for the button object and do necessary function call if needed
            if btn_return.event(e):
                display_main_menu()

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add(txt_rules_title)
        renderer.add(txt_goal)
        renderer.add(btn_return)

        renderer.draw("bg_plain")


def load_highscores():
    """ Load the highscores """
    # Try to open the file, catch if the file is not found (i.e game not completed at least once yet)
    try:
        file = open("highscores.dat", "rb")
        data = pickle.load(file)
        file.close()
    except FileNotFoundError:
        return None

    return data


def save_highscores(data):
    """ Save highscores to highscores.dat"""
    file = open("highscores.dat", "wb")
    pickle.dump(data, file)
    file.close()


def display_winner(winner, score):
    """ Display winner of the current match to the users """
    # Create the main menu button/text objects
    txt_title = Entities.Text(title_font, "Congratulations!", Colours.WHITE, width / 2, 38)
    txt_winner = Entities.Text(main_font, "The winner is " + winner + "!", Colours.WHITE, width / 2, height / 2)

    btn_return = Entities.Button(main_font, "Return to Main Menu", Colours.WHITE, width / 2, 300)

    update_highscores(score, winner)

    while True:
        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            # Call the event handler for the button object and do necessary function call if needed
            display_main_menu() if btn_return.event(e) else False

        # Draw everything to the screen
        renderer.update_display(display)

        renderer.add(txt_title)
        renderer.add(txt_winner)
        renderer.add(btn_return)

        renderer.draw("bg_plain")


def quit_game():
    """ Exit the application """
    pygame.quit()
    quit()


display_main_menu()
