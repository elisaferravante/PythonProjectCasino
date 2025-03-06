import random


# Load player profile or create a new one
def load_profile():
   try:
       with open("casino_profile.txt", "r") as file:
           balance = float(file.readline().strip())
           games_played = int(file.readline().strip())
           win_ratio = float(file.readline().strip())
           return {"balance": balance, "games_played": games_played, "win_ratio": win_ratio}
   except FileNotFoundError:
       return {"balance": 1000, "games_played": 0, "win_ratio": 0.0}


def save_profile(profile):
   with open("casino_profile.txt", "w") as file:
       file.write(f"{profile['balance']}\n")
       file.write(f"{profile['games_played']}\n")
       file.write(f"{profile['win_ratio']}\n")


def start_casino():
  profile = load_profile()
  money = profile["balance"]
  print("Welcome to the Casino!")
  print(f"Current Balance: ${money:.2f}")


  if money <= 0:
      print("You have run out of money. Better luck next time!")
      save_profile(profile)
      return


  while money > 0:
      print("\nChoose a game to play:")
      print("1. Roulette")
      print("2. Blackjack")
      print("3. Slots")
      print("4. View Stats")
      print("5. Exit")
      choice = input("Enter the number of your choice: ")


      if choice == "1":
          money = play_roulette(money, profile)
      elif choice == "2":
          money = play_blackjack(money, profile)
      elif choice == "3":
          money = play_slots(money, profile)
      elif choice == "4":
          view_stats(profile)
          continue
      elif choice == "5":
          profile["balance"] = money
          save_profile(profile)
          print(f"You are leaving the casino with ${money:.2f}")
          break
      else:
          print("Invalid choice. Please select again.")
          continue  # Skip the rest of the loop if the input was invalid


      if money <= 0:
          print("You have run out of money. Better luck next time!")
          break


      save_profile(profile)  # Save after every round


def play_roulette(money, profile):
  print("\nWelcome to Roulette!")
  bet = get_bet(money)
  money -= bet  # Deduct bet first to ensure losses are accounted for
  valid_bets = ["red", "black", "even", "odd", "1-18", "19-36", "1st12", "2nd12", "3rd12", "0"]


  # Add single number bets 0-36
  for i in range(37):
      valid_bets.append(str(i))


  while True:
      bet_type = input("Place your bet (red / black / even / odd / 1-18 / 19-36 / 1st12 / 2nd12 / 3rd12 / 0-36): ").lower()
      if bet_type in valid_bets:
          break
      print("Invalid bet. Please choose a valid option.")


  result = random.randint(0, 36)
  red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
  color = "red" if result in red_numbers else "black"
  win = False
  payout = 0


  if bet_type.isdigit():
      bet_type = int(bet_type)
      if bet_type == result:
          payout = bet * 36  # Pays 35x winnings plus the original bet
          win = True
  elif bet_type == "red" and color == "red":
      payout = bet * 2
      win = True
  elif bet_type == "black" and color == "black":
      payout = bet * 2
      win = True
  elif bet_type == "even" and result % 2 == 0 and result != 0:
      payout = bet * 2
      win = True
  elif bet_type == "odd" and result % 2 != 0:
      payout = bet * 2
      win = True
  elif bet_type == "1-18" and 1 <= result <= 18:
      payout = bet * 2
      win = True
  elif bet_type == "19-36" and 19 <= result <= 36:
      payout = bet * 2
      win = True
  elif bet_type == "1st12" and 1 <= result <= 12:
      payout = bet * 3
      win = True
  elif bet_type == "2nd12" and 13 <= result <= 24:
      payout = bet * 3
      win = True
  elif bet_type == "3rd12" and 25 <= result <= 36:
      payout = bet * 3
      win = True


  if win:
      money += payout  # Add winnings to balance
      if profile["games_played"] > 0:
          profile["win_ratio"] = ((profile["win_ratio"] * profile["games_played"]) + 1) / (profile["games_played"] + 1)
      else:
          profile["win_ratio"] = 1.0  # If this is the first game, and it's a win, set win_ratio to 1
  else:
      if profile["games_played"] > 0:
          profile["win_ratio"] = (profile["win_ratio"] * profile["games_played"]) / (profile["games_played"] + 1)
      else:
          profile["win_ratio"] = 0.0  # If this is the first game, and it's a loss, set win_ratio to 0


  profile["games_played"] += 1  # Increment games played


  print(f"Roulette spun: {result} ({color if result != 0 else 'green'})")
  print(f"{'You won!' if win else 'You lost!'} New balance: ${money:.2f}")
  return money


