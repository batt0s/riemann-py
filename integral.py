# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:01:20 2024

@author: kerem (kerem.ullen@pm.me)

TODO:
    - [ ] Fonksiyonun integrallenebilirliğini kontrol et
    
"""

# Imports
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from sympy import sympify, lambdify, integrate, Symbol, SympifyError, Piecewise


# İnteraktif olmayan backend (https://matplotlib.org/stable/users/explain/backends.html)
matplotlib.use('agg')


# Fonksiyonun aralıktaki max ve minimum değerini bulmak için fonksiyonlar.
# f değeri fonksiyon, x değeri aralığın başı ve width de aralık boyu.
def get_max(f, x: float, width: float = 1):
    X = np.linspace(x, x+width)
    return np.max(f(X))

def get_min(f, x: float, width: float = 1):
    X = np.linspace(x, x+width)
    return np.min(f(X))


# Görselleri hazırlamak için fonksiyonlar
def riemann_alt_gorsel(f: str, a: str, b: str, N: int,
                       output_path: str = "riemann_alt.png") -> str:
    # Değişkenler
    x_sym = Symbol("x")
    
    # Fonksiyon
    f_str = f
    try:
        f_sym = sympify(f_str)
    except SympifyError:
        raise SyntaxError(f"Girilen ifade {f} anlaşılmadı")
    if f_sym.is_number:
        raise SyntaxError(f"Girilen ifade {f} bir fonksiyon belirtmiyor")
    f = lambdify(x_sym, f_sym)
    
    # Sınırlar
    try:
        a_sym = sympify(a)
    except SympifyError:
        raise SyntaxError(f"Verilen ifade {a} anlaşılmadı")
    if not a_sym.is_number:
        raise ValueError(f"Sınır değeri {a_sym} bir sayı değil")
    if not a_sym.is_real:
        raise ValueError(f"Sınır değeri {a_sym} bir gerçel sayı değil")
    a = float(a_sym)
    
    try:
        b_sym = sympify(b)
    except SympifyError:
        raise SyntaxError(f"Verilen ifade {b} anlaşılmadı")
    if not b_sym.is_number:
        raise ValueError(f"Sınır değeri {b_sym} bir sayı değil")
    if not b_sym.is_real:
        raise ValueError(f"Sınır değeri {b_sym} bir gerçel sayı değil")
    b = float(b_sym)
    
    # ! Sürekli olmayıp integrallenebilir ve sürekli olup integrallenebilen 
    # fonksiyonlar var.
    # Verilen sınırlar verilen fonksiyonun sürekli olduğu aralıkta
    # değilse hata döndür. (reel sayılar üstünde)
    # if not Interval(a_sym, b_sym).is_subset(continuous_domain(f_sym, x_sym, S.Reals)):
    #     raise NotIntegrableError
    
    # Hesaplamalar için x ve y değerleri
    x = np.linspace(a, b, N+1) # a'dan b'ye değerler, N+1 eşit parça
    y = f(x)
    # Fonksiyon çizimi için x ve y değerleri
    # Burada daha çok parça kullanıyoruz ki çizerken daha köşesiz bir görüntü
    # oluşsun.
    X = np.linspace(a, b, 10*N+1)
    Y = f(X)
    
    # Y değerleri arasında NaN varsa hata döndür. Genelde tanımsız olduğu
    # zaman nan döner. Sonsuzda da olabilir.
    if np.isnan(Y).any():
        raise ValueError("Fonksiyon verilen aralıkta tanımsız")
    
    dx = (b-a)/N
    
    # Grafiği çizeceğimiz alanı figsize boyunda oluşturuyoruz
    plt.figure(figsize=(6,6))

    # X ve Y değerleri ile fonksiyonu çiziyoruz.
    # Fonksiyon parçalı değilse noktaların arasını doldurarak çiziyoruz.
    # Eğer fonksiyon parçalı ise sadece verilen noktaları çiziyoruz.
    # Bu kontrolü koymazsak kritik noktalar çizimde belli olmaz.
    if type(f_sym) == Piecewise:
        plt.plot(X, Y, 'r.', markersize=3)
    else:
        plt.plot(X, Y, 'r')
    
    # alt toplam hesaplarken kullanacağımız x ve y değerleri
    x_alt = x[:-1]
    y_alt= np.zeros(len(x_alt))  # doğru boyutta bir vektör oluşturuyoruz
    # x değerleri içinde dönüp x değerlerine karşılık aralıklardaki min
    # y değerini bulup vektörün içine yerleştiriyoruz.
    for i, x_ in enumerate(x_alt):
        y_alt[i] = get_min(f, x_, dx)
    # x ve y değerlerini noktalarla işaretliyoruz
    plt.plot(x, y, 'm.', markersize=10)
    # Diktörtgenleri çiziyoruz, x_alt'dan alınan x başlangıç noktası, 
    # dx taban boyu, y_alt'dan alınan y de dikdörtgenin yüksekliği.
    plt.bar(x_alt, y_alt, width=dx, alpha=0.25, align='edge', edgecolor='b')
    
    # x ve y eksenlerini çiziyoruz
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    
    # Toplamın değerini bulmak için y değerlerini ve aralık boyunu çarpıp
    # topluyoruz yani aslında dikdörtgenlerin alanlarını bulup topluyoruz.
    deger = np.sum(y_alt * dx)
    # sympy ile integralin gerçek değerini hesaplıyoruz.
    gercek_deger = integrate(f_sym, (x_sym, a_sym, b_sym)).evalf()

    plt.title(f"Riemann Alt Toplamı, f(x)={f_sym}")
    txt=f"a={a}, b={b} N={N}, dx={dx}\nToplam = {deger:.4f}, Gerçek değer = {gercek_deger:.4f}"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    
    plt.savefig(output_path, bbox_inches='tight')
    
    return output_path

def riemann_ust_gorsel(f: str, a: str, b: str, N: int,
                       output_path: str = "riemann_ust.png") -> str:
    # Değişkenler
    x_sym = Symbol("x")
    
    # Fonksiyon
    f_str = f
    try:
        f_sym = sympify(f_str)
    except SympifyError:
        raise SyntaxError(f"Girilen ifade {f} anlaşılmadı")
    if f_sym.is_number:
        raise SyntaxError(f"Girilen ifade {f} bir fonksiyon belirtmiyor")
    f = lambdify(x_sym, f_sym)
    
    # Sınırlar
    try:
        a_sym = sympify(a)
    except SympifyError:
        raise SyntaxError(f"Verilen ifade {a} anlaşılmadı")
    if not a_sym.is_number:
        raise ValueError(f"Sınır değeri {a_sym} bir sayı değil")
    if not a_sym.is_real:
        raise ValueError(f"Sınır değeri {a_sym} bir gerçel sayı değil")
    a = float(a_sym)
    
    try:
        b_sym = sympify(b)
    except SympifyError:
        raise SyntaxError(f"Verilen ifade {b} anlaşılmadı")
    if not b_sym.is_number:
        raise ValueError(f"Sınır değeri {b_sym} bir sayı değil")
    if not b_sym.is_real:
        raise ValueError(f"Sınır değeri {b_sym} bir gerçel sayı değil")
    b = float(b_sym)
    
    # ! Sürekli olmayıp integrallenebilir ve sürekli olup integrallenebilen 
    # fonksiyonlar var.
    # Verilen sınırlar verilen fonksiyonun tanımlı olduğu aralıkta
    # değilse hata döndür. (reel sayılar üstünde)
    # if not Interval(a_sym, b_sym).is_subset(continuous_domain(f_sym, x_sym, S.Reals)):
    #     raise NotIntegrableError
    
    # Hesaplamalar için x ve y değerleri
    x = np.linspace(a, b, N+1) # a'dan b'ye değerler, N+1 eşit parça
    y = f(x)
    # Fonksiyon çizimi için x ve y değerleri
    X = np.linspace(a, b, 10*N+1)
    Y = f(X)
    
    # Y değerleri arasında NaN varsa hata döndür. Genelde tanımsız olduğu
    # zaman nan döner. Sonsuzda da olabilir.
    if np.isnan(Y).any():
        raise ValueError("Fonksiyon verilen aralıkta tanımsız")

    dx = (b-a)/N
    
    plt.figure(figsize=(6,6))
    
    # X ve Y değerleri ile fonksiyonu çiziyoruz.
    # Fonksiyon parçalı değilse noktaların arasını doldurarak çiziyoruz.
    # Eğer fonksiyon parçalı ise sadece verilen noktaları çiziyoruz.
    # Bu kontrolü koymazsak kritik noktalar çizimde belli olmaz.
    if type(f_sym) == Piecewise:
        plt.plot(X, Y, 'r.', markersize=3)
    else:
        plt.plot(X, Y, 'r')
    
    x_ust = x[:-1]
    y_ust= np.zeros(len(x_ust))
    for i, x_ in enumerate(x_ust):
        y_ust[i] = get_max(f, x_, dx)
    plt.plot(x, y, 'm.', markersize=10)
    plt.bar(x_ust, y_ust, width=dx, alpha=0.25, align='edge', edgecolor='b')
    
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')

    deger = np.sum(y_ust * dx)
    gercek_deger = integrate(f_sym, (x_sym, a_sym, b_sym)).evalf()

    plt.title(f"Riemann Üst Toplamı, f(x)={f_sym}")
    txt=f"a={a}, b={b}, N={N}, dx={dx}\nToplam = {deger:.4f}, Gerçek değer = {gercek_deger:.4f}"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    
    plt.savefig(output_path, bbox_inches='tight')
    
    return output_path
