class Trade:
    __take_profits = [
        {
            "status": False,
            "percent": 2,
            "amount": 25
        },
        {
            "status": False,
            "percent": 5,
            "amount": 25
        },
        {
            "status": False,
            "percent": 7,
            "amount": 25
        },
        {
            "status": False,
            "percent": 10,
            "amount": 13
        },
        {
            "status": False,
            "percent": 12,
            "amount": 12
        },
    ]
    __commission = 0.019
    __entry_price = 0.0
    __position_size = 0.0

    use_tp = False
    in_position = False
    balance = 0.0
    side = 'long'

    def reset(self, balance, use_tp=False):
        self.balance = balance
        self.use_tp = use_tp
        self.in_position = False
        self.__entry_price = 0.0
        self.__position_size = 0.0

    def __reset_take_profits(self):
        for tp in range(0, len(self.__take_profits)):
            self.__take_profits[tp]["status"] = False

    def __get_commission(self, size, price):
        return round((size * price) / 100 * self.__commission, 2)

    def __take_profit_price(self, percent):
        return self.__entry_price + (self.__entry_price / 100 * percent) \
            if self.side == 'long' else self.__entry_price - (self.__entry_price / 100 * percent)

    def __change_balance_calculation(self, price, size):
        if self.side == 'long':
            return (price * size) - (self.__entry_price * size)
        return (self.__entry_price * size) - (price * size)

    def __next_take_profit(self):
        unused_take_profits = [tp for tp in self.__take_profits if tp["status"] is not True]
        if len(unused_take_profits) == 0:
            return None
        return unused_take_profits[0]

    def __actual_take_profit_price(self):
        unused_take_profit = self.__next_take_profit()
        if unused_take_profit is None:
            return 0.0

        return self.__take_profit_price(unused_take_profit['Percent'])

    def new_position(self, entry_price, side, position_size):
        self.__entry_price = entry_price
        self.__position_size = position_size
        self.side = side
        self.in_position = True
        self.balance -= self.__get_commission(position_size, entry_price)

    def close_position(self, price):
        self.balance += self.__change_balance_calculation(price=price, size=self.__position_size)
        self.balance -= self.__get_commission(size=self.__position_size, price=price)
        self.in_position = False
        self.__reset_take_profits()
        self.__entry_price = 0.0
        self.__position_size = 0.0

    def in_long_position(self):
        return self.in_position and self.side == 'long'

    def in_short_position(self):
        return self.in_position and self.side == 'short'

    def should_close_by_tp(self, price):
        if self.side == 'long':
            return self.use_tp and price >= self.__actual_take_profit_price()

        return self.use_tp and price <= self.__actual_take_profit_price()

    def close_by_tp(self, price):
        next_tp = self.__next_take_profit()
        amount_to_sell = round((self.__position_size / 100) * next_tp["amount"])
        self.__position_size -= amount_to_sell
        self.balance += self.__change_balance_calculation(price=price, size=amount_to_sell)
        self.balance -= self.__get_commission(size=amount_to_sell, price=price)
        next_tp["status"] = True
