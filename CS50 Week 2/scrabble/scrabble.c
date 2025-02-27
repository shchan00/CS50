#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

const int scoreboard[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                          1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int countPoints(string word);

int main(void)
{
    string p1 = get_string("Player 1: ");
    string p2 = get_string("Player 2: ");
    string test = "HI!1";
    if (countPoints(p1) > countPoints(p2))
    {
        printf("Player 1 wins!\n");
    }
    else if (countPoints(p1) < countPoints(p2))
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int countPoints(string word)
{
    int sum = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        char lowercase = tolower(word[i]);
        if (lowercase >= 'a' && lowercase <= 'z')
        {
            sum += (scoreboard[lowercase - 'a']);
        }
    }
    return sum;
}
