from fastapi import FastAPI

app = FastAPI()

# 1. Peta Data (Graph)
peta = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# 2. Fungsi DFS dengan Target Tujuan (Sesuai Teori Slide)
def dfs_cari_tujuan(graf, titik_sekarang, tujuan, sudah_dikunjungi=None, hasil_jalur=None):
    if sudah_dikunjungi is None:
        sudah_dikunjungi = set()
        hasil_jalur.clear() # Kosongkan jalur tiap kali request baru
    
    if titik_sekarang not in sudah_dikunjungi:
        sudah_dikunjungi.add(titik_sekarang)
        hasil_jalur.append(titik_sekarang)
        
        # LANGKAH 1 (Dari Slide): Jika ini adalah goal state, quit dan return success (True)
        if titik_sekarang == tujuan:
            return True 
            
        # LANGKAH 2a: Tentukan successor (cabang)
        if titik_sekarang in graf:
            for cabang in graf[titik_sekarang]:
                # LANGKAH 2b: Jalankan DFS dengan cabang sebagai initial state baru
                sukses = dfs_cari_tujuan(graf, cabang, tujuan, sudah_dikunjungi, hasil_jalur)
                
                # LANGKAH 2c: Jika success dihasilkan dari cabang bawah, langsung teruskan sinyal success ke atas
                if sukses:
                    return True
                    
    # Sinyal Gagal jika jalur ini buntu
    return False

# 3. Endpoint API yang menerima Titik Awal DAN Tujuan
@app.get("/jalur-dfs/{titik_awal}/{tujuan}")
def cari_jalur(titik_awal: str, tujuan: str):
    # Validasi input
    if titik_awal not in peta:
        return {"pesan": f"Gagal: Titik awal '{titik_awal}' tidak ada di peta!"}
    
    # Menyiapkan list kosong untuk diisi oleh fungsi rekursif
    jalur_ditemukan = []
    
    # Menjalankan algoritma
    apakah_ketemu = dfs_cari_tujuan(peta, titik_awal, tujuan, hasil_jalur=jalur_ditemukan)
    
    # Menentukan hasil akhir untuk ditampilkan ke pengguna
    if apakah_ketemu:
        return {
            "status": "Sukses",
            "pesan": f"Titik {tujuan} berhasil ditemukan!",
            "rute_pencarian": jalur_ditemukan
        }
    else:
        return {
            "status": "Gagal",
            "pesan": f"Titik {tujuan} tidak bisa dijangkau dari {titik_awal}.",
            "rute_pencarian": jalur_ditemukan
        }