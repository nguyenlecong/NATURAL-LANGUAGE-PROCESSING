#!/usr/bin/env python
# coding: utf-8

# # Import những thư viện sử dụng

# In[47]:


import re
from pyvi import ViTokenizer, ViPosTagger, ViUtils
import pandas as pd
import json
from glob import glob


# # Tiền xử lý

# In[48]:


#chuyển các đoạn thành một đoạn
def makeParagraph(m):
    l = [':','.','-',';']
    tmp = m
    tmp = tmp.split('\n')
    para = ""
    for i in tmp:
        if i=='': continue
        if para=="":
            para+=i
            continue
        if para[-1] in l: 
            para+=' '+i
            continue
        if para[-1] not in l: 
            para+='. '+i
            continue
    return para


# In[74]:


#thay thế những chữ viết tắt
def replaceAcr(para):
    emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"  # emoticons
           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
           u"\U0001F680-\U0001F6FF"  # transport & map symbols
           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
           u"\U00002702-\U000027B0"
           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    m = para
    m = m.replace('TPHCM',' thành phố Hồ Chí Minh')
    m = m.replace('NC', 'nguyên căn')
    m = emoji_pattern.sub(r'', m)
#     m = re.sub(r'[^\d\s\d]',',',m)
    m = m.replace('\r','')
    m = m.replace('BĐS','bất động sản')
    m = m.replace('CĐT','chủ đầu tư')
    m = m.replace('CNQSĐ','chuyển nhượng quyền sử dụng đất')
    m = m.replace('CNQSDĐ','chuyển nhượng quyền sử dụng đất')
    m = m.replace('BĐS','bất động sản')
    m = m.replace('LH','liên hệ')
    m = m.replace('lh','liên hệ')
    m = m.replace('Lh','liên hệ')
    m = m.replace(' LK ',' liền kề ')
    m = m.replace(' KĐT ',' khu đô thị ')
    m = m.replace(' TK ',' thiết kế ')
    m = m.replace('WC',' nhà vệ sinh ')
    m = m.replace('KCN','khu công nghiệp')
    m = m.replace('KDC','khu dân cư')
    m = m.replace('PN',' phòng ngủ ')
    m = m.replace('pn',' phòng ngủ ')
    m = m.replace('wc',' nhà vệ sinh ')
    m = m.replace('MT',' mặt tiền ')
    m = m.replace('mt',' mặt tiền ')
    m = m.replace('Mt',' mặt tiền ')
    m = m.replace('TL','thương lượng ')
    m = m.replace('TĐC','tái định cư')
    m = m.replace('HXH','hẻm xe hơi')
    m = m.replace('HXT','hẻm xe tải')
    m = m.replace('HCM','Hồ Chí Minh')
    m = m.replace(' TT ','trung tâm ')
    m = m.replace(' tt ','trung tâm ')
    m = m.replace(' TTTM ',' trung tâm thương mại ')
    m = m.replace(' ttmt ',' trung tâm thương mại ')
    m = m.replace(' TX ',' thị xã ')
    m = m.replace(' tx ',' thị xã ')
    m = m.replace(' TP ',' thành phố ')
    m = m.replace(' Tp.',' thành phố ')
    m = m.replace(' tp ',' thành phố ')
    m = m.replace('P.','phường ')
    m = m.replace('Q.','quận ')
    m = m.replace('P. ','phường ')
    m = m.replace('Q. ','quận ')
    m = m.replace(' P ',' phường ')
    m = m.replace(' Q ',' quận ')
    m = m.replace(' p ',' phường ')
    m = m.replace(' p ',' quận ')
    m = m.replace('HT','hỗ trợ')
    m = m.replace('DT','diện tích')
    m = m.replace('Dt','diện tích')
    m = m.replace('dt','diện tích')
    m = m.replace(' TR ',' triệu ')
    m = m.replace('m2',' m2')
    m = m.replace('m²',' m²')
    m = m.replace(' .',' .')
    m = m.replace('SHR','sổ hồng riêng')
    m = m.replace('XDTD','xây dựng tự do')
    m = m.replace('XD','xây dựng')
    for j in range(10):
      m = m.replace(str(j)+'tr ', str(j)+' triệu')
      m = m.replace(str(j)+'TR ', str(j)+' triệu')
    m = m.replace('tr/th',' triệu/tháng')
    m = m.replace('TR/',' triệu/')
    m = m.replace(' TR ',' triệu ')
    m = m.replace(' tr ',' triệu ')
    m = m.replace('tr/',' triệu/')
    m = m.replace(' HH cho mg',' hoa hồng cho môi giới')
    m = m.replace(' TC ',' thổ cư ')
    m = re.sub(r"\s\s+", ' ', m)
    return m


