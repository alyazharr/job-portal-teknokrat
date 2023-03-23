# Generated by Django 4.1.7 on 2023-03-23 02:43

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('npm', models.CharField(max_length=255)),
                ('nik', models.CharField(blank=True, max_length=255, null=True)),
                ('no_telp', models.CharField(blank=True, max_length=255, null=True)),
                ('ipk', models.CharField(blank=True, max_length=255, null=True)),
                ('tgl_lahir', models.DateField(blank=True, null=True)),
                ('tempat_lahir', models.CharField(blank=True, max_length=255, null=True)),
                ('alamat', models.CharField(blank=True, max_length=255, null=True)),
                ('jenis_kelamin', models.CharField(blank=True, max_length=255, null=True)),
                ('agama', models.CharField(blank=True, max_length=255, null=True)),
                ('tahun_masuk', models.DateField(blank=True, null=True)),
                ('tahun_keluar', models.DateField(blank=True, null=True)),
                ('pembimbing', models.CharField(max_length=255)),
                ('penguji', models.CharField(max_length=255)),
                ('judul_skripsi', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('email_verified_at', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=10)),
                ('remember_token', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('role_id', models.PositiveBigIntegerField()),
                ('prodi_id', models.PositiveBigIntegerField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Fakultas',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nama_fakultas', models.CharField(max_length=255)),
                ('perguruan_tinggi_id', models.PositiveBigIntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'fakultas',
            },
        ),
        migrations.CreateModel(
            name='KabKota',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nm_wil', models.CharField(max_length=255)),
                ('provinsi_id', models.PositiveBigIntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'kab_kota',
            },
        ),
        migrations.CreateModel(
            name='Lamar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('users_id', models.PositiveBigIntegerField()),
                ('lowongan_id', models.PositiveBigIntegerField()),
                ('subject', models.TextField()),
                ('berkas', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lamar',
            },
        ),
        migrations.CreateModel(
            name='PasswordResets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'password_resets',
            },
        ),
        migrations.CreateModel(
            name='PerguruanTinggi',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('kode_pt', models.CharField(max_length=255, unique=True)),
                ('perguruan_tinggi', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'perguruan_tinggi',
            },
        ),
        migrations.CreateModel(
            name='Prodi',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('prodi', models.CharField(max_length=255)),
                ('fakultas_id', models.PositiveBigIntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'prodi',
            },
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nm_wil', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'provinsi',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='Lowongan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('posisi', models.CharField(max_length=255)),
                ('gaji', models.FloatField(max_length=255)),
                ('lama_pengalaman', models.PositiveIntegerField()),
                ('deskripsi', ckeditor.fields.RichTextField(null=True)),
                ('requirements', ckeditor.fields.RichTextField(null=True)),
                ('status', models.CharField(choices=[('Belum terverifikasi', 'Belum terverifikasi'), ('Sudah terverifikasi', 'Sudah terverifikasi'), ('Ditolak', 'Sudah Ditolak'), ('Buka', 'Buka'), ('Tutup', 'Tutup')], default='Belum terverifikasi', max_length=255)),
                ('buka_lowongan', models.DateField(null=True)),
                ('batas_pengumpulan', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('users_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lowongan',
            },
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('profile', models.TextField()),
                ('posisi', models.CharField(max_length=255)),
                ('instansi', models.TextField()),
                ('lama_instansi', models.TextField()),
                ('keterangan_posisi', models.TextField()),
                ('asal_sekolah', models.TextField()),
                ('masa_waktu', models.TextField()),
                ('keterangan_pendidikan', models.TextField()),
                ('kontak', models.TextField()),
                ('jenis_kontak', models.TextField()),
                ('kemampuan', models.TextField()),
                ('prestasi', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('users_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'c_v',
            },
        ),
    ]
