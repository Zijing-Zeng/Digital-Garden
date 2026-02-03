---
# === 必填项 ===
title: "Matlab 备忘录"
date: 2026-02-03T16:00:00+08:00  # 建议精确到秒，决定排序
# === 核心状态 ===
draft: false            # true=草稿(不发布)，false=发布
publish: true           # 配合你的Python脚本，只有true才会被同步
# === 分类与标签 (决定文章在侧边栏的位置和归类) ===
categories: ["技术", "随笔"] # 分类 (Hextra侧边栏可能会用到)
tags: ["Hugo", "教程"]       # 标签 (文章底部的Tag)
# === 作者信息 (覆盖全局设置) ===
author: "Zijing"
# === 目录与结构 ===
weight: 10              # 排序权重：数字越小，在侧边栏/列表中越靠前
# menu:                   # 如果你想把这篇文章直接钉在顶部菜单栏
  # main:
    # weight: 20
# === SEO 与 描述 ===
description: "这里是文章的简短摘要，会显示在列表页和Google搜索结果中。"
slug: "my-custom-url"   # 自定义链接后缀 (比如 /posts/my-custom-url/)
# === 功能开关 (覆盖 hugo.yaml 的设置) ===
toc: true               # 本文是否显示目录
math: true              # 本文是否启用数学公式
comments: true          # 本文是否开启评论
---

## 1 Matlab 学习笔记

```table-of-contents
title: 
style: nestedList # TOC style (nestedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
debugInConsole: false # Print debug info in Obsidian console
```

## 2 语言特点速记

1. 数组是从 1 开始索引的
2. 数组是闭区间，比如 `a = [1, 2, 3, 4, 5, 6]` 中，`a(1:3)) = [1, 2, 3]`

## 3 矩阵分析

### 3.1 线性方程组

#### 3.1.1 行阶梯形矩阵

```matlab
[L,U] = lu(A) 
# 将满矩阵或稀疏矩阵 A 分解为一个上三角矩阵 U 和一个经过置换的下三角矩阵 L，使得 A = L*U。

[L,U,P] = lu(A) 
# 还返回一个置换矩阵 P，并满足 A = P'*L*U。在此语法中，L 是单位下三角矩阵，U 是上三角矩阵。

[L,U,P] = lu(A,outputForm)  
# 以 outputForm 指定的格式返回 P。将 outputForm 指定为 'vector' 会将 P 返回为一个置换向量，并满足 A(P,:) = L*U。

[L,U,P,Q] = lu(S)  
# 将稀疏矩阵 S 分解为一个单位下三角矩阵 L、一个上三角矩阵 U、一个行置换矩阵 P 以及一个列置换矩阵 Q，并满足 P*S*Q = L*U。

[L,U,P,Q,D] = lu(S)  
# 还返回一个对角缩放矩阵 D，并满足 P*(D\S)*Q = L*U。行缩放通常会使分解更为稀疏和稳定。
```

#### 3.1.2 最简行阶梯型矩阵

```matlab
R = rref(A)  使用 Gauss-Jordan 消去法和部分主元消去法返回简化行阶梯形的 A。

R = rref(A,tol)  指定算法用于确定可忽略列的主元容差。

[R,p] = rref(A)  多返回非零主元 p。
```

#### 3.1.3 求解线性方程组

```matlab
B=null(A)   % B的列向量是AX=0的规范正交的基础解系
B=null(A,'r')  % B的列向量是AX=0的有理数形式的基础解系
```

### 3.2 秩

#### 3.2.1 求秩的方法

```matlab
k = rank(A) 返回矩阵 A 的秩。
sprank(A) 确定稀疏矩阵的结构秩。

k = rank(A,tol) \指定在秩计算中使用另一个容差。秩计算为 A 中大于 tol 的奇异值的个数。

# 示例
a1=[1;2;2;3];
>> a2=[1;4;-3;6];
>> a3=[-2;-6;1;-9];
>> A=[a1,a2,a3];
>> r=rank(A)
```

### 3.3 正交化

#### 3.3.1 单位正交化

```matlab
Q = orth(A) 返回适用于 A 的范围的一个标准正交基。矩阵 Q 的列是涵盖了 A 范围的向量。Q 中列的数量等于 A 的秩。

Q = orth(A,tol) 也指定容差。小于 tol 的 A 的奇异值被视为零，这会影响 Q 中的列数。
```

#### 3.3.2 Gram-Schmidt 正交化

```matlab
function answer = schmidt(matrixIn, transpose)
% 默认取矩阵列向量为待正交化向量
% 函数调用 schmidt(A)
% 	如 A=[1,-1,4;2,3,-1;-1,1,0]
% 	则待正交化向量为 [-1,2,1], [-1,3,1], [4,-1,0]

if nargin > 1
    % 如果要求取矩阵行向量为待正交化向量
    % 函数调用方式为 schmidt(A,1)
    % 但是注意: 得到的结果矩阵仍然是列向量为正交化之后的向量
    if transpose == 1
       matrixIn = matrixIn';
    end
end

answer = zeros(size(matrixIn));
answer(:,1) = matrixIn(:,1);

if size(matrixIn,2)>1
    %正交化
    for column = 2:size(matrixIn,2)
        for beta = 1:column-1
            answer(:,column) = answer(:,column) ...
                - dot(matrixIn(:,column),answer(:,beta)) ...
                / dot(answer(:,beta),answer(:,beta)) * answer(:,beta);
        end
        answer(:,column) = answer(:,column) + matrixIn(:,column);
    end

    %单位化
    for column = 1:size(matrixIn,2)
        answer(:,column) = answer(:,column) ...
            / sqrt(dot(answer(:,column),answer(:,column)));
    end
end
end
```

### 3.4 特征分析

#### 3.4.1 特征多项式

```matlab
poly2sym(poly(A)) % 特征多项式
factor(poly2sym(poly(A))) % 特征多项式因式分解
```

#### 3.4.2 特征值

```matlab
e = eig(A) % 返回一个列向量，其中包含方阵 A 的特征值。
```

#### 3.4.3 特征向量

```matlab
% 返回特征值的对角矩阵 D 和矩阵 V，其列是对应的右特征向量
% 使得 A*V = V*D，即V-1 * A * V = D
[V,D] = eig(A) 
```

#### 3.4.4 对角化

```matlab
% 判断A是否是一个对角矩阵，返回逻辑值 1 (true)；0 (false)
tf = isdiag(A) 

% 返回一个由方阵 A 的特征值组成的列向量
e = eig(A) 

% 返回特征值的对角矩阵 D 和矩阵 V，其列是对应的右特征向量
% 使得 A*V = V*D，即V-1 * A * V = D
[V,D] = eig(A) 

% 还返回满矩阵 W，其列是对应的左特征向量，使得 W'*A = D*W'。
% 特征值问题是用来确定方程 Av = λv 的解，其中，A 是 n×n 矩阵，v 是长度 n 的列向量，λ 是标量。满足	方程的 λ 的值即特征值。满足方程的 v 的对应值即右特征向量。左特征向量 w 满足方程 w’A = λw’。
[V,D,W] = eig(A) 
```

反 Hermite 矩阵是复数域上的一个特殊矩阵，它满足以下条件：对于矩阵 A，其转置共轭（Hermitian transpose）为负矩阵，即 A^H = -A，其中 A^H 表示 A 的转置共轭。

我们要证明如果 A 是反 Hermite 矩阵，则 A 的特征值的实部为 0。设 A 的特征值为λ，对应的特征向量为 v。则有 Av = λv。

现在，我们来证明特征值λ的实部为 0。

首先，将上述方程两边取共轭转置，得到：

$$
\begin{align*}
(Av)^H &= (λv)^H \\
v^H A^H &= λ^*v^H \\
v^H (-A) &= λ^*v^H \quad \text{(根据A是反Hermite矩阵，所以} A^H = -A) \\
- v^H A &= λ^*v^H
\end{align*}
$$

现在，将两个方程相乘：

$$
\begin{align*}
v^H A (- v^H A) &= λ^*v^H v^H \\
- v^H A^2 &= λ^*|v|^2 \\
- v^H A^2v &= λ^*|v|^2 \quad \text{(} |v| \text{表示向量v的模)}
\end{align*}
$$

考虑到 A 是反 Hermite 矩阵，所以 A\^2 是正定的，因此 v\^H A\^2v 是实数且大于等于零。而右侧λ\^*|v|^2 也是实数。

由于左侧和右侧相等，那么λ\^_必须是非正实数。设λ^_ = α + iβ，其中α和β是实数，i 是虚数单位。

由于λ^* 是非正实数，我们可以得到α ≤ 0。现在，我们来看原特征。

### 3.5 Smith 标准型

### 3.6 矩阵分解

#### 3.6.1 满秩分解

```matlab
function [Final_P,Final_Q] = fullRankDecomps(A)
    % 对矩阵A进行最大秩分解
    %	Final_P 列满秩矩阵
    %	Final_Q 行满秩矩阵
    
    B = rref(A);    %计算行最简式
    [m, n] = size(A);
    P(1:m,:) = 0;
    Q(:,1:n) = 0;
    for i = 1:m
        for j = 1:n
            if(B(i,j)==1.0 && sum(B(1:i-1,j))==0 && sum(B(i+1:m,j))==0)
                P = [P,A(:,j)];
                Q = [Q;B(i,:)];
            end
        end
    end
    Final_P = P(:,2:end);
    Final_Q = Q(2:end,:);
end
```

#### 3.6.2 QR 分解

#### 3.6.3 奇异值分解

任何一个矩阵，都可以分解为三个特殊的矩阵。

$A_{m \times n} = U_{m \times m} \Sigma_{m \times n} V^T_{n \times n}$

$U$ 和 $V$ 都是正交矩阵；$U$ 中是 $AA^T$ 的特征向量；$V$ 中式 $A^TA$ 的特征向量

$ \Sigma$ 是长方形对角矩阵，对角线上是 $A$ 降序排列的奇异值；$\Sigma$ 还可以理解为一个对角矩阵 $\Lambda$ 右乘一个单位矩阵（可以非方阵）$E$ 。

对于任意一个矩阵 $A$，可以理解为 $A_{m \times n} = U_{m \times m} \Lambda_{m \times m} E_{m \times n} V^T_{n \times n}$ ，也就是说，将一个球旋转，然后消去或者增加维度，然后伸缩变换，然后再旋转。

