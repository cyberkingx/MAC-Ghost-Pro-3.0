MAC Ghost Pro, ağ arayüzlerinizin MAC adreslerini gerçek üretici bilgilerine dayalı olarak değiştirmenizi sağlayan gelişmiş bir araçtır. Bu tool, penetrasyon testleri, ağ güvenlik denetimleri ve gizlilik gerektiren durumlar için tasarlanmıştır.


Gereksinimler
Tool'u çalıştırmak için aşağıdaki bağımlılıkları kurmanız gerekmektedir:

      sudo pip3 install keyboard colorama 



Gelişmiş Arayüz Kategorilendirme:
Ethernet (eth0, enp3s0 vb.)
Kablosuz (wlan0, wlp2s0 vb.)
Loopback (lo)
Diğer özel arayüzler
Gerçek Üretici MAC Veritabanı:
12 popüler üreticinin gerçek MAC adresi önekleri
Intel, Cisco, Apple, Samsung, AMD, Nvidia, Dell, Asus, Microsoft, HP, TP-Link, Razer
Akıllı Doğrulama Sistemi:
MAC adresinin seçtiğiniz üreticiye ait olup olmadığını kontrol
Yanlış üretici formatında girişleri engelleme
Hızlı Geri Dönüş Kısayolu:
Ctrl+K kombinasyonu ile anında orijinal MAC adresine dönüş
Çalışan uygulamayı kapatmadan MAC değiştirme
Kullanıcı Dostu Özellikler:
Renkli ve açıklayıcı terminal çıktıları
R tuşu ile otomatik rastgele MAC oluşturma
Örnek MAC adresleri gösterimi
Adım adım rehberlik
 
tool'u root yetkisiyle çalıştırmanız gerekmektedir:

      sudo python3 mac_ghost_pro.py



Temel Adımlar:
Ağ arayüzünüzü seçin (Ethernet, Kablosuz vb.)
Tercih ettiğiniz donanım üreticisini seçin
Gösterilen OUI örneklerini kullanarak yeni MAC adresi girin (veya 'R' ile rastgele oluşturun)
Tool, MAC adresinizi değiştirecek ve sonucu doğrulayacaktır
İstediğiniz zaman Ctrl+K ile orijinal MAC adresinize dönebilirsiniz
Teknik Detaylar
Sürücü Uyumluluğu: Linux Kernel 2.6+ sistemlerde test edilmiştir
Python Sürümü: Python 3.6 ve üzeri desteklenir
Ağ Yönetimi: ifconfig komut seti kullanılarak gerçekleştirilir
Gizlilik: Veritabanı sadece gerçek üretici MAC OUI'lerini içerir
Hata Ayıklama: Kapsamlı hata yakalama ve kullanıcı geri bildirimleri
Güvenlik Notları
MAC adresi değiştirme işlemi, bazı ağlarda TOS (Hizmet Şartları) ihlali sayılabilir
Sadece kendi ağınızda veya izinli testlerde kullanın
Bu tool eğitim ve güvenlik araştırmaları için tasarlanmıştır

                  Katkıda Bulunma
                  Geliştirmeler ve hata raporları için GitHub üzerinden pull request oluşturabilirsiniz.

![1](https://github.com/user-attachments/assets/07685d7a-974e-4ff0-899f-a776b36f3527)

![2](https://github.com/user-attachments/assets/4cb7ecc8-7ad5-4e1e-9c23-4895a12faeea)

