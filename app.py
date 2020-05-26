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
posel_kbbi = "POS-EL KBBI"
katasandi_kbbi = "KATA SANDI KBBI"

# koneksi ke Twitter
try:
	auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	print("Berhasil masuk ke Twitter!")
except:
	raise Exception("Gagal masuk ke Twitter!")

# otentikasi ke KBBI untuk
# akses dengan jumlah unlimited
# jika tidak membuat akun maka Anda
# hanya dapat mengakses KBBI sebanyak
# 100 kali per hari
try:
	auth = AutentikasiKBBI(posel_kbbi, katasandi_kbbi)
except:
	raise Exception("Gagal masuk ke KBBI Daring!")

# fungsi untuk ambil baris random
def jumlahBaris():
	# variabel untuk menyimpan jumlah kata
	total_jumlah_baris = 0

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
		return kata.serialisasi()

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

					# ambil detail kata dan tautan
					tautan_ke_kbbi = kata_dari_KBBI['pranala']
					detail_kata = kata_dari_KBBI['entri']

					# cek apakah baku atau tidak
					# bila kata tersebut tidak baku
					# maka kemungkinan besar kata tersebut
					# hanya memiliki satu objek kata, makna,
					# dan submakna
					makna = detail_kata[0]['makna'][0]
					submakna = makna['submakna'][0]

					# cek apakah terdapat →
					# yang berarti kata tersebut
					# tidak baku
					if "→" in submakna:
						# kata tidak baku, kita ambil kata
						# baku yang diberikan oleh KBBI
						kata = submakna.replace("→ ", "")

						# karena mengambil kata baru, maka
						# kita wajib untuk mengambil detail
						# kata yang baru juga
						kata_dari_KBBI = ambilDariKBBI(kata)

						# ambil detail kata dan tautan
						tautan_ke_kbbi = kata_dari_KBBI['pranala']
						detail_kata = kata_dari_KBBI['entri']

	# kata valid
	kata = kata

	# variabel untuk menyimpan detail kata
	detail_semua = []

	# ambil semua detail kata
	for detail in detail_kata:
		# ambil nama dan ganti . menjadi •
		# untuk menghindari hukuman dari Twitter
		# yang mungkin mengira sedang mengirim
		# sembarang pranala untuk tautan balik "backlink"
		nama = detail['nama'].replace(".", "•")

		# ambil kata dasar bagi kata berimbuhan
		kata_dasar = ", ".join(detail['kata_dasar'])

		# ambil juga makna dan contoh
		# contoh untuk sementara belum
		# digunakan untuk posting ke Twitter
		makna_dan_contoh = []

		# ambil objek makna
		makna = detail['makna']
		
		# for loop dalam makna
		for detail_makna in makna:
			# ambil kelas
			kelas = detail_makna['kelas']
			macam_macam_kelas = ""

			# for loop dalam kelas
			for k in kelas:
				# ambil kode kelasnya saja
				kode = k['kode']

				# masukkan dalam variabel
				macam_macam_kelas += "(%s) " % kode

			# hapus spasi paling ujung pada variabel
			macam_macam_kelas = macam_macam_kelas.rstrip()

			# ambil submakna dan contoh
			submakna = "; ".join(detail_makna['submakna'])
			contoh = "; ".join(detail_makna['contoh'])

			# jadikan satu kelas dan submakna
			makna_lengkap = "%s %s" % (macam_macam_kelas, submakna)

			# masukkan dalam satu perpusatakaan "dictionary"
			makna_dan_contoh.append({
				"makna": makna_lengkap,
				"contoh": contoh
			})
		
		# simpan datanya
		detail_semua.append({
			"nama": nama,
			"kata dasar": kata_dasar,
			"makna dan contoh": makna_dan_contoh
		})

	# buat teks status
	teks = "%s\n\nLihat detailnya di KBBI Daring: %s" % (kata, tautan_ke_kbbi)

	# coba untuk perbaharui status
	try:
		# perbaharui status
		status = api.update_status(status = teks)

		# ambil id status untuk
		# dibalas kembali oleh bot
		# sebagai makna/pengertian
		# dari kata tersebut
		id_status = status.id

		# siapkan tweet untuk mengirim makna
		for detail in detail_semua:
			nama = detail['nama']
			kata_dasar = detail['kata dasar']
			makna_dan_contoh = detail['makna dan contoh']

			"""
			TEKS CONTOH UNTUK DIKIRIM SBB.:
			me.ngo.ta.kan
			Kata dasar: kota (1)

			1. (v) (kl) menjadikan seperti kota; menjadikan bersifat kota; menjadikan sebagai konsumsi orang kota
			2. (v) (kl) memperkuat dengan benteng; memakai sesuatu untuk benteng
			"""

			# ambil makna
			makna = ""
			for i in range(1, len(makna_dan_contoh)+1):
				# ambil makna yang ada
				makna_per_makna = makna_dan_contoh[i-1]['makna']

				# jika hanya terdapat satu makna maka
				# tidak perlu diberikan nomor di depannya
				# ini hanya untuk mempercantik teks
				if len(makna_dan_contoh) == 1:
					# jika satu maka hanya perlu makna
					makna += "%s" % (makna_per_makna)
				else:
					# jika lebih dari satu maka perlu
					# penomoran dan juga nama
					makna += "%s. %s\n" % (i, makna_per_makna)
			
			# hapus pembatas baris "line break"
			# pada akhir teks makna
			makna = makna.rstrip()

			# jika ada kata dasar
			# maka ikut di-posting
			if kata_dasar != "":
				# ada kata dasar, maka perlu di-posting juga
				teks = "%s\nKata dasar: %s\n\n%s" % (nama, kata_dasar, makna)
			else:
				# jika tidak ada berarti hanya
				# perlu untuk mem-posting nama dan makna
				teks = "%s\n\n%s" % (nama, makna)

			# perbaharui status dengan
			# membalas ke status yang
			# pertama dikirimkan
			status = api.update_status(status = teks, in_reply_to_status_id = id_status)

			# ambil id status yang
			# baru saja dikirimkan
			id_status = status.id

			# selesai sudah untuk
			# satu makna, maka akan
			# berlanjut hingga makna
			# makna yang ada dalam KBBI
			# untuk satu kata habis

		# tidur selama dua menit
		# agar tidak di-suspend
		# oleh Twitter
		time.sleep(2*60)

	except tweepy.TweepError as e:
		# cek apakah errornya merupakan
		# error karena status duplikat
		if e.api_code == 187:
			# status duplikat!
			print("status duplikat untuk kata: %s" % kata)
		else:
			# bukan status duplikat
			# namun tetap ada error
			# dari Twitter
			print("Error: %s" % e)

	# cek apakah sudah semua kata ter-posting
	if len(kata_terambil) == jumlah_baris:
		kata_terambil = []