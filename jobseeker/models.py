from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UsersManager
from django.conf import settings


class CV(models.Model):
    id = models.BigAutoField(primary_key=True)
    users_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.TextField()
    posisi = models.CharField(max_length=255)
    instansi = models.TextField()
    lama_instansi = models.TextField()
    keterangan_posisi = models.TextField()
    asal_sekolah = models.TextField()
    masa_waktu = models.TextField()
    keterangan_pendidikan = models.TextField()
    kontak = models.TextField()
    jenis_kontak = models.TextField()
    kemampuan = models.TextField()
    prestasi = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'c_v'



class Fakultas(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama_fakultas = models.CharField(max_length=255)
    perguruan_tinggi_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'fakultas'


class KabKota(models.Model):
    id = models.BigAutoField(primary_key=True)
    nm_wil = models.CharField(max_length=255)
    provinsi_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'kab_kota'


class Lamar(models.Model):
    id = models.BigAutoField(primary_key=True)
    users_id = models.PositiveBigIntegerField()
    lowongan_id = models.PositiveBigIntegerField()
    subject = models.TextField()
    berkas = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lamar'


class Lowongan(models.Model):
    id = models.BigAutoField(primary_key=True)
    users_id = models.PositiveBigIntegerField()
    posisi = models.CharField(max_length=255)
    gaji = models.CharField(max_length=255)
    lama_pengalaman = models.CharField(max_length=255)
    deskripsi = models.TextField()
    status = models.CharField(max_length=255)
    batas_pengumpulan = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lowongan'

class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'password_resets'


class PerguruanTinggi(models.Model):
    id = models.BigAutoField(primary_key=True)
    kode_pt = models.CharField(unique=True, max_length=255)
    perguruan_tinggi = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'perguruan_tinggi'



class Prodi(models.Model):
    id = models.BigAutoField(primary_key=True)
    prodi = models.CharField(max_length=255)
    fakultas_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'prodi'


class Provinsi(models.Model):
    id = models.BigAutoField(primary_key=True)
    nm_wil = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'provinsi'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'role'

class Users(AbstractUser):
    name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)
    npm = models.CharField(max_length=255)
    nik = models.CharField(max_length=255, blank=True, null=True)
    no_telp = models.CharField(max_length=255, blank=True, null=True)
    ipk = models.CharField(max_length=255, blank=True, null=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    tempat_lahir = models.CharField(max_length=255, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=255, blank=True, null=True)
    agama = models.CharField(max_length=255, blank=True, null=True)
    tahun_masuk = models.DateField(blank=True, null=True)
    tahun_keluar = models.DateField(blank=True, null=True)
    pembimbing = models.CharField(max_length=255)
    penguji = models.CharField(max_length=255)
    judul_skripsi = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    role_id = models.PositiveBigIntegerField()
    prodi_id = models.PositiveBigIntegerField()

    last_login = None
    is_active = True
    objects = UsersManager()

    class Meta:
        db_table = 'users'

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name","npm","prodi_id"]

    @property
    def first_name(self):
        return self.name.split(" ")[0]
    
    @property
    def last_name(self):
        return " ".join(self.name.split(" ")[1:])

    @property
    def is_staff(self):
         return self.role_id == 3 or self.role_id == 4
    
    @property
    def date_joined(self):
        return self.created_at

    @property
    def is_superuser(self):
        return self.role_id == 4

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

