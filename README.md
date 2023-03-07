# Guideline Menjalankan Project

Dokumen ini digunakan untuk menjalankan project django. Untuk menjalankan project, diperlukan beberapa langkah yang harus dilakukan.

### Requirements
untuk menjalankan project ini, diperlukan beberapa software yang harus diinstall terlebih dahulu.

1. Python3, untuk menjalankan django. ![python-download](https://www.python.org/downloads/)

2. XAMPP, untuk menjalankan MySQL Server. ![xampp-download](https://www.apachefriends.org/download.html)

![xamp](https://a.fsdn.com/con/app/proj/xampp/screenshots/Screen%20Shot%202016-02-19%20at%2016.png/max/max/1)

Untuk menjalankan mySQL server, tekan tombol `Start` pada bagian MySQL.

## Setup Project
1. Create Teknokrat Database

Pada `settings.py` nama database-nya `teknokrat`, variabel tersebut dapat disesuaikan, tetapi untuk development, diseragamkan saja menjadi `teknokrat`

Kita perlu buat database dengan nama `teknokrat` (diperlukan untuk menjalankan django).

Buka command prompt, ketikkan perintah berikut: 
```
mysql -u root
```

``Note:`` Jika terdapat error MySQL command not found, artinya belum ada di Environment Variables Path MySQL. Tambahkan `C:\xampp\mysql\bin` (sesuaikan dengan tempat instalasi) pada bagian PATH.


Pada terminal MySQL (dapat menggunakan MySQL command client), jalankan perintah
```
create database teknokrat;
```

2. Migrate django
Buka terminal pada `root` direktori django. Aktifkan environment, lalu install semua dependencies


<details>
<summary>Guideline Menjalankan Django Project</summary>
<b> Environment activation </b>

```
python -m venv env
env\Scripts\activate
```

<b> Install dependencies </b>
```
pip install -r requirements.txt
```

<b> Migrate </b>
```
python manage.py makemigrations
python manage.py migrate
```
</details>


3. Transfer Data

Tahap ini tidak wajib dijalankan jika tidak ingin menggunakan data yang sudah ada. Jika ingin mengimport data dari file `.sql` , jalankan perintah berikut pada terminal

```
type alumnite_.sql | python manage.py dbshell
```

Seharusnya data pada `alumnite_.sql` sudah berhasil diimport ke database. Hasilnya dapat dilihat pada dashboard superuser django.

# Akses Dashboard Superuser

Untuk mengakses dashbord superuser django, harus membuat superuser terlebih dahulu.
<b>Create super user</b>
```
python manage.py createsuperuser
```

Dashboard superuser django dapat diakses pada `http://localhost:8000/admin/`