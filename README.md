# 20/21시즌 축구선수 몸값 회귀분석
---
## 1. 개요
<br/>

### 1-1. 프로젝트 목적
두 곳의 축구통계 사이트 크롤링을 통해 축구선수의 현재가치와 여러 feature들간의 회귀분석을 하는 것이 주 목적이며, 통계적관점과 머신러닝관점에서 서로 다른 방향으로 데이터를 분석 및 모델링을 하여 결론을 도출하는 것입니다.

### 1-2. 프로젝트 목표
- 축구선수의 현재가치와 각 feature들 간의 관계를 파악
- 포지션간의 차이점과 특성 파악
- 변수제거 및 파생변수 생성을 통한 회귀모델에 적합한 데이터셋 생성
- 두가지 관점에 맞는 분석과 결과 및 인사이트 도출
  - 머신러닝 관점(all_position_modeling.ipynb) : 모델의 성능을 최대한 높이는 방향으로 데이터 전처리 및 모델링
  - 통계적 및 해석적인 관점(각 포지션별 modeling한 ipynb) : 단순 모델의 성능상승 외에 유의미한 해석을 위해 feature들이 종속변수에 미치는 영향을 확인하는 방향으로 데이터 전처리 및 모델링

### 1-3. 기술적 목표
- selenium을 통한 정적페이지 크롤링
- BeauifulSoup(css-selector, find)과 scrapy(xpath)를 통해 정적페이지 크롤링 및 Null data에 대한 예외처리
- pandas, sklearn을 통한 raw data 전처리 후 pickle파일로 데이터 관리
- 아웃라이어, 불필요한 독립변수 도출 및 Clustering을 통한 새로운 파생변수 생성
- 교차검증을 통한 과적합 방지 및 신뢰성 높은 모델구축
- GridSearch, Pipeline을 통한 모델의 하이퍼 파라미터 튜닝
- 다양한 모델링 및 모델별 시각화를 통한 성능평가
- data EDA를 통한 변수들의 분포 및 특성 파악

