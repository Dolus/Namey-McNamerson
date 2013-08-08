#Obective: When the user runs the script, a random first and last name will be drawn from databases
#containing first and last names, then displayed for the user.

import unittest

from random import choice


class Generator(object):
    def __init__(self, first_names=None, last_names=None, filename=None):
        if filename is not None:
            first_names, last_names = self._load_file(filename)
        self.first_names = first_names
        self.last_names = last_names
        self.used = []

    def getname(self, repeat=True):
        if not repeat and len(self.used) >= len(self.first_names) * len(self.last_names):
            raise Exception('No more names.')
        name = choice(self.first_names) + ' ' + choice(self.last_names)
        if not repeat and name in self.used:
            name = self.getname(repeat)
        self.used.append(name)
        return name

    def _load_file(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
            first_names, last_names = data.split('*')
        return first_names.strip().split('\n'), last_names.strip().split('\n')


class TestNameGenerator(unittest.TestCase):
    def test_generatename(self):
        first_names = ['Bill']
        last_names = ['Smith']
        generator = Generator(first_names, last_names)
        self.assertIsInstance(generator.getname(), str)
        self.assertEqual(generator.getname(), 'Bill Smith')

    def test_list_pull(self):
        first_names = ['Bill', 'Joe']
        last_names = ['Smith']
        generator = Generator(first_names, last_names)
        name1 = generator.getname()
        name2 = generator.getname(repeat=False)
        self.assertNotEqual(name1, name2)
        with self.assertRaises(Exception) as ex:
            generator.getname(repeat=False)
            self.assertEqual(ex.message, 'No more names.')

    def test_parse_file(self):
        generator = Generator(filename='names.txt')
        self.assertTrue(len(generator.first_names) > 0)
        self.assertTrue(len(generator.last_names) > 0)
        self.assertIsInstance(generator.first_names, list)
        self.assertIsInstance(generator.last_names, list)
        self.assertIsInstance(generator.first_names[-1], str)
        self.assertTrue(len(generator.first_names[-1]) > 0)

if __name__ == '__main__':
    unittest.main()
