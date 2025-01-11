from dis import dis
from hmac import digest_size
import numpy as np
from collections import Counter
import random
from math import *
from threading import Thread,current_thread
import multiprocessing
import time
from multiprocessing.dummy import Pool as ThreadPool
# from tqdm import tqdm
import math

# time.sleep(7200)
print('开始模拟')


kuo_bian=100

data_path='DX/'

num_i=225
num_j=90
num_k=400
num_ijk=num_i*num_j*num_k

dis_x=2
dis_y=5
dis_z=3.27



def read_in_chunks(filepath,chunk_size,num):
    
    file_object=open(filepath,'r',encoding='utf-8')
    while True:
        num+=1
        chunk_data=file_object.readlines(chunk_size)
        if not chunk_data:
            break
        yield chunk_data,num
def Nrotation_angle_get_coor_coordinates(point, center, angle, dis):  #顺时针
    src_i, src_j = point
    src_x=src_i*dis[0]
    src_y=src_j*dis[1]
    add_point_x=(src_i-1)*dis[0]+dis[0]/2
    add_point_y=(src_j-1)*dis[1]+dis[1]/2
    center_i, center_j = center
    center_x=center_i*dis[0]
    center_y=center_j*dis[1]
    radian = math.radians(angle)

    dest_x = round((src_x-center_x) * math.cos(radian) + (src_y-center_y)*math.sin(radian) + center_x)
    dest_y = round((src_y-center_y) * math.cos(radian) - (src_x-center_x)*math.sin(radian) + center_y)

    add_x = round((add_point_x-center_x) * math.cos(radian) + (add_point_y-center_y)*math.sin(radian) + center_x)
    add_y = round((add_point_y-center_y) * math.cos(radian) - (add_point_x-center_x)*math.sin(radian) + center_y)

    dest_i=dest_x/dis[0]
    dest_j=dest_y/dis[1]

    add_x=add_x/dis[0]
    add_y=add_y/dis[1]

    return [[int(dest_i),int(dest_j)],[int(add_x),int(add_y)]]

def Srotation_angle_get_coor_coordinates(point, center, angle, dis):  #逆时针
    src_i, src_j = point
    src_x=src_i*dis[0]
    src_y=src_j*dis[1]
    add_point_x=(src_i-1)*dis[0]+dis[0]/2
    add_point_y=(src_j-1)*dis[1]+dis[1]/2
    center_i, center_j = center
    center_x=center_i*dis[0]
    center_y=center_j*dis[1]
    radian = math.radians(angle)

    dest_x = round((src_x-center_x) * math.cos(radian) - (src_y-center_y)*math.sin(radian) + center_x)
    dest_y = round((src_x-center_x) * math.sin(radian) + (src_y-center_y)*math.cos(radian) + center_y)

    add_x = round((add_point_x-center_x) * math.cos(radian) - (add_point_y-center_y)*math.sin(radian) + center_x)
    add_y = round((add_point_x-center_x) * math.sin(radian) + (add_point_y-center_y)*math.cos(radian) + center_y)

    dest_i=dest_x/dis[0]
    dest_j=dest_y/dis[1]

    add_x=add_x/dis[0]
    add_y=add_y/dis[1]
    
    return [[int(dest_i),int(dest_j)],[int(add_x),int(add_y)]]

# 划分洞穴,根据values值
lei_bie=[]
lei_bie_ijk=[]
print('加载范围数据...')
data_range=[[[-99 for k in range(num_k+int(kuo_bian*2)+1)] for j in range(num_j+int(kuo_bian*2)+1)] for i in range(num_i+int(kuo_bian*2)+1)]
data_range=np.array(data_range)
old_data=[]
data=[]
with open(data_path+'DX_input','r') as f:
    for line in f.readlines():
        line=line.strip('\n').split(' ')[0:4]
        old_data.append(line)
for i in range(6,len(old_data)):
    old_list=[]
    for j in old_data[i]:
        old_list.append(int(float(j)))
    data.append(old_list)
for i in range(len(data)):
    data_range[data[i][0]+kuo_bian,data[i][1]+kuo_bian,data[i][2]+kuo_bian]=data[i][3]
    if data[i][3] not in lei_bie:
        lei_bie.append(data[i][3])
        lei_bie_ijk.append([[data[i][0]+kuo_bian],[data[i][1]+kuo_bian],[data[i][2]+kuo_bian]])
    else:
        lei_bie_ijk[lei_bie.index(data[i][3])][0].append(data[i][0]+kuo_bian)
        lei_bie_ijk[lei_bie.index(data[i][3])][1].append(data[i][1]+kuo_bian)
        lei_bie_ijk[lei_bie.index(data[i][3])][2].append(data[i][2]+kuo_bian)
print('成功加载范围数据')

# 加载断面数据，断面数据仅包含和洞穴相交部分的区域
# print('加载断面数据')
# data_dm=[[[-99 for k in range(num_k+int(kuo_bian*2)+1)] for j in range(num_j+int(kuo_bian*2)+1)] for i in range(num_i+int(kuo_bian*2)+1)]
# data_dm=np.array(data_dm)
# old_data=[]
# data=[]
# try:
#     with open(data_path+'DM_only_DX','r') as f:
#         for line in f.readlines():
#             line=line.strip('\n').split(' ')[0:4]
#             old_data.append(line)
#     for i in range(6,len(old_data)):
#         old_list=[]
#         for j in old_data[i]:
#             old_list.append(int(float(j)))
#         data.append(old_list)
#     for i in range(len(data)):
#         data_dm[data[i][0]+kuo_bian,data[i][1]+kuo_bian,data[i][2]+kuo_bian]=data[i][3]
# except:
#     pass
# print('成功加载断面数据')
# print('data_dm[1308,92,300]=',data_dm[1308+kuo_bian,92+kuo_bian,300+kuo_bian])

# 加载测井电阻率数据，电阻率数据仅包含和洞穴相交部分的区域
# print('加载测井数据')
# data_rs=[[[-99.0 for k in range(num_k+int(kuo_bian*2)+1)] for j in range(num_j+int(kuo_bian*2)+1)] for i in range(num_i+int(kuo_bian*2)+1)]
# data_rs=np.array(data_rs)
# old_data=[]
# data=[]
# try:
#     with open(data_path+'RS_only_DX','r') as f:
#         for line in f.readlines():
#             line=line.strip('\n').split(' ')[0:4]
#             old_data.append(line)
#     for i in range(6,len(old_data)):
#         old_list=[]
#         for j in range(len(old_data[i])-1):
#             old_list.append(int(float(old_data[i][j])))
#         old_list.append(float(old_data[i][len(old_data[i])-1]))
#         data.append(old_list)
#     for i in range(len(data)):
#         data_rs[data[i][0]+kuo_bian,data[i][1]+kuo_bian,data[i][2]+kuo_bian]=data[i][3]
# except:
#     pass
# print('成功加载测井数据')
# print('data_rs[1471,847,147]=',data_rs[1471+kuo_bian,847+kuo_bian,147+kuo_bian])

