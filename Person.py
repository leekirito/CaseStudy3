from abc import ABC, abstractmethod

class Person():

    @classmethod
    def __init__(self, id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address):
        self.id = id
        self.username = username
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.age = age
        self.contact_number = contact_number
        self.gender = gender
        self.email = email
        self.address = address 
        