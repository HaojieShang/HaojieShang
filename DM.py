# from dis import dis
# from hmac import digest_size
import numpy as np
# from collections import Counter
import random
from math import *
# from threading import Thread,current_thread
# import multiprocessing
import time
# from multiprocessing.dummy import Pool as ThreadPool
# from tqdm import tqdm
# import math





time1=time.time()

data_path='DM/'

num_i=225
num_j=90
num_k=400
num_ijk=(num_i+1)*(num_j+1)*(num_k+1)

dis_x=2
dis_y=5
dis_z=3.27


random.seed(12345)


def get_left_right_point_num(i_index, j, k, num_top):
    left_num=0
    left_index=i_index
    left_U_num=0
    for i in range(i_index,0,-1):
        if data_range[i,j,k]!=-99:
            left_num+=1
            left_index=i
        else:
            left_U_num+=1
            if left_U_num>num_top:
                break
    right_num=0
    right_index=i_index
    right_U_num=0
    for i in range(i_index,num_i+1):
        if data_range[i,j,k]!=-99:
            right_num+=1
            right_index=i
        else:
            right_U_num+=1
            if right_U_num>num_top:
                break
    return left_num,right_num,left_index,right_index

print('加载范围数据...')
data_range=[[[-99 for k in range(num_k+1)]for j in range(num_j+1)]for i in range(num_i+1)]
data_range=np.array(data_range)
old_data=[]
data=[]
with open(data_path+'DM_input','r') as f:
    for line in f.readlines():
        line=line.strip('\n').split(' ')[0:4]
        old_data.append(line)
for i in range(6,len(old_data)):
    old_list=[]
    for j in old_data[i]:
        old_list.append(int(float(j)))
    data.append(old_list)
for i in range(len(data)):
    data_range[data[i][0],data[i][1],data[i][2]]=data[i][3]
print('成功加载范围数据')

print('加载模拟数据...')  
data_moni=[[[6 for k in range(num_k+1)] for j in range(num_j+1)] for i in range(num_i+1)]
data_moni=np.array(data_moni)
print('成功加载模拟数据')

print('加载记录节点数据') 
data_index=[[-99 for k in range(num_k+1)] for j in range(num_j+1)] #[当前段最小值，最大值，节点值]
data_index=np.array(data_index)
print('成功加载记录节点数据')

