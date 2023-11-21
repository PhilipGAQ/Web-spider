#利用FOR算法对倒排表进行压缩
import json
from collections import defaultdict
import math
import sys
import copy




#For算法(Frame of Reference)
#首先将倒排表中的tag变成差值保存
def compress(inverted_index,k):
    for key in inverted_index.keys():
        for i in range(len(inverted_index[key])-1,0,-1):
            inverted_index[key][i] = inverted_index[key][i] - inverted_index[key][i-1]
    #print(inverted_index)
    Compressed_inverted_index = defaultdict(list)
    #对于tag差值，进行顺序分组，每组长度为k
    #max_temp : 每组中的最大值
    #bit_max : max_temp的二进制长度
    #str_bit_max : bit_max的二进制串表示
    #k的值待定
    for key in inverted_index.keys():
        str_bit = ''
        for i in range(0,len(inverted_index[key]) ,k):
            temp = []
            temp[0:k] = inverted_index[key][i:i+k]
            max_temp = max(temp)
            bit_max = math.ceil(math.log2(max_temp + 1))
            str_bit_max = '{:04b}'.format(bit_max)
            str_bit = str_bit + str_bit_max
            for j in range(0,k):
                if(j < len(temp)):
                    str_bit_temp = '{:0{}b}'.format(temp[j],bit_max)
                    str_bit = str_bit + str_bit_temp
        #将str_bit反转
        str_bit = str_bit[::-1]
        Compressed_inverted_index[key] = int(str_bit,2)
    return Compressed_inverted_index


#解码Compressed_inverted_index
def depress(Compressed_inverted_index,key,k):
    Decompressed_inverted_index = defaultdict(list)
    temp_str = str(bin(Compressed_inverted_index[key])[2:])
    temp_str = temp_str[::-1]
    while(temp_str != ''):
        bit_max = int(temp_str[0:4],2)
        if(bit_max == 0):
            break
        str_todo = temp_str[4:4+ k * bit_max]
        if(len(str_todo) % bit_max != 0):
            str_todo = str_todo + '0' * (bit_max*(int(len(str_todo)/bit_max) + 1) - len(str_todo))
        for i in range(0,len(str_todo),bit_max):
            Decompressed_inverted_index[key].append(int(str_todo[i:i+bit_max],2))
        temp_str = temp_str[4 + k * bit_max:]
#将Decompressed_inverted_index的tag由差值变回原来的值
    for i in range(1,len(Decompressed_inverted_index[key])):
        Decompressed_inverted_index[key][i] = Decompressed_inverted_index[key][i] + Decompressed_inverted_index[key][i-1]
    return Decompressed_inverted_index[key]