# # Tokernize và phân câu

# In[75]:


def splitTokAndPt(m):
    para = m.split('.')
    l = []
    for i in para:
        l.append(ViPosTagger.postagging(ViTokenizer.tokenize(i)))
    return l


# In[76]:


def tokAndPt(m):
    return ViPosTagger.postagging(ViTokenizer.tokenize(m))


# # Nhập từ điển

# In[77]:


def read(X):
    with open(X, mode='r', encoding='utf-8') as f:
        m = f.read()
    return m.split('\n')


# In[78]:


# import các từ điển
dia_gioi = read('./dictionary/dia_gioi.txt')
huyen = read('./dictionary/huyen')
tinh = read('./dictionary/tinh')
loai_tin = read('./dictionary/loai_tin.txt')
loai_nha = read('./dictionary/loai_nha.txt')
don_vi = ['tỷ', 'triệu', 'Tỷ', 'Triệu']
donvi_tien = ['đ', 'đồng', 'Đồng', 'Đ']
do_luong = ['m²', 'ha', 'km²', 'm2', 'km2']
name = read('./dictionary/ten')
ho = read('./dictionary/ho')


# # Thiết lập các luật 

# In[79]:


# tìm từ bằng từ điển từ
def findCandidateByWords(words, dict_):
    cand = []
    for i in range(len(words)):
        if words[i] in dict_: cand.append(words[i])
        elif words[i].capitalize()  in dict_: cand.append(words[i])
        elif words[i].lower() in dict_: cand.append(words[i])
        else: continue
    return list(set(cand))


# In[80]:


# tìm từ bằng tags
def findCandidateByTags(words, tags, dict_):
    cand = []
    for i in range(len(tags)):
        if tags[i] in dict_: cand.append(words[i])
    return list(set(cand))


# In[81]:


# tìm từ bằng tags và từ điển từ
def findCandidateByBoth(words, tags, dict1, dict2, t):
    cand = []
    for i in range(len(tags)):
        if tags[i] in dict2 and words[i] in dict1 and len(words[:i+1])>t+1:
            cand.append(words[i-t:i+1])
    return cand


# In[82]:


# loại bỏ từ thừa thãi
def deleteRedundant(X, Y, dict1, dict2):
    words=[]
    tags=[]
    for i in range(len(X)):
        if X[i] in dict1: continue
        if Y[i] in dict2: continue
        words.append(X[i])
        tags.append(Y[i])
    return words, tags


# In[83]:


# xóa những từ giống nhau khi viết thường
def removeCL(X):
    cand = []
    for i in X:
        if i.lower() not in cand: cand.append(i.lower())
    return cand


# In[84]:


# xóa tập từ
def remove_(X, Y):
    cand = []
    for i in X:
        if i not in Y: cand.append(i)
    return cand


# In[85]:


# tìm các vị trí từ
def findLocation(X, Y):
    m = []
    for i in range(len(X)):
        if X[i] == Y: m.append(i)
    return m


# In[86]:


# Tìm vị trí đầu tiên của từ
def findFirstLocation(X, Y):
    for i in range(len(X)):
        if X[i] == Y:
            return i
    return False


# In[87]:


