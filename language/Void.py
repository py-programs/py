import sys


class VOIDInterpreter:

    def __init__(self):
        self.variables = {}

    # -------------------------
    # Get a value
    # -------------------------
    def get_value(self, value):
        value = value.strip()

        # String
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            return value[1:-1]

        # Number
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        # Variable
        if value in self.variables:
            return self.variables[value]

        raise Exception("Unknown value: " + value)

    # -------------------------
    # Arithmetic
    # -------------------------
    def calculate(self, command, args):

        if len(args) != 2:
            raise Exception(command + " needs 2 values")

        x = self.get_value(args[0])
        y = self.get_value(args[1])

        if command == "add":
            return x + y

        elif command == "sub":
            return x - y

        elif command == "mul":
            return x * y

        elif command == "div":

            if y == 0:
                raise Exception("Cannot divide by zero")

            return x / y

        elif command == "mod":

            if y == 0:
                raise Exception("Cannot divide by zero")

            return x % y

        else:
            raise Exception("Unknown command: " + command)

    # -------------------------
    # Execute one VOID line
    # -------------------------
    def execute(self, line):

        line = line.strip()

        # Empty line
        if not line:
            return

        # Comment
        if line.startswith("#"):
            return

        # EXIT
        if line.lower() == "exit":
            return "exit"

        # HELP
        if line.lower() == "help":

            print()
            print("VOID Commands")
            print("----------------")
            print("X = 10")
            print("Y = 20")
            print("A = add X, Y")
            print("A = sub X, Y")
            print("A = mul X, Y")
            print("A = div X, Y")
            print("Print A")
            print("vars")
            print("clear")
            print("exit")
            print()

            return

        # VARIABLES
        if line.lower() == "vars":

            if not self.variables:
                print("No variables.")
            else:
                for name, value in self.variables.items():
                    print(name, "=", value)

            return

        # CLEAR
        if line.lower() == "clear":

            self.variables.clear()
            print("Variables cleared.")

            return

        # PRINT
        if line.lower().startswith("print "):

            value = line[6:].strip()

            result = self.get_value(value)

            print(result)

            return

        # ASSIGNMENT
        if "=" not in line:
            raise Exception("Expected '='")

        name, expression = line.split("=", 1)

        name = name.strip()
        expression = expression.strip()

        # Check variable name
        if not name.isidentifier():
            raise Exception("Invalid variable name: " + name)

        # Simple value
        parts = expression.split(None, 1)

        if len(parts) == 1:

            self.variables[name] = self.get_value(parts[0])

            return

        # Command
        command = parts[0].lower()

        args = parts[1].split(",")

        args = [x.strip() for x in args]

        self.variables[name] = self.calculate(command, args)

    # -------------------------
    # Run VOID code
    # -------------------------
    def run(self, code):

        for line_number, line in enumerate(code.splitlines(), 1):

            try:

                result = self.execute(line)

                if result == "exit":
                    break

            except Exception as error:

                print(
                    "VOID Error on line",
                    line_number,
                    ":",
                    error
                )


# ==========================================
# INTERACTIVE MODE
# ==========================================

def start_repl():

    void = VOIDInterpreter()

    print()
    print("================================")
    print("          VOID v0.1")
    print("     Graphics Programming")
    print("================================")
    print()
    print('Type "help" for commands.')
    print('Type "exit" to quit.')
    print()

    while True:

        try:

            line = input("VOID> ")

            if line.lower() == "exit":
                print("Goodbye!")
                break

            void.execute(line)

        except KeyboardInterrupt:

            print()
            print("Type 'exit' to quit.")

        except Exception as error:

            print("VOID Error:", error)


# ==========================================
# FILE MODE
# ==========================================

def run_file(filename):

    void = VOIDInterpreter()

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            code = file.read()

        void.run(code)

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
# START
# ==========================================

if len(sys.argv) == 1:

    start_repl()

else:

    filename = sys.argv[1]

    if not filename.lower().endswith(".void"):

        print("VOID Error: Use a .void file")

    else:

        run_file(filename)
