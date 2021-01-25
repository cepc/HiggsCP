#coding=utf-8
#!/usr/bin/env python3

import sys
import os
import random
#import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import ROOT 
import joblib

import imblearn
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

def usage():
	print ('test usage')
	sys.stdout.write('''
			SYNOPSIS

			./BDT_pre.py signal, bkg 

			AUTHOR
			Yanxi Gu <GUYANXI@ustc.edu>

			DATE
			10 Jan 2021
			\n''')

def main():

    args = sys.argv[1:]
    if len(args) < 2:
        return usage()

    print ('part1')   

    # get root files and convert them to array
    branch_names = """ZPx,ZPy,ZPz,ZE,HiggsPx,HiggsPy,HiggsPz,HiggsE,MuonZPlusPx,MuonZPlusPy,MuonZPlusPz,MuonZPlusE,MuonZMinusPx,MuonZMinusPy,MuonZMinusPz,MuonZMinusE,Muon1PlusPx,Muon1PlusPy,Muon1PlusPz,Muon1PlusE,Muon1MinusPx,Muon1MinusPy,Muon1MinusPz,Muon1MinusE,Muon2PlusPx,Muon2PlusPy,Muon2PlusPz,Muon2PlusE,Muon2MinusPx,Muon2MinusPy,Muon2MinusPz,Muon2MinusE""".split(",")
#    branch_names = """ZPx,ZPy,ZPz,ZE,HiggsPx,HiggsPy,HiggsPz,HiggsE""".split(",")
#    branch_names = """MuonZPlusPx,MuonZPlusPy,MuonZPlusPz,MuonZPlusE,MuonZMinusPx,MuonZMinusPy,MuonZMinusPz,MuonZMinusE,Muon1PlusPx,Muon1PlusPy,Muon1PlusPz,Muon1PlusE,Muon1MinusPx,Muon1MinusPy,Muon1MinusPz,Muon1MinusE,Muon2PlusPx,Muon2PlusPy,Muon2PlusPz,Muon2PlusE,Muon2MinusPx,Muon2MinusPy,Muon2MinusPz,Muon2MinusE""".split(",")

    fin1 = ROOT.TFile(args[0])
    fin2 = ROOT.TFile(args[1])

    tree1 = fin1.Get("trialTree")
    signal = tree1.AsMatrix(columns=branch_names)
    tree2 = fin2.Get("trialTree")
    backgr = tree2.AsMatrix(columns=branch_names)

    # for sklearn data is usually organised into one 2D array of shape (n_samples * n_features)
    # containing all the data and one array of categories of length n_samples
    X_raw = np.concatenate((signal, backgr))
    y_raw = np.concatenate((np.ones(signal.shape[0]), np.zeros(backgr.shape[0])))

    print ('part2')

    #imbalanced learn
    n_sig = len(y_raw[y_raw==1])
    n_bkg = len(y_raw[y_raw==0])
    sb_ratio = len(y_raw[y_raw==1])/(1.0*len(y_raw[y_raw==0]))
    if (sb_ratio > 0.2 and sb_ratio < 0.5):
        smote = SMOTE(ratio=0.5)
        X, y = smote.fit_sample(X_raw, y_raw)
        print ('Number of events: ')
        print ('before: signal: ', len(y_raw[y_raw==1]), ' background: ', len(y_raw[y_raw==0]))
        print ('after: signal: ', len(y[y==1]), ' background: ', len(y[y==0]))
    elif (n_sig > 1000 and sb_ratio < 0.2 and sb_ratio > 0.1):
        smote = SMOTE(ratio=0.2)
        X, y = smote.fit_sample(X_raw, y_raw)
        print ('Number of events: ')
        print ('before: signal: ', len(y_raw[y_raw==1]), ' background: ', len(y_raw[y_raw==0]))
        print ('after: signal: ', len(y[y==1]), ' background: ', len(y[y==0]))
    elif (n_sig < 1000 and sb_ratio < 0.2 and sb_ratio > 0.1):
        smote = SMOTE(ratio=0.4)
        X, y = smote.fit_sample(X_raw, y_raw)
        print ('Number of events: ')
        print ('before: signal: ', len(y_raw[y_raw==1]), ' background: ', len(y_raw[y_raw==0]))
        print ('after: signal: ', len(y[y==1]), ' background: ', len(y[y==0]))
    elif (sb_ratio < 0.1 and sb_ratio > 0.05):
        smote = SMOTE(ratio=0.4)
        X, y = smote.fit_sample(X_raw, y_raw)
        print ('Number of events: ')
        print ('before: signal: ', len(y_raw[y_raw==1]), ' background: ', len(y_raw[y_raw==0]))
        print ('after: signal: ', len(y[y==1]), ' background: ', len(y[y==0]))
    elif (sb_ratio < 0.05 and sb_ratio > 0.01):
        smote = SMOTE(ratio=0.1)
        X, y = smote.fit_sample(X_raw, y_raw)
        print ('Number of events: ')
        print ('before: signal: ', len(y_raw[y_raw==1]), ' background: ', len(y_raw[y_raw==0]))
        print ('after: signal: ', len(y[y==1]), ' background: ', len(y[y==0]))
    elif (sb_ratio < 0.01):
        smote = SMOTE(ratio=0.03)
        X, y = smote.fit_sample(X_raw, y_raw)
        print ('Number of events: ')
        print ('before: signal: ', len(y_raw[y_raw==1]), ' background: ', len(y_raw[y_raw==0]))
        print ('after: signal: ', len(y[y==1]), ' background: ', len(y[y==0]))
    else:
        X = X_raw
        y = y_raw
        print ('Number of events: ')
        print ('signal: ', len(y[y==1]), ' background: ', len(y[y==0]))


    """
    Training Part
    """
    # Train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50, random_state=3443)

    dt = DecisionTreeClassifier(max_depth=1, min_samples_leaf=10, min_samples_split=20)

    bdt = AdaBoostClassifier(dt, algorithm='SAMME', n_estimators=800, learning_rate=0.5)
    bdt.fit(X_train, y_train)

    importances = bdt.feature_importances_
    f = open('bdt_results/output_importance.txt', 'w')
    f.write("%-25s%-15s\n"%('Variable Name','Output Importance'))
    for i in range (32):
        f.write("%-25s%-15s\n"%(branch_names[i], importances[i]))
        print("%-25s%-15s\n"%(branch_names[i], importances[i]), file=f)
    f.close() 

    y_predicted = bdt.predict(X_train)
    print (classification_report(y_train, y_predicted, target_names=["background", "signal"]))
    print ("Area under ROC curve: %.4f"%(roc_auc_score(y_train, bdt.decision_function(X_train))))

    y_predicted = bdt.predict(X_test)
    print (classification_report(y_test, y_predicted, target_names=["background", "signal"]))
    print ("Area under ROC curve: %.4f"%(roc_auc_score(y_test, bdt.decision_function(X_test))))

    decisions1 = bdt.decision_function(X_train)
    decisions2 = bdt.decision_function(X_test)

    filepath = 'SM-vs-BSM-CPeven'

    # Compute ROC curve and area under the curve
    fpr1, tpr1, thresholds1 = roc_curve(y_train, decisions1)
    fpr2, tpr2, thresholds2 = roc_curve(y_test, decisions2)
    roc_auc1 = auc(fpr1, tpr1)
    roc_auc2 = auc(fpr2, tpr2)
    fig=plt.figure(figsize=(8,6))
    fig.patch.set_color('white')
    plt.plot(fpr1, tpr1, lw=1.2, label='train:ROC (area = %0.4f)'%(roc_auc1), color="r")
    plt.plot(fpr2, tpr2, lw=1.2, label='test: ROC (area = %0.4f)'%(roc_auc2), color="b")
    plt.plot([0,1], [0,1], '--', color=(0.6, 0.6, 0.6), label = 'Luck')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating  characteristic')
    plt.legend(loc = "lower right")
    plt.grid()
    plt.savefig('./bdt_results/'+filepath+'/ROC.png')
