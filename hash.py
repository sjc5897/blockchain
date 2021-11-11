"""
This file is used to create the hashing strategy pattern used in the testing of blockchain

:author       Stephen Cook <sjc5897@rit.edu>
:language      Python 3
:date_created  11/11/21
:last_edit     11/11/21
"""
import abc
import hashlib

class HashStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def hash(self, string):
        pass

class MD5Strategy(HashStrategy):
    def hash(self, string):
        return hashlib.md5(string.encode()).hexdigest()

class SHA256Strategy(HashStrategy):
    def hash(self, string):
        return hashlib.sha256(string.encode()).hexdigest()

class SHA512Strategy(HashStrategy):
    def hash(self, string):
        return hashlib.sha512(string.encode()).hexdigest()

class SHA3256Strategy(HashStrategy):
    def hash(self, string):
        return hashlib.sha3_256(string.encode()).hexdigest()

class SHA3512Strategy(HashStrategy):
    def hash(self, string):
        return hashlib.sha3_512(string.encode()).hexdigest()

class BLAKE2BStrategy(HashStrategy):
    def hash(self, string):
        return hashlib.blake2b(string.encode()).hexdigest()

class BLAKE2SStrategy(HashStrategy):
    def hash(self, string):
        return hashlib.blake2s(string.encode()).hexdigest()