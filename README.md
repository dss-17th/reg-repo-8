# 20/21시즌 축구선수 몸값 회귀분석
---
## 1. 개요
<br/>

### 1-1. 프로젝트 목적
두 곳의 축구통계 사이트 크롤링을 통해 축구선수의 현재가치와 여러 feature들간의 회귀분석을 하는 것이 주 목적이며, 베이스라인을 통해 데이터의 전반적인 특성을 파악하고 데이터셋의 세분화를 통해 세분화된 데이터의 성향 및 차이점을 발견하고 중요 요인을 통해 인사이트를 제공하는 것입니다.


### 1-2. 프로젝트 목표
- 축구선수의 현재가치와 각 feature들 간의 관계를 파악
- 포지션간의 차이점과 특성 파악
- 변수제거 및 파생변수 생성을 통한 회귀모델에 적합한 데이터셋 생성
- 베이스라인과 데이터 세분화를 통한 분석과 결과 및 인사이트 도출
  - 베이스라인 (all_position_modeling.ipynb) : 전반적인 중요 요인을 파악하고 세분화할 특성 변수 정의, 성능 관점에서의 다양한 머신러닝 기법 적용
  - 세분화 (각 포지션별 modeling한 ipynb) : 세분화 데이터셋에 대한 통계적인 검정의 회귀 진행 및 사용자 관점에서 유의미한 인사이트 도출

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
1. **세분화를 진행할 변수 : position**
2. **전반적인 인사이트 : 축구선수의 나이가 많을수록 현재가치는 떨어지고 대체적으로 좋은 팀에 있고 많은 경기를 뛰며 팬층이 두텁고 수상경력이 많으면 현재가치를 높아진다.**

---

<br/>

### 2-2. 포지션을 기준으로 세분화한 회귀분석
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
- 인사이트 측면에서 중요하지 않은 컬럼들을 제거 및 데이터의 개수와 차원 수가 베이스라인보다 적기에 전체 포지션에 대해 모델링했을 때보다 성능이 낮게 나왔다.
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
- **공격수는 경기당 슈팅, 골이 가장 양의 영향을 주고, 미드필더는 평균패스 수가 가장 양의 영향을 주는 등 각 포지션별로 큰 영향을 주는 요인들이 달랐고 공격수는 공격성의 띄는 요인, 미드필더는 패스에 대한 요인들이 중요한 판단의 기준이 된다는 것을 알 수 있다.**

>**따라서 구단이 특정 포지션의 선수에 구매를 고려할 때 포지션별 중요 요인과 해당 선수의 이적료를 비교해 효율적인 구매를 할 수 있도록 정보를 제공해줄 수 있다.**

---
---

## 3. 과정
### 3-1. 베이스라인 분석에 대한 기술적 Summary

<br/>

#### **modeling 성능평가에 사용된 함수**
```
from patsy import dmatrix
from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold


# OLS 모델을 만든 후 5번의 교차검증을 통해 r2-score, mse, rmse의 평균값을 출력해주는 함수
def get_scores(df, formula, inplace=False, get_model=False, show_dfX=False):
    
    scores = np.zeros(5)
    mses = np.zeros(5)
    rmses = np.zeros(5)
    cv = KFold(5, shuffle=True, random_state=3)
    for i, (idx_train, idx_test) in enumerate(cv.split(df)):
        
        df_X = dmatrix(formula, df, return_type='dataframe')
        df_y = df['market_value']
        
        X_train, X_test = df_X.iloc[idx_train], df_X.iloc[idx_test]
        y_train, y_test = df_y.iloc[idx_train], df_y.iloc[idx_test]

        model = sm.OLS(y_train, X_train).fit()
        pred = model.predict(X_test)
        
        mse = metrics.mean_squared_error(y_test, pred)
        rmse = np.sqrt(metrics.mean_squared_error(y_test, pred))
        r_squared = r2_score(y_test, pred)
        
        scores[i] = r_squared
        mses[i] = mse
        rmses[i] = rmse
    
    avg_r_score = np.mean(scores).round(4)
    avg_mse = np.mean(mses).round(4)
    avg_rmse = np.mean(rmses).round(4)
    
    print("r-score :", avg_r_score)
    print("mse :", avg_mse)
    print("rmse :", avg_rmse)
    
    if inplace:
        return [avg_r_score, avg_mse, avg_rmse]
    
    if get_model:
        return model, [avg_r_score, avg_mse, avg_rmse]
    
    if show_dfX:
        return df_X, [avg_r_score, avg_mse, avg_rmse]


# 두 모델의 성능을 비교해주는 함수
def compare_scores(prev_score, curr_score):
    print("r-score 변화량: ", (curr_score[0] - prev_score[0]).round(4))
    print("mse 변화량 :", (curr_score[1] - prev_score[1]).round(4))
    print("rmse 변화량 :", (curr_score[2] - prev_score[2]).round(4))
```
- get_scores
  - dmatrix를 이용해 문자열로 OLS 회귀모델 생성 후 5번의 교차검증을 통해 성능에 대한 결과를 도출하는 함수
  - inplace, get_model, show_dfX 파라미터를 통해 성능과 모델객체, 독립변수셋을 return받을 수 있음

