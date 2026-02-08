import random as rd  # Import random module for generating random numbers

random_number = lambda: rd.randint(0, 1)  # Lambda to generate random 0 or 1

# Character classes with their stats
classes = {
    'Warrior': {'HP': 17.5, 'ATTACK': 5, 'BUDGET': 0},
    'Sorcerer': {'HP': 22.5, "ATTACK": 2.5, 'BUDGET': 0},
    'Aristocrat': {'HP': 15, 'ATTACK': 2.5, 'BUDGET': 10}
}
spawn_point = 'Spawn Point'  # Starting location

# Global variables
players_hp = 0
damage_point = 0
budget = 0
inventory = []
max_hp = 0

# Tracking cleared/defeated areas
defeated_bosses = set()
cleared_traps = set()
cleared_rewards = set()

# Map of the dungeon and possible moves
the_map = {
    'Spawn Point': {'Left': 'Merchant', 'Forward': 'Temple Entrance'},
    'Merchant': {'Right': 'Spawn Point'},
    'Temple Entrance': {'Left': 'Dirty Path', 'Forward': 'Flaming Path', 'Right': 'Bloody Path', 'Back': 'Spawn Point'},
    'Dirty Path': {'Left': 'Goblin Trap', 'Forward': 'Goblin Boss', 'Right': 'Goblin Treasure', 'Back': 'Temple Entrance'},
    'Goblin Trap': {'Right': 'Dirty Path'},
    'Goblin Boss': {'Back': 'Dirty Path'},
    'Goblin Treasure': {'Left': 'Dirty Path'},
    'Flaming Path': {'Left': 'Dragon Trap', 'Forward': 'Dragon Boss', 'Right': 'Dragon Treasure', 'Back': 'Temple Entrance'},
    'Dragon Trap': {'Right': 'Flaming Path'},
    'Dragon Boss': {'Back': 'Flaming Path'},
    'Dragon Treasure': {'Left': 'Flaming Path'},
    'Bloody Path': {'Left': 'Vampire Boss', 'Forward': 'Vampire Treasure', 'Right': 'Vampire Trap', 'Back': 'Temple Entrance'},
    'Vampire Boss': {'Right': 'Bloody Path'},
    'Vampire Treasure': {'Back': 'Bloody Path'},
    'Vampire Trap': {'Left': 'Bloody Path'}
}

# Merchant shop items
merchant_items = [('Goblin Poison',10), ('Dragon Sword', 10), ('Garlic',10)]

# Required items to fight bosses
required_items = {
    'Goblin Boss': 'Goblin Poison',
    'Dragon Boss': 'Dragon Sword',
    'Vampire Boss': 'Garlic'
}

# Trap locations and damage they deal
traps = {
    'Goblin Trap': 5,
    'Dragon Trap': 5,
    'Vampire Trap': 5
}

# Boss stats (HP and attack damage)
bosses = {
    'Goblin Boss': {'HP': 7.5, 'ATTACK': 2.5},
    'Dragon Boss': {'HP': 12.5, 'ATTACK': 5},
    'Vampire Boss': {'HP': 10, 'ATTACK': 2.5}
}

# Treasure rooms and their gold rewards
rewards = {
    'Goblin Treasure': 10,
    'Dragon Treasure': 10,
    'Vampire Treasure': 10
}

def character_choice():
    """Allows player to choose their character and assigns stats"""
    global players_hp, damage_point, budget, max_hp

    print(classes)
    while True:
        try:
            char_ch = input("Choose Your Class:\n")  # Player chooses class
        except (EOFError, KeyboardInterrupt, ValueError):
            print("Input error! Try again.")
            continue

        for name in classes:
            if char_ch.lower() == name.lower():  # Case-insensitive match
                char_ch = name
                players_hp = classes[char_ch]['HP']
                damage_point = classes[char_ch]['ATTACK']
                budget = classes[char_ch]['BUDGET']
                max_hp = classes[char_ch]['HP']
                print("Your champion is", char_ch)
                print(f"Starting budget: {budget} gold")
                return char_ch
        print("Choose between the characters above!")


