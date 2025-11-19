// DIGIMON DIGITAL ADVENTURE - CTF CHALLENGE
// Heap Overflow Exploitation Challenge
// "The Digital World awaits your commands..."

#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>
#include <time.h>

#define MAX_DIGIMON 5
#define DIGIVOLUTION_THRESHOLD 100

struct DigimonData {
    char name[64];
    int power_level;
    int experience;
    int evolution_stage; // 0=Agumon, 1=Greymon, 2=WarGreymon
};

struct BattleSystem {
    int (*battle_function)();
    int evolution_stage;
    char digital_signature[16];
};

// Forward declarations
void display_agumon();
void display_greymon();
void display_wargreymon();

// Hidden function - only accessible through heap overflow
int wargreymon_appears()
{
    printf("\n");
    printf("╔═══════════════════════════════════════════════════════════╗\n");
    printf("║          ⚡⚡⚡ CRITICAL DIGIVOLUTION! ⚡⚡⚡              ║\n");
    printf("║                                                           ║\n");
    printf("║     Your Digimon has achieved the ultimate form...       ║\n");
    printf("║                    ✧ WARGREYMON ✧                        ║\n");
    printf("║                                                           ║\n");
    printf("║    The legendary warrior of courage has been born!       ║\n");
    printf("╚═══════════════════════════════════════════════════════════╝\n\n");

    display_wargreymon();

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
    printf("\nCongratulations, DigiDestined! You've mastered the Digital World!\n");
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

void display_agumon()
{
    printf("\n");
    printf("          ████████████\n");
    printf("        ██            ██\n");
    printf("  ██████        ████    ██\n");
    printf("██                ████  ██\n");
    printf("██              ██████  ██\n");
    printf("██        ████          ██\n");
    printf("██████████              ██\n");
    printf("  ██            ████  ██\n");
    printf("    ████████████      ██\n");
    printf("      ████      ████    ██\n");
    printf("    ██  ██    ██      ████      \n");
    printf("    ██████.   ██████      ██████\n");
    printf("        ████      ██  ██████  ██\n");
    printf("   █████    ████████      ████ \n");
    printf("  ██  ██    ██. ██  ██  ██  ██\n");
    printf("  ████████████. ██████████████\n");
    printf("\n");
}

void display_greymon()
{
    printf("\n");
    printf("          ██████████.   ██████`\n");
    printf("████    ██          ████.   ██\n");
    printf("██  ██████    ████.       ██\n");
    printf("████        ████    ████████\n");
    printf("██      ██            ██\n");
    printf("████████████          ██\n");
    printf("  ██                    ██\n");
    printf("    ██████████          ██\n");
    printf("        ██          ██    ██\n");
    printf("    ████        ████      ██      \n");
    printf("  ██  ██.     ██          ██████\n");
    printf("  ██  ██      ██          ██. ██\n");
    printf("    ████        ██████    ██. ██ \n");
    printf("  ████  ██          ██      ██ \n");
    printf("██. ██    ██████████  ██  ██. ██\n");
    printf("████████████████. ██████████████\n");
    printf("\n");
}

void display_wargreymon()
{
    printf("\n");
    printf("  ██.                   ██\n");
    printf("██. ██.   ██████████████. ██\n");
    printf("██.   ████.       ██.     ██\n");
    printf("██. ██.   ██████. ██████████\n");
    printf("  ██    ██████.         ██\n");
    printf("  ██. ██            ██████████\n");
    printf("  ██████████. ████████      ██\n");
    printf("    ██.   ██. ██████.     ██\n");
    printf("      ██████████    ██████████\n");
    printf("    ████            ████.   ██\n");
    printf("  ██. ██. ████.   ████.     ██\n");
    printf("  ██. ████.   ██████. ██. ██ \n");
    printf("    ████████████.   ██. ██\n");
    printf("    ████  ██. ██    ████████\n");
    printf("  ██. ██. ████████. ██. ██. ██\n");
    printf("  ██████████.   ██████████████\n");
    printf("\n");
}

void show_menu(int show_digivolve)
{
    printf("\n╔════════════════════════════════════╗\n");
    printf("║      DIGI-TERMINAL MENU            ║\n");
    printf("╠════════════════════════════════════╣\n");
    printf("║ 1. Name your Digimon               ║\n");
    printf("║ 2. Train your Digimon              ║\n");
    printf("║ 3. View Digimon stats              ║\n");
    printf("║ 4. Challenge opponent              ║\n");
    printf("║ 5. Exit Digital World              ║\n");
    if (show_digivolve) {
        printf("║ 6. Digivolve                       ║\n");
    }
    printf("╚════════════════════════════════════╝\n");
    printf("\nEnter choice: ");
}

void clear_screen()
{
    // Clear screen using ANSI escape codes
    printf("\033[2J\033[H");
}

void wait_for_enter()
{
    printf("\nPress Enter to continue...");
    getchar();
}

int main(int argc, char **argv)
{
    struct DigimonData *digimon;
    struct BattleSystem *battle;
    int choice;
    char input[256];
    char safe_name[32]; // Safe buffer for initial naming
    int training_count = 0;
    int has_initial_name = 0; // Track if initial naming is done
    int has_digivolved = 0; // Track if digivolution has occurred

    // Seed random number generator
    srand(time(NULL));

    display_banner();

    printf("Welcome, DigiDestined! You've been chosen to partner with a Digimon!\n");
    printf("Your adventure in the Digital World is about to begin...\n\n");

    // Allocate structures on heap
    digimon = malloc(sizeof(struct DigimonData));
    battle = malloc(sizeof(struct BattleSystem));

    // Initialize defaults
    strcpy(digimon->name, "Unknown");
    digimon->power_level = 10;
    digimon->experience = 0; // Start at 0, need 50 to digivolve
    digimon->evolution_stage = 0; // Start as Agumon
    battle->battle_function = agumon_greets;
    battle->evolution_stage = 1;
    strcpy(battle->digital_signature, "Rookie");

    printf("A small orange dinosaur Digimon approaches you...\n");
    printf("It seems friendly and wants to be your partner!\n");

    display_agumon();

    // Show Agumon's greeting
    battle->battle_function();

    // Interactive loop
    while (1) {
        // Show digivolve option only if exp >= 50 and not yet digivolved
        int show_digivolve = (digimon->experience >= 50 && !has_digivolved);
        if (show_digivolve) {
            printf("\n⚡ Your Digimon is ready to digivolve! ⚡\n");
        }

        show_menu(show_digivolve);

        if (fgets(input, sizeof(input), stdin) == NULL) {
            break;
        }

        choice = atoi(input);

        // Clear screen after user input (before processing action)
        clear_screen();

        switch(choice) {
            case 1:
                if (has_initial_name) {
                    printf("\n❌ You've already named your Digimon!\n");
                    printf("Your Digimon refuses to change its name.\n");
                    printf("💡 Hint: Digivolution might give you another chance...\n");

                    // Display current form
                    if (digimon->evolution_stage == 0) {
                        display_agumon();
                    } else if (digimon->evolution_stage == 1) {
                        display_greymon();
                    } else if (digimon->evolution_stage == 2) {
                        display_wargreymon();
                    }
                } else {
                    printf("\n📝 Enter your Digimon's name: ");
                    if (fgets(safe_name, sizeof(safe_name), stdin) != NULL) {
                        safe_name[strcspn(safe_name, "\n")] = 0; // Remove newline
                        // SAFE: Using safe buffer for initial naming
                        strncpy(digimon->name, safe_name, sizeof(digimon->name) - 1);
                        digimon->name[sizeof(digimon->name) - 1] = '\0';
                        has_initial_name = 1;
                        printf("✅ Your Digimon's name is now: %s\n", digimon->name);

                        // Display current form
                        if (digimon->evolution_stage == 0) {
                            display_agumon();
                        } else if (digimon->evolution_stage == 1) {
                            display_greymon();
                        } else if (digimon->evolution_stage == 2) {
                            display_wargreymon();
                        }
                    }
                }
                wait_for_enter();
                clear_screen();
                break;

            case 2:
                printf("\n💪 Training session initiated...\n");
                training_count++;
                // Random experience between 5-15
                int exp_gain = (rand() % 11) + 5; // Random number between 5-15

                // Cap experience at 100
                if (digimon->experience + exp_gain > 100) {
                    exp_gain = 100 - digimon->experience;
                }
                digimon->experience += exp_gain;

                // Cap power at 100
                int power_gain = 5;
                if (digimon->power_level + power_gain > 100) {
                    power_gain = 100 - digimon->power_level;
                }
                digimon->power_level += power_gain;

                printf("⬆️  Experience gained: +%d (Total: %d)\n", exp_gain, digimon->experience);
                printf("⬆️  Power level increased: +%d (Total: %d)\n", power_gain, digimon->power_level);

                if (digimon->experience >= 50 && !has_digivolved) {
                    printf("⚡ Your Digimon is glowing with energy! You can evolve it!\n");
                }

                if (digimon->experience >= 100) {
                    printf("💫 Your Digimon has reached maximum experience!\n");
                }
                if (digimon->power_level >= 100) {
                    printf("💪 Your Digimon has reached maximum power!\n");
                }

                // Display current form
                if (digimon->evolution_stage == 0) {
                    display_agumon();
                } else if (digimon->evolution_stage == 1) {
                    display_greymon();
                } else if (digimon->evolution_stage == 2) {
                    display_wargreymon();
                }

                wait_for_enter();
                clear_screen();
                break;

            case 3:
                printf("\n╔════════════════════════════════════════════════════════════╗\n");
                printf("║                    DIGIMON STATUS                          ║\n");
                printf("╠════════════════════════════════════════════════════════════╣\n");
                printf("║ Name:       %-47s║\n", digimon->name);
                printf("║ Power:      %-47d║\n", digimon->power_level);
                printf("║ Experience: %-47d║\n", digimon->experience);
                printf("║ Level:      %-47s║\n", battle->digital_signature);
                printf("╠════════════════════════════════════════════════════════════╣\n");

                // Display description based on evolution stage
                if (digimon->evolution_stage == 0) {
                    printf("║ Description:                                               ║\n");
                    printf("║ A Reptile Digimon which has grown and become able to      ║\n");
                    printf("║ walk on two legs.                                          ║\n");
                } else if (digimon->evolution_stage == 1) {
                    printf("║ Description:                                               ║\n");
                    printf("║ A Dinosaur Digimon whose cranial skin has hardened so     ║\n");
                    printf("║ that it is covered in a rhinoceros beetle-like shell.     ║\n");
                } else if (digimon->evolution_stage == 2) {
                    printf("║ Description:                                               ║\n");
                    printf("║ The strongest dragon warrior whose body is clad in armor   ║\n");
                    printf("║ of the super-metal \"Chrome Digizoid\", it is the ultimate  ║\n");
                    printf("║ form of Greymon-species Digimon.                           ║\n");
                }
                printf("╚════════════════════════════════════════════════════════════╝\n");

                // Display current form
                if (digimon->evolution_stage == 0) {
                    display_agumon();
                } else if (digimon->evolution_stage == 1) {
                    display_greymon();
                } else if (digimon->evolution_stage == 2) {
                    display_wargreymon();
                }

                wait_for_enter();
                clear_screen();
                break;

            case 4:
                printf("\n⚔️  BATTLE MODE ⚔️\n");
                printf("This feature is coming soon...\n");
                printf("Stay tuned for epic battles in the Digital World!\n");

                // Display current form
                if (digimon->evolution_stage == 0) {
                    display_agumon();
                } else if (digimon->evolution_stage == 1) {
                    display_greymon();
                } else if (digimon->evolution_stage == 2) {
                    display_wargreymon();
                }

                wait_for_enter();
                clear_screen();
                break;

            case 5:
                printf("\n👋 Leaving the Digital World...\n");
                printf("Your Digimon will miss you!\n");
                free(digimon);
                free(battle);
                return 0;

            case 6:
                if (digimon->experience < 50) {
                    printf("\n⚠️  Your Digimon is not ready to digivolve yet!\n");
                    printf("Current Experience: %d / 50 needed\n", digimon->experience);
                    printf("Keep training!\n");
                } else if (has_digivolved) {
                    printf("\n⚠️  Your Digimon has already digivolved!\n");
                } else {
                    printf("\n✨ DIGIVOLUTION SEQUENCE INITIATED! ✨\n");
                    printf("The Digital World's energy is surging around your Digimon!\n");
                    printf("To complete the digivolution, you must call out your Digimon's name!\n\n");

                    printf("📝 Enter your Digimon's new name: ");
                    if (fgets(input, sizeof(input), stdin) != NULL) {
                        input[strcspn(input, "\n")] = 0; // Remove newline

                        // VULNERABILITY: No bounds checking during digivolution rename!
                        strcpy(digimon->name, input);

                        clear_screen();
                        printf("\n⚡ DIGIVOLUTION IN PROGRESS... ⚡\n\n");

                        // Check if heap overflow occurred by checking battle_function pointer
                        // If it's been overwritten to wargreymon_appears, trigger WarGreymon path
                        if (battle->battle_function == wargreymon_appears) {
                            // Overflow successful - call the function which will display flag
                            digimon->evolution_stage = 2;
                            strcpy(battle->digital_signature, "Mega");
                            digimon->power_level += 100;
                            if (digimon->power_level > 100) digimon->power_level = 100;

                            battle->battle_function();
                            has_digivolved = 1;
                        } else {
                            // Normal digivolution to Greymon
                            digimon->evolution_stage = 1;
                            strcpy(battle->digital_signature, "Champion");
                            digimon->power_level += 50;
                            if (digimon->power_level > 100) digimon->power_level = 100;

                            printf("🦖 GREYMON! 🦖\n");
                            printf("Your Digimon has evolved to its Champion form!\n");
                            printf("New name: %s\n\n", digimon->name);
                            display_greymon();

                            has_digivolved = 1;
                        }
                    }
                }

                wait_for_enter();
                clear_screen();
                break;

            default:
                printf("\n❌ Invalid choice! Try again.\n");
                wait_for_enter();
                clear_screen();
        }
    }

    free(digimon);
    free(battle);
    return 0;
}