lei_bie_xyz=[] #[0lei_bie,1x_min,2x_max,3y_min,4y_max,5z_min,6z_max]
for i in range(len(lei_bie)):
    lei_bie_xyz.append([lei_bie[i],min(lei_bie_ijk[i][0]),max(lei_bie_ijk[i][0]),min(lei_bie_ijk[i][1]),max(lei_bie_ijk[i][1]),min(lei_bie_ijk[i][2]),max(lei_bie_ijk[i][2])])



DX_id=[]
for iii in range(1):#29+1
    DX_id.append(iii)

for iiii in DX_id:
    values_dx=iiii

    time1=time.time()

    file_path_root=data_path+'DX_output/DX_'+str(values_dx)


    '''# ###
    更改了旋转函数
    以及下面的旋转赋值代码
    添加水平旋转代码块

    对当前洞穴，首先平移一百个网格，做个更大范围的模型
    增加条带数
    # ###'''

    random.seed(12345)


    # 获取指定某个洞穴的外切立方体的坐标范围，此处三方向最大最小值已经全部为真实值+100(kuo_bian)
    for item in lei_bie_xyz:
        if item[0]==values_dx:
            x_min=item[1]
            x_max=item[2]
            y_min=item[3]
            y_max=item[4]
            z_min=item[5]
            z_max=item[6]
            print('item:',item)
    if y_min>=600:
        y_pian_yi=y_min-kuo_bian*3
        y_min=y_min-y_pian_yi
        y_max=y_max-y_pian_yi
    else:
        y_pian_yi=0
    # 此处三个data的初始范围均为按照最大值加101
    print('加载模拟数据...')  
    data_moni=[[[2 for z in range(z_max+kuo_bian*1+1)] for j in range(y_max+kuo_bian*1+1)] for i in range(x_max+kuo_bian*1+1)]
    data_moni=np.array(data_moni)
    print('成功加载模拟数据')

    print('加载旋转数据...')  
    data_xz=[[[2 for z in range(z_max+kuo_bian*1+1)] for j in range(y_max+kuo_bian*1+1)] for i in range(x_max+kuo_bian*1+1)]
    data_xz=np.array(data_xz)
    print('成功加载旋转数据')

    # print('加载水平(sp)旋转数据...')  #    qx:倾斜
    # data_xz_qx=[[[2 for z in range(z_max+kuo_bian*1+1)] for j in range(y_max+kuo_bian*1+1)] for i in range(x_max+kuo_bian*1+1)]
    # data_xz_qx=np.array(data_xz_qx)
    # print('成功加载水平(sp)旋转数据')

    # print('加载水平(sp)旋转数据...')  #    sz:竖直
    # data_xz_sz=[[[2 for z in range(z_max+kuo_bian*1+1)] for j in range(y_max+kuo_bian*1+1)] for i in range(x_max+kuo_bian*1+1)]
    # data_xz_sz=np.array(data_xz_sz)
    # print('成功加载水平(sp)旋转数据')



    # 针对单个洞穴，获取长度，最长度对应的坐标，最长度对应的i值最大最小值
    max_wide_num=[0,0,0,0,0,0] #长度[0]，坐标[123]，i方向最小最大值[45]
    for y in range(y_min,y_max+1):
        for z in range(z_min,z_max+1):
            wide_num=0
            i_zong=[]
            for x in range(x_min,x_max+1):
                if data_range[x,y+y_pian_yi,z]==values_dx:
                    wide_num+=1
                    i_zong.append(x)
            if wide_num>max_wide_num[0]:
                max_wide_num[0]=wide_num
                max_wide_num[1]=x
                max_wide_num[2]=y
                max_wide_num[3]=z
                max_wide_num[4]=min(i_zong)
                max_wide_num[5]=max(i_zong)
    print('max_wide_num: ',max_wide_num)



    # 创建扰动列表
    rao_dong_1d=[]
    rao_dong_1d.append(random.randint(-2,2))
    for j in range(int(num_j+num_k+2900+2900)):
        for _ in range(random.randint(3,6)):
            rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1])
        if rao_dong_1d[len(rao_dong_1d)-1]==2:
            if random.random()>0.5:
                rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1])
            else:
                rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1]-1)
        elif rao_dong_1d[len(rao_dong_1d)-1]==-2:
            if random.random()>0.5:
                rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1])
            else:
                rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1]+1)
        else:
            if random.random()>0.5:
                rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1]+1)
            else:
                rao_dong_1d.append(rao_dong_1d[len(rao_dong_1d)-1]-1)
    rao_dong=[[0 for j in range(num_j+2901)]for k in range(num_k+2901)]
    rao_dong=np.array(rao_dong)

    for j in range(num_j+2900+1):
        for k in range(num_k+2900+1):
            rao_dong[k,j]=rao_dong_1d[j+k]

    # 上述扰动列表适用于单个条带，目的是条带边界有弯曲，为让条带中间最宽，向两端渐窄，下面使用新的扰动列表，
    rd_l=[]
    z_mean=int((z_max+z_min)/2)
    rd_l.append(random.randint(2,2))

    n=0
    for i in range(int(z_mean-z_min)+kuo_bian):
        if rd_l[0]>0:
            yu_zhi=random.random()
            if yu_zhi>0.2 or n<int((z_max-z_min+kuo_bian*2)/10):
                rd_l.insert(0,rd_l[0])
                n+=1
            else:
                rd_l.insert(0,rd_l[0]-1)
                n=0
        else:
            rd_l.insert(0,rd_l[0])
    n=0
    for i in range(int(z_max-z_min)+kuo_bian):
        if rd_l[len(rd_l)-1]>0:
            yu_zhi=random.random()
            if yu_zhi>0.2 or n<int((z_max-z_min+kuo_bian*2)/10):
                rd_l.append(rd_l[len(rd_l)-1])
                n+=1
            else:
                rd_l.append(rd_l[len(rd_l)-1]-1)
                n=0
        else:
            rd_l.append(rd_l[len(rd_l)-1])
    # 上述是左侧偏移值列表，下面是右侧偏移值列表
    rd_r=[]
    rd_r.append(random.randint(0,0))

    n=0
    for i in range(int(z_mean-z_min)+kuo_bian):
        if rd_r[0]>-1:
            yu_zhi=random.random()
            if yu_zhi>0.2 or n<int((z_max-z_min+kuo_bian*2)/10):
                rd_r.insert(0,rd_r[0])
                n+=1
            else:
                rd_r.insert(0,rd_r[0]-1)
                n=0
        else:
            rd_r.insert(0,rd_r[0])
    n=0
    for i in range(int(z_max-z_min)+kuo_bian):
        if rd_r[len(rd_r)-1]>-1:
            yu_zhi=random.random()
            if yu_zhi>0.2 or n<int((z_max-z_min+kuo_bian*2)/10):
                rd_r.append(rd_r[len(rd_r)-1])
                n+=1
            else:
                rd_r.append(rd_r[len(rd_r)-1]-1)
                n=0
        else:
            rd_r.append(rd_r[len(rd_r)-1])

    # 添加扰动列表，控制角砾带断开
    rd_1d=[]
    rd_1d.append(random.randint(0,0))
    for j in range(int(num_j+num_k+2900+2900)):
        for _ in range(random.randint(3,6)):
            rd_1d.append(rd_1d[len(rd_1d)-1])
        if random.random()>0.7:
            while rd_1d[len(rd_1d)-1]<=1:  #表示最大偏移值为3
                if random.random()>0.4:
                    rd_1d.append(rd_1d[len(rd_1d)-1])
                else:
                    rd_1d.append(rd_1d[len(rd_1d)-1]+1)
            while rd_1d[len(rd_1d)-1]>=-1:   #表示最小偏移值为0
                if random.random()>0.4:
                    rd_1d.append(rd_1d[len(rd_1d)-1])
                else:
                    rd_1d.append(rd_1d[len(rd_1d)-1]-1)
        else:
            rd_1d.append(rd_1d[len(rd_1d)-1])
    rd_2d=[[0 for i in range(num_j+2900+1)] for k in range(num_k+2900+1)]
    rd_2d=np.array(rd_2d)
    for j in range(num_j+2901):
        for k in range(num_k+2901):
            rd_2d[k,j]=rd_1d[j+k]


    def get_midd_zhoubian(j,k):
        midd_zhoubian=[]
        try:
            if facies_zhou[j-1,k]!=-99:
                midd_zhoubian.append(int(facies_zhou[j-1,k]))
        except:
            pass
        try:
            if facies_zhou[j+1,k]!=-99:
                midd_zhoubian.append(int(facies_zhou[j+1,k]))
        except:
            pass
        try:
            if facies_zhou[j,k-1]!=-99:
                midd_zhoubian.append(int(facies_zhou[j,k-1]))
        except:
            pass
        try:
            if facies_zhou[j,k+1]!=-99:
                midd_zhoubian.append(int(facies_zhou[j,k+1]))
        except:
            pass
        return midd_zhoubian

    # 创建二维列表，获取中轴面，保证连续
    facies_zhou=[[-99 for k in range(z_max+kuo_bian+1)] for j in range(y_max+kuo_bian+1)]
    facies_zhou=np.array(facies_zhou)
    for j in range(max_wide_num[2],y_max+kuo_bian+1):
        for k in range(max_wide_num[3],z_max+kuo_bian+1):
            i_zong=[]
            for x in range(x_min,x_max+1):
                if data_range[x,j+y_pian_yi,k]==values_dx:
                    i_zong.append(x)
            i_midd_core=int((max_wide_num[4]+max_wide_num[5])/2)
            midd_zhoubian=get_midd_zhoubian(j,k)
            if len(i_zong)>0:
                i_min=min(i_zong)
                i_max=max(i_zong)
                i_midd_chushi=int((i_min+i_max)/2)

                if len(midd_zhoubian)<1:   #当前点周边没有已知值
                    facies_zhou[j,k]=i_midd_chushi
                    # data_moni[i,j_midd_chushi,k]=str(1)
                elif len(midd_zhoubian)==1:  #当前点周边有一个已知值
                    zb_val=midd_zhoubian[0]
                    if zb_val-i_midd_chushi>1:
                        i_midd=zb_val-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    elif zb_val-i_midd_chushi<-1:
                        i_midd=zb_val+1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:
                        facies_zhou[j,k]=i_midd_chushi
                        # data_moni[i,j_midd_chushi,k]=str(1)
                else:  #当前点周边有两个或两个以上已知值
                    zb_min=min(midd_zhoubian)
                    zb_max=max(midd_zhoubian)
                    if zb_max==zb_min: #最大值与最小值相同
                        if zb_min-i_midd_chushi>1:
                            i_midd=zb_min-1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min-i_midd_chushi<-1:
                            i_midd=zb_min+1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            facies_zhou[j,k]=i_midd_chushi
                            # data_moni[i,j_midd_chushi,k]=str(1)
                    elif zb_max-zb_min==1: #最大值与最小值相差1
                        if zb_max==i_midd_chushi:
                            i_midd=zb_max
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min==i_midd_chushi:
                            i_midd=zb_min
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            if facies_zhou[j,k-1]!=-99:
                                i_midd=facies_zhou[j,k-1]
                            elif facies_zhou[j,k+1]!=-99:
                                i_midd=facies_zhou[j,k+1]
                            else:
                                i_midd=random.randint(zb_min,zb_max)
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                    elif zb_max-zb_min==2:  #最大值与最小值相差2
                        i_midd=zb_max-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:  #最大值与最小值相差3及以上
                        if facies_zhou[j,k-1]<zb_max and facies_zhou[j,k-1]>zb_min:
                            i_midd=facies_zhou[j,k-1]
                        elif facies_zhou[j,k+1]<zb_max and facies_zhou[j,k+1]>zb_min:
                            i_midd=facies_zhou[j,k+1]
                        else:
                            i_midd=random.randint(zb_min+1,zb_max-1)
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
            else:
                i_midd=i_midd_core
                facies_zhou[j,k]=i_midd
                # data_moni[i,j_midd,k]=str(1)
    for j in range(max_wide_num[2],y_max+kuo_bian+1):
        for k in range(max_wide_num[3],z_min-kuo_bian-1,-1):
            i_zong=[]
            for x in range(x_min,x_max+1):
                if data_range[x,j+y_pian_yi,k]==values_dx:
                    i_zong.append(x)
            i_midd_core=int((max_wide_num[4]+max_wide_num[5])/2)
            midd_zhoubian=get_midd_zhoubian(j,k)
            if len(i_zong)>0:
                i_min=min(i_zong)
                i_max=max(i_zong)
                i_midd_chushi=int((i_min+i_max)/2)
                
                if len(midd_zhoubian)<1:   #当前点周边没有已知值
                    facies_zhou[j,k]=i_midd_chushi
                    # data_moni[i,j_midd_chushi,k]=str(1)
                elif len(midd_zhoubian)==1:  #当前点周边有一个已知值
                    zb_val=midd_zhoubian[0]
                    if zb_val-i_midd_chushi>1:
                        i_midd=zb_val-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    elif zb_val-i_midd_chushi<-1:
                        i_midd=zb_val+1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:
                        facies_zhou[j,k]=i_midd_chushi
                        # data_moni[i,j_midd_chushi,k]=str(1)
                else:  #当前点周边有两个或两个以上已知值
                    zb_min=min(midd_zhoubian)
                    zb_max=max(midd_zhoubian)
                    if zb_max==zb_min: #最大值与最小值相同
                        if zb_min-i_midd_chushi>1:
                            i_midd=zb_min-1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min-i_midd_chushi<-1:
                            i_midd=zb_min+1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            facies_zhou[j,k]=i_midd_chushi
                            # data_moni[i,j_midd_chushi,k]=str(1)
                    elif zb_max-zb_min==1: #最大值与最小值相差1
                        if zb_max==i_midd_chushi:
                            i_midd=zb_max
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min==i_midd_chushi:
                            i_midd=zb_min
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            if facies_zhou[j,k-1]!=-99:
                                i_midd=facies_zhou[j,k-1]
                            elif facies_zhou[j,k+1]!=-99:
                                i_midd=facies_zhou[j,k+1]
                            else:
                                i_midd=random.randint(zb_min,zb_max)
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                    elif zb_max-zb_min==2:  #最大值与最小值相差2
                        i_midd=zb_max-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:  #最大值与最小值相差3及以上
                        if facies_zhou[j,k-1]<zb_max and facies_zhou[j,k-1]>zb_min:
                            i_midd=facies_zhou[j,k-1]
                        elif facies_zhou[j,k+1]<zb_max and facies_zhou[j,k+1]>zb_min:
                            i_midd=facies_zhou[j,k+1]
                        else:
                            i_midd=random.randint(zb_min+1,zb_max-1)
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
            else:
                i_midd=i_midd_core
                facies_zhou[j,k]=i_midd
                # data_moni[i,j_midd,k]=str(1)

    for j in range(max_wide_num[2],y_min-kuo_bian-1,-1):
        for k in range(max_wide_num[3],z_max+kuo_bian+1):
            i_zong=[]
            for x in range(x_min,x_max+1):
                if data_range[x,j+y_pian_yi,k]==values_dx:
                    i_zong.append(x)
            i_midd_core=int((max_wide_num[4]+max_wide_num[5])/2)
            midd_zhoubian=get_midd_zhoubian(j,k)
            if len(i_zong)>0:
                i_min=min(i_zong)
                i_max=max(i_zong)
                i_midd_chushi=int((i_min+i_max)/2)
                
                if len(midd_zhoubian)<1:   #当前点周边没有已知值
                    facies_zhou[j,k]=i_midd_chushi
                    # data_moni[i,j_midd_chushi,k]=str(1)
                elif len(midd_zhoubian)==1:  #当前点周边有一个已知值
                    zb_val=midd_zhoubian[0]
                    if zb_val-i_midd_chushi>1:
                        i_midd=zb_val-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    elif zb_val-i_midd_chushi<-1:
                        i_midd=zb_val+1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:
                        facies_zhou[j,k]=i_midd_chushi
                        # data_moni[i,j_midd_chushi,k]=str(1)
                else:  #当前点周边有两个或两个以上已知值
                    zb_min=min(midd_zhoubian)
                    zb_max=max(midd_zhoubian)
                    if zb_max==zb_min: #最大值与最小值相同
                        if zb_min-i_midd_chushi>1:
                            i_midd=zb_min-1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min-i_midd_chushi<-1:
                            i_midd=zb_min+1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            facies_zhou[j,k]=i_midd_chushi
                            # data_moni[i,j_midd_chushi,k]=str(1)
                    elif zb_max-zb_min==1: #最大值与最小值相差1
                        if zb_max==i_midd_chushi:
                            i_midd=zb_max
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min==i_midd_chushi:
                            i_midd=zb_min
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            if facies_zhou[j,k-1]!=-99:
                                i_midd=facies_zhou[j,k-1]
                            elif facies_zhou[j,k+1]!=-99:
                                i_midd=facies_zhou[j,k+1]
                            else:
                                i_midd=random.randint(zb_min,zb_max)
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                    elif zb_max-zb_min==2:  #最大值与最小值相差2
                        i_midd=zb_max-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:  #最大值与最小值相差3及以上
                        if facies_zhou[j,k-1]<zb_max and facies_zhou[j,k-1]>zb_min:
                            i_midd=facies_zhou[j,k-1]
                        elif facies_zhou[j,k+1]<zb_max and facies_zhou[j,k+1]>zb_min:
                            i_midd=facies_zhou[j,k+1]
                        else:
                            i_midd=random.randint(zb_min+1,zb_max-1)
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
            else:
                i_midd=i_midd_core
                facies_zhou[j,k]=i_midd
                # data_moni[i,j_midd,k]=str(1)
    for j in range(max_wide_num[2],y_min-kuo_bian-1,-1):
        for k in range(max_wide_num[3],z_min-kuo_bian-1,-1):
            i_zong=[]
            for x in range(x_min,x_max+1):
                if data_range[x,j+y_pian_yi,k]==values_dx:
                    i_zong.append(x)
            i_midd_core=int((max_wide_num[4]+max_wide_num[5])/2)
            midd_zhoubian=get_midd_zhoubian(j,k)
            if len(i_zong)>0:
                i_min=min(i_zong)
                i_max=max(i_zong)
                i_midd_chushi=int((i_min+i_max)/2)
                
                if len(midd_zhoubian)<1:   #当前点周边没有已知值
                    facies_zhou[j,k]=i_midd_chushi
                    # data_moni[i,j_midd_chushi,k]=str(1)
                elif len(midd_zhoubian)==1:  #当前点周边有一个已知值
                    zb_val=midd_zhoubian[0]
                    if zb_val-i_midd_chushi>1:
                        i_midd=zb_val-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    elif zb_val-i_midd_chushi<-1:
                        i_midd=zb_val+1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:
                        facies_zhou[j,k]=i_midd_chushi
                        # data_moni[i,j_midd_chushi,k]=str(1)
                else:  #当前点周边有两个或两个以上已知值
                    zb_min=min(midd_zhoubian)
                    zb_max=max(midd_zhoubian)
                    if zb_max==zb_min: #最大值与最小值相同
                        if zb_min-i_midd_chushi>1:
                            i_midd=zb_min-1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min-i_midd_chushi<-1:
                            i_midd=zb_min+1
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            facies_zhou[j,k]=i_midd_chushi
                            # data_moni[i,j_midd_chushi,k]=str(1)
                    elif zb_max-zb_min==1: #最大值与最小值相差1
                        if zb_max==i_midd_chushi:
                            i_midd=zb_max
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        elif zb_min==i_midd_chushi:
                            i_midd=zb_min
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                        else:
                            if facies_zhou[j,k-1]!=-99:
                                i_midd=facies_zhou[j,k-1]
                            elif facies_zhou[j,k+1]!=-99:
                                i_midd=facies_zhou[j,k+1]
                            else:
                                i_midd=random.randint(zb_min,zb_max)
                            facies_zhou[j,k]=i_midd
                            # data_moni[i,j_midd,k]=str(1)
                    elif zb_max-zb_min==2:  #最大值与最小值相差2
                        i_midd=zb_max-1
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
                    else:  #最大值与最小值相差3及以上
                        if facies_zhou[j,k-1]<zb_max and facies_zhou[j,k-1]>zb_min:
                            i_midd=facies_zhou[j,k-1]
                        elif facies_zhou[j,k+1]<zb_max and facies_zhou[j,k+1]>zb_min:
                            i_midd=facies_zhou[j,k+1]
                        else:
                            i_midd=random.randint(zb_min+1,zb_max-1)
                        facies_zhou[j,k]=i_midd
                        # data_moni[i,j_midd,k]=str(1)
            else:
                i_midd=i_midd_core
                facies_zhou[j,k]=i_midd
                # data_moni[i,j_midd,k]=str(1)
    # 补齐中轴面列表中空白部分

    while -99 in facies_zhou:
        for y in range(y_max+kuo_bian+1):
            for z in range(z_max+kuo_bian+1):
                if facies_zhou[y,z]==-99:
                    zb_data=get_midd_zhoubian(y,z)
                    if len(zb_data)>0:
                        facies_zhou[y,z]=random.choice(zb_data)
    # 此处将i_midd变为扰动值
    # facies_zhou_rd_midd=facies_zhou[max_wide_num[2],max_wide_num[3]]
    # for y in range(y_max+kuo_bian+1):
    #     for z in range(z_max+kuo_bian+1):
    #         facies_zhou[y,z]=facies_zhou[y,z]-facies_zhou_rd_midd


    # 获取总的索引列表与对应的值列表
    point_i_all=[]
    point_data_all=[]
    point_i_zuo_biao=[]
    # 获取井数据上的峰值点，作为角砾带的中心点
    # 首先判断当前洞穴是否存在井条件数据，每隔20网格选一个峰值点
    # for i in range(x_min-kuo_bian,x_max+kuo_bian+1):
    #     rs_v=[]
    #     j_k=[]
    #     for j in range(y_min-kuo_bian,y_max+kuo_bian+1):
    #         for k in range(z_min-kuo_bian,z_max+kuo_bian+1):
    #             if data_range[i,j+y_pian_yi,k]==values_dx:
    #                 if data_rs[i,j+y_pian_yi,k]!=-99.0:
    #                     rs_v.append(data_rs[i,j+y_pian_yi,k])
    #                     j_k.append([j,k])
    #     if len(rs_v)>0:
    #         point_data_all.append(max(rs_v))
    #         point_i_all.append(i)
    #         point_i_zuo_biao.append([i,j_k[rs_v.index(max(rs_v))][0],j_k[rs_v.index(max(rs_v))][1]])
    print('井上数据')
    print('point_i_all:',point_i_all)
    print('point_data_all:',point_data_all)
    print('point_i_zuo_biao:',point_i_zuo_biao)
    # 获取断面上的数据，作为角砾带的中心点
    # if len(point_i_all)<1:
    #     for i in range(x_min-kuo_bian,x_max+kuo_bian+1):
    #         dm_num=0
    #         dm_zuo_biao=[]
    #         for j in range(y_min-kuo_bian,y_max+kuo_bian+1):
    #             for k in range(z_min-kuo_bian,z_max+kuo_bian+1):
    #                 if data_range[i,j+y_pian_yi,k]==values_dx:
    #                     if data_dm[i,j+y_pian_yi,k]!=-99:
    #                         dm_num+=1
    #                         dm_zuo_biao.append([j,k])
    #         if dm_num>0:
    #             point_data_all.append(dm_num)
    #             point_i_all.append(i)
    #             point_i_zuo_biao.append([i,dm_zuo_biao[int(len(dm_zuo_biao)/2)][0],dm_zuo_biao[int(len(dm_zuo_biao)/2)][1]])
    print('断面上数据')
    print('point_i_all:',point_i_all)
    print('point_data_all:',point_data_all)
    print('point_i_zuo_biao:',point_i_zuo_biao)

    point_i_part=[]
    point_data_part=[]
    point_zuo_biao_part=[]
    if len(point_i_all)>0:
        # 滑动窗口开始筛选值列表与对应的索引列表
        point_i_part.append(point_i_all[0])
        point_data_part.append(point_data_all[0])
        point_zuo_biao_part.append(point_i_zuo_biao[0])
        for x in range(1,len(point_i_all)):
            if abs(point_i_all[x]-point_i_part[len(point_i_part)-1])<33:
                if point_data_all[x]>=point_data_part[len(point_data_part)-1]:
                    point_i_part[len(point_i_part)-1]=point_i_all[x]
                    point_data_part[len(point_data_part)-1]=point_data_all[x]
                    point_zuo_biao_part[len(point_zuo_biao_part)-1]=point_i_zuo_biao[x]
            else:
                point_i_part.append(point_i_all[x])
                point_data_part.append(point_data_all[x])
                point_zuo_biao_part.append(point_i_zuo_biao[x])
    print('筛选条件数据')
    print('point_i_part:',point_i_part)
    print('point_data_part:',point_data_part)
    print('point_zuo_biao_part:',point_zuo_biao_part)
    i_m_zuo_biao=[]
    if len(point_zuo_biao_part)>0:
        i_m_zuo_biao.append([point_zuo_biao_part[int(len(point_zuo_biao_part)/2)][1],point_zuo_biao_part[int(len(point_zuo_biao_part)/2)][2]])
    # 既没有井条件数据，也没有断面条件数据
    if len(point_i_part)<1:
        point_i_part.append(int((max_wide_num[4]+max_wide_num[5])/2))
        i_m_zuo_biao.append([max_wide_num[2],max_wide_num[3]])
    # 首先判断筛选的索引列表内部需不需要插值
    if len(point_i_part)>1:
        for i in range(1,len(point_i_part)):
            if abs(point_i_part[i]-point_i_part[i-1])>=55 and abs(point_i_part[i]-point_i_part[i-1])<88:
                new_v=int(abs(point_i_part[i]+point_i_part[i-1])/2)
                point_i_part.insert(i,new_v)
            elif abs(point_i_part[i]-point_i_part[i-1])>=88 and abs(point_i_part[i]-point_i_part[i-1])<132:
                new_v_1=int(point_i_part[i-1]+(point_i_part[i]-point_i_part[i-1])/3)
                new_v_2=int(point_i_part[i]-(point_i_part[i]-point_i_part[i-1])/3)
                point_i_part.insert(i,new_v_1)
                point_i_part.insert(i+1,new_v_2)
            elif abs(point_i_part[i]-point_i_part[i-1])>=132:
                new_v_1=int(point_i_part[i-1]+(point_i_part[i]-point_i_part[i-1])/4)
                new_v_2=int(point_i_part[i-1]+2*(point_i_part[i]-point_i_part[i-1])/4)
                new_v_3=int(point_i_part[i-1]+3*(point_i_part[i]-point_i_part[i-1])/4)
                point_i_part.insert(i,new_v_1)
                point_i_part.insert(i+1,new_v_2)
                point_i_part.insert(i+2,new_v_3)
    print('内部插值后')
    print('point_i_part:',point_i_part)
    print('i_m_zuo_biao:',i_m_zuo_biao)
    # 对筛选的索引列表进行插值
    # 此处是在两端进行插值
    # for i in range(point_i_part[0],x_min-kuo_bian,-1):
    #     if abs(point_i_part[0]-i)>=33:
    #         point_i_part.insert(0,i)
    # for i in range(point_i_part[len(point_i_part)-1],x_max+kuo_bian+1):
    #     if abs(point_i_part[len(point_i_part)-1]-i)>=33:
    #         point_i_part.append(i)

    # 此处是将原本的两端插值改为在两端仅插入一个节点，围绕此节点确定簇的数量
    # 洞穴核部角砾带发育厚度
    he_jld_hou_zong=max_wide_num[0]*dis_x/100*4
    he_jld_cu=int(he_jld_hou_zong/6)+1
    he_jld_hou=he_jld_hou_zong/he_jld_cu
    bian_jld_hou_zong=max_wide_num[0]*dis_x/100*4
    bian_jld_cu=int(bian_jld_hou_zong/6)+1
    bian_jld_hou=bian_jld_hou_zong/bian_jld_cu
    lfd_hou=16.4/4*he_jld_hou+2
    print('he_jld_hou_zong=',he_jld_hou_zong)
    print('he_jld_cu=',he_jld_cu)
    print('he_jld_hou=',he_jld_hou)
    print('bian_jld_hou_zong=',bian_jld_hou_zong)
    print('bian_jld_cu=',bian_jld_cu)
    print('bian_jld_hou=',bian_jld_hou)
    print('lfd_hou=',lfd_hou)
    # 更改核心点的x坐标
    if he_jld_cu%2==0:
        point_i_part[0]=point_i_part[0]-int(((lfd_hou+he_jld_hou)*he_jld_cu/2+lfd_hou/2)/dis_x)
    else:
        point_i_part[0]=point_i_part[0]-int(((lfd_hou+he_jld_hou)*((he_jld_cu+1)/2)-he_jld_cu/2)/dis_x)
    # 左侧条带将核心点定位在裂缝带左边界，即裂缝带与角砾带交界线
    point_i_part.insert(0,max_wide_num[4]+int(((bian_jld_hou+lfd_hou)*(bian_jld_cu-1)+bian_jld_hou)/dis_x)+int(max_wide_num[0]*0.05))
    # 右侧条带将核心点定位在裂缝带右边界，即裂缝带与角砾带交界处
    point_i_part.append(max_wide_num[5]-int(((bian_jld_hou+lfd_hou)*(bian_jld_cu-1)+bian_jld_hou)/dis_x)-int(max_wide_num[0]*0.05))
    print('两端插值后')
    print('point_i_part:',point_i_part)
    
    # 为节点添加扰动辅助值，每个节点添加6个值
    # rd_fz=[]
    # for i in range(len(point_i_part)):
    #     for j in range(10):
    #         rd_fz.append(i*200+20*j)

    # 首先判断规模
    rd_j=0
    i_m=facies_zhou[i_m_zuo_biao[0][0],i_m_zuo_biao[0][1]]
    print('i_m:',i_m)
    print('原始i_m:',facies_zhou[max_wide_num[2],max_wide_num[3]])
    c_v_values=[]
    for i in point_i_part:
        if (i<=x_max and i>=x_min):
            c_v_values.append(abs(i-i_m))
    max_c_v=max(c_v_values)
    min_c_v=min(c_v_values)
    nnn=0  #记录模拟进度
    zong_num=(y_max-y_min+kuo_bian*2)*(z_max-z_min+kuo_bian*2)
    for j in range(y_min-kuo_bian,y_max+kuo_bian+1):
        rd_k=0
        for k in range(z_min-kuo_bian,z_max+kuo_bian+1):
            # 找出当前i,k值下j的中间值
            # old_min=1/2  #控制洞穴簇的宽度比例值
            old_min=1
            new_max=0.75
            new_min=-1
            i_zong=[]
            for x in range(x_min,x_max+1):
                if data_range[x,j+y_pian_yi,k]==values_dx:
                    i_zong.append(x)
            dx_wide=max_wide_num[0]
            if len(i_zong)>0:
                i_min=min(i_zong)
                i_max=max(i_zong)
                dx_wide=i_max-i_min+1    # 洞穴在当前截线上的宽度值
            cu_wide_bili=dx_wide/max_wide_num[0]
            c_w_b=math.pow(old_min,1-cu_wide_bili)  #将直线渐变的比例值转换为指数渐变，下降变缓慢
            # if cu_wide_bili<=new_max:
            #     # cu_wide_bili=(cu_wide_bili-old_min)*(new_max-new_min)/(new_max-old_min)+new_min
            #     cu_wide_bili=0
            i_midd=facies_zhou[j,k]
            
            nnn+=1
            if nnn%int(zong_num/2)==0 or nnn==zong_num:
                print('模拟进度_1:',nnn/zong_num*100,'%')


            for item in range(len(point_i_part)):
                try:
                    i_point=point_i_part[item]  #获取每个簇的中心点，即是i的坐标点，一系列节点
                    c_v=i_point-i_m             #计算每个节点与洞穴核心点的i方向差值
                    # r_f_0=rd_fz[10*item]         #获取辅助扰动值，为0，20，40，60，80作为不同簇的扰动选值起点，避免不同簇使用相同的扰动值
                    # r_f_1=rd_fz[10*item+1]
                    # r_f_2=rd_fz[10*item+2]
                    # r_f_3=rd_fz[10*item+3]
                    # r_f_4=rd_fz[10*item+4]
                    # r_f_5=rd_fz[10*item+5]
                    # r_d_0=rao_dong[rd_k+r_f_0,rd_j+r_f_0]    #获取具体扰动值
                    # r_d_1=rao_dong[rd_k+r_f_1,rd_j+r_f_1]
                    # r_d_2=rao_dong[rd_k+r_f_2,rd_j+r_f_2]
                    # r_d_3=rao_dong[rd_k+r_f_3,rd_j+r_f_3]
                    # r_d_4=rao_dong[rd_k+r_f_4,rd_j+r_f_4]
                    # r_d_5=rao_dong[rd_k+r_f_5,rd_j+r_f_5]
                    if max_c_v==min_c_v:
                        wide_bili=0
                    else:
                        wide_bili=abs(abs(c_v)-min_c_v)/(max_c_v-min_c_v)
                    t_w_b=math.pow(1,1-min(1,wide_bili))  # 条带的比例值
                    # for i in range(i_midd+int((c_v-int(8.5*t_w_b))*c_w_b)+r_d_0,i_midd+int((c_v+int(8.5*t_w_b))*c_w_b)+r_d_1):
                    #     data_moni[i,j,k]=str(4)
                    #     for x in range(i_midd+int((c_v-int(4*t_w_b))*c_w_b)+r_d_3+rd_2d[rd_k+r_f_0,rd_j+r_f_0],i_midd+int((c_v+int(3*t_w_b))*c_w_b)+r_d_5):
                    #         data_moni[x,j,k]=str(5)
                        # for x in range(i_midd+int((c_v-int(2*t_w_b))*c_w_b)+r_d_3-rd_l[rd_k]+rd_2d[rd_k+r_f_0,rd_j+r_f_0],i_midd+int((c_v+int(2*t_w_b))*c_w_b)+r_d_5):
                        #     data_moni[x,j,k]=str(5)
                        # for x in range(i_midd+int((c_v+2)*c_w_b)+r_d_4-rd_l[rd_k]+rd_2d[rd_k+r_f_3,rd_j+r_f_3],i_midd+int((c_v+int(6*t_w_b))*c_w_b)+r_d_5):
                        #     data_moni[x,j,k]=str(5)
                    if item==0:
                        left_dis=int(((bian_jld_cu-1)*(bian_jld_hou+lfd_hou)+bian_jld_hou)/dis_x)
                        right_dis=int(lfd_hou/dis_x)+1
                        r_d_0=rao_dong[rd_k+10,rd_j+10]
                        r_d_1=rao_dong[rd_k+30,rd_j+30]
                        for i in range(i_midd+c_v-left_dis+r_d_0,i_midd+c_v+right_dis+r_d_1):
                            data_moni[i,j,k]=str(4)
                        for i_cu in range(bian_jld_cu):
                            left_pianyi=int((i_cu*(bian_jld_hou+lfd_hou)+bian_jld_hou)/dis_x)
                            right_pianyi=int(i_cu*(bian_jld_hou+lfd_hou)/dis_x)-1
                            # rd=rd_2d[rd_k+rd_fz[10*item+20*i_cu],rd_j+rd_fz[10*item+20*i_cu]]
                            rd=rd_2d[rd_k+100+100*i_cu,rd_j+100+100*i_cu]
                            for x in range(i_midd+c_v-left_pianyi+rd,i_midd+c_v-right_pianyi):
                                data_moni[x,j,k]=str(5)
                    if item==1:
                        left_dis=0
                        right_dis=int((he_jld_cu*(he_jld_hou+lfd_hou)+lfd_hou)/dis_x)+1
                        r_d_2=rao_dong[rd_k+50,rd_j+50]
                        r_d_3=rao_dong[rd_k+70,rd_j+70]
                        for i in range(i_midd+c_v-left_dis+r_d_2,i_midd+c_v+right_dis+r_d_3):
                            data_moni[i,j,k]=str(4)
                        for i_cu in range(he_jld_cu):
                            left_pianyi=int((i_cu*(he_jld_hou+lfd_hou)+lfd_hou)/dis_x)
                            right_pianyi=int((i_cu+1)*(he_jld_hou+lfd_hou)/dis_x)
                            # r_d_l=rao_dong[rd_k+rd_fz[10*item+i_cu*10],rd_j+rd_fz[10*item+i_cu*10]]
                            # r_d_r=rao_dong[rd_k+rd_fz[10*item+i_cu*10],rd_j+rd_fz[10*item+i_cu*10]]
                            # rd=rd_2d[rd_k+rd_fz[10*item+40*i_cu],rd_j+rd_fz[10*item+40*i_cu]]
                            rd=rd_2d[rd_k+500+500*i_cu,rd_j+500+500*i_cu]
                            for x in range(i_midd+c_v+left_pianyi+rd,i_midd+c_v+right_pianyi):
                                data_moni[x,j,k]=str(5)
                    if item==2:
                        left_dis=int(lfd_hou/dis_x)+1
                        right_dis=int(((bian_jld_cu-1)*(bian_jld_hou+lfd_hou)+bian_jld_hou)/dis_x)+1
                        r_d_4=rao_dong[rd_k+90,rd_j+90]
                        r_d_5=rao_dong[rd_k+110,rd_j+110]
                        for i in range(i_midd+c_v-left_dis+r_d_4,i_midd+c_v+right_dis+r_d_5):
                            data_moni[i,j,k]=str(4)
                        for i_cu in range(bian_jld_cu):
                            left_pianyi=int(i_cu*(bian_jld_hou+lfd_hou)/dis_x)
                            right_pianyi=int((i_cu*(bian_jld_hou+lfd_hou)+bian_jld_hou)/dis_x)+1
                            # rd=rd_2d[rd_k+rd_fz[10*item+60*i_cu],rd_j+rd_fz[10*item+60*i_cu]]
                            rd=rd_2d[rd_k+1000+1000*i_cu,rd_j+1000+1000*i_cu]
                            for x in range(i_midd+c_v+left_pianyi+rd,i_midd+c_v+right_pianyi):
                                data_moni[x,j,k]=str(5)
                except:
                    pass

            rd_k+=1
        rd_j+=1

    file_path=file_path_root+'_1_model'+'.txt'

    with open(file_path,'w') as f: # 'w'方式可以无需提前新建文件，存在则打开，不存在则新建
        f.write('PETREL: Properties'+'\n')
        f.write('4'+'\n')
        f.write('i_index unit1 scale1'+'\n')
        f.write('j_index unit1 scale1'+'\n')
        f.write('k_index unit1 scale1'+'\n')
        model_name='Facies'+'_DX_'+str(values_dx)+' unit1 scale1'
        f.write(model_name+'\n')

        for i in range(x_min,x_max+1):
            for j in range(y_min,y_max+1):
                for k in range(z_min,z_max+1):
                    if data_range[i,j+y_pian_yi,k]==values_dx:
                        f.write('%s %s %s %s\n'%(str(i-kuo_bian),str(j-kuo_bian+y_pian_yi),str(k-kuo_bian),str(data_moni[i,j,k])))
    f.close()

    # '''
    # 竖直旋转代码段，仅对两边部分做旋转处理
    # 上述旋转代码可能会将边部差储层条带2覆盖中部中好储层条带45，改进：仅仅将45进行旋转

    # if len(point_i_part)%2==0:
    #     if max_c_v==min_c_v:
    #         t_w_b_r=0.9
    #     else:
    #         t_w_b_r=math.pow(0.9,1-(abs(point_i_part[int(len(point_i_part)/2)]-i_m)-min_c_v)/(max_c_v-min_c_v))  #条带的比例值
    #     right_point=int(point_i_part[int(len(point_i_part)/2)]+16*t_w_b_r)
    #     if max_c_v==min_c_v:
    #         t_w_b_l=0.9
    #     else:
    #         t_w_b_l=math.pow(0.9,1-(abs(point_i_part[int(len(point_i_part)/2-1)]-i_m)-min_c_v)/(max_c_v-min_c_v))  #条带的比例值
    #     left_point=int(point_i_part[int(len(point_i_part)/2-1)]-16*t_w_b_l)
    # else:
    #     if max_c_v==min_c_v:
    #         t_w_b=0.9
    #     else:
    #         t_w_b=math.pow(0.9,1-(abs(point_i_part[int(len(point_i_part)/2)]-i_m)-min_c_v)/(max_c_v-min_c_v))  #条带的比例值
    #     right_point=int(point_i_part[int(len(point_i_part)/2)]+16*t_w_b)
    #     left_point=int(point_i_part[int(len(point_i_part)/2)]-16*t_w_b)
    # left_point=int(((max_wide_num[4]+max_wide_num[5])/2+point_i_part[0])/2)
    # right_point=int(((max_wide_num[4]+max_wide_num[5])/2+point_i_part[2])/2)
    # mmm=0
    # zong_num=(x_max-x_min+kuo_bian*2)*(y_max-y_min+kuo_bian*2)*(z_max-z_min+kuo_bian*2)
    # for j in range(y_min-kuo_bian,y_max+kuo_bian+1):
    #     for k in range(z_min-kuo_bian,z_max+kuo_bian+1):

    #         i_zong=[]
    #         for x in range(x_min-kuo_bian,x_max+kuo_bian+1):
    #             if data_range[x,j+y_pian_yi,k]==values_dx:
    #                 i_zong.append(x)
    #         dx_wide=max_wide_num[0]
    #         if len(i_zong)>0:
    #             i_min=min(i_zong)
    #             i_max=max(i_zong)
    #             dx_wide=i_max-i_min+1    # 当前洞穴宽度值
    #         cu_wide_bili=dx_wide/max_wide_num[0]
    #         c_w_b=math.pow(1,1-cu_wide_bili)  #将直线渐变的比例值转换为指数渐变，下降变缓慢
    #         i_midd=facies_zhou[j,k]

    #         for i in range(x_min-kuo_bian,x_max+kuo_bian+1):
    #             mmm+=1
    #             if mmm%int(zong_num/2)==0 or mmm==zong_num:
    #                 print('模拟进度_2:',mmm/zong_num*100,'%')
    #             if i>=i_midd+int((right_point-i_m)*c_w_b):
    #                 # data_xz[i,j,k]=str(6)
    #                 if data_moni[i,j,k]!=2:
    #                     new_xz=Srotation_angle_get_coor_coordinates([i,k],[int((x_min+x_max)/2),int((z_min+z_max)/2)],10,[dis_x,dis_z])
    #                     for item in new_xz:
    #                         if (item[0]<=x_max+kuo_bian and item[1]<=z_max+kuo_bian):
    #                             data_xz[item[0],j,item[1]]=data_moni[i,j,k]
    #             elif i<=i_midd+int((left_point-i_m)*c_w_b):
    #                 # data_xz[i,j,k]=str(6)
    #                 if data_moni[i,j,k]!=2:
    #                     new_xz=Nrotation_angle_get_coor_coordinates([i,k],[int((x_min+x_max)/2),int((z_min+z_max)/2)],10,[dis_x,dis_z])
    #                     for item in new_xz:
    #                         if (item[0]<=x_max+kuo_bian and item[1]<=z_max+kuo_bian):
    #                             data_xz[item[0],j,item[1]]=data_moni[i,j,k]

    #             else:
    #                 if data_moni[i,j,k]!=2:
    #                     data_xz[i,j,k]=data_moni[i,j,k]


    # file_path=file_path_root+'_2_model_szxz'+'.txt'
    # with open(file_path,'w') as f: # 'w'方式可以无需提前新建文件，存在则打开，不存在则新建
    #     f.write('PETREL: Properties'+'\n')
    #     f.write('4'+'\n')
    #     f.write('i_index unit1 scale1'+'\n')
    #     f.write('j_index unit1 scale1'+'\n')
    #     f.write('k_index unit1 scale1'+'\n')
    #     model_name='Facies'+'_DX_'+str(values_dx)+' unit1 scale1'
    #     f.write(model_name+'\n')

    #     for i in range(x_min,x_max+1):
    #         for j in range(y_min,y_max+1):
    #             for k in range(z_min,z_max+1):
    #                 if data_range[i,j+y_pian_yi,k]==values_dx:
    #                     f.write('%s %s %s %s\n'%(str(i-kuo_bian),str(j-kuo_bian+y_pian_yi),str(k-kuo_bian),str(data_xz[i,j,k])))
    # f.close()
    '''
    # 水平旋转代码 旋转倾斜的模型
    nn=0
    zong_num=(x_max-x_min+kuo_bian*2)*(y_max-y_min+kuo_bian*2)*(z_max-z_min+kuo_bian*2)
    for i in range(x_min-kuo_bian,x_max+kuo_bian+1):
        for j in range(y_min-kuo_bian,y_max+kuo_bian+1):
            for k in range(z_min-kuo_bian,z_max+kuo_bian+1):
                nn+=1
                if nn%int(zong_num/2)==0 or nn==zong_num:
                    print('模拟进度_3: ',nn/zong_num*100,'%')
                if data_xz[i,j,k]!=2:
                    new_xy=Srotation_angle_get_coor_coordinates([i,j],[int((x_max+x_min)/2),int((y_max+y_min)/2)],15,[dis_x,dis_y])
                    for item in new_xy:
                        if (item[0]<=x_max+kuo_bian and item[1]<=y_max+kuo_bian):
                            data_xz_qx[item[0],item[1],k]=data_xz[i,j,k]

    file_path=file_path_root+'_3_model_spxzqx'+'.txt'
    with open(file_path,'w') as f: # 'w'方式可以无需提前新建文件，存在则打开，不存在则新建
        f.write('PETREL: Properties'+'\n')
        f.write('4'+'\n')
        f.write('i_index unit1 scale1'+'\n')
        f.write('j_index unit1 scale1'+'\n')
        f.write('k_index unit1 scale1'+'\n')
        model_name='Facies'+'_DX_'+str(values_dx)+' unit1 scale1'
        f.write(model_name+'\n')
        for i in range(x_min,x_max+1):
            for j in range(y_min,y_max+1):
                for k in range(z_min,z_max+1):
                    if data_range[i,j+y_pian_yi,k]==values_dx:  #==values_dx
                        f.write('%s %s %s %s\n'%(str(i-kuo_bian),str(j-kuo_bian+y_pian_yi),str(k-kuo_bian),str(data_xz_qx[i,j,k])))
    f.close()

    # 水平旋转代码 旋转竖直的模型
    nn=0
    zong_num=(x_max-x_min+kuo_bian*2)*(y_max-y_min+kuo_bian*2)*(z_max-z_min+kuo_bian*2)
    for i in range(x_min-kuo_bian,x_max+kuo_bian+1):
        for j in range(y_min-kuo_bian,y_max+kuo_bian+1):
            for k in range(z_min-kuo_bian,z_max+kuo_bian+1):
                nn+=1
                if nn%int(zong_num/2)==0 or nn==zong_num:
                    print('模拟进度_4: ',nn/zong_num*100,'%')
                if data_moni[i,j,k]!=2:
                    new_xy=Srotation_angle_get_coor_coordinates([i,j],[int((x_max+x_min)/2),int((y_max+y_min)/2)],15,[dis_x,dis_y])
                    for item in new_xy:
                        if (item[0]<=x_max+kuo_bian and item[1]<=y_max+kuo_bian):
                            data_xz_sz[item[0],item[1],k]=data_moni[i,j,k]

    file_path=file_path_root+'_4_model_spxzsz'+'.txt'
    with open(file_path,'w') as f: # 'w'方式可以无需提前新建文件，存在则打开，不存在则新建
        f.write('PETREL: Properties'+'\n')
        f.write('4'+'\n')
        f.write('i_index unit1 scale1'+'\n')
        f.write('j_index unit1 scale1'+'\n')
        f.write('k_index unit1 scale1'+'\n')
        model_name='Facies'+'_DX_'+str(values_dx)+' unit1 scale1'
        f.write(model_name+'\n')
        for i in range(x_min,x_max+1):
            for j in range(y_min,y_max+1):
                for k in range(z_min,z_max+1):
                    if data_range[i,j+y_pian_yi,k]==values_dx:  #==values_dx
                        f.write('%s %s %s %s\n'%(str(i-kuo_bian),str(j-kuo_bian+y_pian_yi),str(k-kuo_bian),str(data_xz_sz[i,j,k])))
    f.close()
    '''

    time2=time.time()

    print(' ')
    print('<< DX: ',values_dx,'>> 用时：',time2-time1,'s')
    print(' ')