def merchant():
    """Merchant shop: buy items with gold"""
    global budget
    print("\nYou entered the merchant")
    print("Merchandiser - Welcome to my shop!")
    print("Merchandiser - Here are the items you might wanna check out:")

    for item, price in merchant_items:
        print(f"{item} - {price} gold", end= " // ")

    while True:
        print("\nYour budget is", budget)
        try:
            ch = input("Would you like to shop? Yes/No: ")
        except (EOFError, KeyboardInterrupt, ValueError):
            print("Input error! Try again.")
            continue

        if ch.lower() not in ["yes", "no"]:
            print("\nEnter only yes or no!")
            continue

        if ch.lower() == 'no':  # Leave shop
            print("Merchandiser - If you want to defeat the monsters you will need these items.")
            print("Merchandiser - I'll see you soon!")
            return

        if ch.lower() == "yes":  # Shopping loop
            while True:
                try:
                    item_ch = input("\nWhat item would you like to purchase (Type Quit to quit): ")
                except (EOFError, KeyboardInterrupt, ValueError):
                    print("Input error! Try again.")
                    continue

                if item_ch.lower() == "quit":
                    return

                for item, price in merchant_items:
                    if item_ch.lower() == item.lower():  # Case-insensitive match
                        if budget >= price:
                            inventory.append(item)
                            budget -= price
                            print(f"You purchased {item} for {price} gold!")
                            print("Remaining budget:", budget)
                            merchant_items.remove((item, price))
                        else:
                            print("You don’t have enough gold!")
                        break
                else:
                    print("Choose from the list above!")

def fight(ch_choice, boss_type):
    """Handles combat system between player and boss"""
    global players_hp
    global damage_point
    global max_hp

    enemy_damage_point = bosses[boss_type]['ATTACK']
    boss_hp = bosses[boss_type]['HP']

    print(f"\n{ch_choice} VS {boss_type}")
    print("Let the fight begin!!!")

    # --- Combat instructions ---
    print("When it is your turn you can either attack or wait...")
    print("Your attack might hit the target and give them full damage or they might counter your attack and give you half damage...")
    print("If you don't want to take risk you can wait and recover you health point by half of the enemy damage point...")
    print("When it is their turn you can either parry or evade the attack...")
    print("If your parry is successful you can avoid the attack and give full damage to the enemy...")
    print("If your parry is not successful you get half damage point from the enemy...")
    print("If you choose to evade the attack and it is successful you avoid the attack and get extra health point unless you already have full health point...")
    print("If your evade is not successful you get regular damage point from the enemy...")
    # ----------------------------

    # Fight continues until either player or boss dies
    while players_hp > 0 and boss_hp > 0:
        rand_val = random_number()  # Use lambda for random 0 or 1
        print("\nYour Turn")
        try:
            fight_ch = input("Attack or Wait: ")
        except (EOFError, KeyboardInterrupt, ValueError):
            print("Input error! Defaulting to 'wait'")
            fight_ch = 'wait'

        # --- Player's turn ---
        if fight_ch.lower() == 'attack':
            if rand_val == 1:
                boss_hp -= damage_point
                print(f"\nYou hit the {boss_type} for {damage_point} damage!")
            else:  # Countered
                players_hp -= enemy_damage_point / 2
                print(f"\nYour attack was countered! You lost {enemy_damage_point/2} HP.")
        elif fight_ch.lower() == 'wait':
            if players_hp < max_hp:
                heal_amount = enemy_damage_point / 2
                actual_healing = min(heal_amount, max_hp - players_hp)
                players_hp += actual_healing
                print(f"\nYou took a defensive stance and recovered {actual_healing} HP!")
            else:
                print("\nYou took a defensive stance. Your HP is already maximum.")


        print(f"Your HP: {players_hp} // {boss_type}'s HP: {boss_hp}")

        if players_hp <= 0 or boss_hp <= 0:
            continue

        # --- Boss's turn ---
        rand_val = random_number()  # Use lambda for random 0 or 1
        print(f"\n{boss_type}'s Turn")
        try:
            fight_ch = input("Parry or Evade: ")
        except (EOFError, KeyboardInterrupt, ValueError):
            print("Input error! Defaulting to 'evade'")
            fight_ch = 'evade'

        if fight_ch.lower() == 'parry' and rand_val == 1:
                boss_hp -= damage_point
                print(f"You successfully countered the attack and gave {damage_point} damage")
        elif fight_ch.lower() == 'parry' and rand_val == 0:
            players_hp -= enemy_damage_point / 2
            print(f"\nFailed parry! Took {enemy_damage_point / 2} damage.")
        elif fight_ch.lower() == 'evade' and rand_val == 1:
            if players_hp < max_hp:
                heal_amount = enemy_damage_point / 2
                actual_healing = min(heal_amount, max_hp - players_hp)
                players_hp += actual_healing
                print(f"\nYou evaded the attack successfully and gained {actual_healing} extra HP!")
            else:
                print("\nYou evaded the attack successfully. Your HP is already maximum.")
        elif fight_ch.lower() == 'evade' and rand_val == 0:
            players_hp -= enemy_damage_point
            print(f"\nYou failed to evade and lost {enemy_damage_point} HP")

        print(f"Your HP: {players_hp} // {boss_type}'s HP: {boss_hp}")

    # Fight ends
    else:
        if players_hp <= 0:
            print("You died game over")
            exit()
        elif boss_hp <= 0:
            print(f"You defeated the {boss_type}!")
            defeated_bosses.add(boss_type)
            return

