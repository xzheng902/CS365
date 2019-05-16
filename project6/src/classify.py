'''
    classify.py
    Mike Zheng and Heidi He
    5/15/19

    classify art type using the vgg-embedding (4096-vector)

    python3 classify.py ../data/data_subset_embedding_4096_reorder.csv ../data/metadata_subset_first_reorder.csv
    python3 classify.py ../data/data_subset_embedding_4096_reorder_train.csv ../data/metadata_subset_first_reorder_train.csv
    python3 classify.py ../data/data_subset_embedding_4096_reorder_test.csv ../data/metadata_subset_first_reorder_test.csv
    python3 classify.py /var/tmp/xzheng20_mhe_cs365_final/data/data_subset_embedding_4096_reorder_test.csv /var/tmp/xzheng20_mhe_cs365_final/data/metadata_subset_first_reorder_test.csv
'''

import sys
import classifiers
import numpy as np

def readlabels(filename):

    # read labels
    dict = {}
    labels = []
    fp = open(filename, "r")
    buf = fp.readline().strip()
    buf = fp.readline().strip()
    while buf!="":
        words = buf.split(",")
        type = words[2]
        if type not in dict:
            dict[type] = len(dict)
        labels.append(dict[type])
        buf = fp.readline().strip()
    fp.close()

    labelsmat = np.matrix(labels).T

    return labelsmat, dict


def main(argv):

    # usage
    if len(argv)<3:
        print("Usage: python3 %s <data.csv> <metadata.csv>"%argv[0])
        exit()

    datafilename = argv[1]
    metadatafilename = argv[2]

    # read data
    datamat = np.genfromtxt(datafilename, delimiter=',')
    # print(datamat)
    # print(datamat.shape)

    data = datamat[:,1:].astype(np.float32)
    # print(data)
    # print(data.shape)

    # read labels
    labelsmat, dict = readlabels(metadatafilename)
    print(dict)
    # print(labelsmat)
    # print(labelsmat.shape)
    inv_dict = {v: k for k, v in dict.items()}


    unique, counts = np.unique(labelsmat, return_counts=True, axis=0)
    print(unique)
    print(counts)


#############################################

    #
    #
    # top25idx = np.argsort(counts)[::-1].tolist()[:25]
    #
    #
    # data_top25 = []
    # labels_top25 = []
    #
    # for i in range(data.shape[0]):
    #     if labelsmat[i,0] in top25idx:
    #         labels_top25.append(labelsmat[i,0])
    #         data_top25.append(data[i,:])
    #
    # data_top25 = np.matrix(data_top25)
    # labels_top25 = np.matrix(labels_top25).T
    # # print(data_top25.shape)
    # # print(len(labels_top25))
    #
    # unique_top25, inverse_top25, counts_top25 = np.unique(labels_top25, return_counts=True, return_inverse=True, axis=0)
    # # print(unique_top25)
    # # print(counts_top25)
    # # print(inverse_top25)
    #
    # print("Labels:")
    # for i in range(unique_top25.shape[0]):
    #     print(i," : ",inv_dict[unique_top25[i,0]])
    #
    #
    # # CLASSIFY
    # K = 5
    # print( 'Building KNN Classifier (K=%d)'%K )
    # knnc = classifiers.KNN( data_top25, inverse_top25, K)
    #
    # print( 'KNN Training Set Results' )
    #
    # newcats, newlabels = knnc.classify( data_top25)
    #
    # confmtx = knnc.confusion_matrix( np.matrix(inverse_top25).T, newlabels )
    # print( knnc.confusion_matrix_str(confmtx) )
    #
    # # for i in range(labels_top25.shape[0]):
    # #     print(inverse_top25[i,0], newlabels[i,0])
    #
    # print("accuracy", knnc.accuracy(np.matrix(inverse_top25).T, newlabels))
    #


#####################################




    nnc= classifiers.NeuralNet(data, labelsmat)
    # nnc.train()
    # print("NN training done")
    test_data = data
    test_cats = labelsmat

    print("NN testing data")
    test_new_cats = nnc.classify(test_data)
    print(test_cats.shape)
    print("NN fisnished prediction")
    print(nnc.accuracy(test_cats, test_new_cats))




if __name__ == "__main__":
    main(sys.argv)
