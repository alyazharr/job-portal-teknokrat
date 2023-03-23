from ..models import Lowongan,Users
from django.test import TestCase
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class LowonganTestCase(TestCase):
    

    def test_buka_lowongan_after_batas_pengumpulan(self):        
        invalid_lowongan = Lowongan(
            posisi="Software Engineer",
            gaji=100000,
            batas_pengumpulan = datetime.today() - timedelta(days=1),
            buka_lowongan= datetime.today() 
        )

        self.assertRaises(ValidationError, invalid_lowongan.clean)
    
    def test_buka_lowongan_before_batas_pengumpulan(self):
        try:
            valid_lowongan = Lowongan(
                posisi="Software Engineer",
                gaji=100000,
                batas_pengumpulan = datetime.today().date() + timedelta(days=1),
                buka_lowongan= datetime.today().date()
            )

            valid_lowongan.clean()
        
        except Exception:
            self.fail()
    
    def test_buka_lowongan_before_today(self):
        invalid_lowongan = Lowongan(
            posisi="Software Engineer",
            gaji=100000,
            batas_pengumpulan = datetime.today().date() ,
            buka_lowongan= datetime.today().date() - timedelta(days=1) 
        )

        self.assertRaises(ValidationError, invalid_lowongan.clean)

class UsersTestCase(TestCase):

    def setUp(self):
        self.alumni = Users(
            name="test ting",
            npm=1,
            prodi_id=1,
            role_id=1,
            password="password"
        )

        self.admin = Users(
            name="test ting",
            npm=1,
            prodi_id=1,
            role_id=3,
            password="password",
        )

        self.super_admin = Users(
            name="test ting",
            npm=1,
            prodi_id=1,
            role_id=4,
            password="password"
        )

    def test_first_name_property(self):
        self.assertEqual(self.alumni.first_name, "test")

    def test_last_name_propery(self):
        self.assertEqual(self.alumni.last_name, "ting")

    def test_is_staff_property_if_admin(self):
        self.assertTrue(self.admin.is_staff)
    
    def test_is_staff_property_if_super_admin(self):
        self.assertTrue(self.super_admin.is_staff)
    
    def test_is_staff_property_if_alumni(self):
        self.assertTrue(not self.alumni.is_staff)
    
    def test_date_joined(self):
        self.assertEqual(self.alumni.date_joined, self.alumni.created_at)
    
    def test_is_super_user_if_alumni(self):
        self.assertTrue(not self.alumni.is_superuser)

    def test_is_super_user_if_super_admin(self):
        self.assertTrue(self.super_admin.is_superuser)
