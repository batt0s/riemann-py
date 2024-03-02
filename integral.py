# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:01:20 2024

@author: kerem (batt0s)
"""

# Imports
import numpy as np
from matplotlib import pyplot as plt
from sympy import sympify, lambdify, integrate


def get_max(f, x: float, width: float = 1):
    X = np.linspace(x, x+width)
    return np.max(f(X))

def get_min(f, x: float, width: float = 1):
    X = np.linspace(x, x+width)
    return np.min(f(X))

def riemann_alt_gorsel(f: str, a: float, b: float, N: int,
                       output_path: str = "riemann_alt.png") -> str:
    # Fonksiyon
    f_str = f
    f_sym = sympify(f_str)
    f = lambdify("x", f_sym)
    
    # Hesaplamalar için x ve y değerleri
    x = np.linspace(a, b, N+1) # a'dan b'ye değerler, N+1 eşit parça
    y = f(x)
    # Fonksiyon çizimi için x ve y değerleri
    X = np.linspace(a, b, 10*N+1)
    Y = f(X)
    
    dx = (b-a)/N
    
    plt.figure(figsize=(6,6))

    plt.plot(X, Y, 'r')
    
    x_alt = x[:-1]
    y_alt= np.zeros(len(x_alt))
    for i, x_ in enumerate(x_alt):
        y_alt[i] = get_min(f, x_, dx)
    plt.plot(x, y, 'm.', markersize=10)
    plt.bar(x_alt, y_alt, width=dx, alpha=0.25, align='edge', edgecolor='b')
    
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    
    deger = np.sum(y_alt * dx)
    gercek_deger = integrate(f_sym, ("x", a, b))

    plt.title(f"Riemann Alt Toplamı, f(x)={f_sym}")
    txt=f"a={a}, b={b} N={N}, dx={dx}\nToplam = {deger}, Gerçek değer = {gercek_deger}"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    
    plt.savefig(output_path, bbox_inches='tight')
    
    return output_path

def riemann_ust_gorsel(f: str, a: float, b: float, N: int,
                       output_path: str = "riemann_ust.png") -> str:
    # Fonksiyon
    f_str = f
    f_sym = sympify(f_str)
    f = lambdify("x", f_sym)
    
    # Hesaplamalar için x ve y değerleri
    x = np.linspace(a, b, N+1) # a'dan b'ye değerler, N+1 eşit parça
    y = f(x)
    # Fonksiyon çizimi için x ve y değerleri
    X = np.linspace(a, b, 10*N+1)
    Y = f(X)
        
    dx = (b-a)/N
    
    plt.figure(figsize=(6,6))
    
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
    gercek_deger = integrate(f_sym, ("x", a, b))

    plt.title(f"Riemann Üst Toplamı, f(x)={f_sym}")
    txt=f"a={a}, b={b}, N={N}, dx={dx}\nToplam = {deger}, Gerçek değer = {gercek_deger}"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    
    plt.savefig(output_path, bbox_inches='tight')
    
    return output_path
