def get_share_price(symbol):
    # Test implementation
    prices = {"AAPL": 150.0, "TSLA": 800.0, "GOOGL": 2500.0}
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, account_id: str, initial_deposit: float):
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float):
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount})

    def withdraw(self, amount: float) -> bool:
        if self.balance - amount >= 0:
            self.balance -= amount
            self.transactions.append({"type": "withdrawal", "amount": amount})
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        total_cost = price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.transactions.append({"type": "buy", "symbol": symbol, "quantity": quantity, "price": price})
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = get_share_price(symbol)
            total_value = price * quantity
            self.balance += total_value
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append({"type": "sell", "symbol": symbol, "quantity": quantity, "price": price})
            return True
        return False

    def get_portfolio_value(self) -> float:
        portfolio_value = self.balance
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            portfolio_value += price * quantity
        return portfolio_value

    def get_profit_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transaction_history(self) -> list:
        return self.transactions