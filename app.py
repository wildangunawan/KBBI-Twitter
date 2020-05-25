# impor perpustakaan "library"
# yang diperlukan
from kbbi import KBBI
from kbbi import TidakDitemukan
from kbbi import AutentikasiKBBI
from random import randint
import tweepy
import time

# data login
consumer_key = "CONSUMER KEY"
consumer_secret = "CONSUMER SECRET"
access_token = "ACCESS TOKEN"
access_token_secret = "ACCESS TOKEN SECRET"
posel_kbbi = "POS-EL UNTUK KBBI"
password_kbbi = "PASSWORD UNTUK KBBI"

# koneksi ke Twitter
auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# otentikasi ke KBBI untuk
# akses dengan jumlah unlimited
# jika tidak membuat akun maka Anda
# hanya dapat mengakses KBBI sebanyak
# 100 kali per hari
auth = AutentikasiKBBI(posel_kbbi, password_kbbi)

# fungsi untuk ambil baris random
def jumlahBaris():
	# variabel untuk menyimpan jumlah kata
	total_jumlah_baris = -1

	# cek berapa kata yang tersedia
	with open("kata.txt", "r") as f:
		# baca dan hitung setiap line
		for _ in f.readlines():
			total_jumlah_baris += 1

	# kembalikan pada user
	return total_jumlah_baris

def ambilBaris(jumlah_baris):
	# ambil kata random berdasarkan line
	baris = randint(1, jumlah_baris) - 1

	# kembalikan pada user
	return baris

# buat fungsi untuk ambil kata
def ambilKata(baris):
	with open("kata.txt", "r") as f:
		# ambil katanya
		kata = f.readlines()[baris]

		# hapus \n yang ada pada akhir kata
		kata = kata.replace("\n", "")

	# kembalikan pada user
	return kata

# ambil ke KBBI
def ambilDariKBBI(kata):
	# ambil ke KBBI menggunakan try except
	# untuk mengetahui apakah kata
	# tsb ada dalam KBBI atau tidak
	try:
		# coba akses ke KBBI daring
		kata = KBBI(kata, auth)

		# jika tidak ada kesalahan
		# maka tersedia
		return True

	except TidakDitemukan as e:
		# kata tidak tersedia
		# kembalikan kepada user
		return False

# siapkan variabel
kata_terambil = []

# total jumlah baris tersedia
jumlah_baris = jumlahBaris()

# jalankan terus menerus
while True:
	# ambil kata baru
	kata_valid = False

	# jalankan terus-menerus selama
	# kata yang diambil pernah
	# di-posting atau tidak valid
	while not kata_valid:
		kata_terposting = False

		# cek apakah pernah ter-posting atau belum
		while not kata_terposting:
			# ambil baris acak sesuai yang tersedia
			baris = ambilBaris(jumlah_baris)

			# ambil kata yang ada pada baris tersebut
			kata = ambilKata(baris)

			# cek apakah sudah pernah terambil dan terposting
			if kata not in kata_terambil:
				kata_terposting = True
			
				# simpan dalam kata terambil
				kata_terambil.append(kata)

		# cek apakah dalam KBBI tersedia
		kata_dari_KBBI = ambilDariKBBI(kata)

		# cek apakah kata valid atau tidak
		if kata_dari_KBBI != False:
			kata_valid = True

	# kata valid
	kata = kata

	# buat teks status
	teks = "%s\n\nLihat detailnya pada KBBI Daring: https://kbbi.kemdikbud.go.id/entri/%s" % (kata, kata)

	# perbaharui status
	api.update_status(status = teks)

	# cek apakah sudah semua kata ter-posting
	if len(kata_terambil) == jumlah_baris:
		kata_terambil = []

	# tidur selama dua menit
	# agar tidak di-suspend
	# oleh Twitter
	time.sleep(2*60)