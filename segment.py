import jieba
import jieba.posseg as psg
import os
import math
import re
from utils import files_processing
 
'''
read() 每次读取整个文件，它通常将读取到底文件内容放到一个字符串变量中，也就是说 .read() 生成文件内容是一个字符串类型。
readline()每只读取文件的一行，通常也是读取到的一行内容放到一个字符串变量中，返回str类型。
readlines()每次按行读取整个文件内容，将读取到的内容放到一个列表中，返回list类型。
'''

class segment():

    user_path = 'data/n.txt'
    jieba.load_userdict(user_path)
 
    stopwords_path='data/stopwords.txt'
    stopwords = []
    with open(stopwords_path, "r", encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            stopwords.append(line.strip())
    
    def segment_line(self, file_list,segment_out_dir,stopwords=[]):
        '''
        字词分割，对每行进行字词分割
        :param file_list:
        :param segment_out_dir:
        :param stopwords:
        :return:
        '''
        for i,file in enumerate(file_list):
            segment_out_name=os.path.join(segment_out_dir,'segment_{}.txt'.format(i))
            segment_file = open(segment_out_name, 'a', encoding='utf8')
            with open(file, encoding='utf8') as f:
                text = f.readlines()
                for sentence in text:
                    # jieba.cut():参数sentence必须是str(unicode)类型
                    sentence = list(jieba.cut(sentence))
                    sentence_segment = []
                    for word in sentence:
                        if word not in stopwords:
                            sentence_segment.append(word)
                    segment_file.write(" ".join(sentence_segment))
                del text
                f.close()
            segment_file.close()

    def segment_lines(self, file_list,segment_out_dir,stopwords=[]):
        '''
        字词分割，对整个文件内容进行字词分割
        :param file_list:
        :param segment_out_dir:
        :param stopwords:
        :return:
        '''

        for i,file in enumerate(file_list):
            segment_out_name=os.path.join(segment_out_dir,str(file.split('\\')[1].split('.')[0])+'_segment.txt')

            with open(file, 'r', encoding='utf-8') as f1, open(segment_out_name, 'w', encoding='utf-8') as f2:
                for line in f1.readlines():
                    sentence_segment = []
                    property = []
                    document_cut = psg.cut(line.strip())
                    for x in document_cut:
                        if x.word not in stopwords:
                            sentence_segment.append(x.word)
                            property.append(x.flag)
                    # result = ' '.join(sentence_segment) + ' ' + ' '.join(property) + '\n'
                    result = ' '.join(sentence_segment) + '\n'
                    f2.write(result)
    def split_lines_list(self, type, file, stopwords=stopwords):
        '''
        字词分割，对整个文件内容进行字词分割
        :param file:
        :param stopwords:
        :return:
        '''
        file_ = open(file, 'r', encoding='utf-8').readlines()
        name = str(file.split('\\')[-1].split('.')[0])

        segment_out_name=os.path.join('./data/segment',name+'_segment.txt')
        label_out_name=os.path.join('./data/segment',name+'_label.txt')

        file_segment = open(segment_out_name, 'w', encoding='utf-8')
        label = open(label_out_name, 'w', encoding='utf-8')

        for index, i in enumerate(file_):
            sentence_segment = []
            # property = []
            p = re.compile('(\\{..)|(\[.*\])|([\uD800-\uDBFF])|([\uDC00-\uDFFF])')
            i=p.sub( '', i.strip())
            # document_cut = jieba.cut(i.strip(), cut_all=False)
            # for x in document_cut:
            #     if x not in stopwords:
            #         sentence_segment.append(x)
                    # property.append(x.flag)
            # result = ' '.join(sentence_segment) + ' ' + ' '.join(property) + '\n'
            if index < len(file_)-1:
                result = ' '.join(i) + '\n'
                label.write(str(type) + '\n')
            else:
                result = ' '.join(i) 
                label.write(str(type))
            
            file_segment.write(result)
        file_segment.close()
        label.close()

        return segment_out_name, label_out_name
        
    def seg_lines_list(self, type, file, stopwords=stopwords):
        '''
        字词分割，对整个文件内容进行字词分割
        :param file:
        :param stopwords:
        :return:
        '''
        file_ = open(file, 'r', encoding='utf-8').readlines()
        name = str(file.split('\\')[-1].split('.')[0])

        segment_out_name=os.path.join('./data/segment',name+'_segment.txt')
        label_out_name=os.path.join('./data/segment',name+'_label.txt')

        file_segment = open(segment_out_name, 'w', encoding='utf-8')
        label = open(label_out_name, 'w', encoding='utf-8')

        for index, i in enumerate(file_):
            sentence_segment = []
            # property = []
            p = re.compile('(/{..)|(\[.*\])|([\uD800-\uDBFF][\uDC00-\uDFFF][\U00010000-\U0010ffff])')
            i=p.sub( '', i.strip())
            document_cut = jieba.cut(i.strip(), cut_all=False)
            for x in document_cut:
                if x not in stopwords:
                    sentence_segment.append(x)
                    # property.append(x.flag)
            # result = ' '.join(sentence_segment) + ' ' + ' '.join(property) + '\n'
            if index < len(file_)-1:
                result = ' '.join(sentence_segment) + '\n'
                label.write(str(type) + '\n')
            else:
                result = ' '.join(sentence_segment) 
                label.write(str(type))
            
            file_segment.write(result)
        file_segment.close()
        label.close()

        return segment_out_name, label_out_name

    def MergeTxt(filepath,outfile):
        k = open(filepath+outfile, 'a+', encoding='utf-8')
        for parent, dirnames, filenames in os.walk(filepath):
            for filepath in filenames:
                txtPath = os.path.join(parent, filepath) 
                f = open(txtPath, encoding='utf-8')
                k.write(f.read()+"\n")

if __name__=='__main__':
    # 多线程分词
    # jieba.enable_parallel()
    # 加载自定义词典
    user_path = 'data/n.txt'
    jieba.load_userdict(user_path)
 
    stopwords_path='data/stopwords.txt'
    stopwords=getStopwords(stopwords_path)
 
    file_dir='data/source/biaozhu'
    segment_out_dir='data/segment/biaozhu_property'
    file_list=files_processing.get_files_list(file_dir,postfix='*.txt')
    segment_lines(file_list, segment_out_dir, stopwords)
    # segment_lines(file_list, segment_out_dir)