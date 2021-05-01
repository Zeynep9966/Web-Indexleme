from flask import Flask, render_template, request, redirect, url_for

import requests
from bs4 import BeautifulSoup
import operator
import wtforms
from wtforms import Form
import re
from collections import ChainMap

app = Flask(__name__)

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def sozlukolustur(tumkelimeler):
    kelimesayisi = {}

    for kelime1 in tumkelimeler:
        if kelime1 in kelimesayisi:
            kelimesayisi[kelime1] += 1
        else:
            kelimesayisi[kelime1] = 1

    return kelimesayisi

def yakin_kelimeler_bul(url_indexleme_frekans):

    yeni_sozluk = {}
    yakin_anlam_sozlugu = { "abide": "anıt", "acayip": "garip", "acıma": "merhamet", "açıkgöz": "kurnaz", "ad": "isim", "adale": "kas", "adet": "tane", "aferin": "bravo", "affetmek": "bağışlamak", 
                            "ahenk": "uyum", "akıl":"us", "aksi":"ters", "al":"kırmızı", "alaka":"ilgi", "alaz":"alev", "alelade":"sıradan", "amale":"işçi", "amel":"iş", "ana":"anne", "aniden":"birden", "anlam":"mana",
                            "anlatım":"ifade", "ant":"yemin", "apse":"iltihap", "araç":"vasıta", "arıza":"bozukluk", "arka":"geri", "armağan":"hediye", "art":"arka", "arzu":"istek", "asır":"yüzyıl", "asil":"soylu", "aş":"yemek",
                            "atak":"girişken", "avare":"aylak", "ayrıcalık":"imtiyaz", "acemi":"toy", "adalet":"hak", "aka":"büyük", "aleni":"açık", "ayakkabı":"pabuç", "bağnaz":"yobaz", "barış":"sulh", "basımevi":"matbaa",
                            "basit":"yalın", "başkaldırı":"isyan", "başkan":"reis", "başvuru":"müracaat", "batı":"garp", "baytar":"veteriner", "beğeni":"gusto", "belde":"şehir", "belge":"vesika", "bellek":"hafıza", 
                            "benlik":"kişilik", "bencil":"egoist", "beraber":"birlikte", "bereket":"bolluk", "besin":"gıda", "beyaz":"ak", "beygir":"at", "beyhude":"boşuna", "biçare":"zavallı", "biçim":"şekil", 
                            "bilakis":"tersine", "bilgin":"alim", "bilgisiz":"cahil", "bilhassa":"özellikle", "bilim":"ilim", "bilgisiz":"cahil", "bilinç":"şuur", "bina":"yapı", "birden":"ani", "birdenbire":"aniden", "birey":"fert",
                            "biricik":"tek", "bucak":"nahiye", "buğu":"buhar", "buhran":"bunalım", "buyruk":"emir", "büro":"ofis", "baş":"kafa", "caka":"gösteriş", "camekan":"vitrin", "canlı":"diri", "cazibe":"çekim",
                            "cenk":"savaş", "cerrah":"operatör", "cesur":"yürekli", "cevap":"yanıt", "cılız":"sıska", "ciddi":"ağırbaşlı", "cihaz":"aygıt", "cilt":"ten", "cimri":"pinti", "cins":"tür", "civar":"yöre", 
                            "cömert":"eli açık", "cümle":"tümce", "çabuk":"acele", "çağ":"devir", "çağdaş":"modern", "çağrı":"davet", "çeviri":"tercüme", "çılgın":"deli", "çizelge":"cetvel", "çare":"deva", "daimi":"sürekli",
                            "darbe":"vuruş", "dargın":"küs", "darılmak":"küsmek", "değer":"kıymet", "değerli":"kıymetli", "değnek":"sopa", "delil":"kanıt", "deneyim":"tecrübe", "denetim":"kontrol", "deprem":"zelzele",
                            "dergi":"mecmua", "derhal":"hemen", "derslik":"sınıf", "devamlı":"sürekli", "devinim":"hareket", "devir":"tur", "devre":"dönem", "dışalım":"ithalat", "dışsatım":"ihracat", "dil":"lisan", "doğa":"tabiat",
                            "doğal":"tabii", "doğu":"şark", "doktor":"hekim", "donuk":"mat", "doruk":"zirve", "dönemeç":"viraj", "döşek":"yatak", "duru":"berrak", "durum":"vaziyet", "duygu":"his", "düş":"rüya", "düşünce":"fikir",
                            "düzen":"seviye", "düzmece":"sahte", "dilek":"istek", "dizi":"sıra", "dost":"arkadaş", "ebat":"boyut", "ebedi":"sonsuz", "edat":"ilgeç", "efe":"zeybek", "ehemmiyet":"önem", "ek":"ilave", 
                            "eklem":"mafsal", "ekonomi":"iktisat", "elbise":"giysi", "emniyet":"güvenlik", "ender":"nadir", "endişe":"kaygı", "endüstri":"sanayi", "enkaz":"yıkıntı", "enlem":"paralel", "enteresan":"ilginç", 
                            "eser":"yapıt", "esir":"tutsak", "etki":"tesir", "etraf":"çevre", "eylem":"fiil", "ev":"konut", "faliyet":"etkinlik", "fakir":"yoksul", "fayda":"yarar", "faktör":"unsur", "fena":"kötü", "ağ":"file",
                            "füze":"roket", "gebe":"hamile", "giz":"sır", "görev":"vazife", "gövde":"beden", "güç":"kuvvet", "gülünç":"komik", "güven":"itimat", "güz":"sonbahar", "gökyüzü":"sema", "ham":"olmamış",
                            "harp":"savaş", "hasret":"özlem", "hatıra":"anı", "hayal":"düş", "hayat":"yaşam", "hiddet":"öfke", "hisse":"pay", "hususi":"özel", "hür":"özgür", "ırak":"uzak", "ırk":"soy", "ırmak":"nehir",
                            "içten":"samimi", "ihtiyar":"yaşlı", "ihtiyaç":"gereksinim", "ilan":"duyuru", "kalite":"nitelik", "kalp":"yürek", "kanıt":"delil", "kanun":"yasa", "kara":"siyah", "katı":"sert", "kelime":"sözcük",
                            "kayıp":"yitik", "kir":"pislik", "kişi":"şahıs", "konuk":"misafir", "koşul":"şart", "kuşku":"şüphe", "küme":"grup", "mabet":"tapınak", "macera":"serüven", "mağlup":"yenik", "mahcup":"utangaç",
                            "mahluk":"yaratık", "mecbur":"zorunlu", "mektep":"okul", "mutlu":"mesut", "meşhur":"ünlü", "millet":"ulus", "milli":"ulusal", "muavin":"yardımcı", "muştu":"müjde", "mühim":"önemli", 
                            "mükafat":"ödül", "müsait":"uygun", "müşteri":"alıcı", "mani":"engel", "muallim":"öğretmen", "merasim":"tören", "nasihat":"öğüt", "nefes":"soluk", "neden":"sebep", "nesil":"kuşak", 
                            "nem":"rutubet", "nispet":"oran", "nutuk":"söylev", "olay":"vaka", "onarım":"tamir", "onay":"tasdik", "onur":"şeref", "ödlek":"korkak", "ödül":"mükafat", "ödün":"taviz", "öğe":"unsur", 
                            "öğrenci":"talebe", "öğrenim":"tahsil", "öneri":"teklif", "özgün":"orijinal", "politika":"siyaset", "problem":"sorun", "sade":"yalın", "sağlık":"sıhhat", "sene":"yıl", "sima":"yüz", "sömestr":"yarıyıl",
                            "suni":"yapay", "surat":"yüz", "şafak" : "tan", "şahit" : "tanık", "şans" : "talih", "tanım" : "tarif", "taraf" : "yan", "tarım" : "ziraat", "tekrar" : "yine", "tümör" : "ur", "ufak" : "küçük", "ulu" : "yüce",
                            "umut" : "ümit", "vakit" : "zaman", "varlıklı" : "zengin", "vatan" : "yurt", "zarar" : "ziyan" }
   
    for keys in yakin_anlam_sozlugu.keys():
            for values in yakin_anlam_sozlugu.values():
                for keyy in url_indexleme_frekans.keys():                    
                    if (keys==keyy):
                        for valuee in url_indexleme_frekans.keys():        
                            if (values == valuee) :
                                yeni_sozluk.setdefault(keyy, yakin_anlam_sozlugu[keyy])
                                #print("Yakin Anlamlilar: ", keyy, yakin_anlam_sozlugu[keyy])
    return yeni_sozluk


