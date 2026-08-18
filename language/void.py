import sys
import readline


# ==========================================
# TERMINAL EDITING
# ==========================================

readline.parse_and_bind("set editing-mode emacs")


# ==========================================
# VOID INTERPRETER
# ==========================================

class VOIDInterpreter:

    def __init__(self):
        self.variables = {}

    # --------------------------------------
    # GET VALUE
    # --------------------------------------

    def get_value(self, value):

        value = value.strip()

        # String
        if (
            len(value) >= 2
            and value[0] == '"'
            and value[-1] == '"'
        ):
            return value[1:-1]

        # Integer / decimal
        try:

            if "." in value:
                return float(value)

            return int(value)

        except ValueError:
            pass

        # Variable
        if value in self.variables:
            return self.variables[value]

        raise Exception(
            "Unknown value: " + value
        )

    # --------------------------------------
    # CALCULATIONS
    # --------------------------------------

    def calculate(self, command, args):

        if len(args) != 2:

            raise Exception(
                command + " needs 2 values"
            )

        x = self.get_value(args[0])
        y = self.get_value(args[1])

        # ADD
        if command == "add":

            return x + y

        # SUBTRACT
        elif command == "sub":

            return x - y

        # MULTIPLY
        elif command == "mul":

            return x * y

        # DIVIDE
        elif command == "div":

            if y == 0:

                raise Exception(
                    "Cannot divide by zero"
                )

            return x / y

        # MODULO
        elif command == "mod":

            if y == 0:

                raise Exception(
                    "Cannot divide by zero"
                )

            return x % y

        else:

            raise Exception(
                "Unknown command: " + command
            )

    # --------------------------------------
    # EXECUTE ONE VOID LINE
    # --------------------------------------

    def execute(self, line):

        line = line.strip()

        # Empty line
        if not line:
            return

        # Comment
        if line.startswith("#"):
            return

        # ----------------------------------
        # PRINT
        # ----------------------------------

        if line.lower().startswith("print "):

            value = line[6:].strip()

            result = self.get_value(value)

            print(result)

            return

        # ----------------------------------
        # VARIABLES
        # ----------------------------------

        if line.lower() == "vars":

            if not self.variables:

                print("No variables.")

            else:

                for name, value in self.variables.items():

                    print(
                        name,
                        "=",
                        value
                    )

            return

        # ----------------------------------
        # CLEAR VARIABLES
        # ----------------------------------

        if line.lower() == "clear":

            self.variables.clear()

            print(
                "VOID: Variables cleared."
            )

            return

        # ----------------------------------
        # ASSIGNMENT
        # ----------------------------------

        if "=" not in line:

            raise Exception(
                "Expected '='"
            )

        name, expression = line.split(
            "=",
            1
        )

        name = name.strip()
        expression = expression.strip()

        # Check variable name
        if not name.isidentifier():

            raise Exception(
                "Invalid variable name: "
                + name
            )

        # ----------------------------------
        # SIMPLE VALUE
        # ----------------------------------

        parts = expression.split(
            None,
            1
        )

        if len(parts) == 1:

            self.variables[name] = (
                self.get_value(parts[0])
            )

            return

        # ----------------------------------
        # COMMAND
        # ----------------------------------

        command = parts[0].lower()

        args = parts[1].split(",")

        args = [
            x.strip()
            for x in args
        ]

        self.variables[name] = (
            self.calculate(
                command,
                args
            )
        )

    # --------------------------------------
    # RUN PROGRAM
    # --------------------------------------

    def run(self, program):

        for line_number, line in enumerate(
            program,
            1
        ):

            try:

                self.execute(line)

            except Exception as error:

                print(
                    "VOID Error on line",
                    line_number,
                    ":",
                    error
                )


# ==========================================
# VOID REPL
# ==========================================

def start_void():

    program = []

    print()
    print(
        "================================"
    )
    print(
        "          VOID v0.1"
    )
    print(
        "     Graphics Programming"
    )
    print(
        "================================"
    )
    print()

    print(
        "Write VOID code."
    )

    print(
        "Type Run! to execute."
    )

    print(
        "Type Clear! to clear code."
    )

    print(
        "Type Show! to view code."
    )

    print(
        "Type exit to quit."
    )

    print()

    while True:

        try:

            # ----------------------------------
            # INPUT
            # ----------------------------------

            line = input("VOID> ")

        except KeyboardInterrupt:

            print()

            continue

        except EOFError:

            print()

            break

        # ======================================
        # EXIT
        # ======================================

        if line.lower() == "exit":

            print(
                "Goodbye!"
            )

            break

        # ======================================
        # RUN!
        # ======================================

        if line.lower() == "run!":

            if not program:

                print(
                    "VOID: Nothing to run."
                )

            else:

                print()

                print(
                    "-------- OUTPUT --------"
                )

                void = VOIDInterpreter()

                void.run(program)

                print(
                    "------------------------"
                )

                print()

            continue

        # ======================================
        # CLEAR!
        # ======================================

        if line.lower() == "clear!":

            program.clear()

            print(
                "VOID: Program cleared."
            )

            continue

        # ======================================
        # SHOW!
        # ======================================

        if line.lower() == "show!":

            if not program:

                print(
                    "VOID: Program is empty."
                )

            else:

                print()

                print(
                    "---------- CODE ----------"
                )

                for number, code in enumerate(
                    program,
                    1
                ):

                    print(
                        str(number)
                        + " | "
                        + code
                    )

                print(
                    "--------------------------"
                )

                print()

            continue

        # ======================================
        # HELP!
        # ======================================

        if line.lower() == "help!":

            print()

            print(
                "VOID Commands"
            )

            print(
                "----------------------"
            )

            print(
                "X = 10"
            )

            print(
                "Y = 20"
            )

            print(
                "A = add X, Y"
            )

            print(
                "A = sub X, Y"
            )

            print(
                "A = mul X, Y"
            )

            print(
                "A = div X, Y"
            )

            print(
                "A = mod X, Y"
            )

            print(
                "Print A"
            )

            print()

            print(
                "Run!"
            )

            print(
                "Show!"
            )

            print(
                "Clear!"
            )

            print(
                "Help!"
            )

            print(
                "exit"
            )

            print()

            continue

        # ======================================
        # ADD LINE TO PROGRAM
        # ======================================

        program.append(line)


# ==========================================
# RUN .VOID FILE
# ==========================================

def run_file(filename):

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            program = file.readlines()

        void = VOIDInterpreter()

        void.run(program)

    except FileNotFoundError:

        print(
            "VOID Error: File not found:",
            filename
        )

    except Exception as error:

        print(
            "VOID Error:",
            error
        )


# ==========================================
# START VOID
# ==========================================

if len(sys.argv) == 1:

    start_void()

else:

    filename = sys.argv[1]

    if not filename.lower().endswith(
        ".void"
    ):

        print(
            "VOID Error:"
            " File must end with .void"
        )

    else:

        run_file(filename)
