#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

string cipher(string key, string text);
int countRepeat(string text, char repeat);
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substituation key\n");
        return 1;
    }
    string key = argv[1];
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    for (int i = 0; i < 26; i++)
    {
        if (!(isalpha(key[i])))
        {
            printf("Key must contain alphabets\n");
            return 1;
        }
        if (countRepeat(key, key[i]) > 1)
        {
            printf("Key must not be repeated\n");
            return 1;
        }
    }
    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                printf("%c", toupper(key[text[i] - 'A']));
            }
            else
            {
                printf("%c", tolower(key[text[i] - 'a']));
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
    return 0;
}
int countRepeat(string text, char repeat)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == repeat)
        {
            count++;
        }
    }
    return count;
}