def indexleme_ilk_kelime_anahtar_kelime_bulma(url_ana_indexleme):
    url_ana_indexleme_tumkelimeler = []
    url_ana_indexleme_anahtar_kelimesayisi_ilk_bes = {}

    url_anahtar_r = requests.get(url_ana_indexleme)
    url_anahtar_soup = BeautifulSoup(url_anahtar_r.content, 'html.parser')

    for url_ana_indexleme_kelimegruplari in url_anahtar_soup.find_all(['p', 'span', 'li']):
        url_ana_indexleme_icerik = url_ana_indexleme_kelimegruplari.text
        url_ana_indexleme_kelimeler = url_ana_indexleme_icerik.lower().split()

        for url_ana_indexleme_kelime in url_ana_indexleme_kelimeler:
            url_ana_indexleme_tumkelimeler.append(url_ana_indexleme_kelime)

    # Gereksiz kelimlerden ayıklama işlemi
    url_ana_indexleme_kelimeler = sembolleritemizle(url_ana_indexleme_tumkelimeler)
    url_ana_indexleme_tumkelimeler_soz = sozlukolustur(url_ana_indexleme_kelimeler)
    url_ana_indexleme_tumkelimeler_temiz = yasakli_kelimel_ayiklama(url_ana_indexleme_tumkelimeler_soz)

    # Anahtar kelime oluşturma işlemi
    url_ana_indexleme_tumkelimeler_temiz_sorted = sorted(url_ana_indexleme_tumkelimeler_temiz.items(),
                                                         key=operator.itemgetter(1))
    url_ana_indexleme_kelimesayisi = {k: v for k, v in url_ana_indexleme_tumkelimeler_temiz_sorted}
    j = 0
    for i in list(reversed(list(url_ana_indexleme_kelimesayisi)))[0:5]:
        url_ana_indexleme_anahtar_kelimesayisi_ilk_bes[j] = i
        j += 1
    # print("url_ana_indexleme_anahtar_kelimesayisi_ilk_bes:",url_ana_indexleme_anahtar_kelimesayisi_ilk_bes)
    # ("url_1_anahtar_kelimesayisi_ilk_bes", url_ana_indexleme_anahtar_kelimesayisi_ilk_bes)
    return url_ana_indexleme_anahtar_kelimesayisi_ilk_bes


def url_kelime_bulma(url_indexleme):
    url_indexleme_tumkelimeler = []

    url_r = requests.get(url_indexleme)
    url_soup = BeautifulSoup(url_r.content, 'html.parser')

    for url_indexleme_kelimegruplari in url_soup.find_all(['p', 'span', 'li']):
        url_indexleme_icerik = url_indexleme_kelimegruplari.text
        url_indexleme_kelimeler = url_indexleme_icerik.lower().split()

        for url_indexleme_kelime in url_indexleme_kelimeler:
            url_indexleme_tumkelimeler.append(url_indexleme_kelime)

    # Gereksiz kelimlerden ayıklama işlemi
    url_indexleme_kelimeler = sembolleritemizle(url_indexleme_tumkelimeler)
    url_indexleme_tumkelimeler_soz = sozlukolustur(url_indexleme_kelimeler)
    url_indexleme_kelime_freakans = yasakli_kelimel_ayiklama(url_indexleme_tumkelimeler_soz)

    # print("url_indexleme_kelime_freakans:",url_indexleme_kelime_freakans)

    return url_indexleme_kelime_freakans


def anahtar_kelime_frekansi(kelimesayisi, url_anahtar_kelimesayisi_ilk_bes):
    url_anahtar_kelimeler_frekans = {}
    for url_tumkelimeler_key in kelimesayisi:
        for index in url_anahtar_kelimesayisi_ilk_bes:
            if url_tumkelimeler_key == url_anahtar_kelimesayisi_ilk_bes[index]:
                url_anahtar_kelimeler_frekans[url_tumkelimeler_key] = kelimesayisi[
                    url_tumkelimeler_key]
    return url_anahtar_kelimeler_frekans


def anahtar_kelime_arama_ve_skor_islemi(ana_url_anahtar_kelimesayisi_ilk_bes, aranacak_url_anahtar_kelimesayisi):
    url_ortak_anahtar_kelimeler = {}

    for aranacak_url_tumkelimeler_key in aranacak_url_anahtar_kelimesayisi:
        for index in ana_url_anahtar_kelimesayisi_ilk_bes:
            if aranacak_url_tumkelimeler_key == ana_url_anahtar_kelimesayisi_ilk_bes[index]:
                url_ortak_anahtar_kelimeler[aranacak_url_tumkelimeler_key] = aranacak_url_anahtar_kelimesayisi[
                    aranacak_url_tumkelimeler_key]

        toplam = 0.0
        Skor = 0.0
        for index in aranacak_url_anahtar_kelimesayisi:
            # print(index)
            toplam += aranacak_url_anahtar_kelimesayisi[index]
        # print("toplam",toplam)
        sayaç = 0.0
        top = 0.0
        sya = 0.0
        for indexi in url_ortak_anahtar_kelimeler:
            top += url_ortak_anahtar_kelimeler[indexi]
            # print("url_ortak_anahtar_kelimeler[indexi]: ",url_ortak_anahtar_kelimeler[indexi])

        Skor = (top) / toplam
        # print("top ",top)

    return Skor


class RegisterForm(wtforms.Form):
    URL1 = wtforms.StringField("URL1", validators=[wtforms.validators.url()])
    URL2 = wtforms.StringField("URL2", validators=[wtforms.validators.url()])


# Anahtar Kelime sayfası için Form
class RegisterFormAnahtar(wtforms.Form):
    URL = wtforms.StringField("URL", validators=[wtforms.validators.url()])


class siteindexleme(wtforms.Form):
    URL1 = wtforms.StringField("URL1", validators=[wtforms.validators.url()])
    URL2 = wtforms.StringField("URL2", validators=[wtforms.validators.url()])
    URL3 = wtforms.StringField("URL3", validators=[wtforms.validators.url()])
    URL4 = wtforms.StringField("URL4", validators=[wtforms.validators.url()])
    URL5 = wtforms.StringField("URL5", validators=[wtforms.validators.url()])
    URL6 = wtforms.StringField("URL6", validators=[wtforms.validators.url()])
class semantikanaliz(wtforms.Form):
    URL1 = wtforms.StringField("URL1", validators=[wtforms.validators.url()])
    URL2 = wtforms.StringField("URL2", validators=[wtforms.validators.url()])
    URL3 = wtforms.StringField("URL3", validators=[wtforms.validators.url()])
    URL4 = wtforms.StringField("URL4", validators=[wtforms.validators.url()])
    URL5 = wtforms.StringField("URL5", validators=[wtforms.validators.url()])
    URL6 = wtforms.StringField("URL6", validators=[wtforms.validators.url()])

