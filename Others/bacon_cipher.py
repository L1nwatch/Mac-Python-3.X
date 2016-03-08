#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import string


def main():
    ciphertext = "BaCoN's cIphEr or THE bacOnIAN CiPHer iS a meThOD oF sTEGaNOGrapHY (a METhoD Of HidIng A sECRet MeSsaGe as OpPOsEd TO a TRUe CiPHeR) dEVIseD BY francis bAcoN. a MessAge Is coNCeALED in THe pRESenTatIoN OF TexT, ratHer thaN iTs coNteNt. tO enCODe A MEsSaGe, eaCh lETter Of THe pLAInText Is rePLAcED By A groUp oF fIvE OF thE lEtTErS 'a' or 'B'. thIS RepLacemEnT Is DOnE accOrdiNg To the aLphAbet of THe BACOnIAN cIpHeR, sHoWn bElOw. NoTe: A SeCoNd vErSiOn oF BaCoN'S CiPhEr uSeS A UnIqUe cOdE FoR EaCh lEtTeR. iN OtHeR WoRdS, i aNd j eAcH HaS ItS OwN PaTtErN. tHe wRiTeR MuSt mAkE UsE Of tWo dIfFeReNt tYpEfAcEs fOr tHiS CiPhEr. AfTeR PrEpArInG A FaLsE MeSsAgE WiTh tHe sAmE NuMbEr oF LeTtErS As aLl oF ThE As aNd bS In tHe rEaL, sEcReT MeSsAgE, tWo tYpEfAcEs aRe cHoSeN, oNe tO RePrEsEnT As aNd tHe oThEr bS. tHeN EaCh lEtTeR Of tHe fAlSe mEsSaGe mUsT Be pReSeNtEd iN ThE ApPrOpRiAtE TyPeFaCe, AcCoRdInG To wHeThEr iT StAnDs fOr aN A Or a b. To dEcOdE ThE MeSsAgE, tHe rEvErSe mEtHoD Is aPpLiEd. EaCh 'TyPeFaCe 1' LeTtEr iN ThE FaLsE MeSsAgE Is rEpLaCeD WiTh aN A AnD EaCh 'TyPeFaCe 2' LeTtEr iS RePlAcEd wItH A B. tHe bAcOnIaN AlPhAbEt iS ThEn uSeD To rEcOvEr tHe oRiGiNaL MeSsAgE. aNy mEtHoD Of wRiTiNg tHe mEsSaGe tHaT AlLoWs tWo dIsTiNcT RePrEsEnTaTiOnS FoR EaCh cHaRaCtEr cAn bE UsEd fOr tHe bAcOn cIpHeR. bAcOn hImSeLf pRePaReD A BiLiTeRaL AlPhAbEt[2] FoR HaNdWrItTeN CaPiTaL AnD SmAlL LeTtErS WiTh eAcH HaViNg tWo aLtErNaTiVe fOrMs, OnE To bE UsEd aS A AnD ThE OtHeR As b. ThIs wAs pUbLiShEd aS An iLlUsTrAtEd pLaTe iN HiS De aUgMeNtIs sCiEnTiArUm (ThE AdVaNcEmEnT Of lEaRnInG). BeCaUsE AnY MeSsAgE Of tHe rIgHt lEnGtH CaN Be uSeD To cArRy tHe eNcOdInG, tHe sEcReT MeSsAgE Is eFfEcTiVeLy hIdDeN In pLaIn sIgHt. ThE FaLsE MeSsAgE CaN Be oN AnY ToPiC AnD ThUs cAn dIsTrAcT A PeRsOn sEeKiNg tO FiNd tHe rEaL MeSsAgE."
    baconer = Baconer(ciphertext)
    plaintext = baconer.decrypt()
    print("plaintext = {0}".format(plaintext))
    print("plaintext with space: {0}".format(plaintext.replace("x", " ")))


class Baconer:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext
        self.bacon_map1 = {
            'a': "AAAAA", 'g': "AABBA", 'n': "ABBAA", 't': "BAABA",
            'b': "AAAAB", 'h': "AABBB", 'o': "ABBAB", '(u-v)': "BAABB",
            'c': "AAABA", '(i-j)': "ABAAA", 'p': "ABBBA", 'w': "BABAA",
            'd': "AAABB", 'k': "ABAAB", 'q': "ABBBB", 'x': "BABAB",
            'e': "AABAA", 'l': "ABABA", 'r': "BAAAA", 'y': "BABBA",
            'f': "AABAB", 'm': "ABABB", 's': "BAAAB", 'z': "BABBB"
        }
        self.bacon_map1_reverse = dict(zip(self.bacon_map1.values(), self.bacon_map1.keys()))

        self.bacon_map2 = {
            'a': "AAAAA", 'b': "AAAAB", 'c': "AAABA", 'd': "AAABB", 'e': "AABAA",
            'f': "AABAB", 'g': "AABBA", 'h': "AABBB", 'i': "ABAAA", 'j': "ABAAB",
            'k': "ABABA", 'l': "ABABB", 'm': "ABBAA", 'n': "ABBAB", 'o': "ABBBA",
            'p': "ABBBB", 'q': "BAAAA", 'r': "BAAAB", 's': "BAABA", 't': "BAABB",
            'u': "BABAA", 'v': "BABAB", 'w': "BABBA", 'x': "BABBB", 'y': "BBAAA",
            'z': "BBAAB"
        }
        self.bacon_map2_reverse = dict(zip(self.bacon_map2.values(), self.bacon_map2.keys()))

    def decrypt(self):
        cipertext = self._transorm()
        plaintext = ""
        for each in cipertext:
            try:
                plaintext += self.bacon_map2_reverse[each]
            except:
                plaintext += "?"

        return plaintext

    def _transorm(self):
        counts = 0
        result = list()
        text = ""
        for each in self.ciphertext:
            if each in string.ascii_lowercase:
                text += "A"
                counts += 1
            elif each in string.ascii_uppercase:
                text += "B"
                counts += 1

            if counts % 5 == 0 and counts != 0:
                result.append(text)
                text = ""
                counts = 0

        return result


if __name__ == "__main__":
    main()
