# catguard-bot — 자경단 디스코드 봇 v1

> 디스코드 명령 4종으로 자경단 운영 자동화. 단장 KakaoTalk 봇 경험 기반.
> 본 스캐폴드는 추후 별도 레포 `catguard-team/catguard-bot`으로 분리 예정.

---

## 명령

| 명령 | 누가 | 결과 |
|------|------|------|
| `!신청` | 새끼고양이/보호자 | 비공개 신청 양식 (단장 DM으로 전달) |
| `!자경단신청` | 자원봉사자 | 자경단원 합류 절차 안내 + 디스코드 역할 부여 후보 |
| `!꿀잠 <키워드>` | 누구나 | `kkulzam-spot` 레포에서 grep 검색 → 상위 5건 링크 |
| `!강령 <번호>` | 누구나 | `manifesto/GANGNYANG.md` 해당 조항 인용 |

---

## 빠른 시작

```bash
cd .github/bot
cp .env.example .env  # DISCORD_TOKEN, GITHUB_PAT 입력
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

---

## 환경 변수

| 변수 | 무엇 |
|------|------|
| `DISCORD_TOKEN` | 디스코드 봇 토큰 (Developer Portal에서 발급) |
| `GITHUB_PAT` | `kkulzam-spot` read 권한만 (fine-grained) |
| `MENTOR_DM_USER_ID` | 신청 DM 받을 단장 디스코드 user ID |

---

## 디스코드 봇 셋업

1. https://discord.com/developers/applications → **New Application** "catguard-bot"
2. **Bot** 탭 → **Add Bot** → **Reset Token** → `DISCORD_TOKEN` 복사
3. **Privileged Gateway Intents**: `MESSAGE CONTENT INTENT` 활성화
4. **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Read Message History`, `Use Slash Commands`, `Add Reactions`
5. 생성된 URL로 자경단 디스코드에 봇 초대

---

## 보안

- `DISCORD_TOKEN`·`GITHUB_PAT`은 **절대 commit 금지**. `.env`는 `.gitignore`.
- 누출 시 [LEAK_CLEANUP.md](https://github.com/catguard-team/manifesto/blob/main/LEAK_CLEANUP.md) 즉시 실행.
- `!신청` 명령으로 받은 새끼고양이 정보는 **단장 DM으로만** 전달, 채널·로그·DB 어디에도 저장하지 않음 ([SAFETY.md](https://github.com/catguard-team/manifesto/blob/main/SAFETY.md)).

---

## 다음 단계 (v2 후보)

- `!회고` — 4주 파일럿 회고 양식 자동 생성
- `!공유요청` — 자료 공유 요청 issue 자동 생성
- 슬래시 명령 (`/`) 마이그레이션
- 자경단원 가입·이탈 자동 디스코드 역할 갱신
