def main():
    height = get_int("Height: ")
    while (height < 1 or height > 8):
        height = get_int("Height: ")
    for i in range(height):
        for j in range(3 + height + i):
            if (j < height - i - 1 or (j > height - 1 and j < height + 2)):
                print(" ", end="")
            else:
                print("#", end="")
        print("\n", end="")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Not an integer")


main()
