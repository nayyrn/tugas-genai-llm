# GenAI Application

## Project Information

**Nama Project:**  
Assignment Requirement Analyzer

**Use Case:**  
Membantu menganalisis instruksi tugas supaya informasi penting di dalamnya lebih gampang dipahami.

**Deskripsi Singkat:**  
Assignment Requirement Analyzer adalah aplikasi yang saya buat untuk membantu membaca instruksi tugas yang cukup panjang. User bisa memasukkan instruksi tugas, lalu aplikasi akan mengambil informasi penting seperti inti tugas, requirement, hasil yang harus dikumpulkan, deadline, dan checklist.

Saya menggunakan Gradio sebagai tampilan frontend supaya aplikasi lebih mudah digunakan dan user tidak harus melakukan testing melalui `/docs`.

---

## Tech Stack

Teknologi yang saya gunakan dalam project ini:

- Python
- FastAPI
- Pydantic
- Groq API
- Gradio
- python-dotenv
- Uvicorn

---

## Application Flow

Alur aplikasi yang saya buat:

User memasukkan instruksi tugas melalui Gradio  
↓  
Input diterima oleh FastAPI  
↓  
Instruksi dikirim ke LLM menggunakan Groq API  
↓  
LLM menganalisis instruksi berdasarkan system prompt  
↓  
Hasil dikembalikan dalam bentuk structured output  
↓  
Hasil analisis ditampilkan kembali di Gradio

**Penjelasan:**

Pertama, user memasukkan instruksi tugas melalui tampilan Gradio. Input tersebut kemudian diproses oleh aplikasi FastAPI dan dikirim ke LLM melalui Groq API.

Pada saat yang sama, aplikasi juga mengirim system prompt yang mengatur apa yang harus dianalisis oleh AI dan bagaimana bentuk hasilnya.

Setelah selesai, hasil analisis dikembalikan dalam bentuk JSON terstruktur. Hasil tersebut kemudian ditampilkan di Gradio menjadi beberapa bagian seperti ringkasan tugas, requirement, hal yang harus dikumpulkan, deadline, dan checklist.

---

## API Endpoint

Endpoint utama yang saya gunakan adalah:

**POST /analyze**

Endpoint ini digunakan untuk menerima instruksi tugas dari user dan mengembalikan hasil analisis.

Saya juga membuat endpoint:

**POST /experiment**

Endpoint ini digunakan khusus untuk melakukan eksperimen Prompt A, Prompt B, dan Prompt C.

Selain itu terdapat:

**GET /health**

Endpoint ini digunakan untuk mengecek apakah backend aplikasi masih berjalan.

Frontend Gradio dapat dibuka melalui:

**/app**

---

## Example Request

Salah satu request yang saya gunakan saat testing:

{
  "text": "Buat laporan tentang penggunaan Generative AI dalam pendidikan. Laporan minimal 5 halaman, menggunakan minimal 3 sumber referensi, dan dikumpulkan dalam bentuk PDF. Deadline pengumpulan 10 November 2026."
}

---

## Example Response

Salah satu actual response yang saya dapatkan dari aplikasi:

{
  "task_summary": "Membuat laporan tentang penggunaan Generative AI dalam pendidikan.",
  "requirements": [
    "Laporan minimal 5 halaman",
    "Menggunakan minimal 3 sumber referensi"
  ],
  "deliverables": [
    "Laporan dalam format PDF"
  ],
  "deadline": "10 November 2026",
  "checklist": [
    "Memastikan laporan memiliki minimal 5 halaman",
    "Menyertakan minimal 3 sumber referensi",
    "Menyimpan dan mengirim laporan dalam format PDF"
  ]
}

---

# Structured Output

Structured output yang digunakan pada aplikasi terdiri dari:

- `task_summary`
- `requirements`
- `deliverables`
- `deadline`
- `checklist`

Strukturnya:

{
  "task_summary": "ringkasan tugas",
  "requirements": [],
  "deliverables": [],
  "deadline": "deadline tugas",
  "checklist": []
}

### Kenapa memilih field-field tersebut?

Saya memilih `task_summary` supaya user bisa langsung melihat inti tugas tanpa harus membaca ulang seluruh instruksi.

`requirements` digunakan untuk memisahkan syarat atau ketentuan yang memang harus dipenuhi.

`deliverables` digunakan untuk menunjukkan hasil atau file yang harus dikumpulkan.

`deadline` digunakan agar batas waktu tugas bisa langsung terlihat.