def explore_map(ch_choice):
    """Exploration system: moving between rooms, handling traps, treasures, and bosses"""
    global budget
    global players_hp

    location = spawn_point  # Start at spawn point

    while True:
        # Show status
        print(f"\nYour Health: {players_hp}", end=" // ")
        print(f"Your Inventory: {inventory}", end=" // ")
        print(f"Your Budget: {budget} // ")
        print("Your current location is", location)
        print("You can go:", ", ".join(the_map[location].keys()))
        print("Enter Quit to leave the game!")

        try:
            move = input("Enter which way you want to go: ")
        except (EOFError, KeyboardInterrupt, ValueError):
            print("Input error! Try again.")
            continue

        # Quit game
        if move.lower() == 'quit':
            print("Game Over")
            break
        # Valid movement
        elif any(move.lower() == key.lower() for key in the_map[location]):
            for key in the_map[location]:
                if move.lower() == key.lower():
                    location = the_map[location][key]
                    break
            if location == 'Merchant':
                merchant()
        else:
            print("Enter a valid way!")
            continue

        # Trap check
        if location in traps:
            if location in cleared_traps:
                print(f"\nYou already cleared the trap at {location}.")
            else:
                damage = traps[location]
                players_hp -= damage
                print(f"\nTrap! You lost {damage} HP at {location}.")
                cleared_traps.add(location)
            if players_hp <= 0:
                print("\nYou died... Game Over!")
                exit()

        # Boss room check
        if location in required_items:
            if location in defeated_bosses:
                print(f"\n{location} already defeated.")
            else:
                needed_item = required_items[location]
                if any(needed_item.lower() == item.lower() for item in inventory):
                    print(f"\nYou have {needed_item}! Time to fight {location}!")
                    fight(ch_choice, location)
                else:
                    print(f"\nYou need {needed_item} to fight {location}. Buy it from the Merchant!")

        # Treasure check
        if location in rewards:
            if location in cleared_rewards:
                print("You already collected the gold here.")
            else:
                gold = rewards[location]
                budget += gold
                print(f"\nTreasure found! You gained {gold} gold!")
                cleared_rewards.add(location)

        # Win condition
        if len(defeated_bosses) == 3:
            print("\nCongratulations! You saved the village!")
            exit()

def main():
    """Main entry point of the game"""
    print("Welcome to King of the Dungeon game!!")
    print("Avoid traps, collect gold, buy items, and slay the monsters!\n")
    ch_choice = character_choice()
    explore_map(ch_choice)

# Start the game
main()
