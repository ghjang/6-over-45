# 수동 업데이트 및 데이터 관리 가이드

이 문서는 `6-over-45` 프로젝트의 로또 데이터 업데이트 워크플로우를 수동으로 제어하고, 데이터 불일치 발생 시 해결하는 방법을 설명합니다.

## 1. 개요: 데이터 흐름

데이터 업데이트는 다음 3단계로 이루어집니다:

1.  **`fetch_latest.py`**: 네이버에서 최신 회차(예: 1210회) 당첨 번호를 가져와 `data/frequency.json`에 추가합니다.
2.  **`update_frequency.py`**: `frequency.json`의 통계를 갱신합니다.
3.  **`update_guesses.py`**:
    *   이전 회차(1209회)의 `next_guess.json`(예상 번호)을 `data/guesses.json`(예상 이력)으로 *이동*시킵니다. (키: `draw_1210`)
    *   새로운 회차(1211회)에 대한 예상 번호를 생성하여 `data/next_guess.json`에 *저장*합니다.

이 과정이 완료되면 Git에 커밋되고, 자동으로 **GitHub Pages 배포 워크플로우**가 트리거되어 웹사이트가 업데이트됩니다.

---

## 2. GitHub Actions 수동 실행 방법

데이터가 누락되었거나 배포를 강제로 다시 하고 싶을 때 사용합니다.

> **참고:** `data/frequency.json` 파일이 수정되어 `main` 브랜치에 푸시되는 경우에도 이 워크플로우(`Update Guesses`)는 **자동으로 실행**됩니다. 따라서 로컬에서 데이터를 수정한 후 푸시하면 별도로 수동 실행할 필요가 없을 수도 있습니다.

1.  GitHub 저장소의 **Actions** 탭으로 이동합니다.
2.  왼쪽 사이드바에서 **Update Guesses** 워크플로우를 선택합니다.
3.  오른쪽의 **Run workflow** 버튼을 클릭합니다.
4.  Branch는 `main`을 선택하고 **Run workflow** 녹색 버튼을 누릅니다.

**결과:**
*   스크립트가 실행되어 최신 데이터를 가져옵니다.
*   변동 사항이 있으면 자동으로 커밋(`Update lottery results...`)됩니다.
*   이후 **Deploy 6-over-45 to GitHub Pages** 워크플로우가 자동으로 실행되어 사이트에 반영됩니다.

---

## 3. 데이터 꼬임 해결 가이드 (롤백 및 복구)

만약 데이터 파일 간의 회차가 맞지 않거나, 특정 회차를 다시 실행하고 싶다면 **데이터를 과거 상태로 되돌리고(Rollback)** GitHub Actions를 실행해야 합니다.

### 상황: 1210회차 업데이트를 다시 하고 싶을 때

현재 상태가 1210회까지 업데이트되어 있지만, 이를 취소하고 1209회 완료 시점으로 되돌리려면 다음 3가지 파일을 수정해야 합니다.

#### 1. `data/frequency.json` 수정
*   파일 맨 아래의 `draw_1210` 블록을 **삭제**합니다.
*   바로 위 `draw_1209` 블록의 닫는 중괄호 `}` 뒤에 있는 **쉼표(`,`)를 제거**해야 합니다. (JSON 문법 오류 방지)

#### 2. `data/guesses.json` 수정
*   상단의 `"end_draw": 1210`을 `"end_draw": 1209`로 **변경**합니다.
*   파일 맨 아래 `guesses` 배열 내의 `draw_1210` 블록을 **삭제**합니다.
*   바로 위 `draw_1209` 블록의 뒤에 있는 **쉼표(`,`)를 제거**합니다.

#### 3. `data/next_guess.json` 확인 및 복구 (중요!)
*   `update_guesses.py`는 `next_guess.json`에 있는 번호를 `guesses.json`의 역사로 기록합니다.
*   따라서, **1210회차의 예상 번호였던 데이터**를 `next_guess.json`에 다시 넣어두어야 1210회차 기록이 올바르게 생성됩니다.
*   만약 이 파일에 이미 1211회차 예상 번호가 들어있다면, GitHub Actions가 돌았을 때 1210회차 기록에 1211회차 번호가 잘못 들어가는 문제가 발생합니다.

### 요약: 파일 상태 타임라인

| 파일 | 업데이트 전 (수동 롤백 목표) | 업데이트 후 (자동 실행 결과) |
| :--- | :--- | :--- |
| **최신 회차** | **1209회** | **1210회** |
| `frequency.json` | 1209회차 데이터까지 있음 | 1210회차 데이터 추가됨 |
| `guesses.json` | 1209회차 추측까지 있음 | 1210회차 추측(이전 `next_guess`) 추가됨 |
| `next_guess.json` | **1210회차 추측 번호** (대기 중) | **1211회차 추측 번호** (새로 생성됨) |

---

## 4. 로컬 테스트 커밋 및 푸시

파일을 수동으로 수정한 후에는 반드시 원격 저장소에 반영해야 합니다.

```bash
# 변경 사항 확인
git status

# 변경 사항 커밋
git add data/frequency.json data/guesses.json data/next_guess.json
git commit -m "Fix: Revert data to draw 1209 manually"

# 원격 저장소로 푸시
git push origin main
```

푸시 후 GitHub Actions에서 **Update Guesses**를 실행하면 정상적으로 복구됩니다.
