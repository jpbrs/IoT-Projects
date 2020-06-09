# “Lazy evaluation is the idea that, especially when dealing with large amounts of data, you do not want process all of the data before using the results”

#“You can use generators in a similar way as range objects. They perform some operation on data in chunks as requested. They pause their state in between calls. This means that you can store variables that are needed to calculate output, and they are accessed every time the generator is called.
#To write a generator function, use the yield keyword rather than a return statement.”


def count():
    n = 0
    while True:
        n += 1
        yield n

counter = count()
print(counter)
print(next(counter))
print(next(counter))
print(next(counter))


def fib():
    first = 0
    last = 1
    while True:
        first, last = last, first + last
        yield first

f = fib()

for x in f: #X assume o papel da variavel em yield, como a primeira vez que first aparece como yield first=1, logo comecara por 1
    print(x) 
    if x > 12:
        break

#Generators
#“We can use generator comprehensions to create one-line generators. They are created using a syntax similar to list comprehensions, but parentheses are used rather than square brackets:”

hundred_array = [x for x in range(100)]
gen_o_nums = (x for x in range(100))


print(hundred_array)
print(gen_o_nums)

import sys

print(sys.getsizeof(hundred_array), sys.getsizeof(gen_o_nums))

print(sum(x*x for x in range(10)))

class Account:

    def __init__(self, name : str, value : float):
        self.name = name
        self.value = value

class Bank:

    def __init__(self):
        self.accounts = []

    def add_account(self, name : str, value : float):
        account = Account(name, value)
        self.accounts.append(account)

    def money_sum(self):
        return sum(account.value for account in self.accounts)

banco = Bank()

banco.add_account("Tulio",300)
banco.add_account("Tulia",300)
banco.add_account("Tulie",300)
banco.add_account("Tulii",300)
banco.add_account("Tuliu",300)

print(banco.money_sum())