def play_blackjack(money, profile):
   print("\nWelcome to Blackjack!")
   bet = get_bet(money)
   money -= bet  # Deduct bet first


   def deal_card():
       cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # Face cards = 10, Ace = 11
       return random.choice(cards)


   def calculate_hand(hand):
       total = sum(hand)
       aces = hand.count(11)
       while total > 21 and aces:
           total -= 10  # Convert Ace from 11 to 1
           aces -= 1
       return total


   def is_blackjack(hand):
       return len(hand) == 2 and calculate_hand(hand) == 21


   # Deal initial hands
   player_hand = [deal_card(), deal_card()]
   dealer_hand = [deal_card(), deal_card()]


   print(f"Your hand: {player_hand} (Total: {calculate_hand(player_hand)})")
   print(f"Dealer's face-up card: {dealer_hand[0]}")


   player_blackjack = is_blackjack(player_hand)
   dealer_blackjack = is_blackjack(dealer_hand)


   # Check for Straight Blackjacks Before Player Moves
   if player_blackjack and dealer_blackjack:
       print("Both you and the dealer have Blackjack! It's a tie, bet refunded.")
       money += bet  # Refund the bet
       win = None  # A tie does not affect win ratio
   elif player_blackjack:
       print("Blackjack! You win 1.5x your bet!")
       money += bet * 2.5  # Player walks away with 2.5x original bet
       win = True
   elif dealer_blackjack:
       print("Dealer has Blackjack! You lose.")
       win = False
   else:
       # Continue game if no immediate Blackjack
       while calculate_hand(player_hand) < 21:
           action = input("Do you want to hit or stand? (h/s): ").lower()
           if action == "h":
               player_hand.append(deal_card())
               print(f"Your new hand: {player_hand} (Total: {calculate_hand(player_hand)})")
           else:
               break


       player_total = calculate_hand(player_hand)


       if player_total > 21:
           print("You busted! Dealer wins.")
           win = False
       else:
           # Dealer's turn
           print(f"Dealer's hand: {dealer_hand} (Total: {calculate_hand(dealer_hand)})")
           while calculate_hand(dealer_hand) < 17:
               dealer_hand.append(deal_card())
               print(f"Dealer draws: {dealer_hand} (Total: {calculate_hand(dealer_hand)})")


           dealer_total = calculate_hand(dealer_hand)


           if dealer_total > 21 or player_total > dealer_total:
               print("You win!")
               money += bet * 2  # Standard win payout
               win = True
           elif player_total == dealer_total:
               print("It's a tie! Bet refunded.")
               money += bet
               win = None  # A tie does not affect win ratio
           else:
               print("Dealer wins!")
               win = False


   # **Update Win Ratio Only for Wins/Losses (Not Ties)**
   if win is not None:
       if win:
           if profile["games_played"] > 0:
               profile["win_ratio"] = ((profile["win_ratio"] * profile["games_played"]) + 1) / (profile["games_played"] + 1)
           else:
               profile["win_ratio"] = 1.0  # First win
       else:
           if profile["games_played"] > 0:
               profile["win_ratio"] = (profile["win_ratio"] * profile["games_played"]) / (profile["games_played"] + 1)
           else:
               profile["win_ratio"] = 0.0  # First loss


   profile["games_played"] += 1  # Increment games played


   print(f"New balance: ${money:.2f}")
   return money


def play_slots(money, profile):
   print("\nWelcome to Slots!")
   bet = get_bet(money)
   money -= bet


   symbols = ["7", "BAR", "CHERRY", "DIAMOND", "LEMON"]
   slot_result = [random.choice(symbols) for _ in range(3)]
   print(f"[ {slot_result[0]} | {slot_result[1]} | {slot_result[2]} ]")


   if slot_result[0] == slot_result[1] == slot_result[2]:  # Jackpot (3 matches)
       print("Jackpot! You win 10x your bet!")
       money += bet * 10
       win = True
   elif slot_result[0] == slot_result[1] or slot_result[1] == slot_result[2] or slot_result[0] == slot_result[2]:  # 2 matches
       print("You win 2x your bet!")
       money += bet * 2
       win = True
   else:
       print("You lost!")
       win = False


   if win:
       if profile["games_played"] > 0:
           profile["win_ratio"] = ((profile["win_ratio"] * profile["games_played"]) + 1) / (profile["games_played"] + 1)
       else:
           profile["win_ratio"] = 1.0  # First win
   else:
       if profile["games_played"] > 0:
           profile["win_ratio"] = (profile["win_ratio"] * profile["games_played"]) / (profile["games_played"] + 1)
       else:
           profile["win_ratio"] = 0.0  # First loss


   profile["games_played"] += 1  # Increment games played


   print(f"New balance: ${money:.2f}")
   return money


def view_stats(profile):
   print("\n===== PLAYER STATS =====")
   print(f"🃏 Total Games Played: {profile['games_played']}")
   print(f"💰 Current Balance: ${profile['balance']:.2f}")
   print(f"🎯 Win Ratio: {profile['win_ratio'] * 100:.2f}%")
   print("========================")


def get_bet(money):
   while True:
       try:
           bet = float(input("Enter your bet amount: $"))
           #Prevents invalid bets
           if bet <= 0:
               print("Bet must be greater than $0.")  # Prevents $0 or negative bets
           elif bet > money:
               print(f"You don't have enough money! Your balance is ${money:.2f}, Please enter a new bet!")  # Prevents over-betting
           else:
               return bet  #Only returns if bet is valid
       except ValueError:
           print("Invalid input. Enter a numerical value.")  # Prevents letter inputs


if __name__ == "__main__":
  start_casino()
