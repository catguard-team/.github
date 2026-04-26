# 자경단 미러 셋업 가이드

> 본인 레포를 자경단에 미러링할 때 따라하는 단계별 가이드. 막히면 디스코드 #도와줘 채널에 한 줄.

이 가이드는 **단장(@GoGoComputer)이 미러를 만들어준 다음** 자동 동기화를 켜는 과정입니다. 자료 공유 요청은 [share-request issue](https://github.com/catguard-team/.github/issues/new?template=share-request.md)로 먼저.

> ⚠️ **왜 SSH deploy key가 아닌 PAT 인가요?**
> 자경단 org는 enterprise 정책상 deploy key가 차단되어 있습니다. 그래서 **fine-grained Personal Access Token** 방식을 씁니다. 토큰은 이 미러 레포 한 곳에만 권한을 주므로 SSH deploy key와 보안 수준이 사실상 같습니다.

---

## 0. 준비물

- [ ] 본인의 **원본 레포** (예: `your-name/your-repo`)
- [ ] 단장이 만들어 준 **자경단 미러 레포** (예: `catguard-team/your-repo`)

미러 레포가 없으면 [share-request](https://github.com/catguard-team/.github/issues/new?template=share-request.md)부터.

---

## 1. Fine-grained PAT 발급

1. GitHub 우상단 프로필 → **Settings** → 좌측 맨 아래 **Developer settings**
2. **Personal access tokens** → **Fine-grained tokens** → **Generate new token**
3. 다음과 같이 입력:
   - **Token name**: `catguard-mirror-{레포명}`
   - **Expiration**: 1년 (또는 원하는 기간)
   - **Resource owner**: `catguard-team` 선택 (드롭다운에 자경단이 보여야 함 — 안 보이면 단장에게 멤버 초대 요청)
   - **Repository access**: **Only select repositories** → 본인 미러 레포 1개만 선택
   - **Permissions** → **Repository permissions**:
     - **Contents**: **Read and write** ✅ (필수)
     - 나머지는 그대로 No access
4. **Generate token** 클릭
5. 화면에 뜬 `github_pat_...` 토큰을 **즉시 복사** (창 닫으면 다시 못 봄)

> 토큰 승인 대기 중이라고 나오면, 단장이 org admin으로서 승인해야 합니다. 디스코드에 한 줄.

---

## 2. PAT를 원본 레포 secret에 등록

이건 **본인 원본 레포** (catguard-team이 아닌 본인 계정)에서.

### 방법 A — 웹

1. `https://github.com/your-name/your-repo` → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. 입력:
   - **Name**: `MIRROR_PAT` (정확히 이 이름, 대소문자 구분)
   - **Secret**: 1단계에서 복사한 `github_pat_...` 토큰 통째로
4. **Add secret**

### 방법 B — gh CLI

```bash
gh secret set MIRROR_PAT --repo your-name/your-repo
# 프롬프트에 토큰 붙여넣고 Enter
```

---

## 3. mirror.yml workflow 추가

원본 레포 루트에서:

```bash
mkdir -p .github/workflows
curl -L https://raw.githubusercontent.com/catguard-team/.github/main/workflow-templates/mirror.yml \
  -o .github/workflows/catguard-mirror.yml
```

`.github/workflows/catguard-mirror.yml`을 에디터로 열어 **한 줄**만 수정:

```yaml
MIRROR: catguard-team/your-repo   # ← 본인 미러 경로
```

저장하고 push:

```bash
git add .github/workflows/catguard-mirror.yml
git commit -m "자경단 미러 동기화 workflow 추가"
git push
```

push와 동시에 워크플로우가 첫 동기화를 시작합니다.

---

## 4. 첫 동기화 확인

1. 원본 레포 → **Actions** 탭
2. **자경단 미러 동기화** 워크플로우 클릭
3. 1~2분 후 ✅ 초록 체크. 미러 레포에 본인 코드가 보이면 끝.

이후로는 push할 때마다 즉시 미러로 반영됩니다. push가 한동안 없어도 6시간마다 안전망으로 한 번 더 돕니다. 수동으로도 **Run workflow** 버튼으로 언제든 돌릴 수 있습니다.

---

## 5. 미러 README 헤더 (단장이 처리)

미러 README 상단의 안내 문구는 단장이 미러 생성 시 [`templates/MIRROR_README_HEADER.md`](./templates/MIRROR_README_HEADER.md)로 박아둡니다. 원작자가 직접 손댈 필요 없음.

---

## 막혔을 때

| 증상 | 확인할 것 |
|------|-----------|
| Actions ❌ "Authentication failed" 또는 403 | PAT의 **Contents: Read and write** 권한 확인. PAT가 만료됐거나 미러 레포가 access 목록에 없을 수 있음. |
| Actions ❌ "MIRROR_PAT not found" | 원본 레포 secret 이름이 정확히 `MIRROR_PAT`인지 확인. |
| Actions ❌ "remote rejected" / "non-fast-forward" | `git push --mirror`는 강제 동기화라 정상적으로는 안 나는 에러. 미러 레포에 누가 직접 커밋했나 확인. |
| 미러 레포가 비어있음 | 원본 레포에 커밋이 있는지, 워크플로우가 실제 실행됐는지 Actions 탭 확인. |
| Resource owner 드롭다운에 catguard-team이 안 보임 | 단장에게 org 멤버 초대 요청. |
| 그 외 | 디스코드 #도와줘 채널에 Actions 로그 스크린샷. |

---

## 6. 다 끝나면

- 디스코드 #공지에 "미러 셋업 완료 🐾" 한 줄 자랑
- 원본 레포 README 상단에 자경단 검증 배지(선택):

```markdown
[![자경단 검증](https://img.shields.io/badge/%EC%9E%90%EA%B2%BD%EB%8B%A8-VERIFIED-8b7355)](https://github.com/catguard-team/your-repo)
```

수고하셨습니다. **냐-옹.**
