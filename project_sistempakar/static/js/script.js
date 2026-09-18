// Konfigurasi Label Kelas (Asumsikan array output model AI sesuai urutan ini)
// Sesuaikan indeks ini dengan konfigurasi kelas saat training MobileNetV2
const CLASS_NAMES = ['K02', 'K01', 'K04', 'K03']; // Herpes, Jerawat, Kutil, Panu (Urutan Alfabetis Folder Dataset)

let model;

// Memuat Model AI
async function loadModel() {
    try {
        console.log("Loading AI model from /static/model/model.json...");
        model = await tf.loadGraphModel('/static/model/model.json');
        console.log("Model loaded successfully!");
    } catch (error) {
        console.error("Error loading model:", error);
        console.warn("Pastikan Anda telah meletakkan model.json dan file .bin di /static/model/");
    }
}

// Inisialisasi saat script dimuat
loadModel();

// Elemen DOM
const imagePreview = document.getElementById('preview-img');
const btnPredict = document.getElementById('btn-proses');
const loadingIndicator = document.getElementById('loadingIndicator');
const predictionResult = document.getElementById('predictionResult');

// ==========================================
// FUNGSI HEURISTIK KUALITAS GAMBAR (SKIN & LUMINANCE)
// ==========================================
function analyzeImageQuality(imgElement) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    // Batasi ukuran agar komputasi pixel tidak berat
    const maxWidth = 300;
    let width = imgElement.naturalWidth || imgElement.width;
    let height = imgElement.naturalHeight || imgElement.height;
    
    if (width > maxWidth) {
        const ratio = maxWidth / width;
        width = maxWidth;
        height = height * ratio;
    }
    
    canvas.width = width;
    canvas.height = height;
    ctx.drawImage(imgElement, 0, 0, width, height);
    
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data;
    
    let skinPixels = 0;
    let totalLuminance = 0;
    const totalPixels = width * height;
    
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i];
        let g = data[i+1];
        let b = data[i+2];
        
        // Luminance (Kecerahan)
        let lum = 0.299*r + 0.587*g + 0.114*b;
        totalLuminance += lum;
        
        // Aturan RGB untuk warna kulit manusia secara umum
        if (r > 95 && g > 40 && b > 20 && 
            (Math.max(r,g,b) - Math.min(r,g,b)) > 15 && 
            Math.abs(r-g) > 15 && r > g && r > b) {
            skinPixels++;
        }
    }
    
    const skinPercentage = (skinPixels / totalPixels) * 100;
    const avgLuminance = totalLuminance / totalPixels;
    
    return { skinPercentage, avgLuminance };
}

