import sys
import  nltk

import frequency_chunking
import dataset_loading
import text_reading.twenty_newsgroups
import text_reading.ruscorpora
import classify

REMOVE_STOPWORDS = True

def tail_cutting_experiment(in_train_set, in_test_set):
    for groups_number in xrange(4):
        freq_group_filter = \
            frequency_chunking.FrequencyGroupFilterWrapper(in_cut_tail = groups_number)
        quality = classify.classify_texts(in_train_set, in_test_set, freq_group_filter)
        print '%d tail groups cut: classification quality = %f' % (groups_number, quality)

def head_cutting_experiment(in_train_set, in_test_set):
    for groups_number in xrange(4):
        freq_group_filter = \
            frequency_chunking.FrequencyGroupFilterWrapper(in_cut_head = groups_number)
        quality = classify.classify_texts(in_train_set, in_test_set, freq_group_filter)
        print '%d head groups cut: classification quality = %f' % (groups_number, quality)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        exit('Usage: frequency_group_experiment.py <head|tail> <training data folder> <testing data root> \
             [dataset=ruscorpora|20newsgroups]')

    dataset_type = sys.argv[4]
    sentences_extractor = None
    stop_list = []
    if dataset_type == '20newsgroups':
        sentences_extractor = getattr(text_reading.twenty_newsgroups, 'load_text_raw')
        if REMOVE_STOPWORDS:
            stop_list = [word for word in nltk.corpus.stopwords.words('english')]
    elif dataset_type == 'ruscorpora':
        sentences_extractor = getattr(text_reading.ruscorpora, 'get_text_raw')
        if REMOVE_STOPWORDS:
            stop_list = [word.decode('utf-8') for word in nltk.corpus.stopwords.words('russian')]
    train_dataset = dataset_loading.DatasetLoader(sys.argv[2],
                                                  sentences_extractor,
                                                  in_stop_list = stop_list)
    test_dataset = dataset_loading.DatasetLoader(sys.argv[3],
                                                 sentences_extractor,
                                                 in_stop_list = stop_list)

    if sys.argv[1] == 'head':
        head_cutting_experiment(train_dataset, test_dataset)
    elif sys.argv[1] == 'tail':
        tail_cutting_experiment(train_dataset, test_dataset)