# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 21:58:26 2024

@author: tomyj
"""

import turtle


"""Exo 20 TD 5 """
# =============================================================================
# tab1 = [3,1,2,3,1,2,2]
# tab2 = [1,2,3,4]
# i = 0
# equivalent = True
# if len(tab1) > len(tab2):
#     n = len(tab2)
# else:
#     n = len(tab1)
# while i < n:
#     if tab1[i] not in tab2 or tab2[i] not in tab1:
#         equivalent = False
#     i = i + 1
# print(equivalent)
# =============================================================================

"""Exo 21 TD 5"""
# =============================================================================
# tab1 = [3,1,2,3]
# tab2 = [1,2,3,3]
# i = 0
# equivalent = True
# if len(tab1) != len(tab2):
#     equivalent = False
#     i = len(tab1)
# while i < len(tab1):
#     if tab1[i] not in tab2 or tab2[i] not in tab1:
#         equivalent = False
#     i = i + 1
# print(equivalent)
# =============================================================================

# =============================================================================
# mat = [[1,2,3],[4,5,6]]
# def somme_mat(mat):
#     somme = 0
#     for i in range(len(mat)):
#         for j in range(len(mat[i])):
#             somme = somme + mat[i][j]
#     return somme
# =============================================================================

# =============================================================================
# mat = [[1,2,3],[4,5,6]]
# def transposition(mat):
#     transpose = [[0,0],[0,0],[0,0]]
#     for i in range(len(mat)):
#         for j in range(len(mat[i])):
#             transpose[j][i] = mat[i][j]
#     return transpose
# =============================================================================

# =============================================================================
# a = "ABCXYZAY"
# b = "XYZABCB"
# plsc = ''
# for i in range(len(a)):
#     for j in range(len(b)):
#         n = 0
#         sca = ''
#         while a[i+n] == b[j+n] and i+n < len(a)-1 and j+n < len(b)-1:
#             sca += a[i+n]
#             n += 1
#         if len(sca) > len(plsc):
#             plsc = sca
# print(plsc)
# =============================================================================

""" TP 6"""

"""Exo 4 intermédiaire"""
# =============================================================================
# c1 = "chien"
# c2 = "chine"
# 
# def anagramme(c1,c2):
#     est_ana = True
#     if len(c1) != len(c2):
#         return "Les deux chaines ne sont pas anagramme"
#     for lettre in c1:
#         if lettre not in c2:
#             est_ana = False
#     if est_ana == True:
#         return "Les deux chaines sont anagramme"
#     else:
#         return "Les deux chaines ne sont pas anagramme"
# =============================================================================

"""Exo 1 avancé"""
# =============================================================================
# employe = {"Nom":["Jean Mackee","Lisa Crawford","Sujan Patel"],
#            "Age":["38","29","33"],
#            "Departement":["Vente","Management","RH"]}
# 
# def total(employe):
#     for i in range(len(next(iter(employe.values())))):
#         for cle,valeur in employe.items():
#             print(f"{cle} : {valeur[i]}")
#             print()
#         print("--------------------")
#         
# def unique(employe,prenom):
#     if prenom in employe['Nom']:
#         k = employe['Nom'].index(prenom)
#         for cle,valeur in employe.items():
#             print(f"{cle} : {valeur[k]}")
#             print()
#     else:
#         return "Désolé, cette personne ne fait pas partie de nos employés"
#     
# def jeunesse(employe,a):
#     for i in range(len(next(iter(employe.values())))):
#         for cle,valeur in employe.items():
#             if int(employe['Age'][i]) < a:
#                 print(f"{cle} : {valeur[i]}")
#                 print()
#                 
# def menu(employe):
#     choix_possible = ['A','U','J'] 
#     choix = input("Choisissez ce que vous voulez faire (A: Afficher tous les employés, U: Afficher un unique employé , J: Afficher un employé étant plus jeune qu'un certain âge) :")
#     while choix not in choix_possible:
#         print()
#         print("Désolé, cette commande n'existe pas.")
#         print()
#         choix = input("Choisissez ce que vous voulez faire (A: Afficher tous les employés, U: Afficher un unique employé , J: Afficher un employé étant plus jeune qu'un certain âge) :")
#     if choix == 'A':
#         return total(employe)
#     elif choix == 'U':
#         prenom = input("Choisissez un employé dont vous voulez connaitre les informations :")
#         return unique(employe, prenom)
#     else:
#         a = int(input("Choisissez l'âge maximum des employés dont vous voulez connaitre les informations :"))
#         return jeunesse(employe, a)
# =============================================================================

"""Exo 2 avancé"""
# =============================================================================
# L = [('Tom',19,80),('John',20,90),('Jony',17,91),('Jony',17,93),('Json',21,85)]
# 
# def tri(L):
#     sorted(L)
#     return L
# =============================================================================

"""Exo 3 avancé"""

