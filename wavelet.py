import pywt
import matplotlib.pyplot as plt
import xlrd
import xlsxwriter
import numpy as np
import pandas as pd
import os



#获取数据
def get_data(csv_path):
    df=pd.read_csv(csv_path)
    dataset=[value for key,value in df.iteritems()]
    return dataset

#长度调整
def reconstruction_plot(yyy,data_length,**kwargs):
    plt.plot(np.linspace(0, data_length, len(yyy)), yyy, **kwargs)

#补全
def rec_coef(coeffs,wavelet,data_length):
    length=len(coeffs)
    l=[]
    for i in range(1,length):
        plt.subplot(length,1,i)
        coef=coeffs[:-i] + [None] * i
        rec_coef=pywt.waverec(coef,wavelet)
        rec_coef_interp=np.interp(x=np.arange(0,data_length),xp=np.linspace(0,data_length,len(rec_coef)),fp=rec_coef)
        l.append(rec_coef_interp)
        reconstruction_plot(rec_coef,data_length)


#进行小波分解并绘图
def do_wavedec(dataset):
    w=pywt.Wavelet("db5")
    data_length=len(dataset)
    print(data_length)
    title=["PH","DO(mg/L)","CODmn(mg/L)","NH3-N(mg/L)"]
    coeffss=[]
    for i in range(1,data_length):
        data=dataset[i]
        data_length=len(data)
        fit_level=pywt.dwt_max_level(data_len=len(data), filter_len=w.dec_len)
        coeffs=pywt.wavedec(data,'db5',level=fit_level)
        rec_coef(coeffs,w,data_length)
        plt.xlabel("second")
        plt.ylabel(title[i-1])
        plt.savefig("./result/result"+str(i)+".jpg")
        plt.close()
        coeffss.append(coeffs)
    return coeffss



coeffss=do_wavedec(get_data("./data/anhuinanwangjiaba.csv"))
print("成功")