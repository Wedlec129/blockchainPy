from fastapi import FastAPI
import hashlib
from fastapi import Request
from time import time
from typing import List
# uvicorn blockchain:app --reload --port 8000      
class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            f"{self.timestamp}{self.data}{self.previous_hash}".encode("utf-8")
        ).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.genesis_block = Block(time(), "Genesis block", "0")
        self.chain.append(self.genesis_block)
        self.transactions = []

    def add_block(self, transaction):
        self.transactions.append(transaction)
        new_block = Block(time(), transaction, self.chain[-1].hash)
        self.chain.append(new_block)

    def get_balance(self, address):
        balance = 0
        for transaction in self.transactions:
            if transaction['sender'] == address:
                balance -= transaction['amount']
            if transaction['receiver'] == address:
                balance += transaction['amount']
        return balance

    def display_chain(self):
        chain_info = []
        for block in self.chain:
            block_info = {
                'timestamp': block.timestamp,
                'data': block.data,
                'previous_hash': block.previous_hash,
                'hash': block.hash
            }
            chain_info.append(block_info)
        return chain_info
# Создание экземпляра FastAPI
app = FastAPI()

# Инициализация блокчейна
blockchain = Blockchain()

@app.get('/mine')
async def mine():
    """
    Создание нового блока (майнинг) в блокчейне.
    """
    return {"message": "Mining a new Block"}

@app.post('/transactions/new')
async def new_transaction(request: Request):
    """
    Добавление новой транзакции в блокчейн.
    Ожидает данные о транзакции в теле POST запроса.
    """
    data = await request.json()
    blockchain.add_block(data)
    return {"message": "Transaction added to the block"}

@app.get('/chain')
async def full_chain():
    """
    Получение всей цепочки блоков.
    """
    chain_info = blockchain.display_chain()
    return chain_info

@app.get('/balance/{address}')
async def get_balance(address: str):
    """
    Получение баланса для указанного адреса.
    """
    balance = blockchain.get_balance(address)
    return {"address": address, "balance": balance}