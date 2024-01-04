import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
import random
import collections
import warnings
warnings.filterwarnings('ignore')

data_path=r'C:\Codefield\CODE_C\PYTHON\ML\data.xlsx'
df=pd.read_excel(data_path)
df.loc[df['VV']=='低于 0.1','VV']=0
df['VV']=df['VV'].astype('float64')
df.drop(columns=["Time Stamp","tR"],inplace=True)
attributes=df.columns.values
discrete=["DD", "WW", "W2", "H"]
continuous=["T", "Po", "P", "Pa", "U", "Ff", "ff3", "Tn", "Tx", "VV", "Td"]
for attribute in attributes:
	if attribute not in ["T", "Po", "P", "Pa", "U", "Ff", "ff3", "Tn", "Tx", "VV", "Td","DD", "WW", "W2", "H","RRR"]:
		df.drop(columns=[attribute],inplace=True)
x0 =np.array(df.iloc[:, :-1])
y0 =np.array(df.iloc[:, -1])
length=15
num=int(len(y0)/8)
x=np.zeros((num,length*8))
x = x.astype(object)
y=np.zeros(num)
for i in range(0,num):
	y[i]=y0[i*8]
	for j in range(0,8):
		x[i,15*j:15*j+15]=x0[8*i+j,:]
for i in range(y.size):
	if y[i]==0:
		y[i]=-1
x=pd.DataFrame(x)
y=pd.DataFrame(y)
xtrain, xtest, y_train, y_test = x.copy(deep=True),x.copy(deep=True),y.copy(deep=True),y.copy(deep=True)
for i in [xtrain, xtest, y_train, y_test]:
	i.index = range(i.shape[0])
discrete=[]
for i in range(0,8):
	for j in [5,8,9,12]:
		discrete.append(15*i+j)
si = SimpleImputer(missing_values=np.nan, strategy="most_frequent").fit(xtrain.loc[:, discrete])
#然后我们用训练集中的众数来同时填补训练集和测试集
xtrain.loc[:, discrete] = si.transform(xtrain.loc[:, discrete])
xtest.loc[:, discrete] = si.transform(xtest.loc[:, discrete])
xtrain.loc[:, discrete].isnull().mean()
xtest.loc[:, discrete].isnull().mean()
#处理分类变量：将分类型变量编码
oe = OrdinalEncoder().fit(xtrain.loc[:, discrete])
#用训练集的编码结果来编码训练和测试矩阵
xtrain.loc[:,  discrete] = oe.transform(xtrain.loc[:, discrete])
xtest.loc[:, discrete] = oe.transform(xtest.loc[:, discrete])
xtrain=xtrain.astype('float64')
xtest=xtest.astype('float64')
continuous=[]
for i in range(0,8):
	for j in range(0,15):
		""" if j in [5,8,9,12]:
			continue """
		continuous.append(15*i+j)
impmean = SimpleImputer(missing_values = np.nan, strategy="mean").fit(xtrain.loc[:, continuous])
xtrain.loc[:, continuous] = impmean.transform(xtrain.loc[:, continuous])
xtest.loc[:, continuous] = impmean.transform(xtest.loc[:, continuous])
ss = StandardScaler().fit(xtrain.loc[:, continuous])
xtrain.loc[:, continuous] = ss.transform(xtrain.loc[:, continuous])
xtest.loc[:, continuous] = ss.transform(xtest.loc[:, continuous])

class optStruct:
	"""
	数据结构，维护所有需要操作的值
	Parameters：
		dataMatIn - 数据矩阵
		classLabels - 数据标签
		C - 松弛变量
		toler - 容错率
		kTup - 包含核函数信息的元组,第一个参数存放核函数类别，第二个参数存放必要的核函数需要用到的参数
	"""
	def __init__(self, dataMatIn, classLabels, C, toler, kTup,class_weight):
		self.X = dataMatIn								#数据矩阵
		self.labelMat = classLabels						#数据标签
		self.C = C 										#松弛变量
		self.tol = toler 								#容错率
		self.m = np.shape(dataMatIn)[0] 				#数据矩阵行数
		self.alphas = np.mat(np.zeros((self.m,1))) 		#根据矩阵行数初始化alpha参数为0	
		self.b = 0 										#初始化b参数为0
		self.eCache = np.mat(np.zeros((self.m,2))) 		#根据矩阵行数初始化虎误差缓存，第一列为是否有效的标志位，第二列为实际的误差E的值。
		self.K = np.mat(np.zeros((self.m,self.m)))		#初始化核K
		for i in range(self.m):							#计算所有数据的核K
			self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup)
		self.class_weight=class_weight