### 1-4. 데이터셋 및 설명
- [whoscored.com](https://www.whoscored.com/) : 축구선수들의 경기정보 및 경기스텟 데이터
- [transfermarkt.com](https://www.transfermarkt.com/) : 축구선수 현재가치 및 신체정보 데이터
```
5대 리그에 대한 수집 : 프리미어리그, 라리가, 분데스리가, 리그앙, 세리에A
row : 20/21시즌 개개인의 축구선수에 대한 정보
```


### 1-5. 팀구성
- 송강 ([GitHub](https://github.com/rivels))
  - whoscored site 크롤링 및 전처리
  - 골키퍼, 수비수에 대한 EDA 및 회귀분석
  - README 작성
- 이승주 ([GitHub](https://github.com/aeea-0605))
  - transfermarkt site 크롤링 및 전처리
  - 공격수, 미드필더, 전체 포지션에 대한 EDA 및 회귀분석
  - README 작성
---
---
## 2. 결론
<br/>

### 2-1. 베이스라인 회귀분석 (전체 포지션에 대한 데이터셋)
#### <최종모델 데이터 전처리>
- 범주형
  - club : 수치형 변수로 변환
    - 챔스 : 5, 유로파 : 3, 일반 : 0, 강등 : -3
  - outfitter 제거 (성능비교를 통한 제거)
  - second_yell, red_card 변수 결합에 대한 파생변수 생성 : out(수치형)
  - VIF로 추출한 독립변수들의 KMeans Clustering을 통한 파생변수 생성 : label(범주형)
- 수치형
  - OLS from_formula의 default scaling
- 종속변수
  - log1p scaling
#### <최종모델 summary table>
![전체포지션_summary.png](https://user-images.githubusercontent.com/80459520/124561898-5ac1ee00-de79-11eb-9dff-7111e1348172.png)
- 첫번째 모델 r-score : 0.5753 >> 최종 모델 r-score : 0.748
- 최종모델에 대한 교차검증(cv=5)후 r-score : 0.7034


<br/>

#### <최종모델에서 현재가치와 각 독립변수간의 가중치에 대한 시각화 그래프>
![전체포지션_가중치.png](https://user-images.githubusercontent.com/80459520/124558702-db7eeb00-de75-11eb-8102-44fb68fca2a4.png)
- KMeans Cluster를 통해 제거된 변수들의 집합으로 만들어진 새로운 파생변수가 가장 큰 양의 가중치를 가짐
- 양의 관계 : label(파생변수), SpG(경기당슈팅), app(경기수), club(팀), AvgP(평균패스 수), sns(sns계정수), period(계약기간), cup(트로피수) ... 순으로 되어있다.
- 음의 관계 : age(나이), Inter(인터셉트), conceded_goals(실점수)
#### 결론
- 모든 변수와 class들을 살려서 모델링 했을 때 r-score가 0.7195로 가장 높았지만 각 변수에 대한 설명력이 떨어졌음
- 반복된 전처리와 모델링을 통해 r-score : 0.7034, mse : 0.5183, rmse : 0.7158의 성능을 갖게되었고 각 독립변수가 종속변수에 어떠한 영향을 미치는 지에 대한 해석 또한 가능했다.
- 두 가지 방법(Cook's distance, boxplot의 outlier)을 통해 아웃라이어 제거를 진행하였지만 제거하지 않은 모델의 성능이 더 좋았음
- RandomForestRegressor 회귀모델에 대한 GridSearch를 통해 best parameter의 조합을 뽑아 모델링을 진행했지만 OLS모델의 성능이 더 좋았음

#### 인사이트
**축구선수의 나이가 많을수록 현재가치는 떨어지고 대체적으로 좋은 팀에 있고 많은 경기를 뛰며 팬층이 많고 수상경력이 많으면 현재가치는 높아진다.**

**포지션 변수를 통한 데이터셋 세분화 **

---
<br/>

### 2-2. 데이터셋 세분화 회귀분석
#### <최종모델 데이터 전처리>
- model : LinearRegression
- 범주형 : 더미변수화
- 수치형 : Standard Scaler
- 종속변수 : log1p Scaler

### 1) 공격수(attack)
#### <regplot을 통한 모델 비교분석>
![attack_regplot.png](https://user-images.githubusercontent.com/80459520/124566621-30266400-de7e-11eb-916a-d917d73bc0cc.png)
- r2-score가 0.5598에서 0.6855로 증가하였고 regplot의 분포도 선형적으로 변화하였다. 또한 예측값과 실제값의 기울기가 좀 더 1에 수렴하게 되었다.

#### <최종모델 summary table>
![attack_summary.png](https://user-images.githubusercontent.com/80459520/124567685-323cf280-de7f-11eb-8ebe-61cccfff2b39.png)

#### <p-value 0.1이하의 독립변수들의 가중치 시각화 그래프>
![attack_weight_plot.png](https://user-images.githubusercontent.com/80459520/124568757-3c132580-de80-11eb-82ea-bb9b5f8c382f.png)

<br/>

### 2) 미드필더(midfield)
#### <regplot을 통한 모델 비교분석>
![midfield_regplot.png](https://user-images.githubusercontent.com/80459520/124569554-0458ad80-de81-11eb-8b95-e9e6a093b808.png)
#### <p-value 0.1이하의 독립변수들의 가중치 시각화 그래프>
![midfield_weight_plot.png](https://user-images.githubusercontent.com/80459520/124569748-2fdb9800-de81-11eb-9adc-f0c51585d66a.png)

<br/>

### 3) 수비수(defender)
#### <regplot을 통한 모델 비교분석>
![defender_regplot.png](https://user-images.githubusercontent.com/80459520/124569987-6ca78f00-de81-11eb-9beb-74f2a9c31bb9.png)
#### <p-value 0.1이하의 독립변수들의 가중치 시각화 그래프>
![defender_weight_plot.png](https://user-images.githubusercontent.com/80459520/124570234-a5476880-de81-11eb-8483-8418131f379c.png)

#### 결론
- 각 포지션별 모델링을 진행하고 좀 더 해석적으로 유의미한 결과를 도출하기 위해 인사이트 측면에서 중요하지 않은 컬럼들을 제거 >> 데이터의 개수와 차원의 수(변수의 수)가 전체 프지션에 대해 모델링했을 때보다 성능이 낮게 나왔다.
- RandomForestRegressor 회귀모델에 대한 GridSearch를 통해 best parameter의 조합을 뽑아 모델링을 진행했지만 sklearn-LinearRegression 모델의 성능이 더 좋았음
- Standard, MinMax, Robust scaler를 모두 적용해본 결과 Standard scaler의 성능이 가장 좋았음

#### 인사이트
- 공격수
  - 양의 가중치 : SpG, Goals, club, period, app ...
  - 음의 가중치 : age, conceded_goals, MotM, yellow_card
- 미드필더
  - 양의 가중치 : AvgP, club, app, Goals, period ...
  - 음의 가중치 : age, conceded_goals, LongB ...
- 수비수
  - 양의 가중치 : club, Rating, app, AvgP, cup ...
  - 음의 가중치 : age, Inter, Tackles ...
- **공격수는 경기당 슈팅, 골이 가장 양의 영향을 주고, 미드필더는 평균패스 수가 가장 양의 영향을 주는 등 각 포지션별로 큰 영향을 주는 요인들이 다르다는 인사이트를 도출하였고 공격수는 공격성의 띄는 요인, 미드필더는 패스에 대한 요인들이 중요한 판단의 기준이 된다는 것을 알 수 있다.**
---
---

## 3. 과정

> ### 1. 데이터 전처리 설명
whoscored.com과 transfermarkt.com에 올라와 있는 선수데이터가 약간 상이한 부분이 있어 소속팀과 선수이름으로 merge하여 약 2000명의 선수 데이터셋을 구성했습니다.  
club 컬럼은 팀명에서 Chapions League 진출팀은 3, Eueropa League 진출팀은 2, 현재 리그 잔류는 1, 현재 리그에서 강등된 팀은 0으로 수치화하여
변경되었습니다.
foot, outfitter, position 은 one hotencoding 처리했습니다.

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

---

## <한계점>

- 몸값은 여러시즌에 걸친 선수의 퍼포먼스에 의해 형성되기 때문에, 단일 시즌으로는 정확한 예측이 어려움.
- 선수의 더 디테일하고 깊이있는 데이터를 수집했다면 더 정확한 결과를 도출해냈을 수 있었을 것으로 예상됨.
- 통계치가 아닌 좀 더 상세한 시간대별 수치들을 수집할 수 있었으면 더 심도있는 분석이 가능했을것으로 예상되나 해당 데이터를 제공하는 사이트가 없음.
