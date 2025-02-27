#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int cindex(string text);

int main(void)
{
    string input_text = get_string("Text: ");
    int index = cindex(input_text);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int cindex(string text)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    int clindex;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    clindex = round(0.0588 * letters / words * 100 - 0.296 * sentences / words * 100 - 15.8);
    return clindex;
}
