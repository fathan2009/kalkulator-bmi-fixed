from flask import Flask, render_template, request

# Inisialisasi aplikasi Flask
# __name__ adalah variabel khusus di Python yang mewakili nama modul saat ini.
# Flask menggunakannya untuk mengetahui di mana mencari resource seperti template dan file statis.
app = Flask(__name__)

# Definisikan rute utama untuk aplikasi.
# Ini menangani permintaan GET (saat halaman pertama kali dimuat) dan POST (saat form disubmit).
@app.route('/', methods=['GET', 'POST'])
def index():
    # Inisialisasi variabel untuk hasil BMI agar tidak ada error saat pertama kali halaman dimuat
    # Ini akan menyimpan nilai BMI, kategori, dan rekomendasi
    bmi = None
    category = None
    recommendation = None
    name = "" # Inisialisasi nama untuk ditampilkan kembali di form jika diperlukan
    gender = ""
    age = ""
    weight = ""
    height_cm = ""

    # Jika metode request adalah POST, artinya form telah disubmit
    if request.method == 'POST':
        # Ambil data dari form
        # request.form adalah objek kamus (dictionary) yang berisi data dari form
        name = request.form['name']
        gender = request.form['gender']
        age = int(request.form['age']) # Konversi ke integer
        weight = float(request.form['weight']) # Konversi ke float
        height_cm = float(request.form['height']) # Tinggi dalam cm

        # Validasi input: pastikan tinggi dan berat badan positif
        if weight <= 0 or height_cm <= 0:
            category = "Input tidak valid"
            recommendation = "Berat dan tinggi badan harus lebih besar dari nol."
        else:
            # Konversi tinggi dari cm ke meter karena rumus BMI menggunakan meter
            height_m = height_cm / 100

            # Hitung BMI menggunakan rumus: berat / (tinggi(m) * tinggi(m))
            bmi = weight / (height_m * height_m)

            # Tentukan kategori BMI berdasarkan nilai yang dihitung
            if bmi < 18.5:
                category = "Kekurangan Berat Badan"
                recommendation = "Disarankan untuk meningkatkan asupan nutrisi dan berkonsultasi dengan ahli gizi."
            elif 18.5 <= bmi <= 24.9:
                category = "Normal"
                recommendation = "Berat badan Anda ideal. Pertahankan pola hidup sehat dengan gizi seimbang dan aktivitas fisik teratur."
            elif 25 <= bmi <= 29.9:
                category = "Kelebihan Berat Badan"
                recommendation = "Disarankan untuk mengurangi asupan kalori dan meningkatkan aktivitas fisik."
            else: # bmi >= 30
                category = "Obesitas"
                recommendation = "Sangat disarankan untuk melakukan perubahan gaya hidup signifikan, termasuk pola makan dan olahraga. Konsultasi dengan dokter atau ahli gizi sangat dianjurkan."

    # Render template index.html
    # Kirimkan variabel bmi, category, recommendation, name, gender, age, weight, height_cm ke template
    # Ini akan membuat data tersebut dapat diakses di dalam HTML menggunakan Jinja2
    return render_template('index.html', 
                           bmi=bmi, 
                           category=category, 
                           recommendation=recommendation,
                           name=name,
                           gender=gender,
                           age=age,
                           weight=weight,
                           height=height_cm)

# Pastikan skrip berjalan hanya jika dieksekusi secara langsung (bukan diimpor sebagai modul)
if __name__ == '__main__':
    # Jalankan aplikasi Flask dalam mode debug.
    # Mode debug akan otomatis me-reload server saat ada perubahan kode
    # dan memberikan informasi error yang lebih detail.
    app.run(debug=True)