data_jie_dian=[]
nnn=0
mmm=0
for k in range(num_k+1):
    # 记录模拟进度
    nnn+=1
    if nnn%int((num_k+1)/10)==0 or nnn==(num_k+1):
        print('模拟进度: {:.2f}%'.format(nnn/(num_k+1)*100))
    for j in range(num_j+1):
        dm_data=[]    #获取断面数据
        for i in range(num_i+1):
            if data_range[i,j,k]!=-99:
                dm_data.append(i)
        if len(dm_data)>0:
            dm_duan=[[dm_data[0]]]
            for it in range(1,len(dm_data)): #将断面数据进行分段
                if dm_data[it]-dm_duan[len(dm_duan)-1][len(dm_duan[len(dm_duan)-1])-1]<2: #间隔5以内都可以作为一段，控制当前截线上的分段
                    dm_duan[len(dm_duan)-1].append(dm_data[it])
                else:
                    dm_duan.append([dm_data[it]])
            # 此处加载上一个截线的段数，进行判断
            last_duan_zong=[]
            try:
                last_duan_zong=data_jie_dian[data_index[j-1,k]]
            except:
                pass
            zong_jie_dian=[]
            # 对已有的段进行延伸
            if len(last_duan_zong)>0:
                for last_d in last_duan_zong: #遍历上一截线的所有段，用于继续延续
                    left_num,right_num,left_index,right_index=get_left_right_point_num(last_d[2],j,k,0) #获取上一截线上的节点在当前截线上左右的网格数量以及索引，控制5个空网格内为一段
                    if left_num>0 or right_num>0:
                        if left_num-right_num>1:
                            pian_yi_num=min(2,int(left_num/right_num))
                            zong_jie_dian.append((left_index,right_index,last_d[2]-pian_yi_num))  #当前段左索引值，右索引值，中间节点值
                        elif right_num-left_num>1:
                            pian_yi_num=min(2,int(right_num/left_num))
                            zong_jie_dian.append((left_index,right_index,last_d[2]+pian_yi_num))
                        else:
                            zong_jie_dian.append((left_index,right_index,last_d[2]))
            # 检查是否存在新出现的段
            for dm_d in dm_duan: #上一截线的所有段遍历完后，用于对新的段添加开始点
                if len(last_duan_zong)>0:
                    is_or_no=True
                    for jie_value in zong_jie_dian:
                        if jie_value[0]>dm_d[len(dm_d)-1] or jie_value[1]<dm_d[0]: #表明不是新的段   表明两段不相交
                            continue                            
                        else:  #表明两段相交
                            is_or_no=False
                            break
                    if is_or_no:
                        # 新出现的段，加入到总节点中
                        zong_jie_dian.append((dm_d[0],dm_d[len(dm_d)-1],dm_d[int(len(dm_d)/2)]))
                        # 在此处判别新出现的段是否为分叉的地方，是的话就往前补充，与主干接上
                        try:
                            is_fen_cha=True
                            for i_i in range(-2,3): #判别依据：上一条截线中，与当前点相邻的5个网格中，不为空值区域且值为初始值
                                if data_range[dm_d[int(len(dm_d)/2)]+i_i,j-1,k]!=-99 and data_moni[dm_d[int(len(dm_d)/2)]+i_i,j-1,k]==6:
                                    pass
                                else:
                                    is_fen_cha=False
                                    pass
                            if is_fen_cha:
                                x_x=dm_d[int(len(dm_d)/2)]
                                for j_j in range(j-1,0,-1): #从j-1往前走，直至与已有节点重合
                                    left_num,right_num,left_index,right_index=get_left_right_point_num(x_x,j_j,k,0)
                                    is_cun_zai=False
                                    for x_add in range(-2,3):
                                        if (left_index,right_index,x_x+x_add) in data_jie_dian[data_index[j_j,k]]:
                                            is_cun_zai=True
                                            break
                                    if is_cun_zai:
                                        break
                                    if left_num-right_num>1:
                                        pian_yi_num=min(2,int(left_num/right_num))
                                        data_jie_dian[data_index[j_j,k]].append((left_index,right_index,x_x-pian_yi_num))
                                        x_x=x_x-pian_yi_num
                                    elif right_num-left_num>1:
                                        pian_yi_num=min(2,int(right_num/left_num))
                                        data_jie_dian[data_index[j_j,k]].append((left_index,right_index,x_x+pian_yi_num))
                                        x_x=x_x+pian_yi_num
                                    else:
                                        data_jie_dian[data_index[j_j,k]].append(left_index,right_index,x_x)

                        except:
                            pass
                else:  #表明不存在上一截线
                    if (dm_d[0],dm_d[len(dm_d)-1],dm_d[int(len(dm_d)/2)]) not in zong_jie_dian:
                        zong_jie_dian.append((dm_d[0],dm_d[len(dm_d)-1],dm_d[int(len(dm_d)/2)]))
            # 对节点去重，主要去除重复的，若是没有重复的，则去除相近的
            # self_jie_dian=[]
            # if len(zong_jie_dian)>0:
            #     self_jie_dian.append(zong_jie_dian[0])
            #     for item in range(1,len(zong_jie_dian)):
            #         is_or_not=True
            #         for self_it in self_jie_dian:
            #             # if zong_jie_dian[item][2]>=self_it[0] and zong_jie_dian[item][2]<=self_it[1]: #表明两段相交
            #             if abs(zong_jie_dian[item][2]-self_it[2])<15:   #根据两个节点相邻的距离选择删除相近的节点
            #                 is_or_not=False
            #         if is_or_not:
            #             self_jie_dian.append(zong_jie_dian[item])
            data_index[j,k]=mmm
            data_jie_dian.append(zong_jie_dian)
            mmm+=1
