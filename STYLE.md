# 자경단 문서 스타일 가이드

> 자경단 문서는 시민단체 톤을 거부하면서도 GitHub에서 보기 좋아야 한다.
> 이 가이드는 "예쁘게"의 자경단스러운 정의다. 냐-옹.

---

## 색

| 용도 | 색 | hex |
|------|----|------|
| 메인 (라즈베리파이 녹색) | 짙은 녹 | `#5A8A3A` |
| 보조 (베이지) | 따뜻한 회색-베이지 | `#F5E6D3` |
| 강조 (밤색) | 다크 모카 | `#3E2C20` |
| 경고 (자경단 빨강) | 톤 다운 | `#B23A3A` |

> ❌ 절대 안 쓰는 색: 형광 핑크, 네온, 무지개, 그라데이션. 시크하지 않음.

---

## README 표준 구조

모든 레포 README는 다음 골격을 따른다.

````markdown
<div align="center">

[![logo](https://raw.githubusercontent.com/catguard-team/.github/main/assets/logo-main.svg#gh-light-mode-only)](https://github.com/catguard-team)
[![logo](https://raw.githubusercontent.com/catguard-team/.github/main/assets/logo-main-dark.svg#gh-dark-mode-only)](https://github.com/catguard-team)

# 레포명

**한 줄 본질** — 시크하게.

[![Discord](https://img.shields.io/badge/Discord-합류-5865F2?logo=discord&logoColor=white)](https://discord.gg/Dp4pKwns2Y)
[![License](https://img.shields.io/badge/License-MIT-5A8A3A.svg)](./LICENSE)
[![자경단 검증](https://catguard-team.github.io/badges/verified.svg)](https://github.com/catguard-team)

</div>

---

> [!NOTE]
> 이 레포는 자경단의 ○○○를 다룬다. 시간 없으면 [`핵심 문서`](./LINK.md) 한 개만.

(본문)

---

<div align="center">
  <sub>기술 골목의 평화와 자유는 우리가 지킨다 · <strong>냐-옹.</strong></sub>
</div>
````

---

## GitHub Callout (적극 사용)

GitHub은 5종 callout을 지원한다. 자경단 톤에 맞춰 다음과 같이.

```markdown
> [!NOTE]
> 알아두면 좋은 컨텍스트.

> [!TIP]
> 자경단원이 발견한 더 나은 방법.

> [!IMPORTANT]
> 빠뜨리면 안 되는 핵심.

> [!WARNING]
> 잘못하면 새끼고양이가 다친다.

> [!CAUTION]
> 절대 하지 마라. 사고 직전.
```

> [!CAUTION]은 SAFETY 위반·데이터 누출 같은 **돌이킬 수 없는** 케이스에만.

---

## 표 (Table)

- 헤더 행은 항상 있어야 함
- 컬럼 정렬: 텍스트 좌측, 숫자 우측 (`---:`)
- 너무 많은 컬럼 ❌ → 4개 이하 권장. 더 필요하면 분할

```markdown
| 항목 | 무엇 | 단가 |
|------|------|----:|
| 케이스 | 정품 팬 포함 | 18,000 |
```

---

## 이모지 (제한적)

| 영역 | 사용 OK | 사용 ❌ |
|------|---------|---------|
| 카테고리 라벨 | 🛠️ 🐙 🐍 🇰🇷 🍎 🐧 🪟 🌐 📚 | 💖 🌟 🎉 🌈 🦄 |
| 자경단 메타포 | 🐾 🐭 🍯 🛡️ 📡 | (대부분 OK) |
| 상태 | ✅ ❌ ⚠️ 🚨 | 🟢🔴🟡 점 (대신 텍스트 사용) |
| 절대 금지 | — | 🌍 (지구본), ❤️ (하트), 👏 (박수), 🤝 (악수), 👑 (왕관) |

> 한 README에 이모지 5개 이하 권장. 카테고리 표는 예외.

---

## 헤더 위계

- `#` 레포 이름 (한 번만, 보통 hero에서)
- `##` 주요 섹션 (3~7개 권장)
- `###` 하위 섹션
- `####` 거의 안 씀 (필요하면 표로 대체)

> 헤더에 이모지 하나 정도는 OK. 두 개 이상 ❌.

---

## 코드 블록

언어 태그 항상 명시.

````
```bash
# 명령
```
```python
# 코드
```
```yaml
key: value
```
````

코드 안에 비밀 정보 예시 넣을 때는 `<TOKEN>` 같은 placeholder. 진짜처럼 보이는 가짜도 ❌ ([LEAK_CLEANUP §8](https://github.com/catguard-team/manifesto/blob/main/LEAK_CLEANUP.md)).

---

## 링크

- 같은 레포 내: 상대 경로 `[X](./PATH.md)`
- 다른 자경단 레포: 절대 경로 `https://github.com/catguard-team/<repo>/...`
- 외부: 신뢰 출처만 (`.go.kr`, 공식 문서, GitHub, 검증된 오픈소스)

---

## Sign-off

모든 README, 매니페스토 문서는 다음으로 끝맺는다.

```markdown
---

<div align="center">
  <sub>기술 골목의 평화와 자유는 우리가 지킨다 · <strong>냐-옹.</strong></sub>
</div>
```

운영 가이드(LEAK_CLEANUP, RECRUITMENT 등) 끝맺음 변형:

- `누출은 사냥감이다 · 냐-옹.`
- `귀찮지만 우리가 한다 · 냐-옹.`

---

## 적용 우선순위

1. 모든 레포 README (외부 첫 인상)
2. `manifesto/MANIFESTO.md`, `GANGNYANG.md` (정체성)
3. 운영 가이드 (`LEAK_CLEANUP`, `RECRUITMENT`, `PILOT_SELECTION`)
4. 트랙별 핸드북 챕터 (작성 시점에)

---

<div align="center">
  <sub>예쁜 건 부수적이다. 우선은 정확함 · <strong>냐-옹.</strong></sub>
</div>
