"""Week 5 Coding Assignment. Juanita Stuenkel"""

import random

def display_player_status(player_stats):
    """prints player's health"""
    print(f"Your current health: {player_stats['health']}." )

def handle_path_choice(player_stats):
    """decides left or right"""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        if player_stats["health"] <= 90:
            player_stats["health"] += 10
        elif player_stats["health"] > 90:
            player_stats["health"] = 100
    elif path == "right":
        print("You fall into a pit and lose 15 health points.")
        player_stats["health"] -= 15
        if player_stats["health"] <= 0:
            player_stats["health"] = 0
            print("You are barely alive!")
    return player_stats

def player_attack(monster_health):
    """player deals 15 damage to the monster"""
    monster_health -= 15
    print("You strike the monster for 15 damage!")
    print(f"The monster is at {monster_health} health!")
    return monster_health

def monster_attack(player_stats):
    """monster attacks the player, with a chance of a critical hit"""
    critical = random.random()

    if critical < 0.5:
        player_stats["health"] -= 20
        print("The monster lands a critical hit for 20 damage!")
    if critical > 0.5:
        player_stats["health"] -= 10
        print("The monster hits you for 10 damage!")
    return player_stats

def check_for_treasure(has_treasure):
    """checks for treasure"""
    if has_treasure is True:
        print("You found the hidden treasure! You win!")
    if has_treasure is False:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory, item):
    """ adds acquired item to list and print aquired item"""

    inventory.append(item) # Add more items to list as they are acquired in the room
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """ displays inventory in a number list"""
    if len(inventory) > 0:
        print("Your inventory:")
        for index, item in enumerate(inventory):
            print(f"{index + 1}. {item}")
    else:
        print("Your inventory is empty.")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """ runs through each dungeon room """
    bypass_puzzle = False
    for dungeon_room in dungeon_rooms:   # used to go through each list within the tuple to use it
        print(dungeon_room[0])
        if dungeon_room[1] is not None:
            acquire_item(inventory, dungeon_room[1])
        if dungeon_room [2] == "puzzle":
            print("You encounter a puzzle!")
            if bypass_puzzle:
                print("You used your knowledge to bypass the challenge")
                print(dungeon_room[3][0])
                player_stats["health"] += dungeon_room[3][2]
                bypass_puzzle = False
            else:
                puzzle_input = input("Solve or skip the puzzle?")
                success_a = True
                if puzzle_input == "solve":
                    success_a = random.choice([True, False])
                if success_a is True:
                    print(dungeon_room[3][0])
                    player_stats["health"] += dungeon_room[3][2]
                else:
                    print(dungeon_room[3][1])
        elif dungeon_room [2] == "trap":
            print("You see a potential trap!")
            trap_input = input("Disarm or bypass the trap?")
            success_b = True
            if trap_input == "disarm":
                success_b = random.choice([True, False])
            else:
                success_b = True
            if success_b is True:
                print(dungeon_room[3][0])
            else:
                print(dungeon_room[3][1])
            player_stats["health"] += dungeon_room[3][2]
        elif dungeon_room [2] == "none":
            print(dungeon_room[0])
            if dungeon_room[1]:
                acquire_item(inventory, dungeon_room[1])
                print(f"You found a {dungeon_room[1]} in the room.")
            else:
                print("There doesn't seem to be a challenge in this room.")
        elif dungeon_room[2] == "library":
            print(dungeon_room[0])
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.", 
                "The key lies with the gnome.", 
                "Beware the shadows.", 
                "The amulet unlocks the final door."
            ]
            selected_clues = random.sample(possible_clues,2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            if "staff_of_wisdom" in inventory:
                print("You understand the clues and can now bypass a puzzle challenge")
            bypass_puzzle = True
    return player_stats, inventory, clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """ deals with artifacts and their effects """
    if artifact_name in artifacts:
        description = artifacts[artifact_name]["description"]
        print(description)
        if artifacts[artifact_name]["effect"] == "increases health":
            player_stats["health"] += artifacts[artifact_name]["power"]
            print(f"This artifact healed you by {artifacts[artifact_name]['power']}")
            del artifacts[artifact_name]
        elif artifacts[artifact_name]["effect"] == "enhances attack":
            player_stats["attack"] += artifacts[artifact_name]["power"]
            print(f"This artifact gave you {artifacts[artifact_name]['power']} more power")
            del artifacts[artifact_name]

    else:
        print("You found nothing of interest.")

    return player_stats, artifacts

def combat_encounter(player_stats, monster_health, has_treasure=False):
    """runs combat encounter"""
    while player_stats["health"] > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        print(player_stats, type(player_stats))
        if monster_health > 0:
            player_stats = monster_attack(player_stats)
    if monster_health <= 0 and has_treasure:
        print("You defeated the monster!")
        return True
    if player_stats["health"] <= 0:
        print("Game Over!")
        return False
    else:
        return False

def find_clue(clues, new_clue):
    """ adds clues to clues """
    if new_clue not in clues:
        clues.add(new_clue)   ## used add function to put new items in clue set
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def main():

    """Main game loop."""

    dungeon_rooms = [

    ("Dusty library", "key", "puzzle",

    ("Solved puzzle!", "Puzzle unsolved.", -5)),

    ("Narrow passage, creaky floor", "torch", "trap",

    ("Avoided trap!", "Triggered trap!", -10)),

    ("Grand hall, shimmering pool", "healing potion", "none", None),

    ("Small room, locked chest", "treasure", "puzzle",

    ("Cracked code!", "Chest locked.", -5)),

    ("Cryptic Library", None, "library", None)

    ]

    player_stats = {'health': 100, 'attack': 5}

    monster_health = 70

    inventory = []

    clues = set()

    artifacts = {

        "amulet_of_vitality": {

            "description": "Glowing amulet, life force.",

            "power": 15,

            "effect": "increases health"

        },

        "ring_of_strength": {

            "description": "Powerful ring, attack boost.",

            "power": 10,

            "effect": "enhances attack"

        },

        "staff_of_wisdom": {

            "description": "Staff of wisdom, ancient.",

            "power": 5,

            "effect": "solves puzzles"

        }

    }

    has_treasure = random.choice([True, False])


    display_player_status(player_stats)

    player_stats = handle_path_choice(player_stats)



    if player_stats['health'] > 0:

        treasure_obtained_in_combat = combat_encounter(

            player_stats, monster_health, has_treasure)

        if treasure_obtained_in_combat is not None:

            check_for_treasure(treasure_obtained_in_combat)



        if random.random() < 0.3:

            artifact_keys = list(artifacts.keys())

            if artifact_keys:

                artifact_name = random.choice(artifact_keys)

                player_stats, artifacts = discover_artifact(

                    player_stats, artifacts, artifact_name)

                display_player_status(player_stats)



        if player_stats['health'] > 0:

            player_stats, inventory, clues = enter_dungeon(

                player_stats, inventory, dungeon_rooms, clues)

            print("\n--- Game End ---")

            display_player_status(player_stats)

            print("Final Inventory:")

            display_inventory(inventory)

            print("Clues:")

            if clues:

                for clue in clues:

                    print(f"- {clue}")

            else:

                print("No clues.")

if __name__ == "__main__":
    main()
