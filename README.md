# 축구선수의 몸값 회귀분석 (송강, 이승주)
## < 팀 구성 >
1. 송강
  - whoscored.com 데이터 크롤링
  - 골키퍼, 수비수에 대한 회귀분석
  - 전처리 및 모델링
3. 이승주
  - transfermkt.com 데이터 크롤링
  - 공격수, 미드필더에 대한 회귀분석
  - 전처리 및 모델링

## < 목표 >
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
- 선수들의 통계치를 나타낸 데이터는 몸값과 뚜렷한 선형적 관계를 가지지 않음.
- 포지션별 세분화된 데이터에서도 유의미한 예측은 어려움.
- 개인 수상 커리어 또한 몸값에 큰 영향을 미치지 않음.

> ### 1. 데이터 전처리 설명

실제로 가져올 수 있고 다룰 수 있는 수준의 데이터를 유럽 5대리그(스페인,영국,프랑스,이탈리아,독일)로 설정했습니다.  
또한 whoscored.com과 transfermarkt.com에 올라와 있는 선수데이터가 약간 상이한 부분이 있어 소속팀과 선수이름으로 merge하여  
약 2000명의 선수 데이터셋을 구성했습니다.
<img width="974" alt="스크린샷 2021-06-14 오후 7 30 23" src="https://user-images.githubusercontent.com/53620138/121878706-fd89bf80-cd46-11eb-9bea-add61ca6a9ee.png">
그 중 600명의 공격수 데이터
<img width="1004" alt="스크린샷 2021-06-14 오후 7 37 59" src="https://user-images.githubusercontent.com/53620138/121879637-0e870080-cd48-11eb-94a7-4cd68ebdbfbe.png">


> 공격수 포지션의 market_value와 다른 컬럼들간의 상관관계 히트맵

![다운로드 (1)](https://user-images.githubusercontent.com/53620138/121879925-5dcd3100-cd48-11eb-9460-096e77935fec.png)

>  Nike, adidas, Puma 외의 class들을 others로 grouping  

<img width="1009" alt="스크린샷 2021-06-14 오후 7 41 27" src="https://user-images.githubusercontent.com/53620138/121880064-881eee80-cd48-11eb-81b4-c4689332a696.png">

> foot, position, outfitter 의 분포와 boxplot
<img width="997" alt="스크린샷 2021-06-14 오후 7 47 00" src="https://user-images.githubusercontent.com/53620138/121880720-4e021c80-cd49-11eb-9a01-6595e9dfb457.png">
<img width="1015" alt="스크린샷 2021-06-14 오후 7 47 50" src="https://user-images.githubusercontent.com/53620138/121880832-71c56280-cd49-11eb-9904-2f2a0887b07b.png">