# kiểm tra chuỗi từ có tag hợp lệ
def check(i, j, tags, dict_):
    while i<j:
        if tags[i] not in dict_: 
            return False
        else: i+=1
    return True


# In[88]:


# tìm mảng lớn nhất
def findMaxLength(X):
    k = 0
    max_ = []
    for i in X:
        if len(i)>k:
            k=len(i)
            max_=i
    return max_


# In[89]:


# check trùng
def checkAdd(X, condition):
    cand, loai = [], []
    max_ = findMaxLength(X)
    cand.append(max_)
    for i in X:
        for j in i:
            if j in condition and i not in loai:
                loai.append(i)
    for i in X:
        if i==[]: continue
        for j in i:
            if j not in max_ and i not in cand and i not in loai:
                cand.append(i)
                break
    return cand


# In[90]:


# xác định loại tin
def findTypeEstate(words, loai_tin):
    m = removeCL(findCandidateByWords(words, loai_tin))
    if m==[]:return ['lô đất']
    return m


# In[91]:


# Xác định loại bds
def findCategoryEstate(words, loai_nha):
    cand = findCandidateByWords(words, loai_nha)
    CE = []
    for i in cand:
        temp = words.index(i)
        if i in ['1', '2', '3', '4']:
            if words[temp-1] in ['cấp','Cấp']:
                CE.append(i)    
        else: CE.append(i)
    return removeCL(CE)


# In[92]:


# Xác định diện tích
def findArea(words, tags, do_luong, dict_):
    Area = []
    cand = findCandidateByBoth(words, tags, do_luong, dict_,1)
    return checkAdd(cand,[])


# In[93]:


# Tìm địa chỉ
def findAddress(words, tags, tinh, huyen):
    road, mem = [], []
    dict_ = ['Địa chỉ','địa chỉ']
    add = []
    for i in dict_:
        add = findLocation(words, i)
        if add!=[]:
            for i in add:
                road=words[i+1:]
    cand = findCandidateByTags(words, tags, ['Np'])
    city = findCandidateByWords(cand, tinh)
    district = findCandidateByWords(cand, huyen)
    if district!=[]:
        cand = remove_(cand, district)
        mem = findLocation(words, district[0])
    if city!=[]:
        cand = remove_(cand, city)
    if city!=[] and district==[]:        
        mem = findLocation(words, city[0])
    if mem!=[] and road==[]:
        for v in cand:
            n = findLocation(words, v)
            for i in mem:
                for j in n:
                    if i>j and i-j<=4 and check(j, i+1, tags, ['N', 'Np', 'M']):
                            road=words[j:i+1]
    return road, district, city


# In[94]:


def getPrice(words, i):
    if words[i] in ['triệu', 'Triệu']:
        w = words[i-3:i+1]
        if 'tỷ' in w or 'Tỷ' in w: return w
        else: return words[i-1:i+1]
    if words[i] in ['tỷ', 'Tỷ']:
        w = words[i-1:i+3]
        if 'triệu' in w or 'Triệu' in w: return w
        else: return words[i-1:i+1]


# In[99]:


# tìm giá nhà
def findPrice(words, tags, donvi_tien, don_vi):
    price = []
    cand = findCandidateByBoth(words, tags, donvi_tien, ['Nu'], 2)
    for i in cand:
        if len(i[1])>6: price.append(i[-2:])
        elif i[1] in don_vi: price.append(i)
    cand = findCandidateByWords(words, don_vi)
    for i in cand:
        l = findLocation(words, i)
        for j in l:
            p = getPrice(words,j)
            if p not in price: price.append(p)
    return price


# In[100]:


# Tìm số điện thoại
def findNumber(words, tags, tien, donvi_tien=donvi_tien):
    number, a, b=[],[],[]
    for i in range(len(tags)):
        if tags[i]=='M' and len(words[i])>=10 and len(words[i])<=12:
            if len(words)>i+1 and words[i+1] in donvi_tien: continue
            else: number.append(words[i])
    for i in number:
        for j in tien:
            if i in j: a.append(i)
            elif i in a: contiue
            else: b.append(i)
    return checkAdd(b,[])