// Menangani tombol proses (Hibrida)
if (btnPredict) {
    btnPredict.addEventListener('click', async () => {
        if (!model) {
            alert("Model AI belum termuat sepenuhnya. Harap tunggu.");
            return;
        }

        // Tampilkan indikator loading dan nonaktifkan tombol
        loadingIndicator.classList.remove('d-none');
        btnPredict.disabled = true;
        predictionResult.innerHTML = '';

        try {
            // ==========================================
            // 0. VALIDASI KUALITAS GAMBAR (BUKAN KULIT & GELAP)
            // ==========================================
            const imgQuality = analyzeImageQuality(imagePreview);
            console.log("Hasil Analisis Kualitas Gambar:", imgQuality);
            
            // Cek Pencahayaan (Luminance di bawah 40 = sangat gelap)
            if (imgQuality.avgLuminance < 40) {
                alert("Pencahayaan terlalu gelap! Harap pastikan foto diambil di tempat yang terang.");
                throw new Error("Foto terlalu gelap.");
            }
            
            // Cek Deteksi Kulit (Jika < 25% pixel kulit terdeteksi, tolak!)
            if (imgQuality.skinPercentage < 25) {
                alert("Gambar Ditolak! Harap unggah foto penyakit kulit dari jarak dekat (Close-up) melalui Galeri Anda, bukan foto selfie/wajah dari kamera.");
                throw new Error("Persentase kulit terlalu rendah atau objek bukan kulit.");
            }

            // ==========================================
            // 1. PREPROCESSING GAMBAR & PREDIKSI AI
            // ==========================================
            
            // Konversi gambar menjadi tensor berukuran 224x224 (RGB)
            const tensor = tf.browser.fromPixels(imagePreview)
                .resizeNearestNeighbor([224, 224])
                .toFloat();
            
            // Normalisasi (menyesuaikan metode saat training, misal: dibagi 255.0)
            const offset = tf.scalar(255.0);
            const normalized = tensor.div(offset).expandDims(); // Tambahkan dimensi batch
            
            // Eksekusi Prediksi Asynchronous
            const predictions = await model.predict(normalized).data();
            
            // Format Hasil AI ke dalam Objek
            let aiPredictionResult = {};
            for (let i = 0; i < CLASS_NAMES.length; i++) {
                aiPredictionResult[CLASS_NAMES[i]] = predictions[i];
            }
            console.log("Output MobileNetV2:", aiPredictionResult);

            // ==========================================
            // 2. MENGAMBIL DATA GEJALA DARI FORM HTML
            // ==========================================
            
            let gejalaUser = [];
            
            // Ambil semua checkbox gejala yang dicentang user
            const checkedGejala = document.querySelectorAll('.gejala-checkbox:checked');
            checkedGejala.forEach(cb => {
                const kodeGejala = cb.value;
                // Ambil nilai certainty factor dari select box yang berpasangan
                const cfValue = document.getElementById(`cf_${kodeGejala.toLowerCase()}`).value;
                
                gejalaUser.push({
                    "kode_gejala": kodeGejala,
                    "cf_user": parseFloat(cfValue)
                });
            });

            if (gejalaUser.length === 0) {
                alert("Mohon pilih setidaknya satu gejala klinis.");
                loadingIndicator.classList.add('d-none');
                btnPredict.disabled = false;
                return;
            }

            // ==========================================
            // 3. KIRIM DATA KE FLASK (FETCH / AJAX)
            // ==========================================
            
            const response = await fetch('/proses_diagnosis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "ai_prediction": aiPredictionResult,
                    "gejala": gejalaUser
                })
            });

            if (!response.ok) {
                throw new Error("Gagal terhubung dengan server (Backend).");
            }

            const data = await response.json();
            console.log("Response dari Flask:", data);

            // ==========================================
            // 4. TAMPILKAN HASIL AKHIR
            // ==========================================
            
            predictionResult.innerHTML = `
                <div class="alert alert-success mt-4 text-start shadow-sm border-0">
                    <h5 class="fw-bold mb-3 border-bottom pb-2 text-success"><i class="fa-solid fa-clipboard-check me-2"></i>Laporan Analisis Hibrida</h5>
                    
                    <div class="row mb-4 align-items-center">
                        <div class="col-md-6 text-center mb-3 mb-md-0">
                            <p class="small text-muted fw-bold mb-2">FOTO LESI ANDA</p>
                            <img src="${imagePreview.src}" class="img-fluid rounded shadow-sm border" style="max-height: 200px; object-fit: cover;">
                        </div>
                        <div class="col-md-6 text-center">
                            <p class="small text-muted fw-bold mb-2">REFERENSI MEDIS (${data.hybrid_result.nama_akhir.toUpperCase()})</p>
                            <img src="/static/img/ref_${data.hybrid_result.kode_akhir}.jpg" class="img-fluid rounded shadow-sm border" style="max-height: 200px; object-fit: cover;" onerror="this.src='https://placehold.co/400x300/e9ecef/495057?text=Gambar+Tidak+Tersedia'">
                        </div>
                    </div>

                    <div class="bg-white p-3 rounded shadow-sm mb-3">
                        <p class="mb-2"><i class="fa-solid fa-robot text-primary me-2"></i><strong>Deteksi Visual AI:</strong> ${data.ai_result.nama} <span class="badge bg-primary rounded-pill ms-1">${data.ai_result.persentase}%</span></p>
                        <p class="mb-0"><i class="fa-solid fa-stethoscope text-info me-2"></i><strong>Deteksi Gejala Pakar:</strong> ${data.cf_result.nama} <span class="badge bg-info rounded-pill ms-1">${data.cf_result.persentase}%</span></p>
                    </div>

                    <div class="p-3 rounded shadow-sm" style="background-color: #f8f9fa; border-left: 5px solid #198754;">
                        <p class="mb-1 text-success fw-bold">Kesimpulan Diagnosis:</p>
                        <p class="mb-2 text-dark">${data.hybrid_result.kesimpulan}</p>
                        <h4 class="mt-3 text-success fw-bolder mb-3">Tingkat Keyakinan Akhir: ${data.hybrid_result.persentase_akhir}%</h4>
                        
                        <div class="alert alert-warning mb-0 border-0" style="background-color: #fff3cd;">
                            <h6 class="fw-bold text-warning-emphasis mb-2"><i class="fa-solid fa-user-doctor me-2"></i>Saran & Penanganan Sementara:</h6>
                            <p class="mb-0 text-dark small">${data.hybrid_result.solusi}</p>
                        </div>
                    </div>
                </div>
            `;

        } catch (error) {
            console.error("Error pada proses hibrida:", error);
            alert("Terjadi kesalahan saat memproses data. Silakan cek console log.");
        } finally {
            loadingIndicator.classList.add('d-none');
            btnPredict.disabled = false;
        }
    });
}