def birinci_dallanma(url_birinci_indexleme):
    links = []
    sayac = 0

    birinci_url_birinci_dallanma_r = requests.get(url_birinci_indexleme)
    birinci_url_birinci_dallanma_soup = BeautifulSoup(birinci_url_birinci_dallanma_r.content, 'html.parser')

    for link in birinci_url_birinci_dallanma_soup.findAll('a', attrs={'href': re.compile("^https://")}):
        links.append(link.get('href'))

    return links


def asama4dallanma(ucuncu_url_dallanma_linkleri, url_ana_indexleme_anahtar_kelime_ilk_bes):
    dallanma = {}
    index3 = 0
    sayac = 0
    while index3 < 3:

        ucuncu_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(
            ucuncu_url_dallanma_linkleri[index3])

        if bool(ucuncu_url_ikinci_dallanma_link_frekanslari):
            ucuncu_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                url_ana_indexleme_anahtar_kelime_ilk_bes,
                ucuncu_url_ikinci_dallanma_link_frekanslari)

            ucuncu_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                ucuncu_url_dallanma_linkleri[index3])
            ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                ucuncu_url_ikinci_dallanma_link_frekanslari, ucuncu_url_ikinci_dallanma_anahtar_kelimeleri)
            dallanma[ucuncu_url_dallanma_linkleri[index3]] = [ucuncu_url_ikinci_dallanma_url_skor,
                                                              ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi]
            index3 += 1
    return dallanma


def sembolleritemizle(tumkelimeler):
    sembolsuzkelimeler = []
    semboller = "!ღ⁂€™↑→↓⇝√∞✔¶§⋮⌃♡♥★☆▶↺↪⇆△·▴⊗☺✈☀☁☂☃☽☾❄❝❞অসমীয়া☯⊕⦿◯⊘◦➢➡∫≠‰‱π∑¬∴⊥≡℃⁰¹²³⁴⁵⁶⁷⁸⁹𝝅Æ˙@❡฿'^+%&/()=?*£#${[]}.,:;\`<>_-|'+-•" + chr(
        775) + chr(250)
    for temizleme_kelime in tumkelimeler:
        for sembol in semboller:
            if sembol in temizleme_kelime:
                temizleme_kelime = temizleme_kelime.replace(sembol, "")

        if (len(temizleme_kelime) > 0):
            sembolsuzkelimeler.append(temizleme_kelime)

    return sembolsuzkelimeler


tumkelimeler = []


def yasakli_kelimel_ayiklama(url_anahtar_kelimesayisi):
    yasakli_kelimeler = {"bir", "gibi", "ve", "ile", "sonra", "önce", "ancak", "değil", "hayır", "şey", "sen", "bana",
                         "sana", "beni", "seni",
                         "bu", "o", "de", "eğer", "kimse", "daha", "mi", "için", "ne", "çok", "ben", "evet", "var",
                         "mı", "mu", "mü", "ama",
                         "herkes", "onun", "onunla", "da", "ya", "to", "with", "1", "2", "3", "4", "5", "sign", "in",
                         "iyi", "tamam", "onu", "bunu",
                         "of", "copied", "clipboard", "mar", "app", "the", "and", "benim", "yok", "her", "ki", "sadece",
                         "burada", "neden",
                         "senin", "hiç", "şimdi", "nasıl", "olduğunu", "en", "misin", "musun", "şu", "hey", "hadi",
                         "öyle", "biraz", "ona",
                         "bak", "böyle", "şöyle", "oldu", "olacak", "istiyor", "istiyorum", "istiyorsun", "geri", "kim",
                         "bay", "yani",
                         "çünkü", "peki", "belki", "başka", "buraya", "olarak", "tek", "efendim", "haydi", "olan",
                         "işte", "orada", "sanırım",
                         "nerede", "biz", "demek", "hiçbir", "ederim", "fazla", "yeni", "bunun", "iki", "kez", "tüm",
                         "kötü", "olsun", "oh",
                         "ol", "tam", "küçük", "şeyler", "siz", "şeyi", "hemen", "size", "sizin", "git", "ver",
                         "onları", "sizi", "bizi",
                         "bize", "bizim", "gerek", "e", "mısın", "müsün", "dur", "kendi", "diye", "hala", "tabi", "al",
                         "şunu", "söyle",
                         "yoksa", "ister", "değilim", "üç", "yüzden", "tekrar", "yine", "hep", "miyim", "muyum",
                         "mıyım", "neler", "niçin",
                         "nedir", "bekle", "göre", "kaç", "dan", "den", "lazım", "tane", "ı", "i", "u", "ü", "a", "e",
                         "karşı", "anda", "for",
                         "ha", "hoş", "az", "an", "ah", "ey", "kes", "ye", "falan", "filan", "etti", "beri", "veya",
                         "sanki", "meğerki", "soup",
                         "oysaki", "halbuki", "la", "lan", "le", "len", "dr", "öyleyse", "pekala", "ilk", "son",
                         "neyse", "alo", "on", "ise",
                         "henüz", "birisi", "olsa", "neredeyse", "vay", "be", "bin", "nun", "yapma", "yeniden", "ta",
                         "le", "şeyin", "böylece",
                         "hatta", "ait", "bi", "varsa", "neyin", "te", "dek", "sam", "tom", "m", "yu", "niçin", "defa",
                         "iyisi", "b", "dair"
                         }
    istenenkelimesayisi = {}

    for istenenkelime1 in url_anahtar_kelimesayisi:
        if istenenkelime1 in yasakli_kelimeler:
            continue
        else:
            istenenkelimesayisi[istenenkelime1] = url_anahtar_kelimesayisi[istenenkelime1]
    return istenenkelimesayisi


@app.route("/")
def deneme():
    return render_template("index.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/asama1", methods=["GET", "POST"])
def asama1():
    tumkelimeler1 = []
    kelimeler1 = []
    degerler1 = []
    url_anahtar_kelimesayisi_ilk_bes = {}
    url_anahtar_kelimeler_frekans = {}
    if request.method == "POST":  # eğer methodumuz post ise işlemleri yap dedik.
        url = request.form["url"]  # burada formda ki name parametremizin ismi ile ad verisini istedik.
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        for url_1_kelimegruplari in soup.find_all(['p', 'span', 'li']):
            url_1_icerik = url_1_kelimegruplari.text
            kelimeler = url_1_icerik.lower().split()

            for url_1_kelime in kelimeler:
                tumkelimeler1.append(url_1_kelime)

        tumkelimeler = sembolleritemizle(tumkelimeler1)
        kelimesayisi = sozlukolustur(tumkelimeler)
        kelimesayisi = yasakli_kelimel_ayiklama(kelimesayisi)

        for anahtar, deger in sorted(kelimesayisi.items(), key=operator.itemgetter(0)):
            # print(anahtar, deger)
            kelimeler1.append(anahtar)
            degerler1.append(deger)

        url_tumkelimeler_temiz_sorted = sorted(kelimesayisi.items(),
                                               key=operator.itemgetter(1))
        url_kelimesayisi = {k: v for k, v in url_tumkelimeler_temiz_sorted}
        j = 0
        for i in list(reversed(list(url_kelimesayisi)))[0:5]:
            url_anahtar_kelimesayisi_ilk_bes[j] = i
            j += 1

        for url_tumkelimeler_key in kelimesayisi:
            for index in url_anahtar_kelimesayisi_ilk_bes:
                if url_tumkelimeler_key == url_anahtar_kelimesayisi_ilk_bes[index]:
                    url_anahtar_kelimeler_frekans[url_tumkelimeler_key] = kelimesayisi[
                        url_tumkelimeler_key]
        print("url_anahtar_kelimeler_frekans:", url_anahtar_kelimeler_frekans)
        return render_template("asama1.html", kelimesayisi=kelimesayisi,
                               url_anahtar_kelimeler_frekans=url_anahtar_kelimeler_frekans)


@app.route("/frekans-hesapla")
def frekans():
    return render_template("frekans_hesapla.html")


