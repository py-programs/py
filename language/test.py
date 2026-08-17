import sys


class VOIDInterpreter:

    def __init__(self):
        self.variables = {}

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

    def execute(self, line):

        line = line.strip()

        if not line:
            return

        # Comments
        if line.startswith("#"):
            return

        # Print
        if line.lower().startswith("print "):

            value = line[6:].strip()
            result = self.get_value(value)

            print(result)

            return

        # Variables
        if line.lower() == "vars":

            if not self.variables:
                print("No variables.")
            else:
                for name, value in self.variables.items():
                    print(name, "=", value)

            return

        # Assignment
        if "=" not in line:
            raise Exception("Expected '='")

        name, expression = line.split("=", 1)

        name = name.strip()
        expression = expression.strip()

        if not name.isidentifier():
            raise Exception(
                "Invalid variable name: " + name
            )

        # Simple value
        parts = expression.split(None, 1)

        if len(parts) == 1:

            self.variables[name] = self.get_value(
                parts[0]
            )

            return

        # Command
        command = parts[0].lower()

        args = parts[1].split(",")

        args = [x.strip() for x in args]

        self.variables[name] = self.calculate(
            command,
            args
        )

    def run(self, code):

        for line_number, line in enumerate(
            code,
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


def start_void():

    program = []

    print()
    print("==============================")
    print("          VOID v0.1")
    print("==============================")
    print()
    print("Write VOID code.")
    print("Type Run! to execute.")
    print("Type Clear! to clear code.")
    print("Type exit to quit.")
    print()

    while True:

        try:

            line = input("VOID> ")

        except KeyboardInterrupt:

            print()
            print("Use Run! or exit.")

            continue

        # EXIT
        if line.lower() == "exit":
            print("Goodbye!")
            break

        # RUN!
        if line.lower() == "run!":

            if not program:

                print("VOID: Nothing to run.")

            else:

                print()
                print("----- OUTPUT -----")

                void = VOIDInterpreter()
                void.run(program)

                print("------------------")
                print()

            continue

        # CLEAR!
        if line.lower() == "clear!":

            program.clear()

            print("VOID: Program cleared.")

            continue

        # Show current code
        if line.lower() == "show!":

            if not program:

                print("VOID: Program is empty.")

            else:

                print()
                print("----- CODE -----")

                for number, code in enumerate(
                    program,
                    1
                ):
                    print(
                        str(number) + " | " + code
                    )

                print("----------------")

            continue

        # Add line to program
        program.append(line)


# Start VOID

if len(sys.argv) == 1:
    start_void()

else:

    filename = sys.argv[1]

    if not filename.lower().endswith(".void"):

        print(
            "VOID Error: "
            "File must end with .void"
        )

    else:

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
