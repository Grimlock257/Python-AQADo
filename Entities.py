import pygame
import Colours
from random import randint

# List of row y values, index + 1 is the row number being referenced
row_positions = (332, 299, 267, 235, 201, 168, 136, 104, 72, 40, 7)


class Render(object):
    """ Render Class, handles the drawing of all entities for the current frame """

    def __init__(self):
        """ Initialise the renderer """
        self._rects = []
        self._fields = []
        self._entities = []
        self._text = []
        self._display = None

        # Make sure all the images are loaded into memory
        AssetManager.load()

    def update_display(self, display):
        """ Update the display for the renderer to draw to """
        self._display = display

    def add(self, item):
        """ Add an entity to the list of entities to be rendered """
        if isinstance(item, InputField):
            self._fields.append(item)
        elif isinstance(item, tuple):
            self._rects.append(item)
        elif isinstance(item, Counter) or isinstance(item, Die):
            self._entities.append(item)
        elif isinstance(item, Text):
            self._text.append(item)

    def draw(self, background, colour=Colours.RED):
        """ Draw each of item from the to render lists to the display """
        # Colour the window background
        self._display.fill(colour)

        # Draw the background
        self._display.blit(AssetManager.assets[background][0], (0, 0))

        # Render any rects we have
        for rect in self._rects:
            pygame.draw.rect(self._display, Colours.WHITE, rect)

        # Render any text fields we have
        for field in self._fields:
            if len(field.get_text_manager().get_render_lines()) > 0:
                input_field_text = field.get_text_manager().get_render_lines()[0]
                input_field_rect = field.get_text_manager().get_rects()[0]
                cursor = field.get_text_manager().get_cursor()

                # Draw the text field followed by the cursor at the appropriate position within the text field
                self._display.blit(input_field_text, input_field_rect)
                self._display.blit(cursor[0], (cursor[1][0] + input_field_rect[0], cursor[1][1]))

        # Render counters and die
        for entity in self._entities:
            self._display.blit(AssetManager.assets[entity.get_image()][0], AssetManager.get_rect(entity.get_image()))

        # Render text elements
        for text in self._text:
            for i, line in enumerate(text.get_text_manager().get_render_lines()):
                self._display.blit(line, text.get_text_manager().get_rects()[i])

        # Update the display so we can see our changes
        pygame.display.update()

        # Clean lists for next frame
        self._rects = []
        self._fields = []
        self._entities = []
        self._text = []


class AssetManager:
    """ Container class for all of the assets """
    assets = {}

    def __init__(self):
        pass  # Nothing to do here...

    @staticmethod
    def load():
        """ Load all the assets """
        AssetManager.assets['p1_c1'] = [pygame.image.load("assets/player_1_counter.png")]
        AssetManager.assets['p1_c2'] = [pygame.image.load("assets/player_1_counter.png")]
        AssetManager.assets['p2_c1'] = [pygame.image.load("assets/player_2_counter.png")]
        AssetManager.assets['p2_c2'] = [pygame.image.load("assets/player_2_counter.png")]
        AssetManager.assets['die_r'] = [pygame.image.load("assets/die_r.png")]
        AssetManager.assets['die_1'] = [pygame.image.load("assets/die_1.png")]
        AssetManager.assets['die_2'] = [pygame.image.load("assets/die_2.png")]
        AssetManager.assets['die_3'] = [pygame.image.load("assets/die_3.png")]
        AssetManager.assets['die_4'] = [pygame.image.load("assets/die_4.png")]
        AssetManager.assets['die_5'] = [pygame.image.load("assets/die_5.png")]
        AssetManager.assets['bg_play'] = [pygame.image.load("assets/background_play.png")]
        AssetManager.assets['bg_plain'] = [pygame.image.load("assets/background_plain.png")]

        # For every image loaded, get the image rect for it (so we know it's width and height)
        for key, value in AssetManager.assets.items():
            AssetManager.assets[key].append(AssetManager.assets[key][0].get_rect())

    @staticmethod
    def get_rect(key):
        """ Return the rect for the specified key """
        return AssetManager.assets[key][1]

    @staticmethod
    def update_rect(key, x, y):
        """ Update the x and y values of the rect for the specified key """
        AssetManager.assets[key][1].x = x
        AssetManager.assets[key][1].y = y