# 添加扰动列表，控制角砾带断开
rd_jl=[]
rd_jl.append(random.randint(-1,1))
for j in range(int(num_j+num_k+5900+5900)):
    for _ in range(random.randint(3,6)):
        rd_jl.append(rd_jl[len(rd_jl)-1])
    if random.random() > 0.7:
        while rd_jl[len(rd_jl) - 1] < 1:  #表示最大偏移值为1
            if random.random() > 0.4:
                rd_jl.append(rd_jl[len(rd_jl) - 1])
            else:
                rd_jl.append(rd_jl[len(rd_jl) - 1] + 1)
        while rd_jl[len(rd_jl) - 1] > -1:  #表示最小偏移值为-1
            if random.random()>0.4:
                rd_jl.append(rd_jl[len(rd_jl)-1])
            else:
                rd_jl.append(rd_jl[len(rd_jl)-1]-1)
    else:
        rd_jl.append(rd_jl[len(rd_jl) - 1])
r_jl=[[0 for j in range(num_j+5900+1)] for k in range(num_k+5900+1)]
r_jl=np.array(r_jl)
for j in range(num_j+5901):
    for k in range(num_k+5901):
        r_jl[k, j] = rd_jl[j + k]
# 添加扰动列表，控制裂缝带断开
rd_lf=[]
rd_lf.append(random.randint(-2,2))
for j in range(int(num_j+num_k+5900+5900)):
    for _ in range(random.randint(3,6)):
        rd_lf.append(rd_lf[len(rd_lf)-1])
    if random.random()>0.7:
        while rd_lf[len(rd_lf)-1]<2:  #表示最大偏移值为3
            if random.random()>0.4:
                rd_lf.append(rd_lf[len(rd_lf)-1])
            else:
                rd_lf.append(rd_lf[len(rd_lf)-1]+1)
        while rd_lf[len(rd_lf)-1]>-2:   #表示最小偏移值为0
            if random.random()>0.4:
                rd_lf.append(rd_lf[len(rd_lf)-1])
            else:
                rd_lf.append(rd_lf[len(rd_lf)-1]-1)
    else:
        rd_lf.append(rd_lf[len(rd_lf)-1])
r_lf=[[0 for j in range(num_j+5900+1)] for k in range(num_k+5900+1)]
r_lf=np.array(r_lf)
for j in range(num_j+5901):
    for k in range(num_k+5901):
        r_lf[k, j] = rd_lf[j + k]