Sedangkan `checklist` digunakan untuk membantu user mengecek kembali requirement tugas dan beberapa hal umum sebelum tugas dikumpulkan.

---

# Prompt Experiment

Pada eksperimen ini saya menggunakan input yang sama pada Prompt A, Prompt B, dan Prompt C agar hasilnya bisa dibandingkan.

## Input yang Digunakan

Buat laporan tentang penggunaan Generative AI dalam pendidikan. Laporan minimal 5 halaman, menggunakan minimal 3 sumber referensi, dan dikumpulkan dalam bentuk PDF. Deadline pengumpulan 10 November 2026.

---

## Prompt A

Prompt A yang saya gunakan masih sangat sederhana:

Analisis instruksi tugas berikut.  
Berikan hasil dalam format JSON.

### Actual Output A

Pada Prompt A, AI sebenarnya bisa memahami isi instruksi, tetapi hasilnya masih terlalu bebas.

AI membuat struktur output sendiri seperti task, topic, requirements, deadline, feasibility, dan notes.

Hasilnya juga masih dibungkus dengan format markdown sehingga aplikasi belum bisa membacanya sebagai JSON murni.

Pada response aplikasi terlihat:

{
  "prompt_version": "A",
  "is_valid_json": false,
  "output": "```json\n{\n  \"task\": \"Create a report\",\n  \"topic\": \"Use of Generative AI in Education\",\n  \"requirements\": {\n    \"minimum_pages\": 5,\n    \"minimum_references\": 3,\n    \"reference_type\": \"scholarly or reputable sources\",\n    \"output_format\": \"PDF\",\n    \"language\": \"Indonesian\"\n  },\n  \"deadline\": \"2026-11-10\",\n  \"feasibility\": {\n    \"content_creation\": true,\n    \"pdf_generation_by AI\": false,\n    \"recommended_steps\": [\n      \"Research and gather at least three reputable sources on Generative AI in education.\",\n      \"Draft the report with clear sections (e.g., introduction, benefits, challenges, case studies, future outlook, conclusion, references).\",\n      \"Ensure the draft spans at least five pages when formatted in a standard word processor (e.g., A4, 12‑pt Times New Roman, 1.5 line spacing).\",\n      \"Convert the final document to PDF using a word processor’s export function or an online converter.\"\n    ]\n  },\n  \"notes\": \"As a text‑based AI, I can provide the full report content in plain text/Markdown, which you can then copy into a document editor and export as PDF.\"\n}\n```"
}

Beberapa isi yang muncul dari output A antara lain:

- Membuat laporan tentang penggunaan Generative AI dalam pendidikan
- Minimal 5 halaman
- Minimal 3 sumber referensi
- Format PDF
- Deadline 10 November 2026
- AI juga menambahkan beberapa rekomendasi yang tidak secara langsung diminta pada instruksi

---

## Prompt B

Pada Prompt B saya mulai memberikan Role, Task, dan Context.

Prompt yang digunakan:

**Role:**  
Kamu adalah AI yang membantu mahasiswa memahami instruksi tugas.

**Task:**  
Analisis instruksi tugas yang diberikan user dan ambil informasi penting.

**Context:**  
User menerima instruksi tugas dan ingin mengetahui inti tugas, requirement, hasil yang harus dikumpulkan, deadline, dan checklist pengerjaan.

Berikan jawaban dalam format JSON.

### Actual Output B

Hasil Prompt B sudah lebih terarah dibanding Prompt A karena AI sudah mengetahui konteks penggunaan aplikasi.

Tetapi hasilnya masih belum menjadi JSON murni sehingga aplikasi masih membaca:

{
  "prompt_version": "B",
  "is_valid_json": false,
  "output": "```json\n{\n  \"task_summary\": \"Menyusun laporan tentang penggunaan Generative AI dalam pendidikan.\",\n  \"requirements\": {\n    \"panjang_laporan\": \"Minimal 5 halaman\",\n    \"sumber_referensi\": \"Minimal 3 sumber referensi yang relevan\",\n    \"format_file\": \"PDF\"\n  },\n  \"deliverables\": [\n    \"Laporan lengkap dalam format PDF\"\n  ],\n  \"deadline\": \"2026-11-10\",\n  \"checklist\": [\n    \"1. Tentukan fokus utama laporan (misalnya: aplikasi, manfaat, tantangan, atau studi kasus Generative AI di pendidikan).\",\n    \"2. Kumpulkan minimal 3 sumber referensi yang kredibel (jurnal, buku, konferensi, atau laporan industri).\",\n    \"3. Buat outline laporan: pendahuluan, tinjauan literatur, pembahasan, kesimpulan, dan daftar pustaka.\",\n    \"4. Tulis draft pertama sesuai outline, pastikan tiap bagian terstruktur dengan jelas.\",\n    \"5. Sisipkan kutipan dan referensi sesuai dengan gaya penulisan yang ditentukan (misalnya APA, MLA, atau Chicago).\",\n    \"6. Review dan revisi draft untuk memperbaiki alur, kejelasan, dan konsistensi format.\",\n    \"7. Pastikan total halaman mencapai minimal 5 (termasuk halaman judul, abstrak, daftar pustaka, dan lampiran bila ada).\",\n    \"8. Convert dokumen akhir ke format PDF.\",\n    \"9. Periksa kembali PDF untuk memastikan tidak ada kesalahan tampilan atau kehilangan konten.\",\n    \"10. Submit laporan PDF sebelum atau pada tanggal 10 November 2026.\"\n  ]\n}\n```"
}

Selain itu AI masih menambahkan beberapa langkah yang sebenarnya tidak disebutkan langsung pada instruksi, seperti:

- menentukan ruang lingkup laporan
- mencari sumber yang dianggap kredibel
- membuat outline
- melakukan review tulisan
- menentukan gaya sitasi
- mengecek tata letak dokumen

Jadi menurut saya hasil Prompt B sudah lebih baik dari Prompt A, tetapi masih terlalu banyak menambahkan asumsi.

---

## Prompt C

Pada Prompt C saya menggunakan prompt yang lebih lengkap.

Prompt C memiliki Role, Task, Context, Constraint, dan Output Format.

**Role:**  
Kamu adalah AI yang membantu menganalisis instruksi tugas.

**Task:**  
Analisis instruksi tugas yang diberikan user dan ambil informasi penting dari tugas tersebut.

**Context:**  
User biasanya menerima instruksi tugas yang panjang dan ingin mengetahui inti tugas, requirement, hasil yang harus dikumpulkan, deadline, dan checklist pengerjaan.

**Constraint:**

- Gunakan hanya informasi yang terdapat pada instruksi user untuk menentukan requirements, deliverables, dan deadline.
- Jangan membuat requirement atau deadline yang tidak disebutkan.
- Jangan melewatkan requirement penting.
- Checklist harus memuat poin penting dari instruksi user.
- Checklist boleh menambahkan langkah pengecekan umum yang membantu user sebelum mengumpulkan tugas, seperti mengecek kelengkapan atau format file.
- Tambahan checklist tidak boleh dianggap sebagai requirement wajib jika tidak disebutkan dalam instruksi user.
- Jangan membuat checklist yang bertentangan dengan instruksi user.
- Jika deadline tidak disebutkan, isi dengan "Tidak disebutkan".
- Jawaban harus berupa JSON valid.
- Jangan menambahkan teks apa pun di luar JSON.
- Checklist boleh menambahkan langkah pengecekan umum, tetapi tidak boleh membuat detail spesifik baru seperti nama file, format penamaan, jumlah, tanggal, atau aturan lain yang tidak disebutkan user.

**Output Format:**

{
  "task_summary": "ringkasan tugas utama",
  "requirements": ["requirement 1", "requirement 2"],
  "deliverables": ["hasil yang harus dikumpulkan"],
  "deadline": "deadline tugas",
  "checklist": ["hal yang harus diperiksa sebelum mengumpulkan"]
}

### Actual Output C

Hasil yang saya dapatkan:

{
  "prompt_version": "C",
  "is_valid_json": true,
   "output": {
    "task_summary": "Menyusun laporan tentang penggunaan Generative AI dalam pendidikan.",
    "requirements": [
      "Laporan harus memiliki minimal 5 halaman",
      "Menggunakan minimal 3 sumber referensi",
      "Dikumpulkan dalam bentuk file PDF"
    ],
    "deliverables": [
      "File PDF berisi laporan lengkap"
    ],
    "deadline": "10 November 2026",
    "checklist": [
      "Pastikan laporan memiliki setidaknya 5 halaman",
      "Pastikan terdapat minimal 3 sumber referensi yang tercantum dengan benar",
      "Konversi dokumen ke format PDF",
      "Periksa apakah file PDF dapat dibuka tanpa error",
      "Pastikan semua bagian laporan (judul, isi, referensi) lengkap"
    ]
  }
}