class TextManager(object):
    """ Represents information about a Text object (the lines it is split into and its rects """

    def __init__(self, font, text, colour, x_pos, y_pos, priority=1, cursor=None):
        self._config = (font, colour, x_pos, y_pos)
        self._render_lines = []
        self._rects = []
        self._priority = priority
        self._cursor = cursor

        def add_line(index, the_line):
            """ Add a line of text to the list of lines to be rendered """
            self._render_lines.append(font.render(the_line, True, colour))
            self._rects.append(self._render_lines[index].get_rect())

            self._rects[index].x = x_pos - (self._rects[index].width / 2)
            self._rects[index].y = y_pos - (self._rects[index].height / 2) + (font.get_height() / 1.5) * index

        # Check each line to see if it exceeds maximum length allowed,
        # if so, split the string in half then add, otherwise just add
        for i, line in enumerate(text.splitlines()):
            if len(line) > 68:
                split_string = line.split(" ")
                split_string.insert(int(len(split_string) / 2) + 1, "\n")
                line = "".join("\n" if word == "\n" else word + " " for word in split_string)

                for j, line_split in enumerate(line.splitlines()):
                    add_line(j, line_split)

                continue

            add_line(i, line)

    def get_render_lines(self):
        """ Return the lines that will be rendered """
        return self._render_lines

    def get_rects(self):
        """ Return the associated rects with the render_lines"""
        return self._rects

    def get_cursor(self):
        """ Return the associated cursor (only used by InputField) """
        return self._cursor

    def update_cursor(self, cursor):
        """ Update the cursor associated with the text, if applicable """
        self._cursor = cursor

    def update_text(self, text, priority):
        """ Update the text that this object contains """
        if priority >= self._priority:
            self.__init__(self._config[0], text, self._config[1], self._config[2], self._config[3], priority)

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, new_priority):
        self._priority = new_priority


class Position:
    """ Represents a Vector2f (2 coordinate position) """

    def __init__(self, x, y):
        """ Initialise the position with the passed in arguments"""
        self.x = x
        self.y = y


class Counter(object):
    """ This class contains method relating to a player counter """

    def __init__(self, player, counter_num, row_position=1):
        """ Initialise the counter object with the passed in arguments """
        self._player = player
        self._counter_num = counter_num
        self._row_pos = row_position
        self._image = "p" + str(player) + "_c" + str(counter_num)
        self._coords = Position(0, row_positions[self._row_pos - 1])

        # Hardcore the counter x's as they are constant throughout
        if self._player == 1:
            self._coords.x = 100 if (self._counter_num == 1) else 185
        else:
            self._coords.x = 250 if (self._counter_num == 1) else 335

        AssetManager.update_rect(self._image, self._coords.x, self._coords.y)

    def get_image(self):
        """ Return the image key associated with the counter """
        return self._image

    def get_row(self):
        """ Return the row number of the counter"""
        return self._row_pos

    def update_row_pos(self, position):
        """ Update the row number and the rect associated with the image key for this counter """
        self._row_pos = position
        self._coords.y = row_positions[self._row_pos - 1]

        AssetManager.update_rect(self._image, self._coords.x, self._coords.y)

    def can_move(self, movement_distance, other_counter, opp_c1, opp_c2):
        """ Determine whether the counter can make a legal move """
        if movement_distance == "available":
            move_counter = 1
            new_pos = self._row_pos + 1

            while (new_pos == other_counter or new_pos == opp_c1 or new_pos == opp_c2) and new_pos <= 11:
                move_counter += 1
                new_pos += 1

            if new_pos > 11:
                return False, 0
            else:
                return True, move_counter
        else:
            # Work out where the counter would end up if it was to move
            new_row_pos = self._row_pos + movement_distance

            if new_row_pos == 11 or new_row_pos == 5 or new_row_pos == 1:
                return True, movement_distance

            if new_row_pos == other_counter:
                return False, 0

            if (movement_distance > 0 and self._row_pos == 11) or (movement_distance < 0 and self._row_pos == 1):
                return False, 0

            return True, movement_distance

    def move(self, destination):
        """ Move the counter to the destination (making sure the counter doesn't call of the board) """
        new_position = self._row_pos + destination

        if new_position > 11:
            self.update_row_pos(11)
        elif new_position < 1:
            self.update_row_pos(1)
        else:
            self.update_row_pos(new_position)

    def counter_moved(self, opponent_counter_pos):
        """ Called when an opponent counter has moved, this counter object needs to check and see if the
        opponent counter now occupies the same row as it is, if so, move to row 1 (unless on safe zone) """
        if opponent_counter_pos == self.get_row() and not (self.get_row() == 5 or self.get_row() == 11):
            self.update_row_pos(1)
            return 1

        return 0

    def from_load(self):
        """ Update the rect for the counter to match the save state """
        AssetManager.update_rect(self._image, self._coords.x, self._coords.y)

    def event(self, e):
        """ Return a whether counter has been clicked """
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and AssetManager.get_rect(self._image).collidepoint(
                e.pos):
            return True