# 开始模拟赋值
for j in range(num_j+1):
    for k in range(num_k+1):
        if data_index[j,k]!=-99:
            for item in data_jie_dian[data_index[j,k]]:
                # data_moni[item[2],j,k]=str(8)
                # 核心段
                for x in range(item[2] - 8 + r_lf[j + 100, k + 100], item[2] + 7 + r_lf[j + 200, k + 200]):
                    if x>=item[0] and x<=item[1]:
                        if data_moni[x, j, k] == 6:
                            data_moni[x, j, k] = str(7)  #裂缝带
                for i in range(item[2] - 2 + r_jl[j + 100, k + 100], item[2] + 1 + r_jl[j + 200, k + 200]):
                    if i>=item[0] and i<=item[1]:
                        if data_moni[i, j, k] == 7:
                            data_moni[i, j, k] = str(8)  #角砾带

                # 左方第一段
                for x in range(item[2] - 22 - 8 + r_lf[j + 300, k + 300], item[2] - 22 + 7 + r_lf[j + 400, k + 400]):
                    if x>=item[0] and x<=item[1]:
                        if data_moni[x, j, k] == 6:
                            data_moni[x, j, k] = str(7)  #裂缝带
                for i in range(item[2] - 22 - 2 + r_jl[j + 300, k + 300], item[2] - 22 + 1 + r_jl[j + 400, k + 400]):
                    if i>=item[0] and i<=item[1]:
                        if data_moni[i, j, k] == 7:
                            data_moni[i, j, k] = str(8)  #角砾带
                # 右方第一段
                for x in range(item[2] + 22 - 8 + r_lf[j + 500, k + 500], item[2] + 22 + 7 + r_lf[j + 600, k + 600]):
                    if x>=item[0] and x<=item[1]:
                        if data_moni[x, j, k] == 6:
                            data_moni[x, j, k] = str(7)  #裂缝带
                for i in range(item[2] + 22 - 2 + r_jl[j + 500, k + 500], item[2] + 22 + 1 + r_jl[j + 600, k + 600]):
                    if i>=item[0] and i<=item[1]:
                        if data_moni[i, j, k] == 7:
                            data_moni[i, j, k] = str(8)  #角砾带

                # # 左方第二段
                # for x in range(item[2] - 32 - 5 + r_lf[j + 700, k + 700], item[2] - 32 + 5 + r_lf[j + 800, k + 800]):
                #     if x>=item[0] and x<=item[1]:
                #         if data_moni[x, j, k] == 6:
                #             data_moni[x, j, k] = str(7)  #裂缝带
                # for i in range(item[2] - 32 - 1 + r_jl[j + 700, k + 700], item[2] - 32 + 1 + r_jl[j + 800, k + 800]):
                #     if i>=item[0] and i<=item[1]:
                #         if data_moni[i, j, k] == 7:
                #             data_moni[i, j, k] = str(8)  #角砾带
                # # 右方第二段
                # for x in range(item[2] + 32 - 5 + r_lf[j + 900, k + 900], item[2] + 32 + 5 + r_lf[j + 1000, k + 1000]):
                #     if x>=item[0] and x<=item[1]:
                #         if data_moni[x, j, k] == 6:
                #             data_moni[x, j, k] = str(7)  #裂缝带
                # for i in range(item[2] + 32 - 1 + r_jl[j + 900, k + 900], item[2] + 32 + 1 + r_jl[j + 1000, k + 1000]):
                #     if i>=item[0] and i<=item[1]:
                #         if data_moni[i, j, k] == 7:
                #             data_moni[i, j, k] = str(8)  #角砾带
file_path = data_path + 'DM_output' + '.txt'

nnnn=0
with open(file_path,'w') as f: # 'w'方式可以无需提前新建文件，存在则打开，不存在则新建
    f.write('PETREL: Properties'+'\n')
    f.write('4'+'\n')
    f.write('i_index unit1 scale1'+'\n')
    f.write('j_index unit1 scale1'+'\n')
    f.write('k_index unit1 scale1'+'\n')
    model_name='Facies'+'_DM'+' unit1 scale1'
    f.write(model_name+'\n')
    for k in range(num_k+1):
        # 记录模拟进度
        nnnn+=1
        if nnnn%int((num_k+1)/10)==0 or nnnn==(num_k+1):
            print('写入进度: {:.2f}%'.format(nnnn / (num_k + 1) * 100))
        # 记录模拟进度
        for j in range(num_j+1):
            for i in range(num_i+1):
                if data_range[i,j,k]!=-99:  #or data_moni[i,j,k]==8
                    f.write('%s %s %s %s\n' % (str(i), str(j), str(k), str(data_moni[i, j, k])))
f.close()
time2=time.time()

print('用时：',time2-time1,'s')

jy_num=0
lf_num=0
jl_num=0
for k in range(num_k+1):
    for j in range(num_j+1):
        for i in range(num_i+1):
            if data_range[i,j,k]!=-99:
                if data_moni[i,j,k]==6:
                    jy_num+=1
                elif data_moni[i,j,k]==7:
                    lf_num+=1
                else:
                    jl_num+=1
zong_num=jy_num+lf_num+jl_num
jy_bili=jy_num/zong_num
lf_bili=lf_num/zong_num
jl_bili=jl_num/zong_num
print('基岩占比：',jy_bili)
print('裂缝占比：',lf_bili)
print('角砾占比：',jl_bili)


