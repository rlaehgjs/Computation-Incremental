# 게임 밸런스 공식 정리

## 1. 하드웨어 업그레이드 비용

### 기본 공식
```
비용 = base × (exp ^ level)
```

### 각 업그레이드별 상수
| 업그레이드 | base | exp (기본) | exp (Impulse Lv.3+) | 최대 레벨 |
|-----------|------|------------|---------------------|----------|
| 행 확장 (rows) | 5 | 2.5 | 2.2 | 8 |
| 열 확장 (cols) | 50 | 3.5 | 3.0 | 8 |
| 클럭 가속 (speed) | 10 | 1.6 | 1.48 | 무제한 |

### Impulse Lv.3 효과
- 하드웨어 비용 스케일링 -20%
- 공식: `exp_new = 1 + (exp_old - 1) × 0.8`
- 예시: rows의 exp가 2.5 → 2.2로 감소

### 비용 예시 (Impulse Lv.3 미적용)
- **행 확장**: 5, 12, 31, 78, 195, 488, 1220, 3051
- **열 확장**: 50, 175, 612, 2143, 7500, 26250, 91875, 321562
- **클럭 가속**: 10, 16, 26, 41, 66, 105, 168, 268, 429, 687...

---

## 2. Cognitive Step 업그레이드 비용

### Impulse
```
비용 = 5 × (4 ^ 현재레벨)
```
- Lv.0 → Lv.1: 5
- Lv.1 → Lv.2: 20
- Lv.2 → Lv.3: 80
- Lv.3 → Lv.4: 320
- Lv.4 → Lv.5: 1280

### Intuition
- 비용: **0** (Impulse 레벨 소모)
- 요구사항: Impulse Lv.4 + (Intuition 레벨 × 2)
  - Intuition Lv.0 → Lv.1: Impulse Lv.4 필요
  - Intuition Lv.1 → Lv.2: Impulse Lv.6 필요
  - Intuition Lv.2 → Lv.3: Impulse Lv.8 필요

---

## 3. 생산량 계산 공식

### 기본 구조
```
생산량 = yieldMult × onCount × comboMult
```

### 1단계: 전구 점등 확률
```
기본 확률 = 50%
Intuition Lv.3 적용 시 = 60%
```

### 2단계: yieldMult 계산
```
baseBonus = 0
if (Impulse >= 4):
    baseBonus = (Impulse + Intuition) × 0.5

yieldMult = 1 + baseBonus
if (Impulse >= 5):
    yieldMult = yieldMult × 2
```

**예시:**
- Impulse 4, Intuition 0: yieldMult = 1 + 2.0 = 3.0
- Impulse 5, Intuition 0: yieldMult = (1 + 2.5) × 2 = 7.0
- Impulse 5, Intuition 2: yieldMult = (1 + 3.5) × 2 = 9.0

### 3단계: comboMult 계산 (Intuition Lv.2+)
```
if (onCount <= 5):
    comboMult = 1 + (onCount × 0.1)
else:
    logBonus = log5(onCount)  // log5 = ln(onCount) / ln(5)
    comboMult = 1 + (logBonus × 0.5)
```

**콤보 보너스 예시:**
- 1개: 1.1배
- 3개: 1.3배
- 5개: 1.5배
- 10개: 1 + (log5(10) × 0.5) = 1 + (1.43 × 0.5) ≈ 1.72배
- 20개: 1 + (log5(20) × 0.5) = 1 + (1.86 × 0.5) ≈ 1.93배
- 32개 (8×4): 1 + (log5(32) × 0.5) = 1 + (2.15 × 0.5) ≈ 2.08배
- 64개 (8×8): 1 + (log5(64) × 0.5) = 1 + (2.58 × 0.5) ≈ 2.29배

---

## 4. 사이클 속도

### 공식
```
delay = 1000 × (0.9 ^ speed)
```

**예시:**
- speed 0: 1000ms
- speed 1: 900ms
- speed 5: 590ms
- speed 10: 349ms
- speed 20: 122ms

---

## 5. 밸런스 분석

### 생산량 증가 요인
1. **하드웨어 확장**: 전구 수 증가 (rows × cols)
2. **클럭 가속**: 사이클 시간 감소
3. **Impulse 레벨**: yieldMult 증가
4. **Intuition Lv.2**: 콤보 보너스
5. **Intuition Lv.3**: 점등 확률 증가

### 비용 증가 패턴
- **하드웨어**: 지수적 증가 (exp 2.2~3.5)
- **Impulse**: 지수적 증가 (exp 4.0)
- **Intuition**: 무료이지만 Impulse 레벨 소모

### 잠재적 밸런스 이슈
1. **Impulse 비용**: 4배씩 증가하여 후반에 매우 비쌈
2. **열 확장 비용**: 3.5배 증가로 매우 빠르게 증가
3. **콤보 보너스**: 로그 기반이라 큰 그리드에서도 완만하게 증가 (의도된 설계)
4. **클럭 가속**: 1.6배 증가로 비교적 저렴하지만 효과는 지수적 (0.9^n)
