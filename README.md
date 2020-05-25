# KBBI-Twitter

Kode dalam Python dibuat untuk mem-posting kata-kata dari [KBBI Daring][kbbi] pada Twitter.

## Instalasi

### Manual

1. Lakukan instalasi untuk paket-paket prasyarat, diantaranya: [`kbbi-python`][kbbi-python] dan [`tweepy`][tweepy].
2. Klonakan repositori ini atau unduh [`app.py`][app-py] dan [`kata.txt`][kata-txt].
3. Letakkan `app.py` dan `kata-txt` dalam direktori yang Anda inginkan.
4. Buka dan sunting berkas "file" `app.py`.
5. Masukkan `consumer key`, `consumer secret`, `access token`, dan `access token secret` Anda pada baris 10 hingga 13.

## Penggunaan

### Melalui kode Python

Anda hanya perlu untuk menjalankan berkas `app.py` pada `command prompt` di Windows atau `terminal` di UNIX dan MacOS.
Dalam `terminal`, Anda perlu mengetikkan `python app.py`. Sistem akan otomatis masuk pada akun Anda dan mengirimkan status baru setiap dua menit sekali.

## Berkontribusi

Saya sangat berterima kasih bila Anda ingin membantu untuk mengembangkan proyek ini. Apabila Anda memiliki kemampuan untuk membuat kode, Anda dapat ikut berkontribusi untuk mengembangkan proyek ini dengan menambahkan fitur-fitur yang belum dimiliki. Apabila Anda tidak memiliki kemampuan untuk membuat kode, Anda juga diundang untuk memutakhirkan daftar kata-kata yang ada dalam KBBI dalam berkas "file" `kata.txt`. Kontribusi yang kecil tetaplah kontribusi. Terima kasih! :)

## Lisensi

Proyek ini didistribusikan dengan lisensi [GNU General Public License v3.0][LICENSE].

[kbbi-python]: https://github.com/laymonage/kbbi-python
[tweepy]: https://www.tweepy.org/
[kbbi]: https://kbbi.kemdikbud.go.id
[app-py]: https://raw.githubusercontent.com/wildangunawan/KBBI-Twitter/master/app.py
[kata-txt]: https://raw.githubusercontent.com/wildangunawan/KBBI-Twitter/master/kata.txt
[LICENSE]: https://github.com/wildangunawan/KBBI-Twitter/blob/master/LICENSE
