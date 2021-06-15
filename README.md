# 축구선수의 몸값 회귀분석 (송강, 이승주)
---
## < 팀 구성 >
---
1. 송강
  - whoscored.com 데이터 크롤링
  - 골키퍼, 수비수에 대한 회귀분석
  - 전처리 및 모델링
3. 이승주
  - transfermkt.com 데이터 크롤링
  - 공격수, 미드필더에 대한 회귀분석
  - 전처리 및 모델링

## < 목표 >
---
> ## 1. 분석의 목적
  평소 흥미가 있는 주제인 축구라는 분야에서 축구선수에게 책정된 몸값이 어떠한 과정을 거쳐 정해지는지 검증하는 것

> ## 2. 가설 수립
    1) 전체 데이터에 대해 선수 개인의 득점, 패스성공률, 수비성공률, 키패스 횟수 등을 분석하면 몸값과의 선형적 관계를 도출해낼 수 있을것이라 예상
    2) 포지션별로 공격수는 득점횟수, 경기당 슈팅 횟수, 드리블돌파 횟수가, 미드필더는 패스성공률 키패스 횟수가, 수비수는 공을 걷어낸 횟수, 태클 횟수가 몸값에 양의 상관관계를 가질 것이라 예상
    3) 개인의 우승횟수나 수상횟수가 스텟보다 더 큰 영향을 미칠 것이라 예상

> ## 3. 분석지표
    - source site 1: https://www.transfermarkt.com/
    - source site 2: https://www.whoscored.com/

## <결론>
---
- 선수들의 통계치를 나타낸 데이터는 몸값과 뚜렷한 선형적 관계를 가지지 않음.
- 포지션별 세분화된 데이터에서도 유의미한 예측은 어려움.
- 개인 수상 커리어 또한 몸값에 큰 영향을 미치지 않음.

> ### 1. 데이터 전처리 설명

실제로 가져올 수 있고 다룰 수 있는 수준의 데이터를 유럽 5대리그(스페인,영국,프랑스,이탈리아,독일)로 설정했습니다.  
또한 whoscored.com과 transfermarkt.com에 올라와 있는 선수데이터가 약간 상이한 부분이 있어 소속팀과 선수이름으로 merge하여  
약 2000명의 선수 데이터셋을 구성했습니다.
#### 수집된 데이터에 골키퍼 관련 데이터의 양이 극히 적어 모델링에서 제외했습니다

<img width="974" alt="스크린샷 2021-06-14 오후 7 30 23" src="https://user-images.githubusercontent.com/53620138/121878706-fd89bf80-cd46-11eb-9bea-add61ca6a9ee.png">
그 중 600명의 공격수 데이터
<img width="1004" alt="스크린샷 2021-06-14 오후 7 37 59" src="https://user-images.githubusercontent.com/53620138/121879637-0e870080-cd48-11eb-94a7-4cd68ebdbfbe.png">

---

> 공격수 포지션의 market_value와 다른 컬럼들간의 상관관계 히트맵