def kernelTrans(X, A, kTup): 
	"""
	通过核函数将数据转换更高维的空间
	Parameters：
		X - 数据矩阵
		A - 单个数据的向量
		kTup - 包含核函数信息的元组
	Returns:
		K - 计算的核K
	"""
	m,n = np.shape(X)
	K = np.mat(np.zeros((m,1)))
	if kTup[0] == 'lin': K = X * A.T   					#线性核函数,只进行内积。
	elif kTup[0] == 'rbf': 								#高斯核函数,根据高斯核函数公式进行计算
		for j in range(m):
			deltaRow = X[j,:] - A
			K[j] = deltaRow*deltaRow.T
		K = np.exp(K*(-1*kTup[1])) 					#计算高斯核K
	else: raise NameError('核函数无法识别')
	return K 											#返回计算的核K

def calcEk(oS, k):
	"""
	计算误差
	Parameters：
		oS - 数据结构
		k - 标号为k的数据
	Returns:
		Ek - 标号为k的数据误差
	"""
	fXk = float(np.multiply(oS.alphas,oS.labelMat).T*oS.K[:,k] + oS.b)
	Ek = fXk - float(oS.labelMat[k])
	return Ek

def selectJrand(i, m):
	"""
	函数说明:随机选择alpha_j的索引值

	Parameters:
		i - alpha_i的索引值
		m - alpha参数个数
	Returns:
		j - alpha_j的索引值
	"""
	j = i                                 #选择一个不等于i的j
	while (j == i):
		j = int(random.uniform(0, m))
	return j

def selectJ(i, oS, Ei):
	"""
	内循环启发方式2
	Parameters：
		i - 标号为i的数据的索引值
		oS - 数据结构
		Ei - 标号为i的数据误差
	Returns:
		j, maxK - 标号为j或maxK的数据的索引值
		Ej - 标号为j的数据误差
	"""
	maxK = -1; maxDeltaE = 0; Ej = 0 						#初始化
	oS.eCache[i] = [1,Ei]  									#根据Ei更新误差缓存
	validEcacheList = np.nonzero(oS.eCache[:,0].A)[0]		#返回误差不为0的数据的索引值
	if (len(validEcacheList)) > 1:							#有不为0的误差
		for k in validEcacheList:   						#遍历,找到最大的Ek
			if k == i: continue 							#不计算i,浪费时间
			Ek = calcEk(oS, k)								#计算Ek
			deltaE = abs(Ei - Ek)							#计算|Ei-Ek|
			if (deltaE > maxDeltaE):						#找到maxDeltaE
				maxK = k; maxDeltaE = deltaE; Ej = Ek
		return maxK, Ej										#返回maxK,Ej
	else:   												#没有不为0的误差
		j = selectJrand(i, oS.m)							#随机选择alpha_j的索引值
		Ej = calcEk(oS, j)									#计算Ej
	return j, Ej 											#j,Ej

def updateEk(oS, k):
	"""
	计算Ek,并更新误差缓存
	Parameters：
		oS - 数据结构
		k - 标号为k的数据的索引值
	Returns:
		无
	"""
	Ek = calcEk(oS, k)										#计算Ek
	oS.eCache[k] = [1,Ek]									#更新误差缓存


def clipAlpha(aj,H,L):
	"""
	修剪alpha_j
	Parameters:
		aj - alpha_j的值
		H - alpha上限
		L - alpha下限
	Returns:
		aj - 修剪后的alpah_j的值
	"""
	if aj > H: 
		aj = H
	if L > aj:
		aj = L
	return aj

def innerL(i, oS):
	"""
	优化的SMO算法
	Parameters：
		i - 标号为i的数据的索引值
		oS - 数据结构
	Returns:
		1 - 有任意一对alpha值发生变化
		0 - 没有任意一对alpha值发生变化或变化太小
	"""
	#步骤1：计算误差Ei
	Ei = calcEk(oS, i)
	#优化alpha,设定一定的容错率。
	if ((oS.labelMat[i] * Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i] * Ei > oS.tol) and (oS.alphas[i] > 0)):
		#使用内循环启发方式2选择alpha_j,并计算Ej
		j,Ej = selectJ(i, oS, Ei)
		#保存更新前的aplpha值，使用深拷贝
		alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy()
		#步骤2：计算上下界L和H
		Ci=oS.C*oS.class_weight[oS.labelMat[i,0]]
		Cj=oS.C*oS.class_weight[oS.labelMat[j,0]]
		if (oS.labelMat[i] != oS.labelMat[j]):
			L = max(0, oS.alphas[j] - oS.alphas[i])
			H = min(Cj, Ci + oS.alphas[j] - oS.alphas[i])
		else:
			L = max(0, oS.alphas[j] + oS.alphas[i] - Ci)
			H = min(Cj, oS.alphas[j] + oS.alphas[i])
		if L == H: 
			print("L==H")
			return 0
		#步骤3：计算eta
		eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j]
		if eta >= 0: 
			print("eta>=0")
			return 0
		#步骤4：更新alpha_j
		oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej)/eta
		#步骤5：修剪alpha_j
		oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
		#更新Ej至误差缓存
		updateEk(oS, j)
		if (abs(oS.alphas[j] - alphaJold) < 0.00001): 
			print("alpha_j变化太小")
			return 0
		#步骤6：更新alpha_i
		oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold - oS.alphas[j])
		#更新Ei至误差缓存
		updateEk(oS, i)
		#步骤7：更新b_1和b_2
		b1 = oS.b - Ei- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i,i] - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[i,j]
		b2 = oS.b - Ej- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i,j]- oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[j,j]
		#步骤8：根据b_1和b_2更新b
		if (0 < oS.alphas[i]) and (Ci > oS.alphas[i]): oS.b = b1
		elif (0 < oS.alphas[j]) and (Cj > oS.alphas[j]): oS.b = b2
		else: oS.b = (b1 + b2)/2.0
		return 1
	else: 
		return 0