$A^TA$ 和 $AA^T$ 都一定是对称矩阵

如果矩阵 $A$ 列满秩，那么 $A^TA$ 和 $AA^T$ 一定可逆，并且都是半正定矩阵，所有特征值都是非负的；如果将特征值降序排列，对应部分都是一样的，把共享的部分求开方，就是矩阵 $A$ 的奇异值。

对称矩阵的特征向量都是垂直的

当 $A = U \Sigma V^T$ 时，此时：

$A^TA = (U \Sigma V^T)^T (U \Sigma V^T) = (V \Sigma^T U^T)(U \Sigma V^T) = V \Sigma^T \Sigma V^T = V (\Sigma^T \Sigma) V^T$

也就是**对称矩阵的特征值对角化**，所以**特征值就是奇异值的平方**。此时 $V$ 是 $A^TA$ 的**单位正交特征向量矩阵**。同理，$U$ 是 $AA^T$ 的**单位正交特征向量矩阵**。

```matlab
S = svd(A) 以降序顺序返回矩阵 A 的奇异值。

[U,S,V] = svd(A) 执行矩阵 A 的奇异值分解，因此 A = U*S*V'。
```

### 3.7 约当标准型

```matlab
% 求矩阵A的Jordan标准形J和相似变换矩阵P
>> [P,J] = jordan(A)
```

### 3.8 最小二乘法

投影矩阵

```matlab
P = A*inv(A'*A)*A'
```

## 4 Matlab 的基础

### 4.1 常用函数

| 函数        | 功能                  |
| ----------- | --------------------- |
| help +fun   | 查看函数帮助手册      |
| clc         | 清空命令行            |
| clear       | 清空工作区变量        |
| whos + var  | 查看变量属性          |
| save / load | 保存 / 加载工作区变量 |
|             |                       |
|             |                       |
|             |                       |
|             |                       |
|             |                       |

### 4.2 关键字

```matlab
>> iskeyword % 查看 matlab 全部关键字
ans = 
    'break'
    'case'
    'catch'
    'classdef'
    'continue'
    'else'
    'elseif'
    'end'
    'for'
    'function'
    'global'
    'if'
    'otherwise'
    'parfor'
    'persistent'
    'return'
    'spmd'
    'switch'
    'try'
    'while'
```

**特别说明**

| 关键字     | 说明 |
| ---------- | ---- |
| catch      |      |
| classdef   |      |
| global     |      |
| otherwise  |      |
| parfor     |      |
| persistent |      |
| spmd       |      |

### 4.3 运算符

#### 4.3.1 算数运算符

- 加法 (`+`)：用于两个数或数组的相加。
- 减法 (`-`)：用于两个数或数组的相减。
- 乘法 (`*`)：用于两个数或数组的相乘。
- 除法 (`/`)：用于两个数或数组的相除。
- 幂运算 (`^`)：用于计算一个数的指定次方。
- 取余 (`mod`)：用于计算两个数相除后的余数。

#### 4.3.2 逻辑运算符

- 与运算 (`&`)：用于对两个逻辑表达式进行逻辑与操作。
- 或运算 (`|`)：用于对两个逻辑表达式进行逻辑或操作。
- 非运算 (`~`)：用于对逻辑表达式取反。
- 异或运算 (`xor`)：用于对两个逻辑表达式进行逻辑异或操作。

#### 4.3.3 【Tips】逻辑运算技巧

```matlab
x = [1,2,3];
y = [1,2,2];

all(x<=y) && any(x<y) % 表示 x 的每一个元素都 ≤y，并且至少有一个元素 <y

```

#### 4.3.4 关系运算符

- 等于 (`==`)：判断两个值是否相等。
- 不等于 (`~=`)：判断两个值是否不相等。
- 大于 (`>`)：判断一个值是否大于另一个值。
- 小于 (`<`)：判断一个值是否小于另一个值。
- 大于等于 (`>=`)：判断一个值是否大于或等于另一个值。
- 小于等于 (`<=`)：判断一个值是否小于或等于另一个值。

#### 4.3.5 数组运算符

- 拼接运算符 (`[]`)：用于将多个数组拼接成一个新的数组。
- 复制运算符 (`:`)：用于生成一个指定范围的数组。
- 元素访问运算符 (`()`)：用于访问数组中特定位置的元素。

### 4.4 Matlab 的程序流程

#### 4.4.1 For 循环

```matlab
for var=向量表达式
	循环体
end

% 向量表示式常用 s:h:e
```

#### 4.4.2 While 循环

```matlab
while 关系表达式
	循环体
end
```

#### 4.4.3 【Tips】循环的技巧

**从一个有序集合中抽取出两个元素两两操作**
用以下的代码，可以避免两个元素重复索引出来，即“**是组合而非排列**”

```matlab
for i = 1:nPop
    for j = i+1:nPop
        index(i,j);
    end
end
```

#### 4.4.4 If 分支

```matlab
% 格式1
if 条件按表达式
	条件语句组
end

% 格式2
if 条件表达式
	条件语句组1
else
	条件语句组2
end

% 格式3
if 条件表达式
	条件语句组1
elseif
	条件语句组2
	...
elseif
	条件语句组n
else
    条件语句组n+1
end
```

#### 4.4.5 Switch 分支

```matlab
switch(表达式)
	case 常量表达式1
		语句组1
    case 常量表达式2
    	语句组2
    	...
    case 常量表达式
    	语句组n
    otherwise:
    	语句组 n+1
end
```

### 4.5 try-catch 机制

```python
try
    % 假设我们要读取一个文件
    fid = fopen('不存在的文件.txt', 'r');
    if fid == -1
        error('MyToolbox:FileNotFound', '找不到指定的文件');
    end
    data = fread(fid);
    fclose(fid);
catch ME % 可以省略ME
    switch ME.identifier % 可以不对错误进行针对性处理
        case 'MyToolbox:FileNotFound'
            disp('请检查文件路径是否正确。');
        case 'MATLAB:nomem'
            disp('内存不足，尝试清理变量。');
        otherwise
            % 对于未知的其他错误，重新抛出，让程序崩溃或由上层处理
            rethrow(ME);
    end
end
```

### 4.6 Matlab 函数

#### 4.6.1 输入参数类型检验