![다운로드 (1)](https://user-images.githubusercontent.com/53620138/121879925-5dcd3100-cd48-11eb-9460-096e77935fec.png)

>  Nike, adidas, Puma 외의 class들을 others로 grouping  
  
  <img width="1009" alt="스크린샷 2021-06-14 오후 7 41 27" src="https://user-images.githubusercontent.com/53620138/121880064-881eee80-cd48-11eb-81b4-c4689332a696.png">

> foot, position, outfitter 의 분포와 boxplot

 <img width="997" alt="스크린샷 2021-06-14 오후 7 47 00" src="https://user-images.githubusercontent.com/53620138/121880720-4e021c80-cd49-11eb-9a01-6595e9dfb457.png">
<img width="1015" alt="스크린샷 2021-06-14 오후 7 47 50" src="https://user-images.githubusercontent.com/53620138/121880832-71c56280-cd49-11eb-9904-2f2a0887b07b.png">


> ### 2. 데이터 모델링 설명
#### 1. 초기모델
    - 범주형 : 더미변수화
    - 수치형 : 전처리만 진행
    - 종속변수 : original
<img width="1081" alt="스크린샷 2021-06-15 오후 5 08 39" src="https://user-images.githubusercontent.com/53620138/122016813-56fff600-cdfc-11eb-8964-5b5737caa272.png">

#### 2. Standard, MinMax, Robust 모델 비교
    - 범주형 : 더미변수화
    - 수치형 : 각 스케일러 적용
    - 종속변수 : original
<img width="1086" alt="스크린샷 2021-06-15 오후 5 05 21" src="https://user-images.githubusercontent.com/53620138/122016291-e22cbc00-cdfb-11eb-8b5f-840ee89d2e1d.png">

#### 3. 종속변수에 log scaling을 진행한 모델
    - 범주형 : 더미변수화
    - 수치형 : Standard Scaler
    - 종속변수 : log1p Scaler
<img width="1095" alt="스크린샷 2021-06-15 오후 5 08 51" src="https://user-images.githubusercontent.com/53620138/122016864-654e1200-cdfc-11eb-8100-9357e64f31e3.png">

#### 4. RandomForest Regessor Model, GridSearchCV를 통한 best hyper parameter 추출
    - model : RandomForest Regressor
    - 범주형 : 더미변수화
    - 수치형 : Standard Scaler
    - 종속변수 : log1p Scaler
<img width="1093" alt="스크린샷 2021-06-15 오후 5 07 26" src="https://user-images.githubusercontent.com/53620138/122016640-2f109280-cdfc-11eb-80d2-f5c4de40e0fd.png">

#### 6. Pipeline을 이용한 Model 생성
    - ploynomialFeatures을 이용한 다향회귀 진행 : 삼차항
    - pipeline : PolynomialFeatures > StandardScaler > RandomForestRegressor
    - 범주형 : 더미변수화
    - 수치형 : Standard Scaler
    - 종속변수 : log1p Scaler
<img width="1092" alt="스크린샷 2021-06-15 오후 5 10 17" src="https://user-images.githubusercontent.com/53620138/122017107-a34b3600-cdfc-11eb-9d3c-229cf6ff9c9c.png">
<img width="1090" alt="스크린샷 2021-06-15 오후 5 10 41" src="https://user-images.githubusercontent.com/53620138/122017168-b231e880-cdfc-11eb-89b4-a2e0901f74bf.png">


#### 7. 최종 모델 선정 및 OLS객체를 통한 통계분석
    - model : LinearRegression
    - 범주형 : 더미변수화
    - 수치형 : Standard Scaler
    - 종속변수 : log1p Scaler
    
```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:           market_value   R-squared:                       0.686
Model:                            OLS   Adj. R-squared:                  0.661
Method:                 Least Squares   F-statistic:                     27.84
Date:                Fri, 11 Jun 2021   Prob (F-statistic):          3.54e-113
Time:                        19:52:54   Log-Likelihood:                -687.61
No. Observations:                 606   AIC:                             1465.
Df Residuals:                     561   BIC:                             1664.
Df Model:                          44                                         
Covariance Type:            nonrobust                                         
===========================================================================================
                              coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------------
const                      15.5159      0.032    488.334      0.000      15.453      15.578
app                         0.1653      0.043      3.815      0.000       0.080       0.250
conceded_goals             -0.2149      0.103     -2.089      0.037      -0.417      -0.013
clean_sheets                0.1489      0.100      1.496      0.135      -0.047       0.344
yellow_card                -0.0699      0.040     -1.768      0.078      -0.147       0.008
second_yell                 0.0241      0.029      0.829      0.408      -0.033       0.081
red_card                    0.0046      0.025      0.187      0.852      -0.044       0.053
age                        -0.3141      0.041     -7.598      0.000      -0.395      -0.233
height                      0.0339      0.043      0.782      0.435      -0.051       0.119
club                        0.3080      0.045      6.826      0.000       0.219       0.397
cup                         0.1381      0.040      3.422      0.001       0.059       0.217
Tackles                     0.0452      0.054      0.833      0.405      -0.061       0.152
Inter                       0.0721      0.049      1.483      0.139      -0.023       0.168
Fouls                      -0.0374      0.050     -0.751      0.453      -0.135       0.060
Offsides                   -0.0511      0.035     -1.464      0.144      -0.120       0.017
Clear                      -0.0061      0.049     -0.124      0.901      -0.102       0.090
Drbed                      -0.0367      0.049     -0.746      0.456      -0.133       0.060
Blocks                      0.0190      0.038      0.502      0.616      -0.055       0.093
OwnG                        0.0370      0.033      1.120      0.263      -0.028       0.102
Rating                     -0.0352      0.215     -0.164      0.870      -0.458       0.387
Goals                       0.3277      0.146      2.238      0.026       0.040       0.615
Assists                    -0.0582      0.100     -0.582      0.561      -0.255       0.138
SpG                         0.3945      0.076      5.159      0.000       0.244       0.545
Fouled                     -0.0258      0.050     -0.518      0.605      -0.124       0.072
Off                         0.0689      0.043      1.603      0.110      -0.016       0.153
Disp                        0.0204      0.058      0.349      0.727      -0.094       0.135
UnsTch                      0.0459      0.064      0.717      0.474      -0.080       0.172
Drb                         0.0816      0.089      0.912      0.362      -0.094       0.257
KeyP                        0.0173      0.091      0.191      0.849      -0.161       0.196
AvgP                        0.1574      0.091      1.730      0.084      -0.021       0.336
PS                          0.1246      0.044      2.850      0.005       0.039       0.210
Crosses                     0.0553      0.061      0.907      0.365      -0.065       0.175
LongB                      -0.0528      0.057     -0.926      0.355      -0.165       0.059
ThrB                        0.0361      0.041      0.890      0.374      -0.044       0.116
AerialsWon                  0.0153      0.069      0.222      0.824      -0.120       0.151
MotM                       -0.1467      0.061     -2.415      0.016      -0.266      -0.027
period                      0.2746      0.037      7.460      0.000       0.202       0.347
total_out                   0.0174      0.017      1.020      0.308      -0.016       0.051
position_Centre-Forward     0.0399      0.030      1.320      0.187      -0.019       0.099
position_LeftWinger        -0.0103      0.028     -0.374      0.709      -0.065       0.044
position_RightWinger       -0.0340      0.028     -1.235      0.217      -0.088       0.020
position_SecondStriker     -0.0050      0.031     -0.159      0.874      -0.066       0.056
foot_both                   0.0166      0.029      0.568      0.571      -0.041       0.074
foot_left                   0.0069      0.021      0.331      0.741      -0.034       0.048
foot_right                 -0.0149      0.018     -0.814      0.416      -0.051       0.021
outfitter_Nike              0.0195      0.020      0.995      0.320      -0.019       0.058
outfitter_Puma             -0.0115      0.029     -0.394      0.694      -0.069       0.046
outfitter_adidas           -0.0177      0.020     -0.890      0.374      -0.057       0.021
outfitter_others            0.0108      0.032      0.341      0.733      -0.051       0.073
==============================================================================
Omnibus:                       27.516   Durbin-Watson:                   1.476
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               43.423
Skew:                          -0.353   Prob(JB):                     3.72e-10
Kurtosis:                       4.105   Cond. No.                     1.12e+16
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The smallest eigenvalue is 4.95e-29. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
```
   ---
   - p-value <= 0.1인 index 추출
```
app               0.165288
conceded_goals   -0.214899
yellow_card      -0.069854
age              -0.314128
club              0.308020
cup               0.138083
Goals             0.327745
SpG               0.394476
AvgP              0.157358
PS                0.124564
MotM             -0.146729
period            0.274621
dtype: float64
```
<img width="1074" alt="스크린샷 2021-06-15 오후 5 15 13" src="https://user-images.githubusercontent.com/53620138/122017819-4603b480-cdfd-11eb-9ccb-83e9e425435c.png">

