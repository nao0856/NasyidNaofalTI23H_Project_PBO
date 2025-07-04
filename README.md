# Project UAS OOP: CoC War Schedule Manager

Aplikasi ini adalah sistem penjadwalan dan pencatatan sederhana berbasis Command-Line Interface (CLI) yang dibuat menggunakan Python dengan konsep Object-Oriented Programming (OOP) untuk mengelola Clan War pada game Clash of Clans.

## Inspirasi

Aplikasi ini terinspirasi dari kebutuhan pribadi sebagai pemain game Clash of Clans. Karena clan sering mengadakan *Clan War*, seringkali dibutuhkan catatan sederhana untuk mengatur jadwal, daftar peserta, dan hasil serangan sebagai bahan strategi. Aplikasi ini bertujuan untuk menjadi solusi praktis dari masalah tersebut.

## Fitur

-   Membuat jadwal *war* baru (lawan, ukuran, tanggal).
-   Mendaftarkan peserta untuk setiap *war*.
-   Menambahkan catatan singkat untuk setiap serangan yang dilakukan peserta.
-   Menampilkan semua jadwal *war* beserta detailnya.
-   Semua data disimpan di database MySQL lokal untuk persistensi data.

---

## Prasyarat (Requirements)

Sebelum menjalankan aplikasi, pastikan Anda telah menginstal:
1.  **Python 3.x**
2.  **XAMPP** (atau server lokal sejenis seperti MAMP, WAMP) yang menyediakan MySQL.
3.  Library Python `mysql-connector-python`.

## Instalasi dan Konfigurasi (Wajib Dilakukan)

Ikuti langkah-langkah berikut untuk menyiapkan project agar bisa berjalan:

**1. Clone Repository**
   -   Unduh atau clone repository ini ke komputer lokal Anda.

**2. Instal Dependensi Python**
   -   Buka terminal atau Command Prompt, navigasikan ke folder utama project ini (`coc_war_tracker/`).
   -   Jalankan perintah berikut untuk menginstal library yang dibutuhkan:
     ```bash
     pip install mysql-connector-python
     ```

**3. Siapkan Server Database**
   -   Buka **XAMPP Control Panel**.
   -   Klik **Start** pada modul **Apache** dan **MySQL**.

**4. Buat Database dan Tabel**
   -   Buka browser dan akses `phpMyAdmin` dengan alamat: `http://localhost/phpmyadmin`
   -   **Buat Database:**
     -   Klik "New" di panel kiri.
     -   Masukkan nama database: `coc_tracker_db_simple`
     -   Pilih collation `utf8mb4_general_ci` (opsional, tapi direkomendasikan).
     -   Klik "Create".
   -   **Buat Tabel `wars`:**
     -   Klik pada database `coc_tracker_db_simple` yang baru saja Anda buat.
     -   Buka tab **"SQL"**.
     -   Salin (copy) seluruh kode di bawah ini dan tempel (paste) ke dalam kotak teks SQL:
       ```sql
       CREATE TABLE wars (
           id INT AUTO_INCREMENT PRIMARY KEY,
           opponent_clan VARCHAR(255) NOT NULL,
           war_size INT NOT NULL,
           start_date DATE NOT NULL,
           status VARCHAR(50) DEFAULT 'Preparation',
           participants_data TEXT 
       );
       ```
     -   Klik tombol **"Go"** untuk menjalankan query dan membuat tabel.

**5. Verifikasi Koneksi (Opsional)**
   -   Pastikan detail koneksi di file `db_connector.py` sesuai dengan pengaturan XAMPP Anda. Pengaturan default (`user='root'`, `password=''`) seharusnya sudah benar jika Anda tidak mengubah konfigurasi XAMPP.

## Cara Menjalankan Aplikasi

Setelah semua langkah instalasi dan konfigurasi di atas selesai:
1.  Pastikan terminal Anda masih berada di direktori utama project.
2.  Jalankan aplikasi dengan perintah:
    ```bash
    python main.py
    ```
3.  Ikuti menu interaktif yang muncul di layar.

---

https://youtu.be/gp_C8sj0ths?si=SOq078kKKtzJ6QRa