@app.route("/anahtar-kelime-benzerlik")
def anahtar_kelime_benzerlik():
    return render_template("anahtar_kelime_benzerlik.html")


@app.route("/asama23", methods=["GET", "POST"])
def asama23():
    url_1_anahtar_kelimesayisi_ilk_bes = {}
    url_1_anahtar_tumkelimeler = []
    url_2_anahtar_tumkelimeler = []
    url_2_anahtar_kelimesayisi = {}

    url_ortak_anahtar_kelimeler = {}
    # İlk url için işlemler

    form = RegisterForm(request.form)
    form.validate()

    if request.method == "POST" and form.validate():  # eğer methodumuz post ise işlemleri yap dedik.

        url_anahtar_tumkelimeler = []
        url_anahtar_kelime_frekans = {}
        url_anahtar_kelimesayisi_ilk_bes = {}

        if request.method == "POST":  # eğer methodumuz post ise işlemleri yap dedik.

            url_1_anahtar_url = form.URL1.data  # burada formda ki name parametremizin ismi ile ad verisini istedik.
            url_1_anahtar_r = requests.get(url_1_anahtar_url)
            url_1_anahtar_soup = BeautifulSoup(url_1_anahtar_r.content, 'html.parser')

            for url_1_anahtar_kelimegruplari in url_1_anahtar_soup.find_all(['p', 'span', 'li']):
                url_1_anahtar_icerik = url_1_anahtar_kelimegruplari.text
                url_1_anahtar_kelimeler = url_1_anahtar_icerik.lower().split()

                for url_1_anahtar_kelime in url_1_anahtar_kelimeler:
                    url_1_anahtar_tumkelimeler.append(url_1_anahtar_kelime)

            # Gereksiz kelimlerden ayıklama işlemi
            url_1_tumkelimeler = sembolleritemizle(url_1_anahtar_tumkelimeler)
            url_1_anahtar_kelimesayisi = sozlukolustur(url_1_tumkelimeler)
            url_1_anahtar_kelimesayisi = yasakli_kelimel_ayiklama(url_1_anahtar_kelimesayisi)

            # Anahtar kelime oluşturma işlemi
            url_1_anahtar_kelimesayisi_sorted = sorted(url_1_anahtar_kelimesayisi.items(), key=operator.itemgetter(1))
            url_1_anahtar_kelimesayisi = {k: v for k, v in url_1_anahtar_kelimesayisi_sorted}
            j = 0
            for i in list(reversed(list(url_1_anahtar_kelimesayisi)))[0:5]:
                url_1_anahtar_kelimesayisi_ilk_bes[j] = i
                j += 1

            # print("url_1_anahtar_kelimesayisi_ilk_bes",url_1_anahtar_kelimesayisi_ilk_bes)

            # İkinci url için işlemler
            url_2_anahtar_url = form.URL2.data  # burada formda ki name parametremizin ismi ile ad verisini istedik.
            url_2_anahtar_r = requests.get(url_2_anahtar_url)
            url_2_anahtar_soup = BeautifulSoup(url_2_anahtar_r.content, 'html.parser')

            for url_2_anahtar_kelimegruplari in url_2_anahtar_soup.find_all('p'):
                url_2_anahtar_icerik = url_2_anahtar_kelimegruplari.text
                url_2_anahtar_kelimeler = url_2_anahtar_icerik.lower().split()

                for url_2_anahtar_kelime in url_2_anahtar_kelimeler:
                    url_2_anahtar_tumkelimeler.append(url_2_anahtar_kelime)

            # Gereksiz kelimlerden ayıklama işlemi
            url_2_tumkelimeler = sembolleritemizle(url_2_anahtar_tumkelimeler)
            url_2_anahtar_kelimesayisi = sozlukolustur(url_2_tumkelimeler)
            url_2_anahtar_kelimesayisi = yasakli_kelimel_ayiklama(url_2_anahtar_kelimesayisi)
            # print("url_2_anahtar_kelimesayisi :",url_2_anahtar_kelimesayisi)

            for url_2_tumkelimeler_key in url_2_anahtar_kelimesayisi:
                for index in url_1_anahtar_kelimesayisi_ilk_bes:
                    if url_2_tumkelimeler_key == url_1_anahtar_kelimesayisi_ilk_bes[index]:
                        url_ortak_anahtar_kelimeler[url_2_tumkelimeler_key] = url_2_anahtar_kelimesayisi[
                            url_2_tumkelimeler_key]

            # print(url_ortak_anahtar_kelimeler)
            toplam = 0
            Skor = 0
            for index in url_2_anahtar_kelimesayisi:
                # print(index)
                toplam += url_2_anahtar_kelimesayisi[index]
            # print(toplam)
            sayaç = 0
            top = 0
            sya = 0
            for indexi in url_ortak_anahtar_kelimeler:
                f1 = url_ortak_anahtar_kelimeler[indexi]
                top += f1

            # print(top)
            Skor = (top) / toplam
            # print(Skor)

            return render_template("asama23.html", form=form,
                                   url_1_anahtar_kelimesayisi_ilk_bes=url_1_anahtar_kelimesayisi_ilk_bes,
                                   url_2_anahtar_kelimesayisi=url_2_anahtar_kelimesayisi, Skor=Skor)


    else:
        # print("anahtar_kelime_benzerlik get")
        return render_template("asama23.html", form=form, url_2_anahtar_kelimesayisi=url_2_anahtar_kelimesayisi,
                               url_1_anahtar_kelimesayisi_ilk_bes=url_1_anahtar_kelimesayisi_ilk_bes)

    return render_template("asama23.html", form=form,
                           url_1_anahtar_kelimesayisi_ilk_bes=url_1_anahtar_kelimesayisi_ilk_bes,
                           url_2_anahtar_kelimesayisi=url_2_anahtar_kelimesayisi)


@app.route("/indeksleme-siralama", methods=["GET", "POST"])
def indeksleme_siralama():
    return render_template("indeksleme_siralama.html")


