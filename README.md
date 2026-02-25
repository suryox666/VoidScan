<p align="center">
  <img src="https://e.top4top.io/p_37088sn8x1.png" width="700" alt="VoidScan Banner"/>
</p>

<h1 align="center">VoidScan</h1>
<p align="center">
  <b>Multi-Purpose OSINT Recon Toolkit (CLI)</b><br>
  Fast • Lightweight • Powerful
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python">
  <img src="https://img.shields.io/badge/Type-OSINT-black?style=flat-square">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=flat-square">
</p>

---

## 🔎 Overview

**VoidScan** adalah toolkit OSINT berbasis Command Line yang dirancang untuk melakukan pengumpulan informasi publik secara cepat dan efisien dari berbagai sumber digital.

Tool ini menggabungkan beberapa modul reconnaissance dalam satu aplikasi ringan tanpa kebutuhan API berbayar.

Cocok untuk:

* OSINT investigator
* Cybersecurity enthusiast
* Bug hunter
* Digital forensics
* Research & education

---

## ⚡ Features

### 👤 Username Search

Mencari keberadaan username di berbagai platform populer.

* GitHub, Reddit, Instagram, Telegram, TikTok
* Pinterest, Twitch, Steam, SoundCloud
* Medium, Keybase, Threads, Facebook
* X (Twitter), YouTube, LinkedIn, Snapchat

**Fitur:**

* Multi-threaded scanning
* Deteksi akun valid
* Export hasil ke file laporan

---

### 🌐 Domain Intelligence

Analisis informasi domain secara cepat.

* Resolve domain → IP address
* Reverse DNS lookup
* WHOIS data extraction
* Registrar information
* Name servers
* Registration timeline

---

### 📱 Phone Lookup (Beta)

Analisis nomor telepon berbasis data publik.

* Validity & possibility check
* Country & timezone detection
* Carrier identification
* Line type detection
* WhatsApp activity estimation
* Telegram presence check
* Activity scoring

---

### 🖼️ Image OSINT

Ekstraksi informasi dari file gambar.

* File metadata
* MD5 / SHA1 / SHA256 hash
* EXIF metadata
* Camera information
* GPS coordinate detection
* Google Maps link
* Reverse image search links

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/voidscan.git
cd voidscan
```

### 2. Install Dependencies

```bash
pip install requests Pillow termcolor colorama phonenumbers geopy exifread
```

---

## ▶️ Usage

Jalankan program:

```bash
python main.py
```

Menu utama:

```
1. Username Search
2. Domain Intelligence
3. Phone Lookup (Beta)
4. Image OSINT
5. Exit
```

---

## 📂 Output Reports

Beberapa modul akan menghasilkan laporan yang disimpan secara otomatis:

```
reports/
 ├── username_search/
 └── image_osint/
```

---

## 🖥️ Requirements

* Python 3.x
* Internet connection
* Windows / Linux / macOS

---

## ⚠️ Disclaimer

Tool ini dibuat untuk tujuan:

* Pendidikan
* Penelitian keamanan
* Investigasi OSINT legal

Penggunaan ilegal atau melanggar privasi merupakan tanggung jawab pengguna.

---

## 👤 Author

**Suryo Saputro (SURYOX)**

* GitHub: https://github.com/suryox666
* Support: https://saweria.co/suryos
* Support: https://trakteer.id/suryos

---

<p align="center">
  <i>Built for research, security, and digital intelligence.</i>
</p>
