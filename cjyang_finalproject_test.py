import unittest
import cjyang_finalproject as proj
import json

class TestMovie(unittest.TestCase):

    def testAccess(self):
        self.assertEqual(proj.film_n_link['Fight Club']['content_rating'], "R")
        self.assertEqual(proj.film_n_link['12 Angry Men']['average_rating'], '8.9')
        self.assertEqual(proj.film_n_link['Inception']['year_published'], '2010')
        self.assertEqual(len(proj.film_n_link.keys()), 250)
        self.assertEqual(proj.film_n_link['The Shawshank Redemption']['ranking'], '1')
        self.assertGreater(len(proj.movie_stars), 250)
        self.assertGreater(len(proj.movie_director), 250)
        self.director_godfather = ''
        for i in proj.movie_director:
            if i[0] == 'The Godfather':
                self.director_godfather = i[1]
        self.assertEqual(self.director_godfather, 'Francis Ford Coppola')
        self.director_se7en = ''
        for i in proj.movie_director:
            if i[0] == 'Se7en':
                self.director_se7en = i[1]
        self.assertEqual(self.director_se7en, 'David Fincher')
        self.morganappears = 0
        for i in proj.movie_stars:
            if i[1] == 'Morgan Freeman':
                self.morganappears = 1
        self.assertEqual(self.morganappears, 1)

class testStorage(unittest.TestCase):

    def testStor(self):
        self.cache = open('movie_info.json', 'r')
        self.row_reader = self.cache.readlines()
        self.assertTrue(self.row_reader[0].split()[0])
        self.cache.close()

class testProcessing(unittest.TestCase):

    def testProc(self):
        self.assertGreater(len(proj.plot_actor_count()),0)
        self.assertGreater(len(proj.plot_year_count()),0)
        self.assertGreater(len(proj.plot_rating_count()),0)
        self.assertGreater(len(proj.plot_director_count()),0)



unittest.main(verbosity=2)
