import time
from web3 import Web3, HTTPProvider

import blockchain.settings as settings
import threading

contract_address     = Web3.toChecksumAddress(settings.CONTRACT_ADDRESS)
wallet_private_key   = settings.PRIVATE_KEY
wallet_address       = Web3.toChecksumAddress(settings.WALLET_ADDRESS)
INFURA_URL           = settings.INFURA_URL
contract_abi = settings.CONTRACT_ABI

w3 = Web3(HTTPProvider(INFURA_URL))
w3.eth.enable_unaudited_features()

contract = w3.eth.contract(address = contract_address, abi = contract_abi)

def addVoter(address):
    print("async call begin - addvoter")
    nonce = w3.eth.getTransactionCount(wallet_address) 
    print(nonce)
    txn_dict = contract.functions.addVoter(address).buildTransaction({
        'chainId': 3,
        'gas': 3000000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.getTransactionReceipt(result)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = w3.eth.getTransactionReceipt(result)
        print(tx_receipt)
        count += 1
    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}
    return {'status': 'added', 'processed_receipt': tx_receipt}

def add_voter_async(address):
    t = threading.Thread(target = addVoter, args=(address,))
    t.start()