class Die:
    """ This class contains methods relating to the die """

    def __init__(self):
        self._image = None

        self.update_image(0)

    def get_image(self):
        """ Return the image key associated with the die """
        return self._image

    def update_image(self, die_number):
        """ Update the image key for the die based on the die_number """
        # If die_number is 0, assume default image of "Roll Me"
        die_img_tag = "r" if die_number == 0 else str(die_number)

        self._image = "die_" + die_img_tag

        # Set position of die, hardcoded as die position constant
        AssetManager.update_rect(self._image, 390, 46)

    def roll_die(self):
        result = randint(1, 5)
        self.update_image(result)
        pygame.display.update()

        return result

    def from_load(self):
        """ Update the rect for the die to match the save state """
        AssetManager.update_rect(self._image, 390, 46)

    def event(self, e, has_rolled_already):
        """ Return a tuple as (has been clicked, die roll result) """
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and AssetManager.get_rect(self._image).collidepoint(
                e.pos):
            if has_rolled_already:
                return True, None
            else:
                return True, self.roll_die()
        else:
            return False, 0


class Text:
    """ Represent a text element """

    def __init__(self, font, text, colour, x_pos, y_pos):
        self._text_manager = TextManager(font, text, colour, x_pos, y_pos)

    def get_text_manager(self):
        """ Return the text manager for this object """
        return self._text_manager

    def update_text(self, text, priority=1):
        """ Update the text that this objects _text_manager contains """
        self.get_text_manager().update_text(text, priority)


class Button(Text):
    """ Represents a button, extending Text """

    def __init__(self, font, text, colour, x_pos, y_pos):
        super().__init__(font, text, colour, x_pos, y_pos)

    def event(self, e):
        """ Return whether the button was clicked or not """
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for rect in self.get_text_manager().get_rects():
                if rect.collidepoint(e.pos):
                    return True


class InputField(Text):
    """ Represents an input field for the user to enter text, extending Text """

    def __init__(self, font, default_text, colour, x_pos, y_pos, max_length):
        super().__init__(font, "", colour, x_pos, y_pos)
        self._text = default_text
        self._font = font
        self._y_pos = y_pos
        self._max_length = max_length
        self._is_default = True

        self._cursor_surface = pygame.Surface((2, self._font.get_height()))
        self._cursor_surface.fill(colour)
        self._cursor_pos = 0

    def event(self, e):
        """ Update the value of the input field, return True ONLY IF key_return is pressed """
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                self._text = self._text[:max(self._cursor_pos - 1, 0)] + self._text[self._cursor_pos:]
                self._cursor_pos = max(self._cursor_pos - 1, 0)
            elif e.key == pygame.K_DELETE:
                self._text = self._text[:self._cursor_pos] + self._text[self._cursor_pos + 1:]
            elif e.key == pygame.K_RIGHT:
                self._cursor_pos = min(self._cursor_pos + 1, len(self._text))
            elif e.key == pygame.K_LEFT:
                self._cursor_pos = max(self._cursor_pos - 1, 0)
            elif e.key == pygame.K_RETURN:
                return True
            else:
                if self._is_default:
                    self._text = ""
                    self._is_default = False

                if not self._cursor_pos == self._max_length:
                    self._text = self._text[:self._cursor_pos] + e.unicode + self._text[self._cursor_pos:]
                    self._cursor_pos += len(e.unicode)

        # Update the text via this objects TextManager
        self.update_text(self._text)

        cursor_x_pos = self._font.size(self._text[:self._cursor_pos])[0]
        cursor_y_pos = self._y_pos - self._font.get_height() / 2

        self._text_manager.update_cursor([self._cursor_surface, [cursor_x_pos, cursor_y_pos]])

        return False

    def get_text(self):
        """ Return the currently entered text """
        return self._text

    def reset(self, text=""):
        """ Reset the text of the input field """
        self._text = text
        self._cursor_pos = 0
        self._is_default = True