@app.route("/asama4", methods=["GET", "POST"])
def asama4():
    url_ana_indexleme_anahtar_kelime_ilk_bes = {}
    birinci_url_birinci_dallanma_anahtar_kelimeleri = {}
    birinci_url = {}
    birinci_url_dict = {}
    ikinci_url_dict = {}
    ucuncu_url_dict = {}
    dorduncu_url_dict = {}
    besinci_url_dict = {}
    ucuncu_url = {}
    dorduncu_url = {}
    besinci_url = {}
    birinci_url_birinci_dallanma = {}
    birinci_url_birinci_dallanma_skorlar = []
    besinci_url_ikinci_dallanma = {}
    dorduncu_url_ikinci_dallanma = {}
    url_skor_sıralama = {}
    url_skor_sıralama_url5 = {}
    url_skor_sıralama_url2 = {}
    url_skor_sıralama_url3 = {}
    url_skor_sıralama_url4 = {}

    form = siteindexleme(request.form)
    form.validate()

    if request.method == "POST":

        url_ana_indexleme = form.URL6.data  # burada formda ki name parametremizin ismi ile ad verisini istedik.
        url_ana_indexleme_anahtar_kelime_ilk_bes = indexleme_ilk_kelime_anahtar_kelime_bulma(url_ana_indexleme)
       # print("url_ana_indexleme_anahtar_kelime_ilk_bes:", url_ana_indexleme_anahtar_kelime_ilk_bes)

        url_birinci_indexleme = form.URL1.data
        url_birinci_indexleme_frekans = url_kelime_bulma(url_birinci_indexleme)
        birinci_url_birinci_dallanma_linkleri = birinci_dallanma(form.URL1.data)
        birinci_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                         url_birinci_indexleme_frekans)
        birinci_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_birinci_indexleme_frekans,
                                                                         url_ana_indexleme_anahtar_kelime_ilk_bes)
        birinci_url["ilk sayfa skor:"] = birinci_url_ilk_sayfa_skor
        birinci_url["Anahtar Kelime Frakanslari:"] = birinci_url_anahtar_kelime_frekanslari
        url_skor_sıralama[url_birinci_indexleme] = birinci_url_ilk_sayfa_skor
        index = 0
        sayac = 0
        while index < 3:
            birinci_url_birinci_dallanma_birinci_link_frekanslari = url_kelime_bulma(
                birinci_url_birinci_dallanma_linkleri[index])

            if bool(birinci_url_birinci_dallanma_birinci_link_frekanslari):

                birinci_url_birinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                    url_ana_indexleme_anahtar_kelime_ilk_bes, birinci_url_birinci_dallanma_birinci_link_frekanslari)

                birinci_url_birinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                    birinci_url_birinci_dallanma_linkleri[index])

                birinci_url_birinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                    birinci_url_birinci_dallanma_birinci_link_frekanslari,
                    birinci_url_birinci_dallanma_anahtar_kelimeleri)
                birinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                    birinci_url_birinci_dallanma_birinci_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                url_skor_sıralama[birinci_url_birinci_dallanma_linkleri[index]] = birinci_url_birinci_dallanma_url_skor

                # print("birinci_url_birinci_dallanma_ilk_sayfa_url_skor:",birinci_url_birinci_dallanma_ilk_sayfa_url_skor)
                # print("birinci_url_birinci_dallanma_anahtar_kelimeleri:",birinci_url_birinci_dallanma_anahtar_kelimeleri)
                # print("birinci_url_birinci_dallanma_anahtar_kelime_frekansı:",birinci_url_birinci_dallanma_anahtar_kelime_frekansı)
                birinci_url_birinci_dallanma[index] = [birinci_url_birinci_dallanma_url_skor,
                                                       birinci_url_birinci_dallanma_anahtar_kelime_frekansi,
                                                       birinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                index += 1

            birinci_url_dict = ChainMap(birinci_url, birinci_url_birinci_dallanma)
            # print("birinci_url_dict:",birinci_url_dict)

        ikinci_url_birinci_dallanma = {}
        ikinci_url_birinci_dallanma_skorlar = []
        ikinci_url = {}

        if bool(form.URL2.data):

            url_ikinci_indexleme = form.URL2.data
            ikinci_url_ikinci_dallanma_linkleri = birinci_dallanma(form.URL2.data)
            url_ikinci_indexleme_frekans = url_kelime_bulma(url_ikinci_indexleme)

            ikinci_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                            url_ikinci_indexleme_frekans)
            ikinci_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_ikinci_indexleme_frekans,
                                                                            url_ana_indexleme_anahtar_kelime_ilk_bes)
            ikinci_url["AD:"] = url_ikinci_indexleme
            ikinci_url["ikinci_url_ilk_sayfa_skor:"] = ikinci_url_ilk_sayfa_skor
            ikinci_url["Anahtar Kelime Frakansları:"] = ikinci_url_anahtar_kelime_frekanslari
            url_skor_sıralama[url_ikinci_indexleme] = ikinci_url_ilk_sayfa_skor

            index2 = 0

            while index2 < 3:
                ikinci_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(
                    ikinci_url_ikinci_dallanma_linkleri[index2])
                if bool(ikinci_url_ikinci_dallanma_link_frekanslari):
                    ikinci_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                        url_ana_indexleme_anahtar_kelime_ilk_bes, ikinci_url_ikinci_dallanma_link_frekanslari)

                    ikincisi_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                        ikinci_url_ikinci_dallanma_linkleri[index2])
                    ikinci_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ikinci_url_ikinci_dallanma_link_frekanslari, ikincisi_url_ikinci_dallanma_anahtar_kelimeleri)
                    ikinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ikinci_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                    url_skor_sıralama_url2[ikinci_url_ikinci_dallanma_linkleri[index2]] = ikinci_url_ikinci_dallanma_url_skor
                    print("ikinci_url_ikinci_dallanma_url_skor:", url_skor_sıralama_url2)

                    ikinci_url_birinci_dallanma[ikinci_url_ikinci_dallanma_linkleri[index2]] = [
                        ikinci_url_ikinci_dallanma_url_skor, ikinci_url_ikinci_dallanma_anahtar_kelime_frekansi,
                        ikinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                    index2 += 1

            ikinci_url_dict = ChainMap(ikinci_url, ikinci_url_birinci_dallanma)
           # print("ikinci_url_dict:", ikinci_url_dict)

        ucuncu_url_ikinci_dallanma = {}
        ucuncu_url = {}

        if bool(form.URL3.data):

            url_ucuncu_indexleme = form.URL3.data
            ucuncu_url_dallanma_linkleri = birinci_dallanma(form.URL3.data)
            url_ucuncu_indexleme_frekans = url_kelime_bulma(url_ucuncu_indexleme)

            ucuncu_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                            url_ucuncu_indexleme_frekans)
            ucuncu_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_ucuncu_indexleme_frekans,
                                                                            url_ana_indexleme_anahtar_kelime_ilk_bes)
            ucuncu_url["AD"] = url_ucuncu_indexleme
            ucuncu_url["Ucuncu Url Benzerlik Skoru:"] = ucuncu_url_ilk_sayfa_skor
            ucuncu_url["Ucuncu Url Anahtar Kelime Frakansları:"] = ucuncu_url_anahtar_kelime_frekanslari
            url_skor_sıralama[url_ucuncu_indexleme] = ucuncu_url_ilk_sayfa_skor

            index3 = 0
            sayac = 0

            while index3 < 3:

                ucuncu_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(ucuncu_url_dallanma_linkleri[index3])

                if bool(ucuncu_url_ikinci_dallanma_link_frekanslari):
                    ucuncu_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                        url_ana_indexleme_anahtar_kelime_ilk_bes, ucuncu_url_ikinci_dallanma_link_frekanslari)
                    ucuncu_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                        ucuncu_url_dallanma_linkleri[index3])
                    ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ucuncu_url_ikinci_dallanma_link_frekanslari, ucuncu_url_ikinci_dallanma_anahtar_kelimeleri)
                    ucuncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ucuncu_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                    url_skor_sıralama_url3[ucuncu_url_dallanma_linkleri[index3]] = ucuncu_url_ikinci_dallanma_url_skor

                    ucuncu_url_ikinci_dallanma[ucuncu_url_dallanma_linkleri[index3]] = [
                        ucuncu_url_ikinci_dallanma_url_skor, ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi,
                        ucuncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                    index3 += 1

            ucuncu_url_dict = ChainMap(ucuncu_url, ucuncu_url_ikinci_dallanma)
            #print("ucuncu_url_dict:", ucuncu_url_dict)

        if bool(form.URL4.data):

            url_dorduncu_indexleme = form.URL4.data
            dorduncu_url_dallanma_linkleri = birinci_dallanma(form.URL4.data)
            url_dorduncu_indexleme_frekans = url_kelime_bulma(url_dorduncu_indexleme)

            dorduncu_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                              url_dorduncu_indexleme_frekans)
            dorduncu_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_dorduncu_indexleme_frekans,
                                                                              url_ana_indexleme_anahtar_kelime_ilk_bes)
            dorduncu_url["AD"] = url_dorduncu_indexleme
            dorduncu_url["Dorduncu Url Benzerlik Skoru:"] = dorduncu_url_ilk_sayfa_skor
            dorduncu_url["Dorduncu Url Anahtar Kelime Frakansları:"] = dorduncu_url_anahtar_kelime_frekanslari
            url_skor_sıralama[url_dorduncu_indexleme] = dorduncu_url_ilk_sayfa_skor

            index4 = 0
            sayac = 0

            while index4 < 3:

                dorduncu_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(dorduncu_url_dallanma_linkleri[index4])

                if bool(dorduncu_url_ikinci_dallanma_link_frekanslari):
                    dorduncu_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                        url_ana_indexleme_anahtar_kelime_ilk_bes, dorduncu_url_ikinci_dallanma_link_frekanslari)
                    dorduncu_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                        dorduncu_url_dallanma_linkleri[index4])
                    dorduncu_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        dorduncu_url_ikinci_dallanma_link_frekanslari, dorduncu_url_ikinci_dallanma_anahtar_kelimeleri)
                    dorduncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        dorduncu_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                    url_skor_sıralama_url4[dorduncu_url_dallanma_linkleri[index4]] = dorduncu_url_ikinci_dallanma_url_skor

                    dorduncu_url_ikinci_dallanma[dorduncu_url_dallanma_linkleri[index4]] = [
                        dorduncu_url_ikinci_dallanma_url_skor, dorduncu_url_ikinci_dallanma_anahtar_kelime_frekansi,
                        dorduncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                    index4 += 1

            dorduncu_url_dict = ChainMap(dorduncu_url, dorduncu_url_ikinci_dallanma)
            #print("dorduncu_url_dict:", dorduncu_url_dict)

            if bool(form.URL5.data):

                url_besinci_indexleme = form.URL5.data
                besinci_url_dallanma_linkleri = birinci_dallanma(form.URL5.data)
                url_besinci_indexleme_frekans = url_kelime_bulma(url_besinci_indexleme)

                besinci_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(
                    url_ana_indexleme_anahtar_kelime_ilk_bes, url_besinci_indexleme_frekans)
                besinci_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_besinci_indexleme_frekans,
                                                                                 url_ana_indexleme_anahtar_kelime_ilk_bes)
                besinci_url["AD"] = url_besinci_indexleme
                besinci_url["besinci Url Benzerlik Skoru:"] = besinci_url_ilk_sayfa_skor
                besinci_url["besinci Url Anahtar Kelime Frakansları:"] = besinci_url_anahtar_kelime_frekanslari
                url_skor_sıralama[url_besinci_indexleme] = besinci_url_ilk_sayfa_skor

                index5 = 0
                sayac = 0


                while index5 < 3:

                    besinci_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(
                        besinci_url_dallanma_linkleri[index5])

                    if bool(besinci_url_ikinci_dallanma_link_frekanslari):
                        besinci_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                            url_ana_indexleme_anahtar_kelime_ilk_bes, besinci_url_ikinci_dallanma_link_frekanslari)
                        besinci_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                            besinci_url_dallanma_linkleri[index5])
                        besinci_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                            besinci_url_ikinci_dallanma_link_frekanslari,
                            besinci_url_ikinci_dallanma_anahtar_kelimeleri)
                        besinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                            besinci_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                        url_skor_sıralama_url5[besinci_url_dallanma_linkleri[index5]] = besinci_url_ikinci_dallanma_url_skor

                        besinci_url_ikinci_dallanma[besinci_url_dallanma_linkleri[index5]] = [
                            besinci_url_ikinci_dallanma_url_skor, besinci_url_ikinci_dallanma_anahtar_kelime_frekansi,
                            besinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                        index5 += 1

                besinci_url_dict = ChainMap(besinci_url, besinci_url_ikinci_dallanma)
                #print("besinci_url_dict:", besinci_url_dict)
        dict1=Merge(url_skor_sıralama_url5,url_skor_sıralama_url4)
        dict2=Merge(url_skor_sıralama_url3,url_skor_sıralama_url2)
        dict3=Merge(dict1,dict2)
        dict4=Merge(url_skor_sıralama,dict3)
        url_skor_sıralı={}
        url_skor={}
        dict4 = sorted(dict4.items(),key=operator.itemgetter(1))
        dict4 = {k: v for k, v in dict4}
        j = 0
        for i in list(reversed(list(dict4))):
            url_skor[j] = i
            j += 1

        for a in dict4:
            for index in url_skor:
                if a == url_skor[index]:
                    url_skor_sıralı[a] = dict4[a]

        return render_template("asama4.html", form=form,
                               url_ana_indexleme_anahtar_kelime_ilk_bes=url_ana_indexleme_anahtar_kelime_ilk_bes,
                               birinci_url_dict=birinci_url_dict, ikinci_url_dict=ikinci_url_dict,
                               ucuncu_url_dict=ucuncu_url_dict,
                               dorduncu_url_dict=dorduncu_url_dict, besinci_url_dict=besinci_url_dict,url_skor_sıralı=url_skor_sıralı)
    else:
        return render_template("asama4.html", form=form,
                               url_ana_indexleme_anahtar_kelime_ilk_bes=url_ana_indexleme_anahtar_kelime_ilk_bes,
                               birinci_url_dict=birinci_url_dict, ikinci_url_dict=ikinci_url_dict,
                               ucuncu_url_dict=ucuncu_url_dict,
                               dorduncu_url_dict=dorduncu_url_dict, besinci_url_dict=besinci_url_dict, url_skor_sıralı=url_skor_sıralı)


@app.route("/asama5", methods=["GET", "POST"])
def asama5():
    url_ana_indexleme_anahtar_kelime_ilk_bes = {}
    birinci_url_birinci_dallanma_anahtar_kelimeleri = {}
    birinci_url = {}
    birinci_url_dict = {}
    ikinci_url_dict = {}
    ucuncu_url_dict = {}
    dorduncu_url_dict = {}
    besinci_url_dict = {}
    ucuncu_url = {}
    dorduncu_url = {}
    besinci_url = {}
    birinci_url_birinci_dallanma = {}
    birinci_url_birinci_dallanma_skorlar = []
    besinci_url_ikinci_dallanma = {}
    dorduncu_url_ikinci_dallanma = {}
    url_skor_sıralama = {}
    url_skor_sıralama_url5 = {}
    url_skor_sıralama_url2 = {}
    url_skor_sıralama_url3 = {}
    url_skor_sıralama_url4 = {}

    yakin_kelimeler_url1 = {}
    yakin_kelimeler_url2 = {}
    yakin_kelimeler_url3 = {}
    yakin_kelimeler_url4 = {}
    yakin_kelimeler_url5 = {}

    form = siteindexleme(request.form)
    form.validate()
    
    if request.method == "POST":

        url_ana_indexleme = form.URL6.data  # burada formda ki name parametremizin ismi ile ad verisini istedik.
        url_ana_indexleme_anahtar_kelime_ilk_bes = indexleme_ilk_kelime_anahtar_kelime_bulma(url_ana_indexleme)
       # print("url_ana_indexleme_anahtar_kelime_ilk_bes:", url_ana_indexleme_anahtar_kelime_ilk_bes)

        url_birinci_indexleme = form.URL1.data
        url_birinci_indexleme_frekans = url_kelime_bulma(url_birinci_indexleme)
        birinci_url_birinci_dallanma_linkleri = birinci_dallanma(form.URL1.data)
        yakin_kelimeler_url1 = yakin_kelimeler_bul(url_birinci_indexleme_frekans)
        #print("yakın kelimeler: ", yakin_kelimeler_url1)

        birinci_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                         url_birinci_indexleme_frekans)
        birinci_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_birinci_indexleme_frekans,
                                                                         url_ana_indexleme_anahtar_kelime_ilk_bes)
        birinci_url["ilk sayfa skor:"] = birinci_url_ilk_sayfa_skor
        birinci_url["Anahtar Kelime Frakanslari:"] = birinci_url_anahtar_kelime_frekanslari
        url_skor_sıralama[url_birinci_indexleme] = birinci_url_ilk_sayfa_skor
        index = 0
        sayac = 0
        while index < 3:
            birinci_url_birinci_dallanma_birinci_link_frekanslari = url_kelime_bulma(
                birinci_url_birinci_dallanma_linkleri[index])

            if bool(birinci_url_birinci_dallanma_birinci_link_frekanslari):
                birinci_url_birinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                    url_ana_indexleme_anahtar_kelime_ilk_bes, birinci_url_birinci_dallanma_birinci_link_frekanslari)
                birinci_url_birinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                    birinci_url_birinci_dallanma_linkleri[index])
                birinci_url_birinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                    birinci_url_birinci_dallanma_birinci_link_frekanslari,
                    birinci_url_birinci_dallanma_anahtar_kelimeleri)
                birinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                    birinci_url_birinci_dallanma_birinci_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                url_skor_sıralama[birinci_url_birinci_dallanma_linkleri[index]] = birinci_url_birinci_dallanma_url_skor
                yakin_kelimeler_alturl1 = yakin_kelimeler_bul(birinci_url_birinci_dallanma_birinci_link_frekanslari)
                #######yakin_kelimeler_url1.setdefault(yakin_kelimeler_alturl1)

                # print("birinci_url_birinci_dallanma_ilk_sayfa_url_skor:",birinci_url_birinci_dallanma_ilk_sayfa_url_skor)
                # print("birinci_url_birinci_dallanma_anahtar_kelimeleri:",birinci_url_birinci_dallanma_anahtar_kelimeleri)
                # print("birinci_url_birinci_dallanma_anahtar_kelime_frekansı:",birinci_url_birinci_dallanma_anahtar_kelime_frekansı)
                birinci_url_birinci_dallanma[index] = [birinci_url_birinci_dallanma_url_skor,
                                                       birinci_url_birinci_dallanma_anahtar_kelime_frekansi,
                                                       birinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                index += 1

            birinci_url_dict = ChainMap(birinci_url, birinci_url_birinci_dallanma)
            # print("birinci_url_dict:",birinci_url_dict)

        ikinci_url_birinci_dallanma = {}
        ikinci_url_birinci_dallanma_skorlar = []
        ikinci_url = {}

        if bool(form.URL2.data):

            url_ikinci_indexleme = form.URL2.data
            ikinci_url_ikinci_dallanma_linkleri = birinci_dallanma(form.URL2.data)
            url_ikinci_indexleme_frekans = url_kelime_bulma(url_ikinci_indexleme)

            ikinci_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                            url_ikinci_indexleme_frekans)
            ikinci_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_ikinci_indexleme_frekans,
                                                                            url_ana_indexleme_anahtar_kelime_ilk_bes)
            ikinci_url["AD:"] = url_ikinci_indexleme
            ikinci_url["ikinci_url_ilk_sayfa_skor:"] = ikinci_url_ilk_sayfa_skor
            ikinci_url["Anahtar Kelime Frakansları:"] = ikinci_url_anahtar_kelime_frekanslari
            url_skor_sıralama[url_ikinci_indexleme] = ikinci_url_ilk_sayfa_skor
            yakin_kelimeler_url2 = yakin_kelimeler_bul(url_ikinci_indexleme_frekans)

            index2 = 0

            while index2 < 3:
                ikinci_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(
                    ikinci_url_ikinci_dallanma_linkleri[index2])
                if bool(ikinci_url_ikinci_dallanma_link_frekanslari):
                    ikinci_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                        url_ana_indexleme_anahtar_kelime_ilk_bes, ikinci_url_ikinci_dallanma_link_frekanslari)

                    ikincisi_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                        ikinci_url_ikinci_dallanma_linkleri[index2])
                    ikinci_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ikinci_url_ikinci_dallanma_link_frekanslari, ikincisi_url_ikinci_dallanma_anahtar_kelimeleri)
                    ikinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ikinci_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                    url_skor_sıralama_url2[ikinci_url_ikinci_dallanma_linkleri[index2]] = ikinci_url_ikinci_dallanma_url_skor
                    #print("ikinci_url_ikinci_dallanma_url_skor:", url_skor_sıralama_url2)
                    yakin_kelimeler_alturl2 = yakin_kelimeler_bul(ikinci_url_ikinci_dallanma_anahtar_kelime_frekansi)
                    #####yakin_kelimeler_url2.setdefault(yakin_kelimeler_alturl2)
                    
                    ikinci_url_birinci_dallanma[ikinci_url_ikinci_dallanma_linkleri[index2]] = [
                        ikinci_url_ikinci_dallanma_url_skor, ikinci_url_ikinci_dallanma_anahtar_kelime_frekansi,
                        ikinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                    index2 += 1

            ikinci_url_dict = ChainMap(ikinci_url, ikinci_url_birinci_dallanma)
           # print("ikinci_url_dict:", ikinci_url_dict)

        ucuncu_url_ikinci_dallanma = {}
        ucuncu_url = {}

        if bool(form.URL3.data):

            url_ucuncu_indexleme = form.URL3.data
            ucuncu_url_dallanma_linkleri = birinci_dallanma(form.URL3.data)
            url_ucuncu_indexleme_frekans = url_kelime_bulma(url_ucuncu_indexleme)
            yakin_kelimeler_url3 = yakin_kelimeler_bul(url_ucuncu_indexleme_frekans)

            ucuncu_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                            url_ucuncu_indexleme_frekans)
            ucuncu_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_ucuncu_indexleme_frekans,
                                                                            url_ana_indexleme_anahtar_kelime_ilk_bes)
            ucuncu_url["AD"] = url_ucuncu_indexleme
            ucuncu_url["Ucuncu Url Benzerlik Skoru:"] = ucuncu_url_ilk_sayfa_skor
            ucuncu_url["Ucuncu Url Anahtar Kelime Frakansları:"] = ucuncu_url_anahtar_kelime_frekanslari
            url_skor_sıralama[url_ucuncu_indexleme] = ucuncu_url_ilk_sayfa_skor

            index3 = 0
            sayac = 0

            while index3 < 3:

                ucuncu_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(ucuncu_url_dallanma_linkleri[index3])

                if bool(ucuncu_url_ikinci_dallanma_link_frekanslari):
                    ucuncu_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                        url_ana_indexleme_anahtar_kelime_ilk_bes, ucuncu_url_ikinci_dallanma_link_frekanslari)
                    ucuncu_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                        ucuncu_url_dallanma_linkleri[index3])
                    ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ucuncu_url_ikinci_dallanma_link_frekanslari, ucuncu_url_ikinci_dallanma_anahtar_kelimeleri)
                    ucuncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        ucuncu_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                    url_skor_sıralama_url3[ucuncu_url_dallanma_linkleri[index3]] = ucuncu_url_ikinci_dallanma_url_skor

                    yakin_kelimeler_alturl3 = yakin_kelimeler_bul(ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi)
                    #####yakin_kelimeler_url3.setdefault(yakin_kelimeler_alturl3)

                    ucuncu_url_ikinci_dallanma[ucuncu_url_dallanma_linkleri[index3]] = [
                        ucuncu_url_ikinci_dallanma_url_skor, ucuncu_url_ikinci_dallanma_anahtar_kelime_frekansi,
                        ucuncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                    index3 += 1

            ucuncu_url_dict = ChainMap(ucuncu_url, ucuncu_url_ikinci_dallanma)
            #print("ucuncu_url_dict:", ucuncu_url_dict)

        if bool(form.URL4.data):

            url_dorduncu_indexleme = form.URL4.data
            dorduncu_url_dallanma_linkleri = birinci_dallanma(form.URL4.data)
            url_dorduncu_indexleme_frekans = url_kelime_bulma(url_dorduncu_indexleme)
            yakin_kelimeler_url4 = yakin_kelimeler_bul(url_dorduncu_indexleme_frekans)

            dorduncu_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(url_ana_indexleme_anahtar_kelime_ilk_bes,
                                                                              url_dorduncu_indexleme_frekans)
            dorduncu_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_dorduncu_indexleme_frekans,
                                                                              url_ana_indexleme_anahtar_kelime_ilk_bes)
            dorduncu_url["AD"] = url_dorduncu_indexleme
            dorduncu_url["Dorduncu Url Benzerlik Skoru:"] = dorduncu_url_ilk_sayfa_skor
            dorduncu_url["Dorduncu Url Anahtar Kelime Frakansları:"] = dorduncu_url_anahtar_kelime_frekanslari
            url_skor_sıralama[url_dorduncu_indexleme] = dorduncu_url_ilk_sayfa_skor

            index4 = 0
            sayac = 0

            while index4 < 3:

                dorduncu_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(dorduncu_url_dallanma_linkleri[index4])

                if bool(dorduncu_url_ikinci_dallanma_link_frekanslari):
                    dorduncu_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                        url_ana_indexleme_anahtar_kelime_ilk_bes, dorduncu_url_ikinci_dallanma_link_frekanslari)
                    dorduncu_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                        dorduncu_url_dallanma_linkleri[index4])
                    dorduncu_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        dorduncu_url_ikinci_dallanma_link_frekanslari, dorduncu_url_ikinci_dallanma_anahtar_kelimeleri)
                    dorduncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                        dorduncu_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                    url_skor_sıralama_url4[dorduncu_url_dallanma_linkleri[index4]] = dorduncu_url_ikinci_dallanma_url_skor
                    yakin_kelimeler_alturl4 = yakin_kelimeler_bul(dorduncu_url_ikinci_dallanma_anahtar_kelime_frekansi)
                    #####yakin_kelimeler_url4.setdefault(yakin_kelimeler_alturl4)

                    dorduncu_url_ikinci_dallanma[dorduncu_url_dallanma_linkleri[index4]] = [
                        dorduncu_url_ikinci_dallanma_url_skor, dorduncu_url_ikinci_dallanma_anahtar_kelime_frekansi,
                        dorduncu_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                    index4 += 1

            dorduncu_url_dict = ChainMap(dorduncu_url, dorduncu_url_ikinci_dallanma)
            #print("dorduncu_url_dict:", dorduncu_url_dict)

            if bool(form.URL5.data):

                url_besinci_indexleme = form.URL5.data
                besinci_url_dallanma_linkleri = birinci_dallanma(form.URL5.data)
                url_besinci_indexleme_frekans = url_kelime_bulma(url_besinci_indexleme)
                yakin_kelimeler_url5 = yakin_kelimeler_bul(url_besinci_indexleme_frekans)

                besinci_url_ilk_sayfa_skor = anahtar_kelime_arama_ve_skor_islemi(
                    url_ana_indexleme_anahtar_kelime_ilk_bes, url_besinci_indexleme_frekans)
                besinci_url_anahtar_kelime_frekanslari = anahtar_kelime_frekansi(url_besinci_indexleme_frekans,
                                                                                 url_ana_indexleme_anahtar_kelime_ilk_bes)
                besinci_url["AD"] = url_besinci_indexleme
                besinci_url["besinci Url Benzerlik Skoru:"] = besinci_url_ilk_sayfa_skor
                besinci_url["besinci Url Anahtar Kelime Frakansları:"] = besinci_url_anahtar_kelime_frekanslari
                url_skor_sıralama[url_besinci_indexleme] = besinci_url_ilk_sayfa_skor

                index5 = 0
                sayac = 0


                while index5 < 3:

                    besinci_url_ikinci_dallanma_link_frekanslari = url_kelime_bulma(
                        besinci_url_dallanma_linkleri[index5])

                    if bool(besinci_url_ikinci_dallanma_link_frekanslari):
                        besinci_url_ikinci_dallanma_url_skor = anahtar_kelime_arama_ve_skor_islemi(
                            url_ana_indexleme_anahtar_kelime_ilk_bes, besinci_url_ikinci_dallanma_link_frekanslari)
                        besinci_url_ikinci_dallanma_anahtar_kelimeleri = indexleme_ilk_kelime_anahtar_kelime_bulma(
                            besinci_url_dallanma_linkleri[index5])
                        besinci_url_ikinci_dallanma_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                            besinci_url_ikinci_dallanma_link_frekanslari,
                            besinci_url_ikinci_dallanma_anahtar_kelimeleri)
                        besinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi = anahtar_kelime_frekansi(
                            besinci_url_ikinci_dallanma_link_frekanslari, url_ana_indexleme_anahtar_kelime_ilk_bes)
                        url_skor_sıralama_url5[besinci_url_dallanma_linkleri[index5]] = besinci_url_ikinci_dallanma_url_skor
                        yakin_kelimeler_alturl5 = yakin_kelimeler_bul(besinci_url_ikinci_dallanma_anahtar_kelime_frekansi)
                        #####yakin_kelimeler_url5.setdefault(yakin_kelimeler_alturl5)

                        besinci_url_ikinci_dallanma[besinci_url_dallanma_linkleri[index5]] = [
                            besinci_url_ikinci_dallanma_url_skor, besinci_url_ikinci_dallanma_anahtar_kelime_frekansi,
                            besinci_url_ikinci_dallanma__ortak_anahtar_kelime_frekansi]
                        index5 += 1

                besinci_url_dict = ChainMap(besinci_url, besinci_url_ikinci_dallanma)
                #print("besinci_url_dict:", besinci_url_dict)
        dict1=Merge(url_skor_sıralama_url5,url_skor_sıralama_url4)
        dict2=Merge(url_skor_sıralama_url3,url_skor_sıralama_url2)
        dict3=Merge(dict1,dict2)
        dict4=Merge(url_skor_sıralama,dict3)
        url_skor_sıralı={}
        url_skor={}
        dict4 = sorted(dict4.items(),key=operator.itemgetter(1))
        dict4 = {k: v for k, v in dict4}
        j = 0
        for i in list(reversed(list(dict4))):
            url_skor[j] = i
            j += 1

        for a in dict4:
            for index in url_skor:
                if a == url_skor[index]:
                    url_skor_sıralı[a] = dict4[a]

                
        return render_template("asama5.html", form=form,
                               url_ana_indexleme_anahtar_kelime_ilk_bes=url_ana_indexleme_anahtar_kelime_ilk_bes,
                               birinci_url_dict=birinci_url_dict, ikinci_url_dict=ikinci_url_dict,
                               ucuncu_url_dict=ucuncu_url_dict,
                               dorduncu_url_dict=dorduncu_url_dict, besinci_url_dict=besinci_url_dict,url_skor_sıralı=url_skor_sıralı,
                               yakin_kelimeler_url1 = yakin_kelimeler_url1, yakin_kelimeler_url2=yakin_kelimeler_url2, 
                               yakin_kelimeler_url3 = yakin_kelimeler_url3, yakin_kelimeler_url4=yakin_kelimeler_url4,
                               yakin_kelimeler_url5 = yakin_kelimeler_url5)
    else:
        return render_template("asama5.html", form=form,
                               url_ana_indexleme_anahtar_kelime_ilk_bes=url_ana_indexleme_anahtar_kelime_ilk_bes,
                               birinci_url_dict=birinci_url_dict, ikinci_url_dict=ikinci_url_dict,
                               ucuncu_url_dict=ucuncu_url_dict,
                               dorduncu_url_dict=dorduncu_url_dict, besinci_url_dict=besinci_url_dict, url_skor_sıralı=url_skor_sıralı,
                               yakin_kelimeler_url1 = yakin_kelimeler_url1, yakin_kelimeler_url2=yakin_kelimeler_url2, 
                               yakin_kelimeler_url3 = yakin_kelimeler_url3, yakin_kelimeler_url4=yakin_kelimeler_url4,
                               yakin_kelimeler_url5 = yakin_kelimeler_url5)


@app.route("/semantik-analiz")
def semantik_analiz():

    return render_template("semantik_analiz.html")


if __name__ == "__main__":
    app.run(debug=True)