# In[101]:


# Tìm họ tên
def findName(words, tags, road, district, city, ten, ho):
    t=1
    cand = findCandidateByTags(words, tags, ['Np'])
    cand = remove_(cand, road)
    cand = remove_(cand, district)
    cand = remove_(cand, city)
    na=[]
    sur = []
    fullname = []
    for i in cand:
        if i in ten:
            na.append(i)
        if i in ho: 
            sur.append(i)
    if sur != []:
        for i in sur:
            for j in na:
                if j in i: fullname.append(i)
                else: fullname.append(i+' '+j)
    else: fullname = na
    if t==0: return fullname
    return na


# In[102]:


#lọc null
def filter(m):
    l = []
    for i in m:
        if i!=[]: l.append(i)
    return l


# # Tìm thực thể

# In[103]:


def findElement(m):
    p = makeParagraph(m)
    p = replaceAcr(p)
    p = tokAndPt(p)
    for i in range(len(p[0])):
        p[0][i]=p[0][i].replace('_',' ')
    rem = ['E','C', 'I','L','P', 'R', 'T', 'X', 'F','Nc']
    words, tags = deleteRedundant(p[0], p[1], [], rem)
    dtt1 = ''
    tmp = findFirstLocation(words, 'Quận')
    if tmp==False: tmp = findFirstLocation(words, 'quận')
    if tmp!=False: dtt1 = words[tmp+1]
    ctt1 = ''
    tmp = findFirstLocation(words, 'Thành phố')
    if tmp==False: tmp = findFirstLocation(words, 'thành phố')
    if tmp!=False: ctt1 = words[tmp+1]
    price = findPrice(words, tags, donvi_tien, don_vi)
    number = findNumber(words, tags, donvi_tien, price)
    area = findArea(words, tags, do_luong, ['Nu','N','Np'])
    typeE = findTypeEstate(words, loai_tin)
    cateE = findCategoryEstate(words, loai_nha)
    return typeE, cateE, area, price, number, dtt1, ctt1


# In[104]:


def findElement1(m):
    p = makeParagraph(m)
    p = replaceAcr(p)
    p = splitTokAndPt(p)
    rd, dt, ct, fullname = [], [], [], []
    for k in p:
        for i in range(len(k[0])):
            k[0][i]=k[0][i].replace('_',' ')
        rem = ['E','C', 'I','L','P', 'R', 'T', 'X', 'F','Nc']
        words, tags = deleteRedundant(k[0], k[1], [], rem)
        road, district, city = findAddress(words, tags, tinh, huyen)
        if road!=[] and len(road)<=10: rd.append(road)
        dt+=district
        ct+=city
        fullname+=findName(words, tags, road, huyen, tinh, name, ho)
    rd = checkAdd(rd,[])
    dt = checkAdd(dt,[])
    ct = checkAdd(ct,[])
    for i in rd:
        for j in i:
            fullname = checkAdd(fullname, j)
    fullname = checkAdd(fullname, [])
    return rd, dt, ct, fullname


# In[105]:


def findAll(test):
    road, pr, ae = [], [], []
    typeE, cateE, area, price, number, dtt, ctt = findElement(test)
    rd, dt, ct, fullname = findElement1(test)
    if dt == [[]]:
        dt = [dtt]
    if ct == [[]]:
        ct = [ctt]
    for i in rd: 
        if i != None: road.append(connectString(i, dia_gioi))
    for i in price:
        if i != None: pr.append(connectString(i,[]))
    for i in area: 
        if i != None: ae.append(connectString(i,[]))
    return typeE, cateE, ae, road, dt, ct, pr, number, fullname


# In[106]:


def connectString(m, constraint):
    s = ''
    if m == []: return s
    for i in m:
        if i.lower() in constraint: i = i.lower()
        if s=='': s+=i
        else: s += ' '+i
    return s