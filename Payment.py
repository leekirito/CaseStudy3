class Payment():
    def __init__(self):
        pass

    @classmethod
    def pay(cls, price):
        payment = int(input("Payment: "))
        if payment >= price:
            print(f"Payed successfully!, change: {payment - price}")
            return True
        else:
            print("insufficient funds!")
            return False
