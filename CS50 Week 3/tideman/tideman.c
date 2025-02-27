#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool is_cycle(int origin, int winner);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    // TODO
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    // TODO
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    // TODO
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = pair_count - 1; i > 0; i--)
    {
        for (int j = pair_count; j > 0; j--)
        {
            if (preferences[pairs[j].winner][pairs[j].loser] >
                preferences[pairs[j - 1].winner][pairs[j - 1].loser])
            {
                printf("Winner: %s, Loser: %s\n", candidates[pairs[j].winner],
                       candidates[pairs[j].loser]);
                printf("Winner: %s, Loser: %s\n", candidates[pairs[j - 1].winner],
                       candidates[pairs[j - 1].loser]);
                pair temp;
                temp.winner = pairs[j - 1].winner;
                temp.loser = pairs[j - 1].loser;
                pairs[j - 1].winner = pairs[j].winner;
                pairs[j - 1].loser = pairs[j].loser;
                pairs[j].winner = temp.winner;
                pairs[j].loser = temp.loser;
            }
        }
    }
    // TODO
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }
    for (int i = 0; i < pair_count; i++)
    {
        bool cycle = false;
        printf("Winner: %s, Loser: %s\n", candidates[pairs[i].winner], candidates[pairs[i].loser]);
        for (int j = 0; j < pair_count; j++)
        {
            if (pairs[j].loser == pairs[i].winner &&
                locked[pairs[j].winner][pairs[j].loser] == true)
            {
                printf("Origin: %s, Winner: %s\n", candidates[pairs[i].winner],
                       candidates[pairs[j].winner]);
                if (is_cycle(pairs[i].winner, pairs[j].winner) == true)
                {
                    cycle = true;
                }
            }
        }
        if (cycle == false)
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    // TODO
    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool all_false = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == true)
            {
                all_false = false;
            }
        }
        if (all_false == true)
        {
            printf("%s\n", candidates[i]);
        }
    }
    // TODO
    return;
}
bool is_cycle(int origin, int winner)
{
    if (origin == winner)
    {
        return true;
    }
    for (int j = 0; j < pair_count; j++)
    {
        if (pairs[j].loser == winner &&
            (locked[pairs[j].winner][winner] == true || pairs[j].winner == origin))
        {
            return is_cycle(origin, pairs[j].winner);
        }
    }
    return false;
}