def smoP(dataMatIn, classLabels, C, toler, maxIter, kTup = ('rbf',1/120)):
	"""
	完整的线性SMO算法
	Parameters：
		dataMatIn - 数据矩阵
		classLabels - 数据标签
		C - 松弛变量
		toler - 容错率
		maxIter - 最大迭代次数
		kTup - 包含核函数信息的元组
	Returns:
		oS.b - SMO算法计算的b
		oS.alphas - SMO算法计算的alphas
	"""
	class_weight=dict(collections.Counter(classLabels))
	for item in class_weight:
		class_weight[item]=len(classLabels)/2/class_weight[item]
	oS = optStruct(np.mat(dataMatIn), np.mat(classLabels).transpose(), C, toler, kTup,class_weight)				#初始化数据结构
	iter = 0 																						#初始化当前迭代次数
	entireSet = True; alphaPairsChanged = 0
	while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):							#遍历整个数据集都alpha也没有更新或者超过最大迭代次数,则退出循环
		alphaPairsChanged = 0
		if entireSet:																				#遍历整个数据集   						
			for i in range(oS.m):        
				alphaPairsChanged += innerL(i,oS)													#使用优化的SMO算法
				print("全样本遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter,i,alphaPairsChanged))
			iter += 1
		else: 																						#遍历非边界值
			nonBoundIs = np.nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]						#遍历不在边界0和C的alpha
			for i in nonBoundIs:
				alphaPairsChanged += innerL(i,oS)
				print("非边界遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter,i,alphaPairsChanged))
			iter += 1
		if entireSet:																				#遍历一次后改为非边界遍历
			entireSet = False
		elif (alphaPairsChanged == 0):																#如果alpha没有更新,计算全样本遍历 
			entireSet = True  
		print("迭代次数: %d" % iter)
	return oS.b,oS.alphas 																			#返回SMO算法计算的b和alphas


def testRbf(k1 = 1/120):
	"""
	测试函数
	Parameters:
		k1 - 使用高斯核函数的时候表示到达率
	Returns:
		无
	"""
	dataArr,labelArr = np.array(xtrain),y_train.T.values.tolist()[0]						#加载训练集
	b,alphas = smoP(dataArr, labelArr, 100, 1e-6, 200, ('rbf', k1))		#根据训练集计算b和alphas
	datMat = np.mat(dataArr); labelMat = np.mat(labelArr).transpose()
	svInd = np.nonzero(alphas.A > 0)[0]										#获得支持向量
	sVs = datMat[svInd] 													
	labelSV = labelMat[svInd]
	print("支持向量个数:%d" % np.shape(sVs)[0])
	m,n = np.shape(datMat)
	errorCount = 0
	for i in range(m):
		kernelEval = kernelTrans(sVs,datMat[i,:],('rbf', k1))				#计算各个点的核
		predict = kernelEval.T * np.multiply(labelSV,alphas[svInd]) + b 	#根据支持向量的点，计算超平面，返回预测结果
		if np.sign(predict) != np.sign(labelArr[i]): errorCount += 1		#返回数组中各元素的正负符号，用1和-1表示，并统计错误个数
	print("训练集错误率: %.2f%%" % ((float(errorCount)/m)*100)) 			#打印错误率
	dataArr,labelArr = np.array(xtest),y_test.T.values.tolist()[0]						#加载测试集
	errorCount = 0
	datMat = np.mat(dataArr); labelMat = np.mat(labelArr).transpose() 		
	m,n = np.shape(datMat)
	result=np.zeros(m)
	for i in range(m):
		kernelEval = kernelTrans(sVs,datMat[i,:],('rbf', k1)) 				#计算各个点的核			
		predict=kernelEval.T * np.multiply(labelSV,alphas[svInd]) + b 		#根据支持向量的点，计算超平面，返回预测结果
		if np.sign(predict) != np.sign(labelArr[i]): errorCount += 1    	#返回数组中各元素的正负符号，用1和-1表示，并统计错误个数
		if np.sign(predict)==-1:
			result[i]=-1
		else:
			result[i]=1
	print("测试集错误率: %.2f%%" % ((float(errorCount)/m)*100)) 			#打印错误率
	macro=f1_score(y_true=y_test, y_pred=result, average="macro")
	print(macro)

testRbf()