---

# Prompt Evaluation

### Dari ketiga prompt tersebut, mana yang menurut kalian menghasilkan output paling baik?

Menurut saya Prompt C menghasilkan output yang paling baik.

### Kenapa?

Karena Prompt C memberikan instruksi yang paling jelas kepada AI.

AI sudah diberi tahu perannya, tugasnya, konteks penggunaannya, batasan yang harus diikuti, dan bentuk output yang diinginkan.

Hasilnya juga sudah menjadi JSON valid sehingga dapat langsung diproses oleh aplikasi.

### Apa perbedaan paling terlihat antara Prompt A, Prompt B, dan Prompt C berdasarkan hasil testing kalian?

Prompt A terlalu sederhana sehingga AI masih bebas menentukan sendiri bentuk output dan memberikan cukup banyak informasi tambahan.

Prompt B sudah lebih terarah karena terdapat Role, Task, dan Context, tetapi AI masih menambahkan beberapa asumsi yang tidak disebutkan pada instruksi.

Prompt C paling konsisten karena sudah memiliki Constraint dan Output Format. Hasilnya lebih rapi, lebih sesuai dengan instruksi, dan bisa langsung digunakan oleh aplikasi.

---

# Failure Case

### Input yang menghasilkan output kurang baik

Buat tugas analisis tentang penggunaan AI di sekolah. Pilih salah satu bentuk tugas: jika memilih laporan, buat minimal 5 halaman dalam format PDF. Jika memilih video, durasi minimal 7 menit dan kumpulkan dalam format MP4. Jangan mengumpulkan laporan dan video sekaligus. Deadline kedua pilihan adalah 15 November 2026 pukul 20.00 WIB.

### Actual Output

Pada testing awal, AI sebenarnya sudah berhasil memahami bahwa user harus memilih laporan atau video.

Namun pada bagian checklist AI menambahkan contoh nama file:

**AI_di_Sekolah_Laporan.pdf**

atau

**AI_di_Sekolah_Video.mp4**

Padahal instruksi yang diberikan tidak pernah menyebutkan aturan nama file.

AI juga menampilkan checklist seperti:

- Pilih format tugas laporan atau video
- Jika laporan, minimal 5 halaman dan format PDF
- Jika video, minimal 7 menit dan format MP4
- Jangan mengumpulkan keduanya sekaligus
- Verifikasi nama file dan struktur sesuai petunjuk, misalnya AI_di_Sekolah_Laporan.pdf atau AI_di_Sekolah_Video.mp4

### Menurut kalian apa masalah dari output tersebut?

Menurut saya masalahnya adalah AI menambahkan detail yang terlalu spesifik dan tidak diberikan pada instruksi.

Kalau user melihat contoh nama file tersebut, user bisa mengira bahwa nama file itu memang diwajibkan oleh tugas, padahal sebenarnya hanya dibuat oleh AI.

### Apa yang kalian ubah pada prompt / constraint / kode?

Saya memperbaiki bagian constraint pada system prompt.

Saya menambahkan aturan:

Checklist boleh menambahkan langkah pengecekan umum, tetapi tidak boleh membuat detail spesifik baru seperti nama file, format penamaan, jumlah, tanggal, atau aturan lain yang tidak disebutkan user.

Dengan constraint tersebut, AI masih boleh memberikan checklist tambahan yang membantu user, tetapi tidak boleh membuat aturan baru.

### Output setelah diperbaiki

Setelah input yang sama dijalankan kembali, contoh nama file sudah tidak muncul.

Hasilnya menjadi:

**Ringkasan Tugas:**  
Membuat analisis penggunaan AI di sekolah dengan memilih satu bentuk tugas: laporan PDF atau video MP4.

**Requirements:**

- Pilih salah satu bentuk tugas dan jangan mengumpulkan keduanya sekaligus
- Jika memilih laporan, minimal 5 halaman dan harus dalam format PDF
- Jika memilih video, durasi minimal 7 menit dan harus dalam format MP4

**Yang Harus Dikumpulkan:**

- Laporan analisis dalam format PDF dengan minimal 5 halaman
- atau video analisis dalam format MP4 dengan durasi minimal 7 menit

**Deadline:**  
15 November 2026 pukul 20.00 WIB

**Checklist:**

