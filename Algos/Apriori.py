import csv
from itertools import compress, product
import math
import time
import copy as cp
from os import path

from Algos.Rule import regle as r

start_time = time.time()


def combinations(items):
    """ Fonction qui me retourne une combinaison des items d'un itemset
        exemple : ['a','b','c']   ----> {}
                                        {'c'}
                                        {'b'}
                                        {'b', 'c'}
                                        {'a'}
                                        {'a', 'c'}
                                        {'a', 'b'}
                                        {'a', 'b', 'c'}
    """
    return (tuple(compress(items, mask)) for mask in product(*[[0, 1]] * len(items)))


def count_sup(itemSet, Transactions):
    """Calcul le support d'un itemset genre {"milk,coffee,bread"}
        Le support (X) = FREQUENCE(X) / NB(Transactions)"""
    sup = 0
    for transaction in Transactions:
        exists = True
        for item in itemSet:
            if item not in transaction:
                exists = False
        # si tous les items existent dans une transaction on incremente la freq
        if exists == True:  sup += 1

    return sup / len(Transactions)


def elagage(items, minsup):
    """Elagage des items set d'un dict< MINSUP"""
    for item in list(items):
        if items[item] < minsup: del items[item]


def combine_items(item1, item2):
    """
        Combine 2 itemset de meme taille -------- A,B,C              A,B,D
    """
    left = item1.split(',')
    right = item2.split(',')

    accepted = True

    # SI cest un itemset de taille = 1
    if len(left) == 1:
        return str(item1 + "," + item2)
    else:
        # SI TAILLE >= 2 : je verifie si les k-1 items sont ==
        for i in range(len(left) - 1):
            if left[i] != right[i]:
                accepted = False
        if accepted:
            return str(item1 + ',' + ','.join(map(str, right[i + 1:len(left)])))
        else:
            return None


# LALGORITHME APRIORI ====================================================================
def apriori(Prods, minsup, Transactions):
    items = cp.deepcopy(Prods)  # Items a traiter a une etape k
    elagage(items, minsup)

    # Prods Contient les itemsets-1 donc k=1
    k = 1
    # Dict qui va contenir ts nos tableaux intermediaires
    items_k = {}
    items_k[k] = cp.deepcopy(items)

    # on s'arrete quand ya plus d'items a combiner
    while len(items) > 1:
        k += 1
        items_k[k] = {}
        for item1 in list(items):
            del items[item1]
            for item2 in list(items):
                combo = combine_items(item1, item2)
                if combo != None:
                    list_of_items = combo.split(',')
                    items_k[k][str(combo)] = count_sup(list_of_items, Transactions)

        elagage(items_k[k], minsup)
        if items_k[k].__len__() == 0:
            del items_k[k]
            break
        else:
            items = cp.deepcopy(items_k[k])

    return items_k


# 1ere Méthode
#  chaque itemset a un dictionnaire de regles
def extract_rules(itemsets):
    Rules = {}
    for items in itemsets:
        ls = list(combinations("".join(items).split(",")))
        ls.pop(0)
        ls.pop(len(ls) - 1)
        Rules[items] = dict(zip(ls, [r(i, 0, 0) for i in ls[::-1]]))
    return Rules


def ELAGAGE(ItemSets, Transactions, minconf, minlift):
    Valid_Rules = {}

    for i in ItemSets:
        if i != 1:
            Rules = extract_rules(ItemSets[i])
            count_Trust(Rules, Transactions)
            Valid_Rules[i] = cp.deepcopy(Rules)
            for itemset in Rules:
                for rule in Rules[itemset]:
                    if Rules[itemset][rule].confidence < minconf or Rules[itemset][rule].lift < minlift:
                        del Valid_Rules[i][itemset][rule]
                        if len(Valid_Rules[i][itemset]) == 0: del Valid_Rules[i][itemset]
                        if len(Valid_Rules[i]) == 0:
                            del Valid_Rules[i]

    return Valid_Rules


def count_Trust(Rules, Transactions):
    """ Calcul de la confiance utilise count_sup
        Confiance(A→B)=Sup(AB)/Sup(A)
    """

    for itemset in Rules:
        for rule in Rules[itemset]:
            liste = list(rule) + list(Rules[itemset][rule].tuple)
            confidence = count_sup(liste, Transactions) / count_sup(list(rule), Transactions)
            lift = confidence / count_sup(list(Rules[itemset][rule].tuple), Transactions)
            Rules[itemset][rule].confidence = confidence
            Rules[itemset][rule].lift = lift


def Ajouter_transaction(list_items, client):
    with open('../DataBase/Clients/' + client + '.csv', 'a') as fd:
        fd.write(list_items[0])
        for item in list_items[1:]:
            fd.write("," + item)
        fd.write("\n")


# minsup = 0.5 if n <= 50 else 0.25 if n <= 500 else 0.1
#             minconf = 0.6
#             minlift = 1 if n < 20 else 1.5 if n < 500 else 1
# minsup = 0.28 * math.exp(-8.3 * math.pow(10, -4) * n)
# minconf = 0.6 * math.exp(-1.8 * math.pow(10, -4) * n)

def game(client_name, tenta, minsup, minconf, minlift):
    if path.exists('../DataBase/Clients/' + client_name + '.csv'):
        with open('../DataBase/Clients/' + client_name + '.csv', 'r') as read_obj:
            # Lire les transactions
            Transactions = csv.reader(read_obj)
            # Stock les transactions dans une liste
            Transactions = list(Transactions)

            print("\n\n---------------------Tentative :", tenta)
            # Extraction des items-1 avec leurs supports
            n = len(Transactions)
            print("Nombre de Transactions:", n, "\nMin Support: ", minsup, "\nMinConf: ", minconf, "\nLift: ", minlift)
            Prods = {}
            for tran in Transactions:
                for prod in tran:
                    if prod in Prods:  # si le produit existe déja je ++ son suport
                        Prods[prod] += 1 / n
                    elif prod.strip():  # si le produit n'est pas dans ma liste je l'ajoute avec un support de 1/n
                        Prods[prod] = 1 / n

            # Apriori nous retourne ts les itemsets frequents avec leurs supports
            ItemSets = apriori(Prods, minsup, Transactions)
            for s in ItemSets:
                print("Itemsets de Taille:", s)
                for i in ItemSets[s]:
                    print("{", i, "}")

            if ItemSets.__len__() == 1:
                if tenta < 10:
                    tenta += 1
                    if minsup > 0.1:
                        minsup -= 0.1
                        minconf -= 0.05
                    return game(client_name, tenta, minsup, minconf, minlift)
                else:
                    return None
            else:
                Rules = ELAGAGE(ItemSets, Transactions, minconf, minlift)
                if len(Rules) == 0:
                    if tenta < 10:
                        tenta += 1
                        if minsup > 0.01:
                            minsup -= 0.05
                        if minconf > 0.1:
                            minconf -= 0.05
                        elif minlift >= 1:
                            minlift -= 0.5
                        return game(client_name, tenta, minsup, minconf, minlift)
                    else:
                        return None
                else:
                    print("Valid Rules:")
                    l = 0
                    for r in Rules:
                        for i in Rules[r]:
                            for rr in Rules[r][i]:
                                l += 1
                                print(l, rr, "->", Rules[r][i][rr])
                    return Rules

    else:
        print("FILE NOT EXITS")

