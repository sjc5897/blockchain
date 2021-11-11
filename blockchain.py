"""
This project is used in an experiment for my CSEC-604 class.
The experiment is the implementation of Blockchain using different Hashing Algorithms
and testing their performance via computation time, cpu monitoring, and more

:author       Stephen Cook <sjc5897@rit.edu>
:language      Python 3
:date_created  10/29/21
:last_edit     10/29/21
"""
import time
import json
from hash import *

"""
This is the Block class. In blockchain, blocks are the atomic units of the system
Blocks contain various information, such as block id, transaction information, timestamps,
previous_hashing, and a nonce (Number used once).
These blocks are hashed and chained in the block chain
"""


class Block:
    """
    Initializes a single block, an atomic unit within a blockchain
    :param index:           integer,    Representing the blocks index in the blockchain
    :param transactions:    string,     The data we wish to store, in this version it is just any string
    :param timestamp:       time,       The time stamp of the transaction
    :param previous_hash:   string,     The string of the previous hash in the block chain
    :param hasher:          hasher,     The hash strategy that used
    :param nonce:           integer,    A nonce is a number used once, it is used to help sign our blocks
    """

    def __init__(self, index, transactions, timestamp, previous_hash, hasher, nonce=0 ):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hasher = hasher

    """
    Converts the block to json and computes its hash
    :returns:   the block as a hash
    """

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


"""
This class represents the blockchain. 
It contains the methods for creating and proving new blocks as well as adding them to the chain
"""


class Blockchain:
    """
    Initializes the blockchain object
    :param difficulty:  an integer representing the difficulty of the signature,
    simply the number of 0s that need to be prepended to the hash function
    """

    def __init__(self, difficulty):
        self.chain = []
        self.unconfirmed_transactions = []
        self.difficulty = difficulty
        self.create_genesis_block()

    """
    Creates the genesis (initial) block in the block chain 
    """

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    """
    quick property definition for the last block in our chain
    :returns:   The last block in the blockchain
    """
    @property
    def last_block(self):
        return self.chain[-1]

    """
    proof_of_work is a key function to blockchaining, it ensures that the block is "signed" with our difficulty,
    using a nonce. this system makes it far harder to difficult to modify previous blocks 
    :param block:   the block we wish to prove
    :returns:       A valid worked block hash
    """

    def proof_of_work(self, block):
        # init the block nonce and hash
        block.nonce = 0
        computed_hash = block.compute_hash()
        # continue calculating the block hash with a new nonce until the block hash matches our desired signature
        while not computed_hash.startswith('0'*self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        # when it does retunr the hash
        return computed_hash

    """
    A method used to validate the block
    checks that the hash starts with our signature (prepended with a number of 0) AND
    that the block is configured to correctly compute to its current hash.
    :param block:       this is the block we are checking
    :param block_hash:  the hash we calculated as valid
    :returns:           Boolean representing if the proof is valid 
    """

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith('0' * self.difficulty) and block_hash == block.compute_hash()

    """
    Adds a transaction to the transaction listing
    :param transaction:     Some discrete transaction
    """
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    """
    Adds a block to the chain after checking the blocks validity
    """

    def add_block(self, block, proof):
        # get the hash of the last block
        previous_hash = self.last_block.hash

        # confirm that the last blocks hash matches the one we have set in the block
        if previous_hash != block.previous_hash:
            return False

        # check that the proof is valid
        if not self.is_valid_proof(block, proof):
            return False

        # add the block
        block.hash = proof
        self.chain.append(block)
        return True

    """
    The mine function is the process of adding unconfirmed_transactions to the block chain
    """

    def mine(self):
        # check if new transactions exist
        if not self.unconfirmed_transactions:
            return False

        # if yes, get the last block
        last_block = self.last_block

        # create our new block
        new_block = Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash
                          )

        # calculate our proof of work
        proof = self.proof_of_work(new_block)

        # add the block to the chain
        self.add_block(new_block,proof)

        # clear the transaction log
        self.unconfirmed_transactions = []

        # return the new blocks index
        return new_block.index

    def get_chain(self):
        chain_data = []
        for block in self.chain:
            chain_data.append(block.__dict__)
        return json.dumps(chain_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Welcome to my basic blockchain demo")
    difficulty = input("To initialize the blockchain, please provide an integer difficulty (1-5): ")
    blockchain = Blockchain(int(difficulty))
    transaction = ""
    while transaction != "quit":
        transaction = input("Input Transaction Message :")
        if transaction == "mine":
            blockchain.mine()
        else:
            blockchain.add_new_transaction(transaction)
    print(blockchain.get_chain())
