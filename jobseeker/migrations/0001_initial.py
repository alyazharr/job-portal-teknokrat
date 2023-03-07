# Generated by Django 4.1.7 on 2023-03-06 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='AnswerKuesioners',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('users_id', models.PositiveBigIntegerField()),
                ('kategori_id', models.PositiveBigIntegerField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'answer_kuesioners',
            },
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('users_id', models.PositiveBigIntegerField()),
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
            ],
            options={
                'db_table': 'c_v',
            },
        ),
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('format', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'excel',
            },
        ),
        migrations.CreateModel(
            name='FailedJobs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=255, unique=True)),
                ('connection', models.TextField()),
                ('queue', models.TextField()),
                ('payload', models.TextField()),
                ('exception', models.TextField()),
                ('failed_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'failed_jobs',
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
            name='FormKepuasan',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('soal', models.TextField()),
                ('kategori', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'form_kepuasan',
            },
        ),
        migrations.CreateModel(
            name='JawabanFormKepuasan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'jawaban_form_kepuasan',
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
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('kategori', models.CharField(max_length=255)),
                ('deskripsi', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'kategori',
            },
        ),
        migrations.CreateModel(
            name='Kuesioner',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('soal', models.TextField()),
                ('kategori_id', models.PositiveBigIntegerField()),
                ('syarat', models.CharField(max_length=255)),
                ('syarat_value', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'kuesioner',
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
            name='Lowongan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('users_id', models.PositiveBigIntegerField()),
                ('posisi', models.CharField(max_length=255)),
                ('gaji', models.CharField(max_length=255)),
                ('lama_pengalaman', models.CharField(max_length=255)),
                ('deskripsi', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('batas_pengumpulan', models.DateField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lowongan',
            },
        ),
        migrations.CreateModel(
            name='Migrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('migration', models.CharField(max_length=255)),
                ('batch', models.IntegerField()),
            ],
            options={
                'db_table': 'migrations',
            },
        ),
        migrations.CreateModel(
            name='MinimumSalaryByRegion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('provinsi_id', models.PositiveBigIntegerField()),
                ('ump', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'minimum_salary_by_region',
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
            name='Posts',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('judul', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('excerpt', models.TextField()),
                ('body', models.TextField()),
                ('users_id', models.PositiveBigIntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'posts',
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
            name='SubKuesioner',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('deskripsi', models.CharField(max_length=255)),
                ('validasi', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('syarat', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('kuesioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobseeker.kuesioner')),
            ],
            options={
                'db_table': 'sub_kuesioner',
            },
        ),
        migrations.CreateModel(
            name='QuestAnswer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quest_answer',
            },
        ),
    ]
