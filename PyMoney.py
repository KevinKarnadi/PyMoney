import sys

class Record:
    """Represent a record."""
    def __init__(self, cat, dsc, amt):
        '''Record initialization'''
        self._category = cat
        self._desc = dsc
        self._amount = int(amt)

    @property
    def category(self):
        '''Return record category'''
        return self._category
    
    @property
    def desc(self):
        '''Return record description'''
        return self._desc
    
    @property
    def amount(self):
        '''Return record amount'''
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        '''Records initialization'''
        try:
            with open("records.txt", "r") as fh:
                try:
                    money = int(fh.readline())
                except ValueError:    # Invalid format of initial money
                    print("Invalid format of initial money in 'records.txt' (must be int).")
                    print("Money set to 0.")
                    money = 0
                lines = fh.readlines()
                records = [l[:-1] for l in lines]
                try:
                    L = [Record(it.split()[0], it.split()[1], int(it.split()[2])) for it in records]    # Create a [('category', 'desc', amt), ...] data structure
                    records = L
                except:    # Invalid format of records
                    print("Invalid format of records in 'records.txt' (must be '[str] [str] [int]').")
                    print("Records set to an empty list.")
                    records = []
        except FileNotFoundError:    # 1st time running the program
            try:
                money = int(input("How much money do you have? "))
            except ValueError:    # Invalid type of input for initial money
                money = 0
                print("Invalid value for initial money.")
                print("Initial money set to 0.")
            records = []
        else:
            print("Welcome back!")
        self._initial_money = money
        self._records = records

    def add(self, record, categories):
        '''Add new record'''
        try:
            cat, dsc, amt = record.split()
            if categories.is_category_valid(cat):
                try:
                    self._records.append(Record(cat, dsc, int(amt)))
                except ValueError:    # Invalid input for amount
                    print("Invalid value for amount (must be int).")
                    print("Failed to add a record.")
            else:   # Invalid category
                print("The specified category is not in the category list.")
                print('You can check the category list by command "view categories".')
                print("Failed to add a record.")
        except ValueError:    # Invalid format of input
            print("The format of the record is invalid. (must be '[str] [str] [int]').")
            print("Failed to add a record.")

    def view(self):
        '''View record list'''
        expenses = []
        print("Here's your expense and income records:")
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        for it in self._records:
            print(f"{it.category:15s} {it.desc:20s} {it.amount:6d}")
            expenses.append(it.amount)
        money = self._initial_money + sum(expenses)    # Update value of money by total expenses
        print("===========================================")
        print(f"Now you have {money} dollars.")

    def delete(self, del_record):
        '''Delete a record'''
        n = 0
        i = 0
        idx = 0
        for it in self._records:
            if it.desc == del_record:
                n += 1
                idx = i
            i += 1
        if n == 1:
            del self._records[idx]
        elif n > 1:
            print(f'More than 1 items with description "{del_record}" found.')
            print("Please specify which record to delete based on index:")
            print("Index Category        Description          Amount")
            print("===== =============== ==================== ======")
            i = 1
            for it in self._records:
                print(f"{i:5d} {it.category:15s} {it.desc:20s} {it.amount:6d}")
                i += 1
            print("=================================================")
            try:
                idx = int(input("Please specify which record to delete based on index: "))
                try:
                    del self._records[idx-1]
                except IndexError:    # Item does not exist (index is out of bounds)
                    print("The specified record does not exist.")
            except ValueError:    # Invalid input for index
                print("Invalid value for index.")

    def find(self, subcategories):
        '''Find record with a certain category'''
        items = filter(lambda x : x.category in subcategories, self._records)
        total = 0
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        for it in items:
            print(f"{it.category:15s} {it.desc:20s} {it.amount:6d}")
            total += int(it.amount)
        print("===========================================")
        print(f"The total amount above is {total}.")

    def save(self):
        '''Save records on a txt file'''
        with open("records.txt", "w") as fh:
            fh.write(str(self._initial_money))
            fh.write("\n")
            L = [it.category+" "+it.desc+" "+str(it.amount)+"\n" for it in self._records]    # Save record in a '[category] [desc] [amount]\n' format
            fh.writelines(L)
    
class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        '''Categories initialization'''
        L = ['expense',
                ['food',
                    ['meal',
                     'snack',
                     'drink'],
                'transportation',
                    ['bus',
                     'railway']],
             'income',
                ['salary',
                 'bonus']]
        self._categories = L

    def view(self, L=[0], level=-1):
        '''View category list'''
        if L == [0]:
            L = self._categories
        if L == None:
            return
        if type(L) in {list, tuple}:
            for child in L:
                self.view(child, level+1)
        else:
            print("  "*level, end='')
            print(f"- {L}")

    def is_category_valid(self, cat, L=[0]):
        '''Check if a category exists or not'''
        if L == [0]:
            L = self._categories
        for it in L:
            if type(it) in {list, tuple}:
                if self.is_category_valid(cat, it):
                    return True
            else:
                if it == cat:
                    return True
        return False

    def find_subcategories(self, category):
        '''Find subcategories of a certain category'''
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list and found == False:
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found == True:
                    yield categories

        return [x for x in find_subcategories_gen(category, self._categories)]

categories = Categories()
records = Records()
 
while True:
    command = input("\nWhat do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == 'add':
        record = input("Add an expense or income record with category, description, and amount:\n")
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? ")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input("Which category do you want to find? ")
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")