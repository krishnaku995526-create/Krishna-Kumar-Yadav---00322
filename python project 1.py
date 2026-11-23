import json

# Initial inventory
inventory = {
    "Rice": {"price": 50, "stock": 100},
    "Sugar": {"price": 45, "stock": 50},
    "Milk": {"price": 30, "stock": 40},
    "Oil": {"price": 150, "stock": 20}
}

# Load previously saved inventory
try:
    file = open("inventory.json", "r")
    inventory = json.load(file)
    file.close()
except FileNotFoundError:
    pass


# Function to display inventory
def view_stock():
    print("\n---------- AVAILABLE STOCK ----------")
    print("Item\tPrice\tStock")

    for item in inventory:
        print(item, "\t", inventory[item]["price"],
              "\t", inventory[item]["stock"])


# Main program
while True:

    print("\n===== GROCERY STORE MANAGEMENT SYSTEM =====")
    print("1. New Bill")
    print("2. View Stock")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        cart = []
        errors = []

        view_stock()

        n = int(input("\nEnter number of different items: "))

        # Taking item details
        for i in range(n):

            item = input("\nEnter item name: ").strip().title()
            quantity = int(input("Enter quantity: "))

            if item not in inventory:
                errors.append("Item '" + item +
                              "' not found in inventory.")

            elif quantity <= 0:
                errors.append("Invalid quantity for " + item)

            elif quantity > inventory[item]["stock"]:
                errors.append(
                    "Insufficient stock for " + item +
                    ". Available: " +
                    str(inventory[item]["stock"])
                )

            else:
                cart.append([item, quantity])

        # Check errors
        if len(errors) > 0:

            print("\n---------- ERRORS ----------")

            for error in errors:
                print(error)

            print("Bill cancelled. Stock not changed.")

        else:

            subtotal = 0

            # Calculate subtotal
            for item, quantity in cart:

                price = inventory[item]["price"]
                amount = price * quantity
                subtotal = subtotal + amount

            # Calculate discount
            if subtotal >= 1000:
                discount = subtotal * 10 / 100
            else:
                discount = 0

            # Calculate GST after discount
            amount_after_discount = subtotal - discount
            gst = amount_after_discount * 5 / 100

            total = amount_after_discount + gst

            # Display bill
            print("\n========== GROCERY BILL ==========")

            for item, quantity in cart:

                price = inventory[item]["price"]
                amount = price * quantity

                print(item, "x", quantity,
                      "=", format(amount, ".2f"))

            print("----------------------------------")
            print("Subtotal:", format(subtotal, ".2f"))
            print("Discount:", format(discount, ".2f"))
            print("GST (5%):", format(gst, ".2f"))
            print("Total: Rs.", format(total, ".2f"))
            print("==================================")

            # Update stock
            for item, quantity in cart:
                inventory[item]["stock"] -= quantity

            # Save updated inventory
            file = open("inventory.json", "w")
            json.dump(inventory, file, indent=4)
            file.close()

            # Save bill in bills.txt
            file = open("bills.txt", "a")

            file.write("\n========== GROCERY BILL ==========\n")

            for item, quantity in cart:
                price = inventory[item]["price"]
                file.write(item + " x " + str(quantity) +
                           " = Rs. " +
                           str(price * quantity) + "\n")

            file.write("Subtotal: " + str(subtotal) + "\n")
            file.write("Discount: " + str(discount) + "\n")
            file.write("GST: " + str(gst) + "\n")
            file.write("Total: Rs. " + str(total) + "\n")
            file.write("==================================\n")

            file.close()

            print("\nBill saved successfully!")
            print("Stock updated successfully!")

    elif choice == "2":

        view_stock()

    elif choice == "3":

        print("\nThank you for visiting!")
        break

    else:

        print("Invalid choice! Please try again.")