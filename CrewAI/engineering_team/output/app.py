import gradio as gr
from accounts import Account, get_share_price

# Initialize a single account for the demo
user_account = None

def create_account(account_id, initial_deposit):
    global user_account
    try:
        initial_deposit = float(initial_deposit)
        if initial_deposit <= 0:
            return "Initial deposit must be greater than 0"
        user_account = Account(account_id, initial_deposit)
        return f"Account {account_id} created with ${initial_deposit:.2f}"
    except ValueError:
        return "Please enter a valid number for initial deposit"

def deposit_funds(amount):
    global user_account
    if user_account is None:
        return "Please create an account first"
    try:
        amount = float(amount)
        if amount <= 0:
            return "Deposit amount must be greater than 0"
        user_account.deposit(amount)
        return f"${amount:.2f} deposited. New balance: ${user_account.balance:.2f}"
    except ValueError:
        return "Please enter a valid number for deposit"

def withdraw_funds(amount):
    global user_account
    if user_account is None:
        return "Please create an account first"
    try:
        amount = float(amount)
        if amount <= 0:
            return "Withdrawal amount must be greater than 0"
        if user_account.withdraw(amount):
            return f"${amount:.2f} withdrawn. New balance: ${user_account.balance:.2f}"
        else:
            return "Insufficient funds for withdrawal"
    except ValueError:
        return "Please enter a valid number for withdrawal"

def buy_shares(symbol, quantity):
    global user_account
    if user_account is None:
        return "Please create an account first"
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return "Quantity must be greater than 0"
        
        # Check if symbol is valid
        price = get_share_price(symbol)
        if price == 0.0:
            return f"Invalid symbol: {symbol}. Available symbols: AAPL, TSLA, GOOGL"
        
        if user_account.buy_shares(symbol, quantity):
            return f"Bought {quantity} shares of {symbol} at ${price:.2f} each. New balance: ${user_account.balance:.2f}"
        else:
            return f"Insufficient funds to buy {quantity} shares of {symbol} at ${price:.2f} each"
    except ValueError:
        return "Please enter a valid number for quantity"

def sell_shares(symbol, quantity):
    global user_account
    if user_account is None:
        return "Please create an account first"
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return "Quantity must be greater than 0"
        
        if user_account.sell_shares(symbol, quantity):
            price = get_share_price(symbol)
            return f"Sold {quantity} shares of {symbol} at ${price:.2f} each. New balance: ${user_account.balance:.2f}"
        else:
            return f"You don't have {quantity} shares of {symbol} to sell"
    except ValueError:
        return "Please enter a valid number for quantity"

def get_portfolio():
    global user_account
    if user_account is None:
        return "Please create an account first"
    
    portfolio_text = f"Account ID: {user_account.account_id}\n"
    portfolio_text += f"Cash Balance: ${user_account.balance:.2f}\n\n"
    portfolio_text += "Holdings:\n"
    
    if not user_account.holdings:
        portfolio_text += "No shares currently owned\n"
    else:
        portfolio_text += "Symbol | Quantity | Price | Value\n"
        portfolio_text += "------|----------|-------|------\n"
        total_holdings_value = 0
        for symbol, quantity in user_account.holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            total_holdings_value += value
            portfolio_text += f"{symbol} | {quantity} | ${price:.2f} | ${value:.2f}\n"
        
        portfolio_text += f"\nTotal Holdings Value: ${total_holdings_value:.2f}\n"
    
    portfolio_text += f"Total Portfolio Value: ${user_account.get_portfolio_value():.2f}\n"
    portfolio_text += f"Profit/Loss: ${user_account.get_profit_loss():.2f}\n"
    
    return portfolio_text

def get_transactions():
    global user_account
    if user_account is None:
        return "Please create an account first"
    
    if not user_account.transactions:
        return "No transactions yet"
    
    transaction_text = "Transaction History:\n\n"
    for i, transaction in enumerate(user_account.transactions, 1):
        transaction_text += f"Transaction {i}:\n"
        transaction_text += f"Type: {transaction['type']}\n"
        
        if transaction['type'] == 'deposit' or transaction['type'] == 'withdrawal':
            transaction_text += f"Amount: ${transaction['amount']:.2f}\n"
        elif transaction['type'] == 'buy' or transaction['type'] == 'sell':
            transaction_text += f"Symbol: {transaction['symbol']}\n"
            transaction_text += f"Quantity: {transaction['quantity']}\n"
            transaction_text += f"Price: ${transaction['price']:.2f}\n"
            transaction_text += f"Total: ${transaction['price'] * transaction['quantity']:.2f}\n"
        
        transaction_text += "\n"
    
    return transaction_text

def get_available_symbols():
    return "Available symbols: AAPL ($150.00), TSLA ($800.00), GOOGL ($2500.00)"

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        gr.Markdown("## Create Account")
        with gr.Row():
            account_id = gr.Textbox(label="Account ID")
            initial_deposit = gr.Textbox(label="Initial Deposit ($)")
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_btn.click(create_account, inputs=[account_id, initial_deposit], outputs=create_output)
        
        gr.Markdown("## Deposit & Withdraw")
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Textbox(label="Deposit Amount ($)")
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
            
            with gr.Column():
                withdraw_amount = gr.Textbox(label="Withdraw Amount ($)")
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
        
        deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
        withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Trading"):
        gr.Markdown("## Buy & Sell Shares")
        symbols_info = gr.Markdown(get_available_symbols())
        
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Textbox(label="Symbol to Buy (e.g., AAPL)")
                buy_quantity = gr.Textbox(label="Quantity")
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Result")
            
            with gr.Column():
                sell_symbol = gr.Textbox(label="Symbol to Sell (e.g., AAPL)")
                sell_quantity = gr.Textbox(label="Quantity")
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Result")
        
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        gr.Markdown("## Portfolio Overview")
        portfolio_btn = gr.Button("Get Portfolio Summary")
        portfolio_output = gr.Textbox(label="Portfolio Summary", lines=15)
        portfolio_btn.click(get_portfolio, inputs=[], outputs=portfolio_output)
    
    with gr.Tab("Transactions"):
        gr.Markdown("## Transaction History")
        transactions_btn = gr.Button("View Transaction History")
        transactions_output = gr.Textbox(label="Transactions", lines=20)
        transactions_btn.click(get_transactions, inputs=[], outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()