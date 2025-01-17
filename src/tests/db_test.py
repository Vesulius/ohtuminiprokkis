import os
import unittest
from db import DataBase
from models import KirjaVinkki, Kurssi, VideoVinkki, Tagi, base
from vinkkityyppi import VinkkiTyyppi

class Testdb(unittest.TestCase):

    def setUp(self):
        self.tmp_db = DataBase("tmp123db", base)
        self.kirjavinkki = KirjaVinkki(otsikko = "Pro Git Book", kommentti = "Very cool")
        self.videovinkki = VideoVinkki(otsikko = "New video vinkki", url = "www.newvinkki.com", kommentti = "Very good kommentti")
        self.kurssi = Kurssi(nimi = "TKT20006 Ohjelmistotuotanto")
        self.tagi = Tagi(nimi = "tag1")

    def test_there_are_no_vinkit_in_the_beginning(self):
        query_result = self.tmp_db.session.query(KirjaVinkki).all()
        self.assertEqual(len(query_result), 0)

    # vinkin lisäys
    def test_adding_adds_correct_kirjavinkki_to_db(self):
        self.tmp_db.add_vinkki_to_db(self.kirjavinkki)
        result = self.tmp_db.find_all_vinkit()
        query_result = self.tmp_db.session.query(KirjaVinkki).all()
        otsikko = query_result[0].otsikko
        tyyppi = query_result[0].tyyppi
        kommentti = query_result[0].kommentti
        kurssit = query_result[0].related_courses
        luettu = query_result[0].luettu

        self.assertEqual(len(result), 1)
        self.assertEqual(otsikko, self.kirjavinkki.otsikko)
        self.assertEqual(tyyppi, self.kirjavinkki.tyyppi)
        self.assertEqual(kommentti, self.kirjavinkki.kommentti)
        self.assertEqual(len(kurssit), 0)
        self.assertEqual(luettu, self.kirjavinkki.luettu)
        self.assertFalse(self.kirjavinkki.luettu)

    def test_adding_adds_correct_videovinkki_to_db(self):
        self.tmp_db.add_video_vinkki_to_db(self.videovinkki)
        result = self.tmp_db.find_all_vinkit()
        query_result = self.tmp_db.session.query(VideoVinkki).all()

        self.assertEqual(len(result), 1)
        self.assertEqual(query_result[0].otsikko, self.videovinkki.otsikko)
        self.assertEqual(query_result[0].tyyppi, self.videovinkki.tyyppi)
        self.assertEqual(query_result[0].url, self.videovinkki.url)
        self.assertEqual(query_result[0].kommentti, self.videovinkki.kommentti)
        self.assertEqual(len(query_result[0].related_courses), 0)
        self.assertEqual(query_result[0].luettu, self.videovinkki.luettu)
        self.assertFalse(query_result[0].luettu, self.videovinkki.luettu)

    # viitteen lisäys vinkille
    def test_course_can_be_added_to_kirjavinkki(self):
        self.tmp_db.add_vinkki_to_db(self.kirjavinkki)
        self.tmp_db.add_course_to_kirjavinkki(self.kirjavinkki.id, self.kurssi)
        query_result = self.tmp_db.session.query(KirjaVinkki).all()
        kurssit = query_result[0].related_courses

        self.assertEqual(kurssit[0].nimi, self.kurssi.nimi)
        self.assertEqual(len(kurssit), 1)
    
    def test_course_can_be_added_to_videovinkki(self):
        self.tmp_db.add_vinkki_to_db(self.videovinkki)
        self.tmp_db.add_course_to_videovinkki(self.videovinkki.id, self.kurssi)
        query_result = self.tmp_db.session.query(VideoVinkki).all()
        kurssit = query_result[0].related_courses

        self.assertEqual(kurssit[0].nimi, self.kurssi.nimi)
        self.assertEqual(len(kurssit), 1)

    def test_tag_can_be_added_to_vinkki(self):
        self.tmp_db.add_vinkki_to_db(self.kirjavinkki)
        self.tmp_db.add_tag_to_vinkki(self.kirjavinkki.id, self.tagi)
        query_result = self.tmp_db.session.query(KirjaVinkki).all()
        tagi = query_result[0].related_tags

        self.assertEqual(tagi[0].nimi, self.tagi.nimi)
        self.assertEqual(len(tagi), 1)

    # viitteen tallentuminen
    def test_course_added_to_kirjavinkki_is_saved_to_Kurssit(self):
        self.tmp_db.add_vinkki_to_db(self.kirjavinkki)
        self.kirjavinkki.add_related_course(self.kurssi)
        query_result = self.tmp_db.session.query(Kurssi).all()
        kurssi = query_result[0]

        self.assertEqual(len(query_result), 1)
        self.assertEqual(kurssi.nimi, self.kurssi.nimi)

    # vinkkien poisto
    def test_delete_vinkki_removes_vinkki_with_correct_tyyppi(self):
        self.tmp_db.add_vinkki_to_db(self.kirjavinkki)
        removed = self.tmp_db.delete_vinkki_with_id(1, VinkkiTyyppi.KIRJA)
        query_result = self.tmp_db.session.query(KirjaVinkki).all()

        self.assertTrue(removed)
        self.assertEqual(len(query_result), 0)

    def test_delete_vinkki_does_nothing_when_given_incorrect_id_and_correct_tyyppi(self):
        self.tmp_db.add_vinkki_to_db(self.kirjavinkki)
        removed = self.tmp_db.delete_vinkki_with_id(15, VinkkiTyyppi.KIRJA)
        query_result = self.tmp_db.session.query(KirjaVinkki).all()

        self.assertFalse(removed)
        self.assertEqual(len(query_result), 1)

    # ei toimi
    def test_deleting_kirjavinkki_deletes_its_related_courses(self):
        pass

    def test_deleting_vinkki_with_nonexistend_id_doesnt_change_db(self):
        pass

    # queryt
    def test_query_with_id_returns_correct_kirja_obect(self):
        pass

    def test_query_with_id_returns_correct_video_obect(self):
        pass

    def test_query_with_nonexisting_id_results_none(self):
        pass

    def tearDown(self):
        os.remove("tmp123db.db")