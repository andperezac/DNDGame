import random

class Character:
    def __init__(self, name, char_class, hp, attack, defense):
        self.name = name
        self.char_class = char_class
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.inventory = []
        self.quests = []
        if char_class == "Warlock":
            self.spells = {
                "Eldritch Blast": {"damage": 10, "cost": 0},
                "Shadow Bolt": {"damage": 20, "cost": 0},
                "Drain Life": {"damage": 15, "heal": 10, "cost": 0}
            }
        elif char_class == "Barbarian":
            self.rages = 2  # Number of rages available
            self.in_rage = False
        elif char_class == "Rogue":
            self.sneak_attack = True  # Sneak Attack available

    def is_alive(self):
        return self.hp > 0

    def rage(self):
        if self.rages > 0:
            self.rages -= 1
            self.in_rage = True
            print(f"{self.name} is now raging!")
        else:
            print("No rages left!")

    def end_rage(self):
        if self.in_rage:
            self.in_rage = False
            print(f"{self.name} has calmed down and is no longer raging.")

    def use_sneak_attack(self):
        if self.sneak_attack:
            self.sneak_attack = False
            return True
        else:
            return False

    def reset_sneak_attack(self):
        self.sneak_attack = True

    def add_quest(self, quest):
        self.quests.append(quest)
        print(f"New quest added: {quest['name']}")

    def complete_quest(self, quest_name):
        quest = next((q for q in self.quests if q['name'] == quest_name), None)
        if quest:
            self.quests.remove(quest)
            print(f"Quest completed: {quest_name}")
            # Reward player for completing the quest
            self.hp = min(100, self.hp + quest['reward']['hp'])
            self.inventory.append(quest['reward']['item'])
        else:
            print(f"No such quest: {quest_name}")

class Enemy:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

def create_character():
    name = input("Enter your character's name: ")
    print("Choose your class:\n1. Rogue\n2. Barbarian\n3. Warlock")
    class_choice = int(input("Enter the number of your choice: "))

    if class_choice == 1:
        return Character(name, "Rogue", 70, 15, 10)
    elif class_choice == 2:
        return Character(name, "Barbarian", 100, 12, 15)
    elif class_choice == 3:
        return Character(name, "Warlock", 80, 18, 8)
    else:
        print("Invalid choice, defaulting to Rogue.")
        return Character(name, "Rogue", 70, 15, 10)

def explore():
    print("\nYou venture into the unknown and encounter...")
    event = random.choice(["combat", "quest"])
    if event == "combat":
        enemy_type = random.choice(["Goblin", "Orc", "Dragon"])
        if enemy_type == "Goblin":
            return "combat", Enemy("Goblin", 30, 5, 3)
        elif enemy_type == "Orc":
            return "combat", Enemy("Orc", 50, 10, 5)
        elif enemy_type == "Dragon":
            return "combat", Enemy("Dragon", 100, 20, 10)
    elif event == "quest":
        quest = {
            "name": "Find the Lost Amulet",
            "description": "Find the lost amulet in the nearby forest.",
            "reward": {"hp": 20, "item": "Amulet of Strength"}
        }
        return "quest", quest

def combat(player, enemy):
    print(f"\nA wild {enemy.name} appears!")
    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name} (HP: {player.hp}) vs {enemy.name} (HP: {enemy.hp})")
        
        if player.char_class == "Warlock":
            action = input("Do you want to (a)ttack, cast a (s)pell or (r)un away? ").lower()
        elif player.char_class == "Barbarian":
            action = input("Do you want to (a)ttack, (r)age, or (r)un away? ").lower()
        else:
            action = input("Do you want to (a)ttack or (r)un away? ").lower()

        if action == 'a':
            if player.char_class == "Barbarian" and player.in_rage:
                damage = max(0, (player.attack + 2) - enemy.defense)  # Bonus damage from rage
            elif player.char_class == "Rogue" and player.use_sneak_attack():
                damage = max(0, player.attack + 10 - enemy.defense)  # Bonus damage from sneak attack
            else:
                damage = max(0, player.attack - enemy.defense)
            enemy.hp -= damage
            print(f"You deal {damage} damage to the {enemy.name}.")
            if player.char_class == "Barbarian" and player.in_rage:
                player.end_rage()  # Rage ends after one attack

        elif action == 's' and player.char_class == "Warlock":
            spell_choice = input("Choose a spell: 1. Eldritch Blast 2. Shadow Bolt 3. Drain Life: ")
            if spell_choice == '1':
                spell = "Eldritch Blast"
            elif spell_choice == '2':
                spell = "Shadow Bolt"
            elif spell_choice == '3':
                spell = "Drain Life"
            else:
                print("Invalid choice, defaulting to Eldritch Blast.")
                spell = "Eldritch Blast"

            spell_info = player.spells[spell]
            damage = spell_info["damage"]
            enemy.hp -= damage
            print(f"You cast {spell} and deal {damage} damage to the {enemy.name}.")
            if spell == "Drain Life":
                player.hp += spell_info["heal"]
                print(f"You heal for {spell_info['heal']} HP.")
        
        elif action == 'r' and player.char_class == "Barbarian":
            player.rage()

        elif action == 'r':
            print("You run away safely!")
            return False
        else:
            print("Invalid action. Please choose a valid action.")

        if enemy.is_alive():
            damage = max(0, enemy.attack - player.defense)
            player.hp -= damage
            print(f"The {enemy.name} deals {damage} damage to you.")
        else:
            print(f"You have defeated the {enemy.name}!")
            if player.char_class == "Rogue":
                player.reset_sneak_attack()  # Reset sneak attack after defeating an enemy
            return True
    
    if not player.is_alive():
        print("You have been defeated. Game Over.")
        return False

    return True

def main():
    print("Welcome to the D&D Adventure Game!")
    player = create_character()
    
    while player.is_alive():
        print("\nWhat would you like to do?\n1. Explore\n2. View Character\n3. Rest\n4. Complete Quest\n5. Quit")
        choice = int(input("Enter the number of your choice: "))

        if choice == 1:
            event_type, event = explore()
            if event_type == "combat":
                if combat(player, event) == False:
                    break
            elif event_type == "quest":
                player.add_quest(event)
                print(f"Quest: {event['name']}\nDescription: {event['description']}")

        elif choice == 2:
            print(f"\nCharacter Info:\nName: {player.name}\nClass: {player.char_class}\nHP: {player.hp}\nAttack: {player.attack}\nDefense: {player.defense}\nInventory: {player.inventory}\nQuests: {[quest['name'] for quest in player.quests]}")
            if player.char_class == "Warlock":
                print(f"Spells: {', '.join(player.spells.keys())}")
            elif player.char_class == "Barbarian":
                print(f"Rages left: {player.rages}")
            elif player.char_class == "Rogue":
                print(f"Sneak Attack available: {'Yes' if player.sneak_attack else 'No'}")
        elif choice == 3:
            print("You take a rest and recover some health.")
            player.hp = min(100, player.hp + 20)
        elif choice == 4:
            if player.quests:
                print("Your current quests are:")
                for i, quest in enumerate(player.quests, 1):
                    print(f"{i}. {quest['name']}: {quest['description']}")
                quest_choice = int(input("Enter the number of the quest you want to complete: "))
                if 1 <= quest_choice <= len(player.quests):
                    player.complete_quest(player.quests[quest_choice - 1]['name'])
                else:
                    print("Invalid choice.")
            else:
                print("You have no active quests.")
        elif choice == 5:
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
