import unittest

from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('12345', 1000.0)

    def test_initialization(self):
        self.assertEqual(self.account.account_id, '12345')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
        self.assertEqual(self.account.initial_deposit, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'deposit', 'amount': 500.0})

    def test_withdraw_success(self):
        result = self.account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'withdrawal', 'amount': 200.0})

    def test_withdraw_failure(self):
        result = self.account.withdraw(1200.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 250.0)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'buy')

    def test_buy_shares_failure(self):
        result = self.account.buy_shares('GOOGL', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertNotIn('GOOGL', self.account.holdings)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 5)
        result = self.account.sell_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'sell')

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 1)
        self.assertFalse(result)

    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 5)
        portfolio_value = self.account.get_portfolio_value()
        self.assertEqual(portfolio_value, 1000.0)

    def test_get_profit_loss(self):
        self.account.buy_shares('AAPL', 5)
        profit_loss = self.account.get_profit_loss()
        self.assertEqual(profit_loss, 0.0)

    def test_get_holdings(self):
        self.account.buy_shares('TSLA', 2)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'TSLA': 2})

    def test_get_transaction_history(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        self.account.buy_shares('AAPL', 3)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[1]['type'], 'withdrawal')
        self.assertEqual(transactions[2]['type'], 'buy')

class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price(self):
        self.assertEqual(get_share_price('AAPL'), 150.0)
        self.assertEqual(get_share_price('TSLA'), 800.0)
        self.assertEqual(get_share_price('GOOGL'), 2500.0)
        self.assertEqual(get_share_price('UNKNOWN'), 0.0)

if __name__ == '__main__':
    unittest.main()