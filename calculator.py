class Calculator:
    # overall class so multiple rental properties can be added and held in memory until user is done

    def __init__(self):
        self.properties = []

    def initialize(self):
        # runner loop that tracks total finalized properties

        question = ''
        thing = ''
        amount = ''
        while True:
            rental = None
            question = input('Would you like to ADD a property, SHOW all calculated properties or EXIT the program? ').lower()
            if question == 'exit': break
            elif question == 'add':
                rental = self.add_property()
                if rental == 'return': continue
                if rental.income_ask() == 'return': continue
                if rental.expenses_ask() == 'return': continue
                if rental.down_ask() == 'return': continue
                if rental.calculate() == 'error': continue
                if rental.income != {} and rental.down_payment != {}:
                    self.properties.append(rental)
                    print(f'Property "{rental.name}" added to your list of properties.')
                else: print('There was an error in one of your submissions. Please try again. ')
            elif question == 'show': self.show_props()
            elif question == 'exit': break
            else: print('Invalid input, please only enter ADD, SHOW, or EXIT please. ')
        self.exit()

    def add_property(self):
        # builds an instance of a rental property and assigns it a name

        question = input('Please give a name to this property or type RETURN to return to initial menu. ')
        if question.lower() == 'return': return 'return'
        else: return Rental(question)

    def show_props(self):
        # shows current properties that have been finalized

        if self.properties:
            print('Your current properties consist of:')
            print('-----------------------------------')
            for each in self.properties:
                print(f'{each.name}')
                print('INCOMES:')
                for stuff, quant in each.income.items():
                    print(f'{stuff.title()}: ${quant:,}')
                print('')
                print('EXPENSES:')
                for stuff, quant in each.expenses.items():
                    print(f'{stuff.title()}: ${quant:,}')
                print('')
                print('DOWN PAYMENTS')
                for stuff, quant in each.down_payment.items():
                    print(f'{stuff.title()}: ${quant:,}')
                print('')
                print(f'YEARLY CASH FLOW: ${each.cash_flow:,}')
                print(f'CASH ON CASH ROI: {each.roi}%')
                print('-----------------------------------')
        else: print('You haven\'t added any properties yet, ya goofball!')
        
    def exit(self):
        # exit code that runs when user is done, terminates the overall loop and prints a finalized list of properties

        if self.properties:
            print('Your finalized list of properties consist of:')
            print('-----------------------------------')
            for each in self.properties:
                print(f'{each.name}')
                print('INCOMES:')
                for stuff, quant in each.income.items():
                    print(f'{stuff.title()}: ${quant:,}')
                print('')
                print('EXPENSES:')
                for stuff, quant in each.expenses.items():
                    print(f'{stuff.title()}: ${quant:,}')
                print('')
                print('DOWN PAYMENTS')
                for stuff, quant in each.down_payment.items():
                    print(f'{stuff.title()}: ${quant:,}')
                print('')
                print(f'YEARLY CASH FLOW: ${each.cash_flow:,}')
                print(f'CASH ON CASH ROI: {each.roi}%')
                print('-----------------------------------')
        else: print('You never added any properties! Indecisive, huh?')

class Rental:
    # class that holds all information about rental properties

    def __init__(self, name):
        self.name = name
        self.income = {}
        self.expenses = {}
        self.down_payment = {}
        self.cash_flow = 0
        self.roi = 0

    def income_ask(self):
        # Ask for various income methods and assign them to the income dictionary, looping until incomes are done

        while True:
            thing = input('Please enter what type of monthly income(s) you\'ll be recieving on this property (rent, storage, etc) or type SUBMIT if done. Type RETURN to return to initial menu. ').lower()
            if thing == 'return': return 'return'
            if thing == 'submit': return
            try:
                if isinstance(int(thing), int) or isinstance(float(thing), float):
                    print('Woah there killer, I think you got too excited and skipped a step. Gotta give a name first. Let\'s give that another whirl.')
            except:
                try:
                    amount = (input(f'How much are you receiving for {thing} every month? Please answer only using numerical digits, omit any dollar signs. ')).lower()
                    if amount == 'return': return 'return'
                    amount = int(amount)
                    self.income[thing] = amount
                except ValueError: print('Come on now, just give it to me in good old fashion digits. Let\'s take it from the top.')
            finally:
                continue

    def expenses_ask(self):
        # Ask for various expenses and assign them to the expenses dictionary, looping until expenses are done

        while True:
            thing = input('Please enter what type of monthly expenses you\'ll be paying on this property (taxes, HOA fees, etc) or type SUBMIT if done. Type RETURN to return to initial menu. ').lower()
            if thing == 'return': return 'return'
            if thing == 'submit': return
            try:
                if isinstance(int(thing), int) or isinstance(float(thing), float):
                    print('Woah there killer, I think you got too excited and skipped a step. Gotta give a name first. Let\'s give that another whirl.')
            except:
                try:
                    amount = (input(f'How much are you paying in {thing} every month? Please answer only using numerical digits, omit any dollar signs. ')).lower()
                    if amount == 'return': return 'return'
                    amount = int(amount)
                    self.expenses[thing] = amount
                except ValueError: print('Come on now, just give it to me in good old fashion digits. Let\'s take it from the top.')
            finally:
                continue
    
    def down_ask(self):
        # Ask for down payment expenses and assign them to the down payment dictionary, looping until done

        while True:
            thing = input('Please enter what type of down payments you\'ve made on this property (down payment, closing fees, etc) or type SUBMIT if done. Type RETURN to return to initial menu. ').lower()
            if thing == 'return': return 'return'
            if thing == 'submit': return
            try:
                if isinstance(int(thing), int) or isinstance(float(thing), float):
                    print('Woah there killer, I think you got too excited and skipped a step. Gotta give a name first. Let\'s give that another whirl.')
            except:
                try:
                    amount = (input(f'How much are you did you pay for a {thing}? Please answer only using numerical digits, omit any dollar signs. ')).lower()
                    if amount == 'return': return 'return'
                    amount = int(amount)
                    self.down_payment[thing] = amount
                except ValueError: print('Come on now, just give it to me in good old fashion digits. Let\'s take it from the top.')
            finally:
                continue

    def calculate(self):
        # Calculates annual cash flow and ROI, and then assigns those values to the rental's appropriate attributes

        self.cash_flow = (sum(self.income.values()) - sum(self.expenses.values()))*12
        try:
            self.roi = round((self.cash_flow / sum(self.down_payment.values()))*100, 2)
        except ZeroDivisionError: 
            print('Huh. You recieved the property for free? Well then buddy, I can\'t give you a return on investment, since I can\'t divide by zero.')
            return 'error'

test = Calculator()
test.initialize()