- compare_scores
  - 두 모델간 성능을 비교해 성능의 변화량을 도출하여 모델을 비교해주는 함수

---
<br/>

#### **VIF와 p-value를 고려한 변수 제거**
```
from statsmodels.stats.outliers_influence import variance_inflation_factor

dfX, score_7 = get_scores(model_df, formula, show_dfX=True)

vif_df = pd.DataFrame()
vif_df["VIF Factor"] = [variance_inflation_factor(dfX.values, i) for i in range(dfX.shape[1])]
vif_df["features"] = dfX.columns
```
- 각 독립변수에 대한 VIF score 도출 후 데이터프레임화
```
vif_df = vif_df.sort_values('VIF Factor', ascending=False).reset_index(drop=True)
vif_df[vif_df['VIF Factor'] > 5]
```
- VIF score가 5보다 큰 독립변수 추출 후 p-value값을 고려 후 불필요한 변수 정의 및 제거

---
<br/>

#### **KMeans를 사용해 제거된 독립변수에 대한 Clustering**
```
remove_df = players_df.copy()
remove_df = remove_df[["position", "foot", "Rating", "PS", "Drb", "Assists", "Clear", "Off"]]
```
- 불필요한 변수에 대한 데이터프레임화
```
remove_df = pd.get_dummies(remove_df, columns=['position', 'foot'], drop_first=True)
```
- 범주형 변수에 대한 더미변수화
```
from sklearn.preprocessing import StandardScaler

ss = StandardScaler().fit_transform(remove_df.iloc[:, :6].values)
remove_df[["Rating", "PS", "Drb", "Assists", "Clear", "Off"]] = ss
```
- 연속형 변수에 대한 Standard Scaling
```
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


distance = []
for i in range(2, 15):
    model = KMeans(n_clusters=i).fit(remove_df)
    distance.append(model.inertia_)

sil = []
for i in range(2, 15):
    model = KMeans(n_clusters=i).fit(remove_df)
    sil.append(silhouette_score(remove_df, model.labels_))
```
<img width="978" alt="스크린샷 2021-07-30 오후 6 12 57" src="https://user-images.githubusercontent.com/80459520/127630818-c492803f-e3c8-4002-9713-d7be3de47b34.png">

- 군집의 개수를 2 ~ 15개로 한 뒤 distance와 실루엣계수로 최적의 군집 수 파악
- distance가 급격히 꺾이는 구간은 보이지 않고 군집 수가 2일때 실루엣계수가 가장 높으므로 2개의 군집으로 라벨링 진행
```
from sklearn.decomposition import PCA

model = KMeans(n_clusters=2).fit(remove_df)

pca = PCA(n_components=2)
datas = pca.fit_transform(remove_df)
pca_df = pd.DataFrame(datas, columns=["PC1", "PC2"])
pca_df['label'] = model.labels_
```
- 분류성능 확인을 위한 PCA 차원축소 후 시각화

<img width="330" alt="스크린샷 2021-07-30 오후 6 23 44" src="https://user-images.githubusercontent.com/80459520/127632250-7bced16e-9dd0-4c86-b55f-2ae7daf666b4.png">

