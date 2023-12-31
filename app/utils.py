from random import randint
from passlib.context import CryptContext
from .database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import oauth2
from . import models, schemas, utils, oauth2
import logging
import string
import random

logging.basicConfig(filename='logfile.log',
                    format='%(asctime)s %(message)s', filemode='a', level=logging.DEBUG)
log = logging.getLogger()

hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return hash_context.hash(password)


def verify_password(password: str, hashpassword):
    return hash_context.verify(password, hashpassword)


def generate_number():
    from random import randint

    def generatenum():
        number = randint(9999999999, 99999999999)
        return number
    verhoeff_table_d = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))
    verhoeff_table_p = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))
    verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def calcsum(number):
        """For a given number returns a Verhoeff checksum digit"""
        c = 0
        for i, item in enumerate(reversed(str(number))):
            c = verhoeff_table_d[c][verhoeff_table_p[(i + 1) % 8][int(item)]]
        return verhoeff_table_inv[c]

    def checksum(number):
        """For a given number generates a Verhoeff digit and
        returns number + digit"""
        c = 0
        for i, item in enumerate(reversed(str(number))):
            c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
        return c

    def generateVerhoeff(number):
        """For a given number returns number + Verhoeff checksum digit"""
        return "%s%s" % (number, calcsum(number))

    def validateVerhoeff(number):
        """Validate Verhoeff checksummed number (checksum is last digit)"""
        return checksum(number) == 0

    while True:
        number = generatenum()
        num = str(generateVerhoeff(number))
        if validateVerhoeff(number) == True:
            var1 = random.choice(string.ascii_uppercase)
            var2 = random.choice(string.ascii_uppercase)
            var3 = 'MH'
            var4 = 'KA'
            return var1+var2+num[:2] + " " + num[4:8] + " " + num[8:]
            break
