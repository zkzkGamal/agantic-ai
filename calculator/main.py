# main.py

import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output


def main():
    try:
        calculator = Calculator()

        if len(sys.argv) < 2:
            print("Calculator App")
            print('Usage: python main.py "<expression>"')
            print('Example: python main.py "3 + 5"')
            return

        expression = " ".join(sys.argv[1:])
        if not expression.strip():
            print("Error: Expression is empty or contains only whitespace.")
            return

        result = calculator.evaluate(expression)

        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            print(f"Error: Could not evaluate expression '{expression}'")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
