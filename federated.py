# Simple implementation of blockchain-based federated learning.

from web3 import Web3
from solc import compile_standard
import json
import hashlib
import random

rpc_url = 'http://127.0.0.1:8545'
fl_address = ''
fl_abi = ''

def deploy_smart_contract(w3_instance, sc_filename, sc_classname):
    # Solidity source code
    # compile_standard was the only compatible way of compiling solidity source
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            sc_filename: {
                 # somehow this must be an absolute path
                "urls": ["/home/guntur/simple-bc-fl/" + sc_filename]
            }
        },
        "settings": {
            'evmVersion': 'shanghai',
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode"
                        , "evm.bytecode.sourceMap"
                    ]
                }
            }
        }
    },
    # somehow this must be an absolute path
    allow_paths= "/home/guntur/simple-bc-fl/")

    # get bytecode and get abi
    bytecode = compiled_sol['contracts'][sc_filename][sc_classname]['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts'][sc_filename][sc_classname]['metadata'])['output']['abi']

    Contract = w3_instance.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({'from': w3_instance.eth.defaultAccount})
    tx_receipt = w3_instance.eth.get_transaction_receipt(tx_hash)

    # get the gas needed to deploy the contract
    # print('Contract: {}, Gas used: {}.'.format(sc_classname, tx_receipt['gasUsed']))

    return (tx_hash, tx_receipt, abi)

def main():
    # the Web3 instance
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # print(w3.eth.defaultAccount)

    # compile and deploy the contract; then get contact ABI and addresses
    (ctr_hash, ctr_receipt, ctr_abi) = deploy_smart_contract(w3, 'federated.sol', 'SimpleFL')
    fl_address = w3.eth.get_transaction_receipt(ctr_hash)['contractAddress']
    fl_abi = ctr_abi

    # create federated learning contract object
    fl_contract = w3.eth.contract(
        address=fl_address,
        abi=fl_abi
    )

    # create some random federated learning details
    client_id = w3.eth.defaultAccount
    compute_id = 'compute1'
    model_hash = hashlib.md5(client_id.encode('utf-8')).hexdigest()
    compute_round = random.randint(0, 9)

    # insert the details to the blockchain
    tx_hash = fl_contract.functions.submitModel(
            compute_id.encode('utf-8'),
            model_hash.encode('utf-8'),
            int(compute_round)
        ).transact({'from': client_id})
    tx_receipt = w3.eth.get_transaction_receipt(tx_hash)

    # the details on chain
    print('Model stored on-chain. Transaction ID: ', tx_receipt['transactionHash'].hex())

if __name__ == "__main__":
    main()