- Pastikan hanya satu jenis tugas yang dipilih
- Periksa bahwa laporan memiliki minimal 5 halaman dan disimpan sebagai PDF
- Periksa bahwa video berdurasi minimal 7 menit dan disimpan sebagai MP4
- Verifikasi bahwa konten membahas penggunaan AI di sekolah
- Cek bahwa file dapat dibuka atau diputar dengan normal
- Kirim file sebelum batas waktu deadline

Menurut saya hasil setelah diperbaiki lebih aman karena AI masih memberikan bantuan tambahan, tetapi tidak membuat requirement baru yang tidak ada pada instruksi.

---

# Personal Reflection

### 1. Menurut kalian, bagian apa yang paling sulit dari project ini?

Menurut saya bagian yang paling sulit adalah saat awal menghubungkan FastAPI dengan LLM karena sebelumnya saya belum pernah membuat aplikasi seperti ini.

Awalnya saya juga masih bingung dengan fungsi API, endpoint, request body, `.env`, dan bagaimana hasil dari AI bisa masuk kembali ke aplikasi.

### 2. Bagian kode mana yang paling banyak dibantu oleh AI?

Bagian kode yang paling banyak dibantu oleh AI adalah koneksi FastAPI dengan Groq, pembuatan endpoint, error handling, prompt experiment, dan frontend menggunakan Gradio.

### 3. Setelah melihat kode tersebut, jelaskan menggunakan bahasa kalian sendiri bagaimana bagian tersebut bekerja.

Menurut pemahaman saya, user memasukkan instruksi tugas melalui Gradio.

Input tersebut diterima oleh FastAPI lalu dikirim ke Groq bersama system prompt.

LLM membaca instruksi tersebut dan menghasilkan analisis dalam bentuk JSON.

Setelah hasil diterima kembali oleh aplikasi, data ditampilkan di Gradio menjadi ringkasan tugas, requirement, hal yang harus dikumpulkan, deadline, dan checklist.

### 4. Menurut kalian, apa kekurangan terbesar dari aplikasi yang kalian buat jika digunakan oleh user sungguhan?

Menurut saya kekurangannya adalah hasil aplikasi masih bergantung pada bagaimana AI memahami instruksi yang diberikan.

Kalau instruksinya sangat panjang, ambigu, atau memiliki banyak kondisi, masih ada kemungkinan AI salah membaca atau menambahkan informasi.

Jadi hasil dari aplikasi tetap perlu dicek kembali dengan instruksi tugas aslinya.

### 5. Jika provider LLM kalian diganti, misalnya dari Groq ke Gemini atau OpenAI, bagian mana dari project yang menurut kalian perlu diubah?

Menurut saya bagian yang perlu diubah adalah library atau SDK provider, API key di `.env`,pembuatan client, nama model, dan bagian request ke LLM.

Sedangkan FastAPI, Gradio, input aplikasi, dan bentuk structured output masih bisa digunakan.

### 6. Setelah mencoba aplikasi kalian sendiri, apa satu improvement yang menurut kalian paling penting jika project ini dilanjutkan?

Kalau project ini dilanjutkan, saya ingin aplikasi bisa menerima file tugas seperti PDF atau dokumen secara langsung.

Sekarang user masih harus copy-paste instruksi tugas ke textbox. Kalau bisa upload file langsung, menurut saya aplikasi akan lebih praktis digunakan.

# AI Usage
### AI tools yang digunakan

ChatGPT.

### AI digunakan untuk membantu bagian apa?

Saya menggunakan AI untuk membantu memahami requirement tugas, menjelaskan konsep FastAPI dan LLM, membantu membuat kode, memperbaiki error, menyusun prompt, dan membuat frontend menggunakan Gradio.

AI juga membantu saya saat merapikan dokumentasi project.

### Bagian apa yang kalian tentukan, perbaiki, atau ubah sendiri setelah melihat hasil dari AI?

Saya memilih sendiri use case Assignment Requirement Analyzer dari beberapa pilihan yang ada.

Saya juga memilih menggunakan Gradio untuk frontend karena menurut saya lebih mudah dipahami dibanding menggunakan HTML, CSS, dan JavaScript.

Selama pengerjaan saya menjalankan project sendiri, mencoba input melalui /docs dan Gradio, melihat actual output, dan mengecek apakah hasil AI sudah sesuai dengan instruksi.

Saat testing saya juga menemukan bahwa AI sempat menambahkan contoh nama file yang sebenarnya tidak ada di instruksi. Setelah melihat hasil tersebut, saya memperbaiki constraint supaya AI masih bisa memberikan checklist tambahan yang membantu tetapi tidak membuat aturan spesifik baru.