---
<br/>

#### **최종모델에 대한 모델링**
```
model_df = players_df.copy()

model_df['second_yell'] = model_df['second_yell'].astype('int')
model_df['red_card'] = model_df['red_card'].astype('int')
model_df['out'] = model_df['red_card'] + model_df['second_yell']
model_df.drop(columns=['red_card', 'second_yell', "outfitter"], inplace=True)

model_df['market_value'] = np.log1p(model_df['market_value'])
model_df['club'] = model_df['club'].apply(convert_club)

remove_ls = remove_df.columns[:6].tolist() + ['position', 'foot']
model_df.drop(columns=remove_ls, inplace=True)
model_df['label'] = model.labels_
```
- 모델링을 위한 데이터셋 전처리
  - 불필요한 변수를 제거한 후 그 변수들의 Clustering Label에 대한 값을 label이라는 변수값으로 대체
```
formula = "+".join([f"scale({var})" for var in model_df.columns.tolist()[1:-1]]) + "+C(label)"

model_8, score_8 = get_scores(model_df, formula, get_model=True)
compare_scores(score_7, score_8)
```
- 독립변수 전처리 방식에 대한 문자열 생성
- 모델링 후 model객체와 성능 return
- 전 모델객체와의 성능비교

---
<br>

#### **아노바검정을 통한 모델간 비교**
```
sm.stats.anova_lm(model_8, model_7)
```
<img width="397" alt="스크린샷 2021-07-30 오후 6 38 12" src="https://user-images.githubusercontent.com/80459520/127634145-e9486228-6c3d-42c5-9a7d-b7458aa860a7.png">

- 전 모델과 아노바검정의 p-value이 유의수준보다 낮기에 귀무가설을 기각하므로 두 모델은 다르다고 할 수 있고, 성능적인 부분에서 최종모델(model_8)이 높기에 모델 채택

---
<br/>

#### **RandomForestRegressor & GridSearch**
```
from sklearn.model_selection import train_test_split

df_X = dmatrix(formula, model_df, return_type='dataframe')
df_y = model_df['market_value']

X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.3, random_state=3)
```
- 최종모델의 데이터셋을 사용해 train, test 데이터셋으로 split
```
from sklearn.model_selection import GridSearchCV

random_params = {'bootstrap': [True, False],
 'max_depth': [1,3,5,7,9],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800]}

randomfr_tuning_model = GridSearchCV(
    randomfr_model,
    param_grid=random_params,
    scoring='neg_mean_squared_error',
    cv=3,
    verbose=3)

randomfr_tuning_model.fit(X_train,y_train)

randomfr_tuning_model.best_params_
```
- random forest regressor의 몇몇 파라미터들에 다양한 값을 통한 GridSearch후 Best Parameters 도출

---
---
<br/>

### 3-2. 세분화 분석에 대한 기술적 Summary

#### **공격수(Attack) 데이터셋 로드**
```
import pickle
from Library.preprocess import *

with open('datas/attack.pkl', 'rb') as f:
    attack_df = pickle.load(f)

attack_df = preprocess_df(attack_df)
```
<img width="974" alt="스크린샷 2021-06-14 오후 7 30 23" src="https://user-images.githubusercontent.com/53620138/121878706-fd89bf80-cd46-11eb-9bea-add61ca6a9ee.png">

- 공격수 데이터프레임을 pickle파일로 불러와 직접 구성한 전처리 함수를 통한 데이터셋 전처리 

---
<br/>

#### **최종모델에 대한 데이터셋 전처리**
```
from sklearn.preprocessing import  StandardScaler
from sklearn.model_selection import train_test_split

model_df = pd.get_dummies(attack_df, columns=['position', 'foot', 'outfitter'])

dfX0 = model_df.loc[:, 'app':]
log_dfy = np.log1p(model_df['market_value'])

ss = StandardScaler().fit(dfX0.loc[:, "app":"total_out"].values)
ss_values = ss.transform(dfX0.loc[:, "app":"total_out"].values)
ss_dfX0 = np.hstack([ss_values , dfX0.loc[:, "position_Centre-Forward":].values])

train_X, test_X, train_y, test_y = train_test_split(ss_dfX0, log_dfy, test_size=0.3, random_state=3)
```
- 범주형 변수에 대해 더미변수화 후 독립변수와 종속변수로 세분화
- 종속변수는 log scaling, 독립변수는 standard scaling 적용
- 7:3 비율로 train, test 데이터셋으로 세분화

