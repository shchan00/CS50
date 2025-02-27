import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Missing command-line argument")
        sys.exit(1)
    dbname = sys.argv[1]
    sqname = sys.argv[2]

    # TODO: Read database file into a variable
    dbrows = []
    with open(dbname) as file:
        reader = csv.DictReader(file)
        for row in reader:
            dbrows.append(row)
    # TODO: Read DNA sequence file into a variable
    sqfile = open(sqname, "r")
    sq = sqfile.read()

    # TODO: Find longest match of each STR in DNA sequence

    # TODO: Check database for matching profiles
    for row in dbrows:
        for i in range(1, len(reader.fieldnames)):
            if (int(row[reader.fieldnames[i]]) != longest_match(sq, reader.fieldnames[i])):
                break
        else:
            print(row["name"])
            break
    else:
        print("No Match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
