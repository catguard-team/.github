# 자경단 미러 셋업 가이드

> 본인 레포를 자경단에 미러링할 때 따라하는 단계별 가이드. 처음이어도 따라할 수 있게 만들어 두었습니다. 막히면 디스코드 #도와줘 채널에 한 줄 던지세요.

이 가이드는 **단장(@GoGoComputer)이 미러를 만들어준 다음** 자동 동기화를 켜는 과정을 설명합니다. 자료 공유 요청은 [share-request issue](https://github.com/catguard-team/.github/issues/new?template=share-request.md)로 먼저 보내세요.

---

## 0. 준비물 점검

다음 두 가지가 있어야 진행 가능합니다.

- [ ] 본인의 **원본 레포** (예: `your-name/your-repo`)
- [ ] 단장이 만들어 준 **자경단 미러 레포** (예: `catguard-team/your-repo-by-your-name`)

미러 레포가 아직 없으면 [share-request](https://github.com/catguard-team/.github/issues/new?template=share-request.md)부터 진행하세요.

---

## 1. 동기화용 SSH 키 한 쌍 만들기

원본 → 미러로 GitHub Actions가 push하려면 SSH 키가 필요합니다. 본인 컴퓨터 터미널에서 한 번만 만들면 됩니다.

```bash
# 메일 주소는 본인 GitHub 메일로
ssh-keygen -t ed25519 -C "catguard-mirror" -f ~/.ssh/catguard_mirror -N ""
```

만들어진 두 파일:

- `~/.ssh/catguard_mirror` — **개인 키** (절대 외부 노출 금지. GitHub Actions secret에만 넣음)
- `~/.ssh/catguard_mirror.pub` — **공개 키** (미러 레포의 deploy key로 등록)

---

## 2. 공개 키를 미러 레포에 등록

### 방법 A — 웹에서 (초보자 추천)

1. 미러 레포로 이동: `https://github.com/catguard-team/your-repo-by-your-name`
2. **Settings** 탭 → 좌측 **Deploy keys** → **Add deploy key** 버튼
3. 다음 입력:
   - **Title**: `catguard-mirror-sync`
   - **Key**: 터미널에서 `cat ~/.ssh/catguard_mirror.pub` 실행 결과를 통째로 붙여넣기
   - **Allow write access**: ✅ **체크 필수** (안 하면 push 못 함)
4. **Add key** 클릭

### 방법 B — gh CLI

```bash
gh repo deploy-key add ~/.ssh/catguard_mirror.pub \
  --repo catguard-team/your-repo-by-your-name \
  --title catguard-mirror-sync \
  --allow-write
```

---

## 3. 개인 키를 원본 레포의 secret에 등록

이건 **원본 레포** (catguard-team이 아니라 본인 계정의 레포)에서 합니다.

### 방법 A — 웹

1. 원본 레포로 이동: `https://github.com/your-name/your-repo`
2. **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
3. 다음 입력:
   - **Name**: `MIRROR_DEPLOY_KEY` (정확히 이 이름)
   - **Secret**: 터미널에서 `cat ~/.ssh/catguard_mirror` 실행 결과를 통째로 붙여넣기 (`-----BEGIN ... -----END` 까지 전부)
4. **Add secret** 클릭

### 방법 B — gh CLI

```bash
gh secret set MIRROR_DEPLOY_KEY \
  --repo your-name/your-repo \
  < ~/.ssh/catguard_mirror
```

---

## 4. mirror.yml workflow 추가

원본 레포 루트에서:

```bash
mkdir -p .github/workflows
curl -L https://raw.githubusercontent.com/catguard-team/.github/main/workflow-templates/mirror.yml \
  -o .github/workflows/mirror.yml
```

그리고 `.github/workflows/mirror.yml`을 에디터로 열어 두 줄만 수정:

```yaml
source_repo: "https://github.com/your-name/your-repo.git"
destination_repo: "git@github.com:catguard-team/your-repo-by-your-name.git"
```

저장하고 push:

```bash
git add .github/workflows/mirror.yml
git commit -m "자경단 미러 동기화 workflow 추가"
git push
```

---

## 5. 첫 동기화 수동 실행

자동으로는 6시간마다 돌지만, 첫 번째는 수동으로 실행해서 잘 되는지 봅니다.

1. 원본 레포 → **Actions** 탭
2. 좌측 목록에서 **자경단 미러 동기화** 선택
3. 우측 **Run workflow** 버튼 → 다시 **Run workflow** 클릭
4. 1~2분 후 새로고침. 초록 체크 ✅ 가 뜨면 성공.

미러 레포(`catguard-team/...`)에 가서 본인 코드가 보이면 끝입니다.

---

## 6. 미러 README 헤더 박기 (단장이 처리)

미러 README 상단에 표준 안내문구가 들어갑니다. 이건 단장이 미러 생성 시 [`templates/MIRROR_README_HEADER.md`](./templates/MIRROR_README_HEADER.md)를 채워서 박아둡니다. 원작자가 직접 손댈 필요 없음.

---

## 막혔을 때

| 증상 | 확인할 것 |
|------|-----------|
| Actions 빨간 ❌, "Permission denied (publickey)" | 미러 레포 deploy key의 **Allow write access** 체크 안 됨. 다시 켜기. |
| Actions 빨간 ❌, "MIRROR_DEPLOY_KEY not found" | 원본 레포 secret 이름이 정확히 `MIRROR_DEPLOY_KEY` 인지 확인. 대소문자 구분. |
| 미러 레포가 비어있음 | 원본 레포에 main 브랜치가 있는지 확인. 다른 이름이면 mirror.yml의 `source_branch`/`destination_branch` 수정. |
| 그 외 | 디스코드 #도와줘 채널에 Actions 로그 스크린샷과 함께 한 줄 던지세요. |

---

## 7. 다 끝나면

- 디스코드 #공지 채널에 "미러 셋업 완료 🐾" 한 줄 자랑.
- 원본 레포 README 상단에 자경단 검증 배지 (선택):

```markdown
[![자경단 검증](https://catguard-team.github.io/badges/verified.svg)](https://github.com/catguard-team/your-repo-by-your-name)
```

수고하셨습니다. **냐-옹.**
