import hashlib
import time


class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash # предыдущий 
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Создание хэша блока на основе его данных и предыдущего хэша
        return hashlib.sha256(
            f"{self.timestamp}{self.data}{self.previous_hash}".encode("utf-8")
        ).hexdigest()


class Blockchain:
    def __init__(self):
        # Инициализация цепочки блоков с генезис-блоком и списка транзакций
        self.chain = []
        self.genesis_block = Block(time.time(), "Genesis block", "0") # в начале не было ничего, потом свет) (первый блок)
        self.chain.append(self.genesis_block)
        self.transactions = []

    def add_block(self, transaction):
        # Добавление транзакции в блокчейн и создание нового блока
        self.transactions.append(transaction)
        new_block = Block(time.time(), transaction, self.chain[-1].hash)
        self.chain.append(new_block)

    def get_balance(self, address):
        # Вычисление баланса адреса на основе транзакций в блокчейне
        balance = 0
        for transaction in self.transactions:
            if transaction['sender'] == address:
                balance -= transaction['amount']
            if transaction['receiver'] == address:
                balance += transaction['amount']
        return balance


def main():
    blockchain = Blockchain()

    # Создание транзакций
    transaction1 = {
        "sender": "0x1234567890abcdef",
        "receiver": "0xdeadbeefcafebabe",
        "amount": 100
    }
    transaction2 = {
        "sender": "0xdeadbeefcafebabe",
        "receiver": "0x9876543210fedcba",
        "amount": 50
    }

    # Добавление транзакций в блокчейн
    blockchain.add_block(transaction1)
    # Проверка баланса адресов
    balance = blockchain.get_balance("0x1234567890abcdef")
    print(balance)  # -100
    balance = blockchain.get_balance("0xdeadbeefcafebabe")
    print(balance)  # 100

    blockchain.add_block(transaction2)
    balance = blockchain.get_balance("0xdeadbeefcafebabe")
    print(balance)  # 50
    balance = blockchain.get_balance("0x9876543210fedcba")
    print(balance)  # 50



main()