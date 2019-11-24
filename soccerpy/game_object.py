from .world_model import ServerParameters

sp = ServerParameters()

class GameObject:
    """
    Root class for all percievable objects in the world model.
    """

    def __init__(self, distance, direction):
        """
        All objects have a distance and direction to the player, at a minimum.
        """

        self.distance = distance
        self.direction = direction

class Line(GameObject):
    """
    Represents a line on the soccer field.
    """

    def __init__(self, distance, direction, line_id):
        self.line_id = line_id
        
        GameObject.__init__(self, distance, direction)

class Goal(GameObject):
    """
    Represents a goal object on the field.
    """

    def __init__(self, distance, direction, goal_id):
        self.goal_id = goal_id

        GameObject.__init__(self, distance, direction)

class Flag(GameObject):
    """
    A flag on the field.  Can be used by the agent to determine its position.
    """

    # a dictionary mapping all flag_ids to their on-field (x, y) coordinates
    # TODO: these are educated guesses based on Figure 4.2 in the documentation.
    #       where would one find the actual coordinates, besides in the server
    #       code?
    pitch_half_l = sp.get_pitch_length() * 0.5
    pitch_half_w = sp.get_pitch_width() * 0.5
    penalty_l = sp.get_penalty_area_length()
    penalty_w = sp.get_penalty_area_width()
    goal_half_width = sp.get_goal_width() * 0.5


    FLAG_COORDS = {
            # perimiter flags
            "tl50": (-50, -pitch_half_l - 5.0),
            "tl40": (-40, -pitch_half_l - 5.0),
            "tl30": (-30, -pitch_half_l - 5.0),
            "tl20": (-20, -pitch_half_l - 5.0),
            "tl10": (-10, -pitch_half_l - 5.0),
            "t0": (0, -pitch_half_l - 5.0),
            "tr10": (10, -pitch_half_l - 5.0),
            "tr20": (20, -pitch_half_l - 5.0),
            "tr30": (30, -pitch_half_l - 5.0),
            "tr40": (40, -pitch_half_l - 5.0),
            "tr50": (50, -pitch_half_l - 5.0),

            "rt30": (pitch_half_w + 5.0, -30),
            "rt20": (pitch_half_w + 5.0, -20),
            "rt10": (pitch_half_w + 5.0, -10),
            "r0": (pitch_half_w + 5.0, 0),
            "rb10": (pitch_half_w + 5.0, 10),
            "rb20": (pitch_half_w + 5.0, 20),
            "rb30": (pitch_half_w + 5.0, 30),

            "bl50": (-50, pitch_half_l + 5.0),
            "bl40": (-40, pitch_half_l + 5.0),
            "bl30": (-30, pitch_half_l + 5.0),
            "bl20": (-20, pitch_half_l + 5.0),
            "bl10": (-10, pitch_half_l + 5.0),
            "b0": (0, pitch_half_l + 5.0),
            "br10": (10, pitch_half_l + 5.0),
            "br20": (20, pitch_half_l + 5.0),
            "br30": (30, pitch_half_l + 5.0),
            "br40": (40, pitch_half_l + 5.0),
            "br50": (50, pitch_half_l + 5.0),

            "lt30": (-pitch_half_w - 5.0, -30),
            "lt20": (-pitch_half_w - 5.0, -20),
            "lt10": (-pitch_half_w - 5.0, -10),
            "l0": (-pitch_half_w - 5.0, 0),
            "lb10": (-pitch_half_w - 5.0, 10),
            "lb20": (-pitch_half_w - 5.0, 20),
            "lb30": (-pitch_half_w - 5.0, 30),

            # goal flags ('t' and 'b' flags can change based on server parameter
            # 'goal_width', but we leave their coords as the default values.
            # TODO: make goal flag coords dynamic based on server_params
            "glt": (-pitch_half_w, -goal_half_width),
            "gl": (-pitch_half_w, 0),
            "glb": (-pitch_half_w, goal_half_width),

            "grt": (pitch_half_w, -goal_half_width),
            "gr": (pitch_half_w, 0),
            "grb": (pitch_half_w, goal_half_width),

            # penalty flags
            "plt": (-(pitch_half_w - penalty_l), -penalty_w*0.5),
            "plc": (-(pitch_half_w - penalty_l), 0.0),
            "plb": (-(pitch_half_w - penalty_l), penalty_w*0.5),

            "prt": ((pitch_half_w - penalty_l), -penalty_w*0.5),
            "prc": ((pitch_half_w - penalty_l), 0.0),
            "prb": ((pitch_half_w - penalty_l), penalty_w*0.5),

            # field boundary flags (on boundary lines)
            "lt": (-pitch_half_w, -pitch_half_l),
            "ct": (0, -pitch_half_l),
            "rt": (pitch_half_w, -pitch_half_l),

            "lb": (-pitch_half_w, pitch_half_l),
            "cb": (0, pitch_half_l),
            "rb": (pitch_half_w, pitch_half_l),

            # center flag
            "c": (0, 0)
        }

    def __init__(self, distance, direction, flag_id):
        """
        Adds a flag id for this field object.  Every flag has a unique id.
        """

        self.flag_id = flag_id

        GameObject.__init__(self, distance, direction)

class MobileObject(GameObject):
    """
    Represents objects that can move.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed):
        """
        Adds variables for distance and direction deltas.
        """

        self.dist_change = dist_change
        self.dir_change = dir_change
        self.speed = speed

        GameObject.__init__(self, distance, direction)

class Ball(MobileObject):
    """
    A spcial instance of a mobile object representing the soccer ball.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed):
        
        MobileObject.__init__(self, distance, direction, dist_change,
                dir_change, speed)

class Player(MobileObject):
    """
    Represents a friendly or enemy player in the game.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed,
            team, side, uniform_number, body_direction, neck_direction):
        """
        Adds player-specific information to a mobile object.
        """

        self.team = team
        self.side = side
        self.uniform_number = uniform_number
        self.body_direction = body_direction
        self.neck_direction = neck_direction

        MobileObject.__init__(self, distance, direction, dist_change,
                dir_change, speed)

