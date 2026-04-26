# 자경단 미러 FAQ — 자동 동기화·보존 동작

> "내가 push 하면 자경단 미러도 자동으로 따라오나요?"
> "내 GitHub 계정이 사라지면 자경단 미러는 어떻게 되나요?"
>
> 이 두 질문에 대한 점검 결과와 동작 설명입니다. 단장이 [2026-04-27 점검](#점검-기록)을 통해 모든 강의 미러에서 확인했습니다.

---

## TL;DR

| 시나리오 | 미러 동작 |
|----------|-----------|
| 원본에 push (브랜치/태그 무관) | ⚡ **즉시 동기화** (보통 10초 내) |
| 6시간 동안 push 없음 | 🕒 **6시간 주기 자동 동기화** (cron) |
| 단장이 수동 트리거 | 🖱️ **workflow_dispatch**로 즉시 실행 가능 |
| 원본 계정·레포 삭제 | 🛡️ **자경단 미러는 그대로 보존** (동기화만 멈춤, 데이터는 안 사라짐) |
| 원본에서 브랜치 강제 삭제 | ⚠️ 미러도 같은 브랜치 삭제 (`--mirror`는 source 거울이라 그대로 따라감) |
| MIRROR_PAT 만료/폐기 | 🟡 동기화만 멈춤. 미러 데이터는 보존. PAT 갱신 시 재개 |

---

## 1. push 자동 동기화

### 트리거 3종

각 원본 레포의 [`.github/workflows/catguard-mirror.yml`](https://github.com/catguard-team/.github/blob/main/workflow-templates/mirror.yml)에 다음 트리거가 박혀있습니다.

```yaml
on:
  push:
    branches: ["**"]   # 모든 브랜치
    tags: ["**"]       # 모든 태그
  schedule:
    - cron: "0 */6 * * *"  # 6시간마다
  workflow_dispatch: {}    # 수동 실행
```

→ 본인이 **어떤 브랜치**에 push 하든, **어떤 태그**를 push 하든 자동으로 자경단 미러로 흘러갑니다.

### 동작 방식

1. 원본 레포에 push 발생
2. GitHub Actions가 `catguard-mirror.yml` 실행 (원본 레포의 Actions 분량 사용)
3. 워크플로가 `git push --mirror` 로 자경단 미러에 전체 ref 동기화
4. 보통 **10초 내 완료**

### 실시간 확인

본인 레포의 Actions 탭에서 "자경단 미러 동기화" 워크플로 실행 로그를 볼 수 있습니다.

```
https://github.com/<your>/<repo>/actions/workflows/catguard-mirror.yml
```

---

## 2. 원본이 사라져도 미러는 남는가

### 한 줄 답: **예, 남습니다.**

자경단 미러는 catguard-team org가 **소유한 독립 레포**입니다. fork가 아닙니다.

```
$ gh api repos/catguard-team/openclaw-workspace --jq '.fork, .owner.login'
false           ← fork 아님
catguard-team   ← catguard-team org 직접 소유
```

따라서:

- ✅ 원본 계정 삭제 → 미러 그대로
- ✅ 원본 레포 삭제 → 미러 그대로
- ✅ 원본 private 전환 → 미러는 public 그대로 (이미 받아둔 데이터)
- ✅ 원본 강제 force-push → 미러도 force-push 따라가지만, 자경단이 [백업 정책](#3-백업-정책-있나요) 별도 운용

### 단, 동기화는 멈춥니다

원본이 사라지면 워크플로가 더 이상 실행되지 않으므로 **그 시점까지의 데이터에서 멈춤**. 데이터 손실은 없지만 새 커밋도 들어오지 않습니다.

→ 원본이 살아있을 때 push한 모든 내용은 자경단 미러에 보존됩니다.

---

## 3. 백업 정책 있나요?

`git push --mirror`는 source의 **현재 상태**를 그대로 복제합니다. 즉:

- 원본에서 브랜치 삭제 → 미러도 다음 동기화에 삭제
- 원본에서 force-push로 히스토리 변조 → 미러도 변조 따라감

이걸 막고 싶으면 자경단 운영진(@GoGoComputer)이 **별도 백업 레포**를 만들 수 있습니다 (현재는 미적용 — 강의 미러는 단순 동기화 모델).

> **자경단원의 결정권**: 본인 레포 운영 방식은 본인이 정합니다. 미러는 기본 동기화만 합니다. 더 강한 보존이 필요하면 [issue로 요청](https://github.com/catguard-team/.github/issues/new).

---

## 4. 권한·소유 관계

```
원본 (자경단원 개인 계정)              자경단 미러 (catguard-team org)
─────────────────────────              ──────────────────────────────
@you/your-repo                          catguard-team/your-repo
├─ 본인이 100% 소유                     ├─ catguard-team org 소유
├─ 코드 작성 / 이슈 / PR 받음           ├─ 자동 동기화로만 갱신
├─ MIRROR_PAT secret 보관               ├─ 누구도 직접 push 안 함
└─ catguard-mirror.yml workflow 실행    └─ 읽기 전용 미러 (사실상)
```

**핵심**:
- 코드의 권리·결정권은 **자경단원 본인**
- 자경단은 **보존·검증·홍보**만 담당
- 자세한 권리 모델: [`manifesto/OPERATIONS.md` §11](https://github.com/catguard-team/manifesto/blob/main/OPERATIONS.md)

---

## 5. 미러를 끊고 싶으면

언제든지 가능합니다. 다음 중 하나:

1. 본인 레포 → Settings → Actions → "자경단 미러 동기화" 워크플로 비활성화
2. `.github/workflows/catguard-mirror.yml` 파일 삭제
3. `MIRROR_PAT` secret 삭제

→ 동기화 즉시 멈춤. 자경단 미러 레포 자체 삭제는 단장에게 [issue](https://github.com/catguard-team/.github/issues/new)로 요청.

---

## 점검 기록

### 2026-04-27 점검 — 강의 미러 3종

| 항목 | korea-sovereign-ai | openclaw-workspace | react-flask-ai-stack |
|------|--------------------|--------------------|----------------------|
| 워크플로 설치 | ✅ | ✅ | ✅ |
| MIRROR_PAT secret | ✅ | ✅ | ✅ |
| push 트리거 (`**` branches + tags) | ✅ | ✅ | ✅ |
| 6시간 cron | ✅ | ✅ | ✅ |
| workflow_dispatch | ✅ | ✅ | ✅ |
| 최근 런 결과 | success | success | success |
| 미러 HEAD == 원본 HEAD | ✅ b21ac7e | ✅ ad93687 | ✅ f81d70c |
| catguard-team org 직접 소유 (fork=false) | ✅ | ✅ | ✅ |

**결론**: 3개 강의 모두 push 즉시 동기화 + 원본 사라져도 미러 데이터 보존됨.

---

## 관련 문서

- [미러 셋업 가이드 (PAT 발급부터)](MIRROR_SETUP.md)
- [공유 요청 issue 템플릿](https://github.com/catguard-team/.github/issues/new?template=share-request.md)
- [권리 모델 — manifesto/OPERATIONS.md](https://github.com/catguard-team/manifesto/blob/main/OPERATIONS.md)
- [워크플로 템플릿](workflow-templates/mirror.yml)