---
<br/>

#### **LinearRegression Model**
```
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


model_log = LinearRegression(fit_intercept=True).fit(train_X, train_y)
pred_log = model_log.predict(test_X)
f = np.polyfit(pred_log, test_y, deg=1)

print("log_scaled MSE : ", mean_squared_error(test_y, pred_log))
print("log_scaled RMSE : ",np.sqrt(mean_squared_error(test_y, pred_log)))
print("Inverse log한 RMSE : ", np.sqrt(np.sum((((np.exp(test_y) -1) - (np.exp(pred_log) -1))**2)) / len(test_y)))
print("log_scaled r2-score : ",r2_score(test_y, pred_log))

sns.regplot(x=pred_log, y=test_y)
plt.title(f"기울기 :{f[0].round(3)}")
plt.xlabel('Predict', fontsize=15)
plt.ylabel("Actual", fontsize=15)

plt.show()
```
<img width="897" alt="스크린샷 2021-07-31 오후 7 46 57" src="https://user-images.githubusercontent.com/80459520/127737467-b4f1cbc9-9347-4080-ae07-c894312d25b7.png">

- 상수항 추가 후 train셋으로 학습한 모델객체 생성
- test셋으로 예측값 도출후 ployfit을 통한 예측값과 실제값 사이의 기울기 생성 및 성능도출
- 예측값과 실제값의 regplot을 통한 Visualization

---
<br/>

#### **GridSearch를 통한 RandomForest Regressor Model**
```
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor


# GridSearch Parameter list
random_params = {'bootstrap': [True, False],
 'max_depth': [1,3,5,7,9],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800]}

# GridSearch Object
result = GridSearchCV(
    RandomForestRegressor(),
    param_grid=random_params,
    scoring='neg_mean_squared_error',
    cv=5,
    verbose=3)

# Modeling
result.fit(train_X, train_y)

grid_model = RandomForestRegressor(**result.best_params_).fit(train_X, train_y)
pred_grid = grid_model.predict(test_X)

print(mean_squared_error(test_y, pred_grid))
print(np.sqrt(mean_squared_error(test_y, pred_grid)))
print(r2_score(test_y, pred_grid))
```
> MSE, RMSE, R-squared Score 순

<img width="178" alt="스크린샷 2021-07-31 오후 7 53 28" src="https://user-images.githubusercontent.com/80459520/127737642-81b1ebba-3f35-48fb-91e7-1ea386d5a9fc.png">

- GridSearch할 하이퍼 파라미터들의 리스트를 생성
- GridSearch 객체를 생성한 뒤 학습
- GridSearch 학습결과의 Best Parameter들로 RandomForestRegressor 객체생성 후 학습

---
<br/>

#### **Pipeline를 사용한 RandomForest Regressor Model**
- ploynomialFeatures을 이용한 다향회귀 진행 : 삼차항
- pipeline : PolynomialFeatures > StandardScaler > RandomForestRegressor
- GridSearch보다 좀 더 성능이 좋은 HalvingGridSearchCV사용
```
import os
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV


# Pipeline 구성 및 객체생성
pipe = Pipeline([
    ('ploy', PolynomialFeatures(degree=3)),
    ('scaler', StandardScaler()),
    ('rf', RandomForestRegressor())
])

# GridSearch Parameter list
pipe_params = {
    'ploy__degree': [3],
    'rf__bootstrap': [True],
    'rf__max_features': ['auto', 'sqrt'],
    'rf__min_samples_leaf': [2, 4, 8],
    'rf__min_samples_split': [2, 4, 8],
    'rf__n_estimators': [200, 1000]
}

# Pipeline 객체의 HalvingGridSearch 학습
pipe_grid = HalvingGridSearchCV(pipe, param_grid=pipe_params, verbose=2, n_jobs=os.cpu_count()-2, scoring="roc_auc", min_resources="exhaust", cv=3)
pipe_grid.fit(train_X, train_y)

pipe_grid.best_params_
```
> Pipeline GridSearch의 Best Parameter

