// Implements a dictionary's functionality
#include "dictionary.h"
#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1000;
int counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int wordhash = hash(word);
    node *ptr = table[wordhash];
    if (ptr == NULL)
    {
        return false;
    }
    while (ptr->next != NULL)
    {
        if (strcasecmp(word, ptr->word) == 0)
        {
            return true;
        }
        ptr = ptr->next;
    }
    if (strcasecmp(word, ptr->word) == 0)
    {
        return true;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *str)
{
    unsigned long hash = 5381;
    int c = *str;
    c = toupper(c);
    while (*str != 0)
    {
        hash = ((hash << 5) + hash) + c;
        c = *str++;
        c = toupper(c);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }
    char *word = malloc(LENGTH * sizeof(char));
    if (word == NULL)
    {
        return false;
    }
    while (fscanf(source, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);
        int wordhash = hash(word);
        if (table[wordhash] == NULL)
        {
            n->next = NULL;
            table[wordhash] = n;
        }
        else
        {
            n->next = table[wordhash];
            table[wordhash] = n;
        }
        counter++;
    }
    free(word);
    fclose(source);
    // TODO
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            node *next = ptr->next;
            free(ptr);
            ptr = next;
        }
    }
    // TODO
    return true;
}