| 资源                                                                                                      | 说明        |
| ------------------------------------------------------------------------------------------------------- | --------- |
| [声明函数名称、输入和输出 - MATLAB function - MathWorks 中国](https://ww2.mathworks.cn/help/matlab/ref/function.html) | 里面参数检验的说明 |

```matlab
function [m,s] = stat3(x)
    arguments
        x (1,:) {mustBeNumeric, mustBeFinite}
    end
    n = length(x);
    m = avg(x,n);
    s = sqrt(sum((x-m).^2/n));
end

function m = avg(x,n)
    m = sum(x)/n;
end
```

在 `arguments` 代码块中，`(1,:)` 表示 `x` 必须为向量。验证函数 `{mustBeNumeric, mustBeFinite}` 将 `x` 中的元素限制为非 `Inf` 或 `NaN` 的数值。有关详细信息，请参阅 [函数参量验证](https://ww2.mathworks.cn/help/matlab/matlab_prog/function-argument-validation-1.html)。

如果调用函数时所带的向量包含 `NaN` 元素，则违反了输入参量声明。此违规会导致 [`mustBeFinite`](https://ww2.mathworks.cn/help/matlab/ref/mustbefinite.html) 验证函数引发错误。

## 5 Matlab 编程思想

### 5.1 向量运算

```matlab
% 梯形法就近似积分
% 常规思路
clear all
a = 0;
b = 3*pi;
n = 1000;
h = (b-a)/n;
x = a;
s = 0;
f0 = exp(-0.5*x) * sin(x+pi/6)
for i = 1:n
	x = x+h;
	f1 = exp(-0.5*x) * sin(x+pi/6);
	s = s + (f0 + f1) * h/2；
	f0 = f1;
end
s

% 向量运算
a = 0;
b = 3*pi;
n = 1000;
h = (b-a)/n;
x = a:h:b;
f = exp(-0.5*x) .* sin(x+pi/6);
for i = 1:n
	s(i) = (f(i)+f(i+1)) * h/2;
end
s = sum(s)
```

### 5.2 面对对象编程

#### 5.2.1 运算符重载

[运算符重载 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/matlab/matlab_oop/implementing-operators-for-your-class.html)

下表列出了 MATLAB 运算符的对应函数名称。实现运算符以处理数组（标量扩展、向量化算术运算等）时，可能还需要修改索引和串联方式。使用下表中的链接可了解关于每个函数的具体信息。

| 运算               | 要定义的方法                                                 | 描述         |
| :----------------- | :----------------------------------------------------------- | :----------- |
| `a + b`            | [`plus`](https://ww2.mathworks.cn/help/matlab/ref/plus.html)`(a,b)` | 二元加法     |
| `a - b`            | [`minus`](https://ww2.mathworks.cn/help/matlab/ref/minus.html)`(a,b)` | 二元减法     |
| `-a`               | [`uminus`](https://ww2.mathworks.cn/help/matlab/ref/uminus.html)`(a)` | 一元减法     |
| `+a`               | [`uplus`](https://ww2.mathworks.cn/help/matlab/ref/uplus.html)`(a)` | 一元加法     |
| `a.*b`             | [`times`](https://ww2.mathworks.cn/help/matlab/ref/times.html)`(a,b)` | 按元素乘法   |
| `a*b`              | [`mtimes`](https://ww2.mathworks.cn/help/matlab/ref/mtimes.html)`(a,b)` | 矩阵乘法     |
| `a./b`             | [`rdivide`](https://ww2.mathworks.cn/help/matlab/ref/rdivide.html)`(a,b)` | 右按元素除法 |
| `a.\b`             | [`ldivide`](https://ww2.mathworks.cn/help/matlab/ref/ldivide.html)`(a,b)` | 左按元素除法 |
| `a/b`              | [`mrdivide`](https://ww2.mathworks.cn/help/matlab/ref/mrdivide.html)`(a,b)` | 矩阵右除     |
| `a\b`              | [`mldivide`](https://ww2.mathworks.cn/help/matlab/ref/mldivide.html)`(a,b)` | 矩阵左除     |
| `a.^b`             | [`power`](https://ww2.mathworks.cn/help/matlab/ref/power.html)`(a,b)` | 按元素求幂   |
| `a^b`              | [`mpower`](https://ww2.mathworks.cn/help/matlab/ref/mpower.html)`(a,b)` | 矩阵幂       |
| `a < b`            | [`lt`](https://ww2.mathworks.cn/help/matlab/ref/lt.html)`(a,b)` | 小于         |
| `a > b`            | [`gt`](https://ww2.mathworks.cn/help/matlab/ref/gt.html)`(a,b)` | 大于         |
| `a <= b`           | [`le`](https://ww2.mathworks.cn/help/matlab/ref/le.html)`(a,b)` | 小于或等于   |
| `a >= b`           | [`ge`](https://ww2.mathworks.cn/help/matlab/ref/ge.html)`(a,b)` | 大于或等于   |
| `a ~= b`           | [`ne`](https://ww2.mathworks.cn/help/matlab/ref/ne.html)`(a,b)` | 不等于       |
| `a == b`           | [`eq`](https://ww2.mathworks.cn/help/matlab/ref/eq.html)`(a,b)` | 相等性       |
| `a & b`            | [`and`](https://ww2.mathworks.cn/help/matlab/ref/and.html)`(a,b)` | 逻辑 AND     |
| `a | b`            | [`or`](https://ww2.mathworks.cn/help/matlab/ref/or.html)`(a,b)` | 逻辑 OR      |
| `~a`               | [`not`](https://ww2.mathworks.cn/help/matlab/ref/not.html)`(a)` | 逻辑非       |
| `a:d:b``a:b`       | [`colon`](https://ww2.mathworks.cn/help/matlab/ref/colon.html)`(a,d,b)``colon(a,b)` | 冒号运算符   |
| `a'`               | [`ctranspose`](https://ww2.mathworks.cn/help/matlab/ref/ctranspose.html)`(a)` | 复共轭转置   |
| `a.'`              | [`transpose`](https://ww2.mathworks.cn/help/matlab/ref/transpose.html)`(a)` | 矩阵转置     |
| `[a b]`            | [`horzcat`](https://ww2.mathworks.cn/help/matlab/ref/double.horzcat.html)`(a,b,…)` | 水平串联     |
| `[a; b]`           | `vertcat(a,b,…)`                                           | 垂直串联     |
| `a(s1,s2,…sn)`   | [`subsref`](https://ww2.mathworks.cn/help/matlab/ref/subsref.html)`(a,s)` | 下标引用     |
| `a(s1,…,sn) = b` | [`subsasgn`](https://ww2.mathworks.cn/help/matlab/ref/subsasgn.html)`(a,s,b)` | 通过下标赋值 |
| `b(a)`             | [`subsindex`](https://ww2.mathworks.cn/help/matlab/ref/subsindex.html)`(a)` | 下标索引     |

**运算符重载实例**

`Adder` 类通过定义 `plus` 方法来实现此类的对象的相加。`Adder` 将对象的相加定义为 `NumericData` 属性值的相加。`plus` 方法构造并返回一个 `Adder` 对象，该对象的 `NumericData` 属性值是执行相加的结果。

`Adder` 类还通过定义 `lt` 方法实现小于运算符 (`<`)。`lt` 方法在比较每个对象的 `NumericData` 属性中的值后，返回一个逻辑值。

```matlab
classdef Adder
   properties
      NumericData
   end
   methods
      function obj = Adder(val)
         obj.NumericData = val;
      end
      function r = plus(obj1,obj2)
         a = double(obj1);
         b = double(obj2);
         r = Adder(a + b);
      end
      function d = double(obj)
         d = obj.NumericData;
      end
      function tf = lt(obj1,obj2)
         if obj1.NumericData < obj2.NumericData
            tf = true;
         else
            tf = false;
         end
      end
   end
end
```

## 6 Matlab 的变量类型

**变量类型引入**

- 变量是任何程序设计语言的基本元素之一。
- Matlab 对所使用的变量并不要求进行事先声明，也不需要指定变量类型，Matlab 会自动根据所赋予变量的值或对变量所进行的操作来确定变量的类型。
- 在赋值过程中，如果变量已经存在，新值代替旧值，新类型代替旧类型。

**变量名定义规则**

- 变量名和函数名对字母的大小写敏感
- 不能使用 `MATLAB` 的关键字作为变量名
- 避免使用函数名作为变量名，如果你使用了函数名，则该函数失效。
- 变量名长度不超过 63 位，以字母开头，可以由字母、数字和下划线组成，但不能使用标点
- 可以通过调用 `isvarname()` 函数,来验证变量名是否符合 `MATLAB` 所接受的合法变量名。

**matlab 中的五种变量类型**

- numeric：数值
- char：字符
- logical：逻辑
- cell：单元、细胞、元胞
- struct：结构

### 6.1 矩阵

#### 6.1.1 矩阵的生成

**一维矩阵整型**

`A = reshape(1:30, 5, 6)`

**中括号定义法**

`matrix = [1 2 3; 4 5 6; 7 8 9]`

**实时添加法**

matrix(1,1) = 1;

		matrix(1,2) = 2;

		matrix(1,3) = 3;

		matric(2,1) = 4;

**函数生成法**

```matlab
zeros() 	% 产生全0矩阵，即零矩阵。
ones() 		% 产生全1的矩阵，即幺矩阵。
eye() 		% 产生对角线为1的矩阵。当矩阵为方阵时，得到一个单位矩阵。
rand() 		% 产生（0,1）区间均匀分布的随机矩阵。
randn() 	% 产生均值为0，方差为1的标准正态分布随机矩阵。
magic() 	% 幻方矩阵 % 产生行、列、对角线和相等的方阵。
vander() 	% 范德蒙矩阵。
hilb() 		% 希尔伯特矩阵。
compan(p) 	% 伴随矩阵。其中p是一个多项式的系数向量，高次幂系数排在前，低次幂系数排在后。
pascal() 	% 帕斯卡矩阵。根据二项式定理，(x+y)^n展开后的系数随着n的增大组成一个三角形表，这个三角形成为杨辉三角形。
	% 函数生成的技巧
	zeros(size(A))  % 生成一个和 A 同样大小的零矩阵
	zeros(n)		% 生成一个 n 阶方阵
	zeros(m,n,p)    % 生成一个 mxnxp 的矩阵

```

**结构体数组/矩阵**

```matlab
>> st(1).x1 = 1;
>> st(1).x2 = 2;
>> st(2)

```

![image-20221105135847562|800](/images/matlab/image-20221105135847562.png)

![image-20221105135824822|725](/images/matlab/image-20221105135824822.png)

![image-20221105135746589|800](/images/matlab/image-20221105135746589.png)

#### 6.1.2 改变矩阵的大小

##### 6.1.2.1 矩阵的合并

[A; B] 表示矩阵按行合并储存；

[A, B] 表示矩阵按列合并储存。即

cat(1, A, B) 表示矩阵按行合并储存；

cat(2, A, B) 表示矩阵按列合并储存；

cat(3, A, B) 表示矩阵以第 3 个维度组合 A、B 矩阵，变成三维矩阵。

> 经验：
>
>   1. [] 不仅可以作为矩阵创建使用，还可以作为矩阵合并操作符。
> 
>   2. 矩阵合并的过程，要保证矩阵的形状都是矩形，且行列匹配

##### 6.1.2.2 矩阵行列的删除

要删除某一矩阵的某一行或某一列，那么，只需要对对应的行或者列赋值为空向量 [] ，剩下的部分会自动“缝合”。例如，删除一个 4 阶方阵 A 的第 2 行，可以使用语句：`A(2, :) = []`

##### 6.1.2.3 一维矩阵整型

`A = reshape(1:30, 5, 6)`

#### 6.1.3 矩阵算数运算

| 运算符  | 功能                                               |
| ------- | -------------------------------------------------- |
| + - * ^ | 加减乘、乘方                                       |
| /       | 矩阵右除 A/B : X * A = B 的解 X 即， A/B=A*inv(B) |
| \       | 矩阵左除 A\B : A * X = B 的解 X 即， A\B=inv(A)*B |

#### 6.1.4 矩阵元素群运算

矩阵中的所有元素按单个元素对应进行运算。

有.* ./ .\ .^ 四种

#### 6.1.5 矩阵元素群的初等函数

Matlab 中的函数大多数都是作用于函数变量（或矩阵）的每一个元素，所以，这些函数的自变量可以是任意阶的矩阵。

#### 6.1.6 矩阵的常用方法

| 函数      | 功能                |
| --------- | ------------------- |
| size(A)   | 计算 A 的大小，返回 [m,n] |
| A‘        | 计算 A 的转置         |
| inv(A)    | 计算 A 的逆 |
| length(A) | 计算 A 的长度（列数） |
| sum()  | 对向量或者矩阵的每一个列向量进行求和，返回一个数值或者行向量，其中行向量中每个元素对应矩阵列向量的和 |
| max()  | 对向量或者矩阵的每一个列向量找最大值，返回一个数值或者行向量，其中行向量中每个元素对应矩阵列向量的最大值 |
| prod() | 如果 `A` 是向量，则 `prod(A)` 返回元素的乘积。 如果 `A` 为非空矩阵，则 `prod(A)` 将 `A` 的各列视为向量，并返回一个包含每列乘积的行向量。 如果 `A` 为 0×0 空矩阵，`prod(A)` 返回 `1`。 |

#### 6.1.7 矩阵索引

```matlab
>> matrix = [1 2 3; 4 5 6; 7 8 9]; % 矩阵示例

>> matrix(1,1) % 索引单个元素
ans = 
		1

>> matrix(1,:)  % 提取行列向量冒号表示从头至尾
ans =
    	1     2     3

>> matrix(:,1)
ans =
        1
        4
        7

>> matrix(2:3, 2:3) % 提取块矩阵
ans = 
        5  6
        8  9
```

#### 6.1.8 【Tips】数组索引的技巧

```matlab
>>> ary = [1,2,3,4,5,6];
>>> ind = [1,3,4];
>>> ary(ind)

1  3  4
```

### 6.2 结构体

#### 6.2.1 结构体的说明

与元胞（cell）类型一样，结构体也可以存储任意类型的数据。当然，它们也存在许多不同点。最大的不同点是，结构体是以不同名字的字段作为存储容器，每个字段都可以存储任意类型的数据。

#### 6.2.2 结构体的生成

```matlab
% struct()函数生成法
% 1x1的结构体数组
>> s1 = struct;            % 不含字段
>> s2 = struct('name', '李四', 'gender',{'男' '女'})  % 定义具体字段

% 1x2的结构体数组
>> s3 = struct('name', {'张三', '李四'}, 'gender', 'male');    % 通过元胞数组，来创建多结构体的结构体数组。所有字段的行数自动复制对齐

% 即时添加法
>> s(1).name = 'LiSi';
>> s(1).gender = 'Male';
>> s(1).age = 18;
>> s(1).test = {'hello', 1};
>> s(2).name = 'LiSi';
>> s(2).gender = 'female';
>> s(2).age = 20;
>> s(2).test = s(1);
>> s % 1x2的结构体数组（不明确指定位置，按水平方式排列）

>> s1 = s(1)
>> s2 = s(2)
```

#### 6.2.3 结构体的常规操作

| 函数                                 | 功能                                     |
| ------------------------------------ | ---------------------------------------- |
| isfield(struct, {name1, name2, …}) | 判断输入的字段是否为输入结构体数组的字段 |
| rmfield(struct, {name1, name2, …}) | 删除结构体中的指定字段                   |

**使用举例**

```matlab
% 1x3的结构体数组
>> s = struct('name', {'张三', '李四', '王二麻子'}, 'gender', 'male', 'age', {18, 20, 'unknown'})
 
% 函数isfield()		
>> fieldStatus = isfield(s, 'name')  			% 返回逻辑值
>> fieldStatus = isfield(s, {'name', 'gender'}) % 返回逻辑数组
 
% 函数rmfield()
>> s_new = rmfield(s, {'name', 'gender'})
>> s_new
```

#### 6.2.4 【Tips】结构体数组的索引技巧

对于结构体数组，可以直接用数组变量名索引 field，再在外侧加中括号整合成一个

```matlab
%% 输入代码
st(1).a = 11;
st(1).b = 22;

st(2).a = 33;
st(2).b = 44;

st.a
[st.a]

%% 输出结果
ans =
    11
ans =
    33
ans =
    11    33
```

### 6.3 字符与字符串

#### 6.3.1 字符与字符串

在 MATLAB 中，单引号和双引号的使用有一些区别。 **单引号 ('') 用于创建字符数组，而双引号 ("") 用于创建字符串数组**。

单引号里面的内容不会被解释，直接输出，而双引号里面的内容会经过编译器解释后再输出。 此外，单引号解析的速度比双引号快，并且单引号支持转义符（如），而双引号支持更多的转义符。

#### 6.3.2 字符串的常规操作

| 函数       | 功能                             |
| -------- | ------------------------------ |
| strcmp   | 比较字符串                          |
| strcmpi  | 忽略大小写比较字符串                     |
| upper    | 转换为大写                          |
| blanks   | 产生空字符串                         |
| strmatch | 查找匹配的字符串                       |
| strjust  | 对其字符数组，包括左对其，右对齐和居中            |
| strrep   | 替换字符串                          |
| strncmp  | 比较字符串的前 n 个字符                  |
| lower    | 转换为小写                          |
| deblank  | 删除字符串中的空格                      |
| findstr  | 在一个字符串中查找另一个字符串                |
| strtok   | 返回字符串中第一个分割符（空格，回车和 Tab 键）前的部分 |
|          |                                |

**创建指定尺寸的字符串数组**

```matlab
strings(5,1,1) % 创建5x1的字符串数组，每个字符串长度为1
```

### 6.4 细胞数组

#### 6.4.1 元胞数组的引入

- 从 5.0 版开始引入了一种新的数据类型 — 细胞 ( cell )，该结构可以把不同类型的数据纳入到一个变量中。
- 普通数组中的每个元素都必须具有相同的数据类型，而细胞则没有此要求。
- 细胞变量的表示方法类似于带有下标的数组，但这些下标不是用圆括号括起来，而是使用大括号。

#### 6.4.2 元胞数组的生成

```matlab
% 直接具体定义
>> A = [1 2; 3 4]; 
>> str = 'Matlab';
>> M = {1:4, A, str}; 
>> celldisp(M)

% 即时添加
>> M{1,1} = 1;
>> M{1,2} = 'strs';
>> 
>> M{2,1} = 

% 预留空间
>> c = cell(2, 2);
>> c{1, 1} = 1;
>> c{1, 2} = 'str';
>> c{2, 2} = struct;
```

### 6.5 函数句柄

#### 6.5.1 函数句柄引入

- 可以为已命名函数和匿名函数创建函数句柄。
- 函数句柄是一种存储指向函数的关联关系的 [MATLAB](https://so.csdn.net/so/search?q=MATLAB&spm=1001.2101.3001.7020)® 数据类型。
- 可以使用 isa(h,'function_handle') 来查看变量 h 是否为函数句柄。
- 函数句柄会存储其绝对路径，因此如果有有效句柄，则可以从任意位置调用该函数，无需考虑调用位置。
- 不必在创建句柄时指定函数路径，只需指定函数名。

#### 6.5.2 函数句柄的生成

```matlab
% 通过在现有自定义或内置函数名称前添加一个 @ 符号来为函数创建句柄
>> f = @myfunction;

% 匿名函数法
>> f = @(x1, x2) x1^2 + x2^3
```

#### 6.5.3 多项式函数句柄

```matlab
p = @(x) x ^ 2 + 2 * x + 3  % p 是一个 function_handle
p(3) % 18
p(7) % 66

p([3 7]) % 报错
p = @(x) x .^ 2 + 2 .* x + 3;
p([3 7])
```

### 6.6 符号变量

#### 6.6.1 符号运算注意事项

1. matlab 中的符号运算功能是建立在 Maple 软件基础上的
2. 整个过程中，即使以数字形式出现的量也是字符量
3. 符号型变量包含：符号常量、符号变量、符号函数和符号表达式四种

#### 6.6.2 内置的符号常量

| 常量名  | 常量值               |
| ------- | -------------------- |
| i,j     | 虚数单位             |
| pi      | 圆周率               |
| NaN     | 不定值，如 0/0        |
| inf     | 无穷大               |
| eps     | 浮点运算相对精度     |
| nargin  | 输入变量数目         |
| nargout | 输出变量数目         |
| realmin | 最小的正浮点数       |
| realmax | 最大的正浮点数       |
| ans     | 用于结果的缺省变量名 |

#### 6.6.3 符号变量的声明

```matlab
>> c = sym('xt')
c = 
	xt


>> g= sym('cos(x+siny)=siny')


>> x = sym('x_%d',[1,3])
x =
	[x_1, x_2, x_3]

>> syms x y z
```

#### 6.6.4 符号常规操作

| 函数 | 说明 |
| ---- | ---- |
| **subs(f,x,y)** | 把 f 中的 x 换成 y |
| **subs(f,y)** | 把 f 中的主变量换成 y |
|**symvar(f)**|找出 f 的符号变量 |
|**symvar(f,1)** | 找出 f 的主变量 |
|**eval(f)** | 重新计算 f 的值 |
|**assume(x<0)**|指定变量范围|

#### 6.6.5 化简符号表达式

#### 6.6.6 替换符号表达式

```
snew = subs(s,old,new)
snew = subs(s,new)
snew = subs(s)
```

```
subs(x + y,a)
ans = a+y
```

#### 6.6.7 符号函数复合

1. `compose(f,g)` returns `f(g(y))` where `f = f(x)` and `g = g(y)`. Here `x` is the symbolic variable of `f` as defined by `symvar` and `y` is the symbolic variable of `g` as defined by `symvar`.
2. `compose(f,g,z)` returns `f(g(z))` where `f = f(x)`, `g = g(y)`, and `x` and `y` are the symbolic variables of `f` and `g` as defined by `symvar`.
3. `compose(f,g,x,z)` returns `f(g(z))` and makes `x` the independent variable for `f`. That is, if `f = cos(x/t)`, then `compose(f,g,x,z)` returns `cos(g(z)/t)` whereas `compose(f,g,t,z)` returns `cos(x/g(z))`.
4. `compose(f,g,x,y,z)` returns `f(g(z))` and makes `x` the independent variable for `f` and `y` the independent variable for `g`. For `f = cos(x/t)` and `g = sin(y/u)`, `compose(f,g,x,y,z)` returns `cos(sin(z/u)/t)` whereas `compose(f,g,x,u,z)` returns `cos(sin(y/z)/t)`.

#### 6.6.8 符号函数求反函数

1. `g = finverse(f)` returns the inverse of function `f`, such that `f(g(x)) = x`. If `f` contains more than one variable, use the next syntax to specify the independent variable.
2. `g = finverse(f,var)` uses the symbolic variable `var` as the independent variable, such that `f(g(var)) = var`.

#### 6.6.9 符号微积分

```matlab
diff(F)						% 求F()的一阶导
diff(F, n)					% 求F()的n阶导
diff(F, x)					% 求F()对x的偏导
diff(F, x, n)				% 求F()对x的n阶偏导
jacobian([F1; F2; F3], [x1; x2; x3])	% 求雅可比矩阵
```

```matlab
%%
%符号微积分
%求符号函数极限limit()
syms x y t;
f1=(cos(x)+sin(x)-x)/x
f2=sin(t)/t
f3=tan(y)
limit(f1,x,inf)
limit(f1,x,-inf)
limit(f2,t,0)
%也可求左右极限
limit(f3,y,pi/2,'left')
limit(f3,y,pi/2,'right')
%符号函数的求导，求微分diff()
clear
clc
syms x y t;
f1=x^4+2*x^3-(1/2)*x^2+6*x%符号表达式表示的多项式函数
g=[1 2 -1/2 6 0]%数值法表示的同一多项式
f2=sin(x^2)
f3=exp(t*sin(x))+log(y)%多元函数亦可用diff()对指定变量求，相当于求偏导
diff(f1,x,1)%1阶微分
polyder(g)
disp('\n');
diff(f2,x)
diff(f2,x,2)
diff(f3,t,1)
diff(f3,x,1)
diff(f3,y)
%注：传入参数也可是表达式构成的符号矩阵
diff([f1 f2],x,1)
%若是求全导数，则用jacobian()，即同时对几个自变量求导
w=[x^2+y^2;2*y+2*x]
jacobian(w,[x y])
%%
%求符号表达式函数的积分（限可以是函数）int()
clear
clc
syms x y t;
f1=x^4+2*x^3-(1/2)*x^2+6*x%符号表达式表示的多项式函数
g=[1 2 -1/2 6 0]%数值法表示的同一多项式
f2=x+x^-1
f3=x^2+y^2
%求不定积分
int(f1,x)
polyint(g)
int(f2,x)
int(f3,y)
disp('/n');
%求定积分
int(f1,x,1,2)
ff=@(x)x.^4+2*x.^3-(1/2)*x.^2+6.*x;
quad(ff,1,2)
int(f2,x,0,x+1)
int(f3,y,y/2,3*y)
%%
%符号表达式的级数求和symsum()
clear
clc
syms s n;
f=s^2;
g=n;
symsum(f,s,0,n)
symsum(g,n,1,100)
%%
%求符号表达式的泰勒级数taylor()
clear
clc
syms x y t;
f=sin(x)/(2+sin(x))
taylor(f,x,'Order', 8,'ExpansionPoint',0)%在x=0处对f做7阶泰勒展开
%taylor(f,t)
%%
%符号表示分段函数piecewise
syms x
y = piecewise(x<0, -1, x>0, 1)
subs(y,x,1)
%%
%符号积分变换
%傅里叶变换及其反变换fourier()ifourier()
clear
clc
syms t w;
f=cos(t)*sin(t);
a=fourier(f,t,w)
b=ifourier(a,w,t)
simplify(b)
% y1=f*exp(-1j*w*t)
% y2=(1/(2*pi))*a*exp(1j*w*t)
% aa=int(y1,t,-inf,inf)
% bb=int(y2,w,-inf,inf)
%拉普拉斯变换及其反变换laplace()ilaplace()
clear
clc
syms s t;
syms a aa positive ;
f=exp(2*t)+5*dirac(a-t)
a=laplace(f,t,s)
b=ilaplace(a,s,t)
% aa=int(f*exp(-s*t),t,0,inf)
%Z变换
clear;
clc;
syms n z;
f=n^2+n;
FZ=ztrans(f,n,z)
ff=iztrans(FZ,z,n)
subs(f,n,1)
subs(ff,n,1)
%%
%代数方程（组）求解solve()
%代数方程，即由多项式组成的方程
%solve只能求出部分超越方程的解析解
%当一元方程?(z)=0的左端函数?(z)不是z的多项式时，称之为超越方程。
%如指数方程、对数方程、三角方程、反三角方程等
clear;
clc;
syms a b c x;
f1=a*x^2+b*x+c;
s1=solve(f1,x)
s2=solve(f1,a)
f2=4*x^3+2*x^2+x+8;
s3=solve(f2,x)
double(s3)
r=roots([4 2 1 8]) 
%解代数方程组
clear;
clc;
syms x y;
f1=x^2+y^2;
f2=sym('x*y=12');
[sx xy]=solve(f1,f2,x,y)
%%
%解微分方程
%解常微分方程用dsolve()
%通过使用diff函数指定微分方程并表示微分方程
clear;
clc;
syms a b x y(t) t;%声明y是t的函数
f=diff(y,t)==a*t%a是系数,diff(y,t)是y对t的一阶导数
cond=y(0)== 0;
dsolve(f,cond)
ef=subs(ans,a,2)
%用ode系列函数解微分方程数值解
tspan = [0 5];
y0=0;
[t,y]= ode45(@(t,y) 2*t, tspan, y0);
%作图比较解析解和数值解
hold on;
ezplot(ef,[0,5]);
plot(t,y,'o')
```

#### 6.6.10 符号积分变换

#### 6.6.11 符号方程求解

**代数方程求解**

```matlab
S = solve(eqn,var)
S = solve(eqn,var,Name,Value)

Y = solve(eqns,vars)
Y = solve(eqns,vars,Name,Value)

[y1,...,yN] = solve(eqns,vars)
[y1,...,yN] = solve(eqns,vars,Name,Value)
[y1,...,yN,parameters,conditions] = solve(eqns,vars,'ReturnConditions',true)
```

**微分方程求解**

**`dsolve()`** 用于求解**常微分方程**的符号解。所谓常微分方程，

```matlab
S = dsolve(eqn)
S = dsolve(eqn,cond)
S = dsolve(___,Name,Value)
[y1,...,yN] = dsolve(___)

% 示例：
> syms a b x(t)
>> f = sym(a*diff(x,t)+b*x==0)  % 生成符号表达式
 
f(t) =
	a*diff(x(t), t) + b*x(t) == 0
 
>> dsolve(f)
 
ans =
	C1*exp(-(b*t)/a)
 
>> dsolve(f,'x(0)=1')  % 输入初始条件
 
ans = 
	exp(-(b*t)/a)
```

## 7 多项式

> Matlab 中的**多项式**都是以 “**行向量**”为基础的。

### 7.1 多项式的生成

#### 7.1.1 由系数生成

在 Matlab 中，n 阶多项式![gif.latex?p%28x%29](/images/matlab/gif.latex)由一个长度为 n＋1 的向量 p 所表示，向量 p 的元素为多项式的系数，且按照自变量 x 的降幂顺序排列。

```
p = poly2sym(V)
p = poly2sym(V,var)  % 指定变量为 var instead of x
```

#### 7.1.2 多项式求根

**`r = roots(p)`** r 是多项式 p 的根组成的**列向量**

- **Matlab 规定：多项式是行向量，根是列向量。**
- **几阶多项式就有几个根，解向量就有几个维度。**

#### 7.1.3 由根生成

**`p = poly(A)`**

- 如果 A 为方阵，则多项式 p 为该方阵的特征多项式
- 如果 A 为向量，则 A 的元素为该多项式 p 的根

### 7.2 多项式的运算

#### 7.2.1 多项式的加减运算

加减法：转化成行向量表达，注意采用首 0 形式，系数一一对齐

**`s = conv(a,b)`** 执行 ab 两个向量的卷积运算，即多项式相乘

**`[q,r] = deconv(v,u)`** 多项式 v 除以 u 的商 q 和余数 r

#### 7.2.2 多项式的微积分

**多项式求导**

**`k = polyder(p)`** 行向量 k 是多项式 p 的导函数的系数
**`k = polyder(a,b`)** 求多项式 a 和多项式 b 的乘积的导函数
**`[q,d] = polyder(a,b)`** 求多项式 a 除以多项式 b 整体的导函数，导函数的分子和分母分别放于 q 和 d 中

**多项式积分**

**`q = polyint(p)`** 返回多项式 p 的不定积分，常数默认为 0

**`q = polyint(p,k)`** 返回多项式 p 的不定积分，常数默认为 k

#### 7.2.3 多项式的部分分式展开

**`[r,p,k] = residue(b,a)`**
**`[b,a] = residue(r,p,k)`** 分子行向量 b、分母行向量 a、rpk 分别是留数、极点和多项式

#### 7.2.4 多项式的常见操作

| 函数                     | 功能                                                         |
| ------------------------ | ------------------------------------------------------------ |
| **expand(f)**            | 对符号表达式利用**恒等变形**进行展开，常用于**多项式、三角函数、指数函数和对数函数** |
| **expand(S,Name,Value)** | Name：`ArithmeticOnly` 、`IgnoreAnalyticConstraints`         |
| **collect(f)**           | 按默认变量合并符号表达式的同类项，f 可以是符号矩阵（元素群运算） |
| **collects(f,v)**        | 按变量 v 合并符号表达式的同类项，f 可以是符号矩阵（元素群运算） |
| **factor(f)**            | 对符号表达式进行因式分解，系数从小到大排序                   |
| **horner(f)**            | 将一般的符号表达式转换成嵌套形式的符号表达式                 |

### 7.3 多项式的估值

```matlab
p = [1, 2, 3]  % x ^ 2 + 2 * x + 3、
polyval(p, [3, 7])  % ans = [18 66] 用`polyval`函数来求多项式在某些点处的值
```

```matlab
syms x
p = x ^ 2 + 2 * x + 3;  % p 是个符号类型
%<！哪怕你赋值让`x=1`，变量 p 也仍然是一个符号类型
subs(p, [3, 7])   % ans = [18, 66] 指定符号变量值求表达式的值
```

### 7.4 符号表达式的形式转化

| 函数               | 说明                                               |
| ------------------ | -------------------------------------------------- |
| **sym2poly**       |                                                    |
| **matlabFunction** | 将标量符号表达式函数句柄生成向量符号表达式函数句柄 |
| **poly2str**       |                                                    |
| **poly2sym**       |                                                    |
| **str2sym**        |                                                    |

符号表达式——>矩阵（向量）

```matlab
sym2poly(p)  % ans = [1 2 3]
```

符号表达式——>函数句柄

```matlab
syms x
p = x ^ 2 + 2 * x + 3;
f = matlabFunction(p);  % function_handle 它会自动把点给加上去
f([3, 7])  % ans = [18 66]
```

向量多项式——>多项式字符串

```matlab
poly2str([1,2,3], 'x')  % ans = '   x^2 + 2 x + 3' （注意这里没有带乘号 `*`）
```

向量多项式——>符号表达式（这样就可以转换为函数句柄了）

```matlab
syms x
poly2sym([1,2,3], x)
```

字符串——>符号表达式

```matlab
str2sym('x^2 + 2 * x + 3')
```

> 在 MATLAB 中，可以用来表示多项式的，通常是向量，以 `poly…` 开头的函数多是以向量作为多项式的输入输出的。有时候在计算中也会引入符号表达式，为了当做参数传递和使用方便还会使用函数句柄。当然，多项式还可以用最原始的字符串来表示。

### 7.5 多项式画图

```matlab
a=[9,-5,3,7];
x=-2:0.01:5;
f=polyval(a,x);
plot(x,f,"LineWidth",2);
xlable("x");ylable("f(x)");
set(gca,"FontSize",14)
```

## 8 Simulink 仿真

### 8.1 Simulink 的特性

- 本质上，各种模块就是图形化的微分或者差分方程。
- Simulink 在内部总是采用连续或者离散的状态方程进行描述。

### 8.2 仿真的基本设置

| 设置项      | 简述  | 描述                                                                                                                                       |
| -------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 仿真起止时间   |     |                                                                                                                                          |
| 求解器/求解方法 |     |                                                                                                                                          |
| 绝对容许误差   |     | 如果出现在**零状态附近反复迭代**的情况，则可以**减小绝对容许误差**                                                                                                    |
| 相对容许误差   |     | 1. 可以**减小相对容许误差**一个量级对仿真结果进行**检验**，如果结果相同，则说明系统是**收敛**的 2. 如果**减小绝对容许误差**，**不足**以提高仿真的精度，则可以可以**调小相对容许误差**，强制减小仿真的步长，从而增加仿真的步数，以**提高精度** |
| 最大仿真步长   |     |                                                                                                                                          |

### 8.3 Simulink 的命令行指令

#### 8.3.1 获得状态信息的指令

**`[sys, x0, str, ts] = <model_name>([], [], [], 'sizes');`**

#### 8.3.2 命令行调试指令

>   - simulink 支持在命令行内输入相应指令进行分析
>   - 通过 matlab 命令进行模型的仿真，是用户可以从 m 文件进行仿真，从而可以试试改变模块参数和仿真环境
>   - 也可以让用户**随机改变**参数反复仿真，可以进行**蒙特卡罗分析**

**`sim('<model_name>', 'param1', value1, 'param2', value2, …)`**

**`simset(proj, 'setting1', value1, 'setting2', value2, …)`**

#### 8.3.3 线性化模型的指令

**`dlinmod()`** **指令** ：用于线性化本身式离散系统或者离散和连续的混合系统的模型

```
argout = dlinmod('sys', Ts)
argout = dlinmod('sys', Ts, x, u)
argout = dlinmod('sys', Ts, x, u, para, 'v5')
argout = dlinmod('sys', Ts, x, u, para, xpert, upert, 'v5')
```

**`linmode`** **指令** ：用于线性化本身式线性和非线性的模型

```
argout = linmod('sys');
argout = linmod('sys', x, u);
argout = linmod('sys', x, u, para);
argout = linmod('sys', x, u, 'v5');
argout = linmod('sys', x, u, para, 'v5');
argout = linmod('sys', x, u, para, xpert, upert, 'v5');
```

## 9 Simulink Multibody 仿真

### 9.1 参考资料

| 资料源                                                                                                       | 备注         |
| --------------------------------------------------------------------------------------------------------- | ---------- |
| [Simscape Multibody Solid和Rigid Transform模块说明 说明 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/87595587) | 便于自定义质心的位置 |

### 9.2 控制理论

#### 9.2.1 传递函数的表达

```matlab
%方法1:定义算子，直接表达法
s = tf('s');        %定义s算子
G1 = 1/((s-1)*(s-7));

%方法2：有理多项式表达法
num = [1,2,3,4];
den = [5,6,7,8];
G2 = tf(num,den);

%方法3：零极点增益表达法
Z = [1,2];
P = [3,4];
K = 6;
G3 = zpk(Z,P,K);
```

#### 9.2.2 传递函数的属性

```matlab
% G1.num{1,1} % 获取第一路输入和第一路输出之间的传递函数
% G1.den{1,1}
% G1.IODelay = 2;

% 传递函数 tf 对象的全部属性
get(tf)
```

#### 9.2.3 传递函数的化简

```matlab
G1 * G2						% 串联
G1 + G2						% 并联
% 反馈
sys1 = feedback(G1,G2)     	% 负反馈
sys2 = feedback(G1,G2,1)   	% 正反馈
```

#### 9.2.4 传递函数的形式转换

```matlab
s = tf('s');
G2 = 1/((s-1)*(s+1));       % 定义有理分式传递函数

% 有理多项式 to 零极点增益
[z,p,k] = tf2zp(G2.num{1},G2.den{1});
tt = zpk(z,p,k)
pzmap(tt)

% 零极点增益 to 状态空间
[a,b,c,d] = zp2ss(z,p,k)

% 零极点增益 to 有理多项式
[num,den] = zp2tf(z,p,k);
tf(num,den)

% 传递函数 to 符号表达式转换
Z = [1,2];
P = [3,4];
K = 6;
G_zpk = zpk(Z,P,K);
G_sym1 = tf_t0_sym(G_zpk);
ilaplace(G_sym)

function tf_G1=sym_t0_tf(G1)
    %符号函数转换为传递函数形式
    [num,den]=numden(G1);%提取符号表达式分子和分母
    Num=sym2poly(num);%返回多项式项式系数
    Den=sym2poly(den);
    tf_G1 = tf(Num,Den); 
end

function sym_G1=tf_t0_sym(G1)
    %传递函数转换为符号函数形式
    syms s
    [num,den]=tfdata(G1);
    Num=poly2sym(num,s);%把系数系数转换为多项式
    Den=poly2sym(den,s);%
    sym_G1=Num/Den; 
end
```

#### 9.2.5 求极点

```matlab
roots(G2.den{1,1})  % 求特征多项式的根
eig(G2)     % 给eig输入传递函数对象时，
            % 会自动转换成状态空间表达，
            % 其中A的特征值就是传递函数的极点
```

#### 9.2.6 求稳态值

```matlab
[y,t] = step(G2);
y(end)
```

#### 9.2.7 求超调量

```matlab
(max(y)-2)/2
```

#### 9.2.8 部分分式展开

```matlab
[r, p, k] = residue(G1.num{1,1},G1.den{1,1}) %{其中r是分式系数，p是极点，k是常项%}
```

#### 9.2.9 积分变换

```matlab
clear
syms s;
G2 = 1/((s-1)*(s+1)); 

%拉氏变换
ilaplace(G2)

%傅氏变换
% ifourier(1/s)

syms x
f = exp(-2*x^2); % our function
fplot(f,[-2,2])  % plot of our function
FT = fourier(f)  % Fourier transform

%Z变换
ztrans(f)
```

#### 9.2.10 常见信号的时域表达

```matlab
syms t;
%冲激信号
d = dirac(t);

%阶跃信号
e = heaviside(t);

%三角波
% t = 0:0.001:8;
% u1 = 0:0.01:2;
% u2 = 2-0.001:-0.01:-2;
% u3 = -1.99:0.01:0;
% u = [u1,u2,u3];
% plot(t,u)
```

#### 9.2.11 常见系统响应

```matlab
s = tf('s');
G = (4-s)/(s^2 + 2*s + 5);
u = s/(s^3 + 3);

% 冲激响应
impulse(G);
grid on;

% 阶跃响应
step(G);
grid on;

% 时域响应
t = 0:0.04:8;  % 201 points
u = max(0,min(t-1,1))
lsim(G,u,t,1);
grid on;
```

#### 9.2.12 系统特性图

```matlab
Z = [1,2];
P = [3,4];
K = 6;
G = zpk(Z,P,K);
% 零极点图
pzmap(G);

[Gm,Pm,Wg,Wp] = margin(G)  %裕度 [ 幅值裕度，相位裕度， ]

% 根轨迹
rlocus(G)

%{
	matlab 图形化界面 分析线性时不变系统
	在命令行中输入
	导入工作空间中的传递函数
}%

ltiview()

% 控制系统的设计工具箱
sisotool()

s = tf('s');
G = 1/(s^2 + 2*s + 5);

% 奈奎斯特图 和 奈奎斯特定理
nyquist(G)  % 传递函数的实部和虚部作为横纵坐标的图
grid

% 伯德图
bode(G)  % 传递函数的模和 相角，分别作角频率的函数
grid on
```

#### 9.2.13 状态空间表达

| 函数         | 说明      |
| ---------- | ------- |
| ctrb(A, B) | 得到可控性矩阵 |
| obsv(A,C)  | 得到可观性矩阵 |
|            |         |

## 10 绘图

### 10.1 绘制折线图

点集 $(X, Y)$ 中，$\boldsymbol{X}=[x_1 \; x_2 \; … \; x_n]$，$\boldsymbol{Y}=[y_1 \; y_2 \; … \; y_n]$

`plot(X, Y)` 绘制以 $\boldsymbol{X}$ 为横坐标，$\boldsymbol{Y}$ 为纵坐标的一条曲线，曲线上含有 n 个点

`plot(Y)` 绘制以 `1: n` 为横坐标，$\boldsymbol{Y}$ 为纵坐标的一条曲线，曲线上含有 n 个点

`plot(Z)` 其中 $Z=X+Yi$ 绘制以 $\boldsymbol{X}$ 为横坐标，$\boldsymbol{Y}$ 为纵坐标的一条曲线，曲线上含有 n 个点，可用于绘制参数方程曲线

`plot(x1, y1, str1, x2, y2, str2, …)` 绘制多条曲线，并且分别根据 str 字符串修改曲线样式

假设矩阵 $\boldsymbol{A}=[\boldsymbol{V}_1 \; \boldsymbol{V}_2 … \boldsymbol{V}_n \;]$ 其中，$\boldsymbol{V}_n=[\boldsymbol{v}_1 \; \boldsymbol{v}_2 … \boldsymbol{v}_n]^T$

`plot(A)` 绘制以 `1: n` 为横坐标，纵坐标为 $\boldsymbol{V}_n$ 的 n 条曲线

`plot(X, A)` 绘制以 $\boldsymbol{X}$ 为横坐标，$\boldsymbol{A}_{m\times n}$ 的各列向量元素为纵坐标的 n 条曲线，曲线上含有 m 个点

### 10.2 函数的绘制

上节所用的 plot() 函数只是将用户指定或计算得到的数据转化为图形。实际绘制函数时，函数随着自变量的变化趋势往往是未知的如果 plot() 指令的自变量间距选取不合适，那么曲线反应的函数图像将失真。于是本节引入 fplot() 指令，该指令可以自适应步长来绘制函数图像。函数的基本用法如下：

`fplot(fun, limits, …)` 绘制定义域为 `limits=[xmin, xmax, ymim, ymax]` 范围的函数图像

同时，还有另外一个用法相近的函数，它可以使用字符串的形式直接输入函数，使用更加方便。

`ezplot('sin(x)')` 直接绘制 sin(x) 函数

`ezplot(f(x,y))` 直接绘制隐函数 `f(x,y)=0` 。例如：`syms x y` `ezplot('x^3+y^3-3*x*y')`

### 10.3 特殊图形绘制

#### 10.3.1 绘制箭头

二维图

```
quiver(X,Y,U,V)
quiver(U,V)
quiver(___,scale)
quiver(___,LineSpec)
quiver(___,LineSpec,'filled')
quiver(___,Name,Value)
quiver(ax,___)
q = quiver(___)
```

三维图

```
quiver3(X,Y,Z,U,V,W)
quiver3(Z,U,V,W)
quiver3(___,scale)
quiver3(___,LineSpec)
quiver3(___,LineSpec,'filled')
quiver3(___,Name,Value)
quiver3(ax,___)
q = quiver3(___)
```

### 10.4 坐标轴操作

| 命令                        | 含义                                                         | 命令        | 含义                                           |
| --------------------------- | ------------------------------------------------------------ | ----------- | ---------------------------------------------- |
| axis auto                   | 使用默认设置                                                 | axis equal  | 纵、横轴采用等长刻度                           |
| axis manual                 | 使当前坐标范围不变                                           | axis fill   | 在 manual 方式下起作用，使坐标充满整个绘图区     |
| axis off                    | 取消轴背景                                                   | axis image  | 纵、横轴采用等长刻度，且坐标框紧贴数据范围     |
| axis on                     | 使用轴背景                                                   | axis normal | 默认矩形坐标系                                 |
| axis ij                     | 矩阵式坐标，原点在左上方                                     | axis square | 产生正方形坐标系                               |
| axis xy                     | 普通直角坐标，原点在左下方                                   | axis tight  | 把数据范围直接设为坐标范围                     |
| axis([xmin,xmax,ymin,ymax]) | 设定坐标范围，必须满足 xmin<xmax,ymin<ymax，可以取 inf 或 -inf。 | axis vis3d  | 保持高宽比不变，用于三维旋转时避免图形大小变化 |

### 10.5 空间解析几何

#### 10.5.1 点到两点直线的垂足

[三维空间：点到直线垂足坐标公式推导_三维空间c++已知两点坐标,求第三点到这两点直线的垂点坐标csdn-CSDN博客](https://blog.csdn.net/qq_32867925/article/details/114294753)

$$
\begin{array}{l}
A(x_{1}，y_{1}， z_{1}) \\
B(x_{2}， y_{2}， z_{2}) \\
P(x_{0}，y_{0}，z_{0}) \\
N(x_{n}， y_{n}， z_{n}) \\
\because \left\{\begin{array}{l}
AB \parallel AN \\
AB \perp PN
\end{array}\right. \\
\therefore \left\{\begin{array}{l}
B-A = k(N-A) --------(1)\\
(B-A) \cdot (N-P) = 0-------(2)
\end{array}\right. \\


\end{array}
$$

## 11 机器人工具箱

### 11.1 学习资料

[Matlab机器人工具箱（0）——旋转与平移变换_JY.G的博客-CSDN博客](https://blog.csdn.net/weixin_43502392/article/details/105468060)

[Matlab机器人工具箱（1）——机器人的建立、绘制与正逆运动学_JY.G的博客-CSDN博客](https://blog.csdn.net/weixin_43502392/article/details/105447785#comments_23269353)

[Matlab机器人工具箱（2）——预分析（可达空间与可操作性的可视化）_JY.G的博客-CSDN博客](https://blog.csdn.net/weixin_43502392/article/details/105551427)

[Matlab机器人工具箱（3）——轨迹规划_JY.G的博客-CSDN博客_matlab多点轨迹规划](https://blog.csdn.net/weixin_43502392/article/details/105634856)

[Matlab机器人工具箱（番外篇）———机器人建立的任意方法_JY.G的博客-CSDN博客](https://blog.csdn.net/weixin_43502392/article/details/105654578)

[机器人RPY角和Euler角 -- 基本公式_lyhbkz的博客-CSDN博客_rpy角](https://blog.csdn.net/lyhbkz/article/details/83542248)

[MATLAB机器人工具箱中机器人逆解是如何求出来的？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/41673569?sort=created)

[ MATLAB Robotics System Toolbox学习笔记（一）：一步一步建造一个机械臂_Wilson Huang（三点羊羽）的博客-CSDN博客_setfixedtransform](https://blog.csdn.net/weixin_43229030/article/details/108928529?spm=1001.2014.3001.5502)

[MATLAB Robotics System Toolbox学习笔记（二）：机器人学数学基础_Wilson Huang（三点羊羽）的博客-CSDN博客](https://blog.csdn.net/weixin_43229030/article/details/112726054?spm=1001.2014.3001.5502)

[创建一个urdf机器人_Robotics System Toolbox学习笔记（一）：简单建立一个机器人_找寻生命的意义的博客-CSDN博客](https://blog.csdn.net/weixin_36195837/article/details/112180209?spm=1001.2101.3001.6650.4&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~Rate-4-112180209-blog-108928529.pc_relevant_3mothn_strategy_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~Rate-4-112180209-blog-108928529.pc_relevant_3mothn_strategy_recovery&utm_relevant_index=9)

### 11.2 工具箱安装

作者的网站：

<http://petercorke.com/wordpress/resources/downloads>

工具箱网页：

[Robotics Toolbox - Peter Corke](https://petercorke.com/toolboxes/robotics-toolbox/)

### 11.3 位姿变换

| 函数                                                    | 功能                                          | 备注                          |
| ----------------------------------------------------- | ------------------------------------------- | --------------------------- |
| Rx = rotx(theta)、Ry = roty(theta)、Rz = rotz(theta)    | **生成**绕坐标轴旋转 theta 弧度的旋转矩阵                  |                             |
| Rx = trotx(theta)、Ry = troty(theta)、Rz = trotz(theta) | **生成**绕坐标轴旋转 theta 弧度的**纯旋转的齐次变换矩阵**        |                             |
| TR = rt2tr(R, p)                                      | **生成**完整的**齐次变换矩阵**                         |                             |
| R=t2r(T)                                              | **提取**齐次变换的**旋转矩阵**                         |                             |
| T = transl(p)                                         | **生成**沿向量 p 平移的**纯平移的齐次变换矩阵**               |                             |
| p = transl(T)                                         | **提取**齐次变换的**平移向量**                         |                             |
| [x,y,z] = transl(T)                                   | **提取**齐次变换**平移向量的分量**                       |                             |
| trplot(R or T)                                        | 将坐标变换的结果**图形化**显示                           |                             |
| tranimate(R or T)                                     | 将坐标变换的过程**动画化**显示                           | 只有在独立窗口才有效，且一次性             |
| tranimate(q.R,'movie','quat.gif');                    | 生成动画文件                                      | 输出 mp4 格式的视频，把.gif 后缀改成.MP4 |
| view([theta alpha])                                   | 将**摄像头**以正对图像笛卡尔坐标 XoZ 平面，右转 theta，上转 alpha | 放在画图函数前面                    |

### 11.4 姿态表示

```matlab
% 欧拉角 <--> 旋转矩阵
R1 = rotz(pi/3) * roty(pi/4) * rotx(pi/6);
R1 = rpy2r(pi/3,pi/4,pi/6,'zyx'); % 该函数默认的是XYZ, 应在后面的选项添加zyx,指定为ZYX顺序。

R = rpy2r(30, 40, 50, 'xyz', 'deg');
Rr = tr2rpy(R, 'xyz') .* (180/pi);
```

```matlab
R2 = eul2r(90,90,90)
EA = tr2eul(R2) .*(180/pi); % 输出1 × 3的矩阵，输出为弧度值
```

### 11.5 刚体模型搭建

| 函数                                                                                                                                      | 功能简介                                               |
| --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [`rigidBody`](https://www.mathworks.com/help/releases/R2021b/robotics/ref/rigidbody.html?doclanguage=zh-CN&nocookie=true&prodfilter=ML) |                                                    |
| [`addBody`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.addbody.html)                                     | Add body to robot                                  |
| [`addSubtree`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.addsubtree.html)                               | Add subtree to robot                               |
| [`centerOfMass`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.centerofmass.html)                           | Center of mass position and Jacobian               |
| [`copy`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.copy.html)                                           | Copy robot model                                   |
| [`externalForce`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.externalforce.html)                         | Compose external force matrix relative to base     |
| [`forwardDynamics`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.forwarddynamics.html)                     | Joint accelerations given joint torques and states |
| [`geometricJacobian`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.geometricjacobian.html)                 | Geometric Jacobian for robot configuration         |
| [`gravityTorque`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.gravitytorque.html)                         | Joint torques that compensate gravity              |
| [`getBody`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.getbody.html)                                     | Get robot body handle by name                      |
| [`getTransform`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.gettransform.html)                           | Get transform between body frames                  |
| [`homeConfiguration`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.homeconfiguration.html)                 | Get home configuration of robot                    |
| [`inverseDynamics`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.inversedynamics.html)                     | Required joint torques for given motion            |
| [`massMatrix`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.massmatrix.html)                               | Joint-space mass matrix                            |
| [`randomConfiguration`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.randomconfiguration.html)             | Generate random configuration of robot             |
| [`removeBody`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.removebody.html)                               | Remove body from robot                             |
| [`replaceBody`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.replacebody.html)                             | Replace body on robot                              |
| [`replaceJoint`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.replacejoint.html)                           | Replace joint on body                              |
| [`show`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.show.html)                                           | Show robot model in a figure                       |
| [`showdetails`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.showdetails.html)                             | Show details of robot model                        |
| [`subtree`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.subtree.html)                                     | Create subtree from robot model                    |
| [`velocityProduct`](https://www.mathworks.com/help/releases/R2020a/robotics/ref/rigidbodytree.velocityproduct.html)                     | Joint torques that cancel velocity-induced forces  |

### 11.6 动力学仿真

[MATLAB 机器人工具箱【3】—— 动力学相关函数及用法 _ 黄小白的进阶之路的博客 -CSDN 博客](<https://blog.csdn.net/huangjunsheng123/article/details/110749830?ops_request_misc=%7B%22request%5Fid%22%3A%22166885538316800186583930%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=166885538316800186583930&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2>~all~sobaiduend~default-2-110749830-null-null.142^v65^control,201^v3^add_ask,213^v2^t3_control1&utm_term=matlab 机器人工具箱 动力学&spm=1018.2226.3001.4187)

[Matlab 机器人工具箱——动力学 _queensyb 的博客 -CSDN 博客](<https://blog.csdn.net/queensyb/article/details/106100456?ops_request_misc=%7B%22request%5Fid%22%3A%22166885538316800186583930%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=166885538316800186583930&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2>~all~sobaiduend~default-1-106100456-null-null.142^v65^control,201^v3^add_ask,213^v2^t3_control1&utm_term=matlab 机器人工具箱 动力学&spm=1018.2226.3001.4187)

[MATLAB机器人工具箱（四）动力学_小磊在路上的博客-CSDN博客](https://blog.csdn.net/weixin_43365751/article/details/100707493)

[Matlab 机器人工具箱（Robotics Toolbox）学习笔记 _Mist_Orz 的博客 -CSDN 博客 _ 机器人工具箱](<https://blog.csdn.net/ooorczgc/article/details/125110656?ops_request_misc=%7B%22request%5Fid%22%3A%22166885538316800186535708%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=166885538316800186535708&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2>~all~first_rank_ecpm_v1~rank_v31_ecpm-5-125110656-null-null.142^v65^control,201^v3^add_ask,213^v2^t3_control1&utm_term=matlab 机器人工具箱 动力学&spm=1018.2226.3001.4187)

[机器人动力学 - 机器人学中的惯性矩阵坐标转换及在SolidWorks中的测量_罗伯特祥的博客-CSDN博客](https://blog.csdn.net/weixin_43455581/article/details/103579030)

[Matlab 机器人工具箱（3-3）：五自由度机械臂（动力学）_ 冰激凌啊的博客 -CSDN 博客](<https://blog.csdn.net/gyxx1998/article/details/106416224/?ops_request_misc=&request_id=&biz_id=102&utm_term=matlab> 机器人工具箱 动力学&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-2-106416224.142^v65^control,201^v3^add_ask,213^v2^t3_control1&spm=1018.2226.3001.4187)

### 11.7 六轴机械臂的仿真实例

[基于MATLAB的关节型六轴机械臂轨迹规划仿真（2021实测完整代码）_关节空间轨迹规划仿真_mustvvvics的博客-CSDN博客](https://blog.csdn.net/mustvvvics/article/details/117025390)

## 12 代码生成

### 12.1 相关资料

| 资源                                                                                                                                                                                                                | 备注    |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| [使用 MATLAB Coder 生成 C 代码 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/coder/gs/generating-c-code-from-matlab-code-using-the-matlab-coder-project-interface_zh_CN.html)                       |       |
| [利用硬件加速大规模科学计算 \| 从MATLAB到C/C++代码 - MATLAB & Simulink (mathworks.cn)](https://ww2.mathworks.cn/company/technical-articles/speed-up-large-scale-scientific-computation-with-hardware-from-matlab-to-c-c-code.html) |       |
| [详细步骤讲解matlab代码通过Coder编译为c++并用vs2019调用_vs调用matlab程序-CSDN博客](https://blog.csdn.net/qingfengxd1/article/details/127993939)                                                                                          |       |
| [利用Matlab Coder 将matlab文件转化为c++文件导入到相应项目中_matlab转c++代码-CSDN博客](https://blog.csdn.net/doudou2weiwei/article/details/131291656)                                                                                     |       |
| [将 MATLAB 类型映射到生成的代码中的类型 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/coder/ug/mapping-matlab-types-to-cc-types.html)                                                                        | 类型映射  |
| [在生成代码中命名 C 结构体类型 - MATLAB coder.cstructname - MathWorks 中国](https://ww2.mathworks.cn/help/coder/ref/coder.cstructname_zh_CN.html#d126e7285)                                                                      | 生成结构体 |

### 12.2 M 程序书写优化

1. 入参多的情况下，一定要建一个类把入参都合并在一起，转成 C 的时候会转成一个结构体。
2. 结构体变量啥的，都要提前赋值好大小。如果不赋值大小，MATLAB 能运行，转 C 的时候就一顿报错。
3. MATLAB 中有很多已有的工具箱，都支持转 C 代码

### 12.3 转换成 c++ 的类的 M 程序书写技巧

### 12.4 转换成 c++ 的函数有结构体的书写技巧

## 13 系统辨识

这个例子的数据是一个对一个惯性系统给定一个阶跃输入，对系统的输出进行采集，并辨别这个系统。

(xdata,ydata) 是一个一阶系统阶跃响应的采集数据,ydata 是输出值，xdata 是时间戳。由于系统是阶跃响应，我们假定系统的传递函数是 $\frac{K}{T_ps+1}$

显然需要辨别的两个参数是 $K$ 和 $T_p$ 。

该系统在阶跃响应输入下的始于表达式为 $c(t)=K(1-e^{-\frac{t}{T_p}})$

因此需要建立的函数 fun 如下

~~~matlab
fun=@(xdata,ydata)(x(1)*(1-exp(-xdata/x(2))))
~~~

是一个指定参数的函数，我们需要求解的参数就是 x(1) 和 x(2)，其中 x 返回值是一个二元参数向量，可直接调用 fun 函数求得 y 根据时间戳生成的辨识系统的计算值。并与实验值 ydata 画在一张图进行比较。

~~~matlab
clc
close all
plot(xdata,ydata);xlim([0,1]);hold on;%实际曲线绘图
fun=@(x,xdata)(x(1)*(1-exp(-xdata/x(2))));%估计函数
x0=[1500,0.025];%初始估计值[x(1),x(2)]
x=lsqcurvefit(fun,x0,xdata,ydata);%非线性函数拟合
y=fun(x,xdata);%代入估计的值，并获得函数点
plot(xdata,y);xlim([0,1]);%绘制估计曲线
title(['[K,Tp]=',num2str(x)]);%标注估计的参数
~~~

绘制的预估曲线如下：(蓝色的是实验数据，红色的是拟合曲线)

![image-20211223001848044](/images/matlab/image-20211223001848044.png)

可以发现，如果沿着实验曲线的大致趋势，拟合的指数逼近曲线如红色线所示，可见辨识的参数较为准确。

## 14 相关参考资料

### 14.1 Matlab 特性

#### 14.1.1 符号计算

[MATLAB 中多项式 那些奇奇怪怪的表示方法 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/99979970)

[【Matlab】符号计算_不牌不改的博客-CSDN博客_matlab符号计算是什么](https://blog.csdn.net/weixin_46221946/article/details/125243060)

[Matlab 符号计算与方程组求解 _ 知行流浪的博客 -CSDN 博客 _vpasolve 用法](<https://blog.csdn.net/zengxiantao1994/article/details/77943305?ops_request_misc=%7B%22request%5Fid%22%3A%22166634935916782425152995%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fblog.%22%7D&request_id=166634935916782425152995&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2>~blog~first_rank_ecpm_v1~rank_v31_ecpm-2-77943305-null-null.nonecase&utm_term=matlab 符号计算 代入方程求解&spm=1018.2226.3001.4450)

#### 14.1.2 代数环和过零检测

[MATLAB Simulink 中的过零检测与代数环_Wilson Huang的博客-CSDN博客_simulink过零检测怎么设置](https://blog.csdn.net/weixin_43229030/article/details/110499075?ops_request_misc=%7B%22request%5Fid%22%3A%22164018624416780274166304%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=164018624416780274166304&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-110499075.first_rank_v2_pc_rank_v29&utm_term=simulink+enable+zero-crossing+detect&spm=1018.2226.3001.4449)

#### 14.1.3 Matlab 方程求解

[matlab 将求解 sin 隐式解,Matlab 隐式符号方程求解和赋值 _ 贺定圆的博客 -CSDN 博客](<https://blog.csdn.net/weixin_35915828/article/details/115890404?ops_request_misc=%7B%22request%5Fid%22%3A%22166634935916782425152995%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fblog.%22%7D&request_id=166634935916782425152995&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2>~blog~first_rank_ecpm_v1~rank_v31_ecpm-11-115890404-null-null.nonecase&utm_term=matlab 符号计算 代入方程求解&spm=1018.2226.3001.4450)

[基于 MATLAB 的隐函数偏导与多重积分（附代码）_ 唠嗑！的博客 -CSDN 博客 _matlab 隐函数求导](<https://blog.csdn.net/forest_LL/article/details/124572228?ops_request_misc=%7B%22request%5Fid%22%3A%22166645757016800184198413%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=166645757016800184198413&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2>~all~sobaiduend~default-2-124572228-null-null.142^v59^control,201^v3^control_2&utm_term=matlab 隐函数求导&spm=1018.2226.3001.4187)

[MATLAB 求二阶隐函数导数,如何用 matlab 对隐函数求导？ 值得收藏 _ 海滨小子 001 的博客 -CSDN 博客](<https://blog.csdn.net/weixin_34157892/article/details/115813613?ops_request_misc=&request_id=&biz_id=102&utm_term=matlab> 隐函数求导&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-115813613.142^v59^control,201^v3^control_2&spm=1018.2226.3001.4187)

#### 14.1.4 Simulink 仿真

[Matlab仿真PID控制（带M文件、simulink截图和参数分析）_体会编程语言独到的美-CSDN博客_matlab pid仿真](https://blog.csdn.net/weixin_44044411/article/details/85891109?ops_request_misc=%7B%22request%5Fid%22%3A%22164018870716780274128736%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fblog.%22%7D&request_id=164018870716780274128736&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-5-85891109.nonecase&utm_term=simulink+导出系统传递函数&spm=1018.2226.3001.4450)

[Matlab对指定参数的曲线进行非线性拟合_体会编程语言独到的美-CSDN博客_matlab参数拟合](https://blog.csdn.net/weixin_44044411/article/details/85636950)

#### 14.1.5 数学基础

## 15 临时

### 15.1 非线性系统线性化的程序

~~~matlab
function z=EquilibriumLinearization()
%{
	date:2020.08.21
    程序功能：对非线性系统线性化，获取系统矩阵A
%}
global N
    N=3;  %状态变量数目
    x=sym('x',[1,N]);  
    xe=[0,0,0];  %平衡点给定
    
    
    z=jacobian(x)
    z=subs(z ,x, xe);
end


%jacobian线性化矩阵
function z=jacobian(x)
    global N
    y=system(x);
    for j=1:N
        
        for k=1:N
            z(j, k)=diff(y(j),x(k));
            
        end
    end

end

%系统描述
function y=system(x)
    
    y(1)=x(2);
    y(2)=-cos(x(1))+sin(x(2));
    y(3)=exp(x(1)+x(3));
    
    
end
~~~

#publish