#    plt.show()

    compare_train_test(bdt, X_train, y_train, X_test, y_test, filepath)

    joblib.dump(bdt, './bdt_results/'+filepath+'/bdt_model.pkl')

# Comparing train and test results
def compare_train_test(clf, X_train, y_train, X_test, y_test, savepath, bins=30):

    decisions = []
    for X,y in ((X_train, y_train), (X_test, y_test)):
        d1 = clf.decision_function(X[y>0.5]).ravel()
        d2 = clf.decision_function(X[y<0.5]).ravel()
        decisions += [d1, d2]

    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low, high)
    fig=plt.figure(figsize=(8,5.5))
    fig.patch.set_color('white')
    plt.hist(decisions[0], color='r', alpha=0.5, range=low_high, bins=bins, histtype='stepfilled', density = True, label='Signal (train)')
    plt.hist(decisions[1], color='b', alpha=0.5, range=low_high, bins=bins, histtype='stepfilled', density = True, label='Background (train)')
    
    hist, bins = np.histogram(decisions[2], bins=bins, range=low_high, density=True)
    scale = len(decisions[2])/sum(hist)
    err = np.sqrt(hist*scale)/scale

    width = (bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='Signal (test)')

    hist, bins = np.histogram(decisions[3], bins=bins, range=low_high, density=True)
    scale = len(decisions[2])/sum(hist)
    err = np.sqrt(hist*scale)/scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='Background (test)')
  
    plt.xlabel("BDT score")
    plt.ylabel("Normalized Unit")
    plt.legend(loc='best')
    plt.savefig("./bdt_results/"+savepath+"/BDTscore.png")
#    plt.show()

if __name__ == '__main__':
	print('start')
	main()
