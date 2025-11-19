// DIGIMON DIGITAL ADVENTURE - CTF CHALLENGE
// Heap Overflow Exploitation Challenge
// "The Digital World awaits your commands..."

#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

#define MAX_DIGIMON 5
#define DIGIVOLUTION_THRESHOLD 100

struct DigimonData {
    char name[64];
    int power_level;
    int experience;
};

struct BattleSystem {
    int (*battle_function)();
    int evolution_stage;
    char digital_signature[16];
};

// Secret function - only accessible through exploitation
int omegamon_appears()
{
    printf("\n");
    printf("╔═══════════════════════════════════════════════════════════╗\n");
    printf("║    ⚡ MIRACULOUS DIGIVOLUTION! ⚡                         ║\n");
    printf("║                                                           ║\n");
    printf("║    Your Digimon has achieved the legendary form...       ║\n");
    printf("║                   ✧ OMEGAMON ✧                           ║\n");
    printf("║                                                           ║\n");
    printf("║    The Digital World recognizes your mastery!            ║\n");
    printf("╚═══════════════════════════════════════════════════════════╝\n\n");

    FILE *file;
    char line[128];
    char *filename = "flag.txt";

    file = fopen(filename, "r");
    if (file == NULL) {
        printf("ERROR: Flag file not found! Contact admin.\n");
        return 1;
    }

    fgets(line, sizeof(line), file);
    fclose(file);

    printf("🏴 FLAG: %s\n", line);
    printf("\nCongratulations, DigiDestined! You've conquered the Digital World!\n");
    return 0;
}

// Hidden function - harder to find
int metalgreymon_appears()
{
    printf("\n⚡ DIGIVOLUTION! Your Digimon evolved into MetalGreymon! ⚡\n");
    printf("But this isn't the ultimate form yet...\n");
    printf("Hint: The legendary warrior Omegamon holds the true power.\n");
    return 0;
}

// Default function
int agumon_greets()
{
    printf("\n🔥 Agumon appears! 🔥\n");
    printf("'Hi! I'm Agumon, nice to meet you!'\n");
    printf("Your journey in the Digital World begins...\n");
    return 0;
}

void display_banner()
{
    printf("\n");
    printf("████████▄   ▄█     ▄██████▄   ▄█    ▄▄▄▄███▄▄▄▄    ▄██████▄  ███▄▄▄▄   \n");
    printf("███   ▀███ ███    ███    ███ ███  ▄██▀▀▀███▀▀▀██▄ ███    ███ ███▀▀▀██▄ \n");
    printf("███    ███ ███▌   ███    █▀  ███▌ ███   ███   ███ ███    ███ ███   ███ \n");
    printf("███    ███ ███▌  ▄███        ███▌ ███   ███   ███ ███    ███ ███   ███ \n");
    printf("███    ███ ███▌ ▀▀███ ████▄  ███▌ ███   ███   ███ ███    ███ ███   ███ \n");
    printf("███    ███ ███    ███    ███ ███  ███   ███   ███ ███    ███ ███   ███ \n");
    printf("███   ▄███ ███    ███    ███ ███  ███   ███   ███ ███    ███ ███   ███ \n");
    printf("████████▀  █▀     ████████▀  █▀    ▀█   ███   █▀   ▀██████▀   ▀█   █▀  \n");
    printf("\n");
    printf("═══════════════════════════════════════════════════════════════════════\n");
    printf("              ⚡ DIGITAL ADVENTURE - TRAINING SIMULATOR ⚡            \n");
    printf("═══════════════════════════════════════════════════════════════════════\n\n");
}

void show_menu()
{
    printf("\n╔════════════════════════════════════╗\n");
    printf("║      DIGI-TERMINAL MENU            ║\n");
    printf("╠════════════════════════════════════╣\n");
    printf("║ 1. Name your Digimon               ║\n");
    printf("║ 2. Train your Digimon              ║\n");
    printf("║ 3. View Digimon stats              ║\n");
    printf("║ 4. Challenge opponent              ║\n");
    printf("║ 5. Exit Digital World              ║\n");
    printf("╚════════════════════════════════════╝\n");
    printf("\nEnter choice: ");
}

int main(int argc, char **argv)
{
    struct DigimonData *digimon;
    struct BattleSystem *battle;
    int choice;
    char input[256];
    int training_count = 0;

    display_banner();

    printf("Welcome, DigiDestined! You've been chosen to partner with a Digimon!\n");
    printf("Your adventure in the Digital World is about to begin...\n\n");

    // Allocate structures on heap
    digimon = malloc(sizeof(struct DigimonData));
    battle = malloc(sizeof(struct BattleSystem));

    // Initialize defaults
    strcpy(digimon->name, "Unknown");
    digimon->power_level = 10;
    digimon->experience = 0;
    battle->battle_function = agumon_greets;
    battle->evolution_stage = 1;
    strcpy(battle->digital_signature, "ROOKIE");

    printf("A small orange dinosaur Digimon approaches you...\n");
    printf("It seems friendly and wants to be your partner!\n");

    // Interactive loop
    while (1) {
        show_menu();

        if (fgets(input, sizeof(input), stdin) == NULL) {
            break;
        }

        choice = atoi(input);

        switch(choice) {
            case 1:
                printf("\n📝 Enter your Digimon's name: ");
                if (fgets(input, sizeof(input), stdin) != NULL) {
                    input[strcspn(input, "\n")] = 0; // Remove newline
                    // VULNERABILITY: No bounds checking!
                    strcpy(digimon->name, input);
                    printf("✅ Your Digimon's name is now: %s\n", digimon->name);
                }
                break;

            case 2:
                printf("\n💪 Training session initiated...\n");
                training_count++;
                digimon->experience += 15;
                digimon->power_level += 5;
                printf("⬆️  Experience gained: +15 (Total: %d)\n", digimon->experience);
                printf("⬆️  Power level increased: +5 (Total: %d)\n", digimon->power_level);

                if (training_count >= 3) {
                    printf("⚡ Your Digimon is glowing with energy!\n");
                }
                break;

            case 3:
                printf("\n╔════════════════════════════════╗\n");
                printf("║     DIGIMON STATUS             ║\n");
                printf("╠════════════════════════════════╣\n");
                printf("║ Name:       %-18s ║\n", digimon->name);
                printf("║ Power:      %-18d ║\n", digimon->power_level);
                printf("║ Experience: %-18d ║\n", digimon->experience);
                printf("║ Stage:      %-18s ║\n", battle->digital_signature);
                printf("╚════════════════════════════════╝\n");
                break;

            case 4:
                printf("\n⚔️  BATTLE MODE ACTIVATED! ⚔️\n");
                printf("Searching for opponent in the Digital World...\n");
                printf("Opponent found! Initiating battle sequence...\n\n");

                // Call the function pointer (this is the exploitation target!)
                battle->battle_function();
                break;

            case 5:
                printf("\n👋 Leaving the Digital World...\n");
                printf("Your Digimon will miss you!\n");
                free(digimon);
                free(battle);
                return 0;

            default:
                printf("\n❌ Invalid choice! Try again.\n");
        }
    }

    free(digimon);
    free(battle);
    return 0;
}
