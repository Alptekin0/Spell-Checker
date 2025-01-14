import tkinter as tk
from tkinter import ttk, messagebox
import grpc
import zemberek_grpc.normalization_pb2 as z_normalization
import zemberek_grpc.normalization_pb2_grpc as z_normalization_g
import re

# Zemberek gRPC bağlantısı
channel = grpc.insecure_channel('localhost:6789')
normalization_stub = z_normalization_g.NormalizationServiceStub(channel)#normalizasyona bağlantı için

def kontrol_et():
    metin = metin_alani.get("1.0", tk.END).strip()#temiz metin
    if not metin: # boş ise uyarı
        messagebox.showwarning("Uyarı", "Lütfen bir metin girin!")
        return

    # Zemberek ile normalizasyon işlemi
    try:
        response = normalization_stub.Normalize(z_normalization.NormalizationRequest(input=metin)) # zemberek normalizasyona metni gönder
        if response.normalized_input: # eğer yanıt varsa dönen metni normalize_text'a at
            normalized_text = response.normalized_input
        else:
            messagebox.showerror("Hata", f"Zemberek normalizasyonu başarısız: {response.error}")
            return
    except grpc.RpcError as e: #grpc hatası ise bağlantı hatasıdır.
        messagebox.showerror("Hata", f"Zemberek'e bağlanırken bir hata oluştu: {e}")
        return

    # Metni kelimelere ayır
    orijinal_kelimeler = re.findall(r"\w+", metin.lower())
    normal_kelimeler = re.findall(r"\w+", normalized_text.lower()) # her iki metni küçük harflere ayırır

    toplam_kelime = len(orijinal_kelimeler)
    dogru_kelime = 0
    hatalar = []

    # KARŞILAŞTIRMA KISMI
    for i, kelime in enumerate(orijinal_kelimeler): # Kelime = orjinal metin kelimesi i = kelimenin indeksi
        try:
            normal_kelime = normal_kelimeler[i]
        except IndexError:
            normal_kelime = kelime  # Eğer dizin dışı hata olursa, orijinal kelimeyi koru

        if kelime != normal_kelime:# Kelime normalleştirilmiş kelime ile aynı değilse
            hatalar.append({
                'kelime': kelime,
                'oneri': [normal_kelime] #zembereğin kelimesini öner
            })
        else: # kelime doğruysa kelime sayacını bir arttır
            dogru_kelime += 1

    # Sonuçları listeye ekleme
    hata_listesi.delete(*hata_listesi.get_children()) # kontrol sonrası arayüzdeeki hata listesini temizler
    if hatalar: # hatalar varsa
        for hata in hatalar: ## her bir hata için
            hata_listesi.insert("", tk.END, values=(hata['kelime'], ", ".join(hata['oneri']))) # hata listesine ekle
    else: #yoksa
        messagebox.showinfo("Sonuç", "Hiçbir yazım hatası bulunamadı!") #hata bulunamadı

    # Raporu güncelle
    hatali_kelime = len(hatalar) #hatalı kelimleri hesaplar
    rapor_label.config(
        text=f"Toplam Kelime: {toplam_kelime} | Doğru Kelime: {dogru_kelime} | Hatalı Kelime: {hatali_kelime}" #rapor kısmına yazar
    )


# Arayüz kısmı
root = tk.Tk()
root.title("Yazım Hatası Kontrolü")
root.geometry("1200x600")

# Üst çerçeve - metin girişi
ust_cerceve = tk.Frame(root, padx=10, pady=10)
ust_cerceve.pack(fill=tk.BOTH, expand=True)

tk.Label(ust_cerceve, text="Metni Girin:", font=("Arial", 12)).pack(anchor="w")
metin_alani = tk.Text(ust_cerceve, wrap=tk.WORD, height=8, font=("Arial", 10))
metin_alani.pack(fill=tk.BOTH, expand=True, pady=5)

# Kontrol Et butonu
kontrol_butonu = tk.Button(root, text="Kontrol Et", command=kontrol_et, font=("Arial", 12), bg="#007bff", fg="white")
kontrol_butonu.pack(pady=10)

# Rapor Label'ı
rapor_label = tk.Label(root, text="Toplam Kelime: 0 | Hatalı Kelime: 0", font=("Arial", 12))
rapor_label.pack(pady=10)

# Alt çerçeve - sonuçlar
alt_cerceve = tk.Frame(root, padx=10, pady=10)
alt_cerceve.pack(fill=tk.BOTH, expand=True)

tk.Label(alt_cerceve, text="Hatalı Kelimeler ve Öneriler:", font=("Arial", 12)).pack(anchor="w")

# Hata listesi
hata_listesi = ttk.Treeview(alt_cerceve, columns=("Kelime", "Öneriler"), show="headings", height=8)
hata_listesi.heading("Kelime", text="Kelime")
hata_listesi.heading("Öneriler", text="Öneriler")
hata_listesi.column("Kelime", width=150)
hata_listesi.column("Öneriler", width=400)
hata_listesi.pack(fill=tk.BOTH, expand=True)

# Tkinter döngüsü
root.mainloop()