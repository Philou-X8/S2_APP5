#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe markov, Ã  utiliser pour solutionner la problÃ©matique.
    C'est un gabarit pour l'application de traitement des frÃ©quences de mots dans les oeuvres d'auteurs divers.

    Les mÃ©thodes aparaissant dans ce fichier dÃ©finissent une API qui est utilisÃ©e par l'application
    de test testmarkov.py
    Les paramÃ¨tres d'entrÃ©e et de sortie (Application Programming Interface, API) sont dÃ©finis,
    mais le code est Ã  Ã©crire au complet.
    Vous pouvez ajouter toutes les mÃ©thodes et toutes les variables nÃ©cessaires au bon fonctionnement du systÃ¨me

    La classe markov est invoquÃ©e par la classe testmarkov (contenue dans testmarkov.py):

        - Tous les arguments requis sont prÃ©sents et accessibles dans args (dans le fichier testmarkov.py)
        - Note: vous pouvez tester votre code en utilisant les commandes:
            + "python testmarkov.py"
            + "python testmarkov.py -h" (donne la liste des arguments possibles)
            + "python testmarkov.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et UniversitÃ© de Sherbrooke
"""

import os
import glob
import ntpath
import math
import random
class ngram():
    def __init__(self):
        self.gram = []


    def append(self, word):
        self.gram.append(word)

    def string(self):
        str = ""
       # print(self.gram)
        for word in self.gram:

            str += word + " "
        return  str
    def __hash__(self):

        return hash(self.string())
    def __eq__(self, other):
        if len(self.gram) != len(other.gram):
            return  False


        return self.string()== other.string()
    def __ne__(self, other):
        return not self.__eq__(other)


def produitScalaire(dict1,dict2 ):

    somme =0


    for key in dict1:

        if key in dict2:
            somme+= dict2[key]*dict1[key][0]
    return somme
def module(dict):
    somme = 0
    for value in dict.values():
        if isinstance(value, int):
            somme += value ** 2
        else:
            somme += value[0] ** 2

    return math.sqrt(somme)

class markov():
    """Classe Ã  utiliser pour coder la solution Ã  la problÃ©matique:

        - Contient certaines fonctions de base pour faciliter le travail (recherche des auteurs).
        - Les interfaces du code Ã  dÃ©velopper sont prÃ©sentes, mais tout le code est Ã  Ã©crire
        - En particulier, il faut complÃ©ter les fonctions suivantes:
            - find_author(oeuvre)
            - gen_text(auteur, taille, textname)
            - get_nth_element(auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et UniversitÃ© de Sherbrooke
    """

    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas Ã  Ãªtre modifiÃ©
    # Signes de ponctuation Ã  retirer (complÃ©ter la liste qui ne comprend que "!" et "," au dÃ©part)
    PONC = ["!","?",",",".","--",";",":","_","...","«","»","(",")","[","]","—"] # char that should be removed
    PONC_toSpace = ["-","'","\n"," "] # char that should be changed to a space

    def set_ponc(self, value):
        """DÃ©termine si les signes de ponctuation sont conservÃ©s (True) ou Ã©liminÃ©s (False)

        Args:
            value (boolean) : Conserve la ponctuation (Vrai) ou Ã©limine la ponctuation (Faux)

        Returns:
            void : ne fait qu'assigner la valeur du champs keep_ponc
        """
        self.keep_ponc = value

    def print_ponc(self):
        print("Signes de ponctuation Ã  retirer: ", self.PONC)

    def set_auteurs(self):
        """Obtient la liste des auteurs, Ã  partir du rÃ©pertoire qui les contient tous

        Note: le champs self.rep_aut doit Ãªtre prÃ©dÃ©fini:
            - Par dÃ©faut, il contient le rÃ©pertoire d'exÃ©cution du script
            - Peut Ãªtre redÃ©fini par la mÃ©thode set_aut_dir

        Returns:
            void : ne fait qu'obtenir la liste des rÃ©pertoires d'auteurs et modifier la liste self.auteurs
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        for auteur in full_path_auteurs:
            self.auteurs.append(ntpath.basename(auteur))
        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args:
            auteur (string): le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns:
            oeuvres (Liste[string]): liste des oeuvres (avec le chemin complet pour y accÃ©der)
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_aut_dir(self, aut_dir):
        """DÃ©finit le nom du rÃ©pertoire qui contient l'ensemble des rÃ©pertoires d'auteurs

        Note: L'appel Ã  cette mÃ©thode extrait la liste des rÃ©pertoires d'auteurs et les ajoute Ã  self.auteurs

        Args (string) : Nom du rÃ©pertoire en question (peut Ãªtre absolu ou bien relatif au rÃ©pertoire d'exÃ©cution)

        Returns:
            void : ne fait que dÃ©finir le nom du rÃ©pertoire qui contient les rÃ©pertoires d'auteurs
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()
        return


    def set_ngram(self, ngram):
        """Indique que l'analyse et la gÃ©nÃ©ration de texte se fera avec des n-grammes de taille ngram

        Args:
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns:
            void : ne fait que mettre Ã  jour le champs ngram
        """
        self.ngram = ngram

    def __init__(self):
        """Initialize l'objet de type markov lorsqu'il est crÃ©Ã©

        Args:
            aucun: Utilise simplement les informations fournies dans l'objet Markov_config

        Returns:
            void : ne fait qu'initialiser l'objet de type markov
        """

        # Initialisation des champs nÃ©cessaires aux fonctions fournies
        self.keep_ponc = True
        self.rep_aut = os.getcwd()
        self.auteurs = []
        self.ngram = 1
        self.dicts = {}
        # Au besoin, ajouter votre code d'initialisation de l'objet de type markov lors de sa crÃ©ation

        return

    # Ajouter les structures de donnÃ©es et les fonctions nÃ©cessaires Ã  l'analyse des textes,
    #   la production de textes alÃ©atoires, la dÃ©tection d'oeuvres inconnues,
    #   l'identification des n-iÃ¨mes mots les plus frÃ©quents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelÃ©e en premier par testmarkov.py
    # Ensuite, selon ce qui est demandÃ©, les fonctions find_author(), gen_text() ou get_nth_element() sont appelÃ©es


    def find_author(self, oeuvre):
        """AprÃ¨s analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximitÃ© (un nombre entre 0 et 1) de l'oeuvre inconnue avec les Ã©crits de chacun d'entre eux

        Args:
            oeuvre (string): Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns:
            resultats (Liste[(string,float)]) : Liste de tuples (auteurs, niveau de proximitÃ©), oÃ¹ la proximitÃ© est un nombre entre 0 et 1)
        """

        #ouverture et lecture du fichier
        with open(oeuvre, 'r', encoding='UTF-8') as currentFile:  # open the file
            currentText = currentFile.read()  # file to string
            currentFile.close()
        ##text formating

        for p in self.PONC:  # remove ponctuation
            currentText = currentText.replace(p, "")
        for p_space in self.PONC_toSpace:  # change some ponctuation to a [space]
            currentText = currentText.replace(p_space, " ")

        currentTextSplitted = []  # text as a list
        currentTextSplitted.extend(currentText.split(" "))
        currentTextFiltered =[]

        for word in currentTextSplitted:

            if len(word) > 2:
                currentTextFiltered.append(word)

        dictOeuvre = {}


        for word in currentTextFiltered:


            ng = ngram()
            ng.append(word)

            for i in range(currentTextFiltered.index(word) + 1, currentTextFiltered.index(word) + self.ngram):

                if (i < len(currentTextFiltered)):
                    ng.append(currentTextFiltered[i])

            if ng in dictOeuvre:
                dictOeuvre[ng] += 1

            else:
                dictOeuvre[ng] = 1

        resultats = []

        for key in self.dicts:
            formule = produitScalaire(self.dicts[key], dictOeuvre) / (module(self.dicts[key]) * module(dictOeuvre))
            resultats.append((key,formule))

        #resultats = [("balzac", 0.1234), ("voltaire", 0.1123)]   # Exemple du format des sorties


        # Ajouter votre code pour dÃ©terminer la proximitÃ© du fichier passÃ© en paramÃ¨tre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximitÃ© au fichier inconnu
        # Plus la proximitÃ© est grande, plus proche l'oeuvre inconnue est des autres Ã©crits d'un auteur
        #   Le produit scalaire entre le vecteur reprÃ©sentant les oeuvres d'un auteur
        #       et celui associÃ© au texte inconnu pourrait s'avÃ©rer intÃ©ressant...
        #   Le produit scalaire devrait Ãªtre normalisÃ© avec la taille du vecteur associÃ© au texte inconnu:
        #   proximitÃ© = (A . B) / (|A| |B|)   oÃ¹ A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           . est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        return resultats

    def gen_text(self, auteur, taille, textname):
        """AprÃ¨s analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args:
            auteur (string): Nom de l'auteur Ã  utiliser
            taille (int): Taille du texte Ã  gÃ©nÃ©rer
            textname (string): Nom du fichier texte Ã  gÃ©nÃ©rer.

        Returns:
            void : ne retourne rien, le texte produit doit Ãªtre Ã©crit dans le fichier "textname"
        """
        TextWordList = [] #liste of word that will make up the text
        writerBuffer = self.get_nth_element(auteur, 0)[0]

        TextWordList.extend(writerBuffer)
        for i in range(len(writerBuffer) , taille):

            currentNgram = ngram()
            for word in writerBuffer:
                currentNgram.append(word)
            """
            print("------new line_______")
            print(currentNgram.gram)
            print(self.dicts[auteur].get(currentNgram))
            print(list(self.dicts[auteur].get(currentNgram)))
            """
            #keyList = list(self.dicts[auteur].get(currentNgram))
            keyList = [key for key in self.dicts[auteur][currentNgram]]
            keyList = keyList[1::]
            valueList = [value for value in self.dicts[auteur][currentNgram].values()]
            valueList = valueList[1::]
            newWord = (random.choices(keyList, weights=valueList, k=1))
            TextWordList.extend(newWord)
            writerBuffer.extend(newWord)
            writerBuffer.pop(0)
            del (currentNgram)


        with open(textname, 'w', encoding='UTF-8') as outputFile:
            endOfLine = 0
            for word in TextWordList:

                outputFile.write(word)
                outputFile.write(" ")
                endOfLine += 1
                if endOfLine % 10 == 0:
                    outputFile.write("\n")

        return

    def get_nth_element(self, auteur, n):
        """AprÃ¨s analyse des textes d'auteurs connus, retourner le n-iÃ¨me plus frÃ©quent n-gramme de l'auteur indiquÃ©

        Args:
            auteur (string): Nom de l'auteur Ã  utiliser
            n (int): Indice du n-gramme Ã  retourner

        Returns:
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherchÃ© (il est possible qu'il y ait plus d'un n-gramme au mÃªme rang)
        """
        # -a pour choisir l'auteur
        # -F pour setter le n-gramme

        sortedNgram = sorted(self.dicts[auteur].items(), key=lambda item: item[1][0], reverse=True)
        nn = n - 1
        if n > len(sortedNgram):
            return [[]]
        returnList = []
        returnList.append(sortedNgram[nn][0].gram)

        frequency = sortedNgram[nn][1][0]
        offset = 1
        while sortedNgram[nn-offset][1][0] == frequency:
            returnList.append(sortedNgram[n-offset][0].gram)
            offset += 1
        offset = 1
        while sortedNgram[nn+offset][1][0] == frequency:
            returnList.append(sortedNgram[n+offset][0].gram)
            offset += 1

        return returnList


    def analyze(self):
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args:
            void: toute l'information est contenue dans l'objet markov

        Returns:
            void : ne retourne rien, toute l'information extraite est conservÃ©e dans des strutures internes
        """

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse:  faire le calcul des frÃ©quences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, Ã  la fois par oeuvre et aussi sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procÃ©dant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur
        # Il serait possible de considÃ©rer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de frÃ©quence pour chacune des oeuvres
        #       de faÃ§on indÃ©pendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant des les additionner pour obtenir le vecteur global d'un auteur
        #   De cette faÃ§on, les mots d'un court poÃ¨me auraient une importance beaucoup plus grande que
        #   les mots d'une trÃ¨s longue oeuvre du mÃªme auteur. Ce n'est PAS ce qui vous est demandÃ© ici.
        splitedTexts={}
        for auteur in self.auteurs:
            self.dicts[auteur]={}
            splitedTexts[auteur]=[]


        for key in splitedTexts.keys(): # for a single autor


            for currentFilePath in self.get_aut_files(key): # for a text of that autor
                #print("auteur: " + currentAutor + " / current file: " + currentFilePath)
                with open(currentFilePath, 'r', encoding='UTF-8') as currentFile: # open the file
                    currentText = currentFile.read().lower() # file to string
                    currentFile.close()
                    for p in self.PONC: # remove ponctuation
                        currentText = currentText.replace(p, "")
                    for p_space in self.PONC_toSpace: # change some ponctuation to a [space]
                        currentText = currentText.replace(p_space, " ")

                    # add current text to the word list of the corresponding autor
                    currentTextSplitted = []  # text as a list
                    currentTextSplitted.extend(currentText.split(" "))

                    currentTextFiltered = []  # text as a list with words above 2 letters
                    for word in currentTextSplitted:
                        if len(word) > 2:
                            splitedTexts[key].append(word)


        #for dict in self.dicts:
        for autorKey in self.dicts.keys(): # for a single dict in the nested dict
            # do something with the word list of the current autor
            # example: split into [Bigramme], [Trigramme], [n-gramme]


            wordList = splitedTexts[autorKey]

            counter = 0

            for word in wordList: # for each word in a single author

                counter += 1

                ng = ngram()
                ng.append(word)

                for i in range(counter, counter + self.ngram -1):
                    if(i<len(wordList)):
                        ng.append(wordList[i])

                if ng in self.dicts[autorKey]:
                    self.dicts[autorKey][ng][0] += 1
                else :
                    self.dicts[autorKey][ng] = {}
                    self.dicts[autorKey][ng].update({0: 1})

                if (counter + self.ngram) < len(wordList):
                    wordFollowup = wordList[counter + self.ngram -1]
                    if wordFollowup in self.dicts[autorKey][ng]:
                        self.dicts[autorKey][ng][wordFollowup] += 1
                    else:
                        self.dicts[autorKey][ng][wordFollowup] = 1
                    """
                    if self.dicts[autorKey][ng].get(nextW) == None:
                        self.dicts[autorKey][ng].update({nextW: 1})
                    else:
                        self.dicts[autorKey][ng][nextW] = 3
                    
                    
                    if nextW in self.dicts[autorKey][ng]:
                        self.dicts[autorKey][ng][nextW] += 1
                    else:
                        self.dicts[autorKey][ng][nextW] = 1
                    """


        return