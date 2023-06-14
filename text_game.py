def start_game():
    print("Welcome to the Text Adventure Game!")
    print("You wake up in a mysterious room. There are two doors in front of you.")

    while True:
        choice = input("Which door do you choose? (1 or 2): ")

        if choice == "1":
            room1()
            break
        elif choice == "2":
            room2()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def room1():
    print("You enter room 1.")
    print("There is a key on the table. You can take it or leave it.")

    while True:
        choice = input("What do you do? (take or leave): ")

        if choice == "take":
            print("You take the key. You can use it to unlock doors.")
            break
        elif choice == "leave":
            print("You leave the key behind.")
            break
        else:
            print("Invalid choice. Please enter 'take' or 'leave'.")

def room2():
    print("You enter room 2.")
    print("There is a monster in the room! You need a weapon to defeat it.")

    while True:
        choice = input("What do you do? (search or run): ")

        if choice == "search":
            print("You find a sword! You can now defeat the monster.")
            break
        elif choice == "run":
            print("You run away from the monster.")
            break
        else:
            print("Invalid choice. Please enter 'search' or 'run'.")

# Start the game
start_game()
