class Category:
	def __init__(self, name):
		self.ledger = []
		self.balance = 0
		self.name = name


	def deposit(self, amount, *args):
		if len(args) == 0:
			description = ""
		else:
			description = args[0]

		self.ledger.append({"amount": amount, "description": description})
		self.balance += amount


	def withdraw(self, amount, *args):
		if self.check_funds(amount):
			if len(args) == 0:
				description = ""
			else:
				description = args[0]
			
			self.deposit(-amount, description)
			return True
		else:
			return False

	
	def get_balance(self):
		return self.balance
		

	def transfer(self, amount, budget):
		if self.check_funds(amount):
			self.withdraw(amount, f"Transfer to {budget.name}")
			budget.deposit(amount, f"Transfer from {self.name}")
			return True
		else:
			return False


	def check_funds(self, amount):
		if self.balance >= amount:
			return True
		else:
			return False 


	def __str__(self):
		LEN = 30
		stringList = [self.name.center(LEN, "*")]

		for transaction in self.ledger:
			amountString = "{:.2f}".format(transaction['amount'])
			description = transaction['description'].ljust(LEN)[:(LEN-len(amountString)- 1)] + " "
			stringList.append(description + amountString)

		stringList.append(f"Total: {self.balance}")
		
		return "\n".join(stringList)


def create_spend_chart(categories):
	title = "Percentage spent by category"
	yAxis = "|"
	nCategories = len(categories)
	LEN = (3 + 1 + 3 * nCategories)

	response = [title]
	expenses = []
	
	for category in categories:
		categoryExpenses = 0
		for transaction in category.ledger:		
			if float(transaction['amount']) < 0:
				categoryExpenses += -float(transaction['amount'])

		expenses.append({
			"name": category.name,
			"expenses": categoryExpenses,
			"percentage": 0})
	
	# Calculate percentages
	fullAmount = 0

	for expense in expenses:
		fullAmount += expense['expenses']

	
	for expense in expenses:
		expense['percentage'] = 100 * expense["expenses"] // fullAmount


	for lineCounter in range(11):
		value = 100 - lineCounter * 10
		valueString = str(value).rjust(3)
		graph = ""
		
		for expense in expenses:
			if value <= expense['percentage']:
				graph += " o "
			else:
				graph += "   "
			
		graph += " "

		string = "".join([valueString, yAxis, graph])

		response.append(string)

	
	# X-Axis
	response.append(f"{'---'*nCategories}".rjust(LEN) + "-")

	# X-values
	heigh = 0

	for expense in expenses:
		if len(expense['name']) > heigh:
			heigh = len(expense['name'])

	categoriesNames = []
	for category in categories:
		categoriesNames.append(category.name.ljust(heigh))

	for line in range(heigh):
		string = " " * (3 + 1)
		for i in range(nCategories):
			string += " " + categoriesNames[i][line] + " "

		string += " "

		response.append(string)

	return "\n".join(response)
	