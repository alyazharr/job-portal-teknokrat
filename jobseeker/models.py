from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UsersManager
from .queryset import LowonganQuerySet
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from .validators import validate_after_today
from django.utils import timezone


class CV(models.Model):
    id = models.BigAutoField(primary_key=True)
    users_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.TextField()
    posisi = models.CharField(max_length=255)
    instansi = models.CharField(max_length=255)
    lama_instansi = models.CharField(max_length=255)
    keterangan_posisi = models.CharField(max_length=255)
    asal_sekolah = models.CharField(max_length=255)
    masa_waktu = models.CharField(max_length=255)
    keterangan_pendidikan = models.CharField(max_length=255)
    kontak = models.CharField(max_length=255)
    jenis_kontak = models.CharField(max_length=255)
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
    class StatusLamaran(models.TextChoices):
        PENDING = "Pending", _("Pending")
        DITOLAK = "Ditolak", _("Ditolak")
        DITERIMA = "Diterima", _("Diterima")
        

    id = models.BigAutoField(primary_key=True)
    users_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lowongan_id = models.ForeignKey('Lowongan',on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        choices=StatusLamaran.choices,
        default=StatusLamaran.PENDING
    )
    subject = models.TextField(null=True)
    berkas = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lamar'

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
    subscribed = models.BooleanField(default=False)

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

class Lowongan(models.Model):
    class StatusLowongan(models.TextChoices):
        UNVERIFIED = "Belum terverifikasi", _("Belum terverifikasi")
        VERIFIED = "Sudah terverifikasi", _("Sudah terverifikasi")
        REJECTED = "Ditolak", _("Sudah Ditolak")
        OPEN = "Buka", _("Buka")
        CLOSED = "Tutup", _("Tutup")

    id = models.BigAutoField(primary_key=True)
    users_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    posisi = models.CharField(max_length=255)
    gaji = models.FloatField(max_length=255)
    lama_pengalaman = models.PositiveIntegerField()
    deskripsi = RichTextField(null=True)
    requirements = RichTextField(null=True)
    status = models.CharField(max_length=255,choices=StatusLowongan.choices,default=StatusLowongan.UNVERIFIED)
    buka_lowongan = models.DateField(null=True)
    batas_pengumpulan = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True,auto_now=True)

    objects = LowonganQuerySet.as_manager()

    @property
    def is_open(self):
        return self.status == self.StatusLowongan.OPEN

    def clean(self):
        if self.batas_pengumpulan <= self.buka_lowongan:
            raise ValidationError(_('Tanggal pembukaan harus sebelum tanggal penutupan'),code='invalid_date')
        validate_after_today(self.buka_lowongan)
        validate_after_today(self.batas_pengumpulan)


    class Meta:
        db_table = 'lowongan'