<img width="244" alt="스크린샷 2021-07-31 오후 8 18 23" src="https://user-images.githubusercontent.com/80459520/127738218-2518a9d8-1a7e-48a2-9409-11d8e1169cbc.png">

- Pipeline을 통해 다차항 독립변수에 대한 모델링 진행
- GridSearch할 파라미터들을 구성 후 최대 CPU에서 2개를 뺀 개수로 HashGridSearch 진행 후 Best Parameter 조합 도출

---
<br/>

# 💡 제언 및 한계점
```
- 데이터의 차원이 높아질수록 성능은 좋아지지만 그 만큼의 연산량이 증가할 뿐더러 중요 요인을 파악할 때에 어려움이 있을 수 있기애 문제정의 단계에서 프로젝트의 목표를 잘 설정하고 목표지향적으로 그에 맞는 분석을 해야한다고 생각합니다.

- 베이스라인을 잡고 분석하여 데이터 전반적인 인사이트와 목적에 맞는 중요 요인을 도출하고, 데이터 세분화를 통해 집요하게 분석하는 과정이 중요하다고 생각합니다.


<한계점>
- 현재가치는 여러시즌에 걸친 선수의 퍼포먼스에 의해 형성되기 때문에, 단일 시즌으로는 정확한 예측이 어려웠습니다.

- 선수의 더 디테일하고 깊이있는 데이터를 수집했다면 더 정확한 결과를 도출해냈을 수 있었을 것으로 예상됩니다.

- 통계치가 아닌 좀 더 상세한 시간대별 수치들을 수집할 수 있었으면 더 심도있는 분석이 가능했을것으로 예상되나 해당 데이터를 제공하는 사이트가 없었습니다.
```

<br/>

# Code Explanation
- 베이스라인 : 모든 포지션에 대한 EDA 및 모델링
  - > [all_position_EDA.ipynb](https://github.com/dss-17th/reg-repo-8/blob/main/all_position/all_position_EDA.ipynb) : 베이스라인 EDA Notebook
  - > [all_position_modeling.ipynb](https://github.com/dss-17th/reg-repo-8/blob/main/all_position/all_position_modeling.ipynb) : 베이스라인 Modeling Notebook

- 데이터 세분화 후 분석 : 각 포지션에 대한 EDA 및 모델링
  - > [EDA_each_position.ipynb](https://github.com/dss-17th/reg-repo-8/blob/main/EDA_each_position.ipynb) : 각 포지션에 대한 EDA Notebook
  - > [modeling_attack.ipynb](https://github.com/dss-17th/reg-repo-8/blob/main/modeling_attack.ipynb) : 공격수에 대한 Modeling Notebook
  - > [modeling_midfield.ipynb](https://github.com/dss-17th/reg-repo-8/blob/main/modeling_midfield.ipynb) : 미드필더에 대한 Modeling Notebook
  - > [modeling_defender.ipynb](https://github.com/dss-17th/reg-repo-8/blob/main/modeling_defender.ipynb) : 수비수에 대한 Modeling Notebook

- 모듈 파일 및 크롤링 코드
  - > [preprocess.py](https://github.com/dss-17th/reg-repo-8/blob/main/Library/preprocess.py) : raw dataset을 모델링을 위한 dataset으로 전처리해주는 모듈
  - > [crawl_transfer.py](https://github.com/dss-17th/reg-repo-8/blob/main/Library/crawl_transfer.py) : 5대 리그 선수들의 현재가치 및 정보 크롤링 모듈
  - > [transfer_run.py](https://github.com/dss-17th/reg-repo-8/blob/main/transfer_run.py) : crawl_transfer module을 import하여 크롤링을 수행하는 코드
  - > [crawl_whoscored.py](https://github.com/dss-17th/reg-repo-8/blob/main/Library/crawl_whoscored.py) : 5대 리그 선수들의 경기정보 크롤링 모듈
  - > [whoscored_run.py](https://github.com/dss-17th/reg-repo-8/blob/main/whoscored_run.py) : crawl_whoscored module을 import하여 크롤링을 수행하는 코드