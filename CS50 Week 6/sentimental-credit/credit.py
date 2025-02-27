import math


def main():
    cardID = input("Number: ")
    sum = 0
    for i in range(len(cardID)):
        if (i % 2 == len(cardID) % 2):
            sum = sum + math.floor(int(cardID[i]) * 2 / 10) + int(cardID[i]) * 2 % 10
        else:
            sum = sum + int(cardID[i])
    if (sum % 10 != 0):
        print("INVALID")
    elif (int(cardID[0]) == 5 and int(cardID[1]) in range(1, 6) and len(cardID) == 16):
        print("MASTERCARD")
    elif (int(cardID[0]) == 3 and int(cardID[1]) in [4, 7] and len(cardID) == 15):
        print("AMEX")
    elif (int(cardID[0]) == 4 and len(cardID) in [13, 16]):
        print("VISA")
    else:
        print("INVALID")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Not an integer")


main()
