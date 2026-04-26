"""catguard-bot v1 — 자경단 디스코드 봇.

명령 4종:
- !신청 — 새끼고양이 신청 (단장 DM으로 전달, 채널·로그 저장 ❌)
- !자경단신청 — 자원봉사 합류 안내
- !꿀잠 <키워드> — kkulzam-spot 검색
- !강령 <번호> — 행동강냥 조항 인용

SAFETY.md 우선. 신청 정보는 메모리에만, persist 금지.
"""
from __future__ import annotations

import os
import re
import textwrap
from typing import Iterable

import discord
import httpx
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GITHUB_PAT = os.environ.get("GITHUB_PAT", "")
MENTOR_DM_USER_ID = int(os.environ.get("MENTOR_DM_USER_ID", "0"))

GH_API = "https://api.github.com"
KKULZAM_REPO = "catguard-team/kkulzam-spot"
MANIFESTO_RAW = (
    "https://raw.githubusercontent.com/catguard-team/manifesto/main/GANGNYANG.md"
)

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


# ──────────────────────────────────────────────────────────────────────
# 유틸
# ──────────────────────────────────────────────────────────────────────

async def _gh_search(keyword: str, limit: int = 5) -> list[dict]:
    """kkulzam-spot 레포에서 키워드 검색."""
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_PAT:
        headers["Authorization"] = f"Bearer {GITHUB_PAT}"
    params = {"q": f"{keyword} repo:{KKULZAM_REPO}"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{GH_API}/search/code", headers=headers, params=params)
        r.raise_for_status()
        return r.json().get("items", [])[:limit]


async def _fetch_gangnyang() -> str:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(MANIFESTO_RAW)
        r.raise_for_status()
        return r.text


def _extract_article(text: str, n: int) -> str | None:
    """행동강냥 N조 본문 추출. `## 제N조` 패턴 가정."""
    pattern = rf"##\s*제\s*{n}\s*조[^\n]*\n(.*?)(?=\n##|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        return None
    body = m.group(1).strip()
    # 1500자 제한 (디스코드 메시지 안전선)
    if len(body) > 1500:
        body = body[:1500] + "…"
    return body


# ──────────────────────────────────────────────────────────────────────
# 명령
# ──────────────────────────────────────────────────────────────────────

@bot.event
async def on_ready() -> None:
    print(f"🐾 catguard-bot ready as {bot.user}")


@bot.command(name="신청")
async def apply_kitten(ctx: commands.Context) -> None:
    """새끼고양이 신청 — 단장 DM으로만 전달."""
    if ctx.guild is not None:
        await ctx.message.delete()  # 공개 채널에 흔적 남기지 않음
        try:
            await ctx.author.send(
                "신청은 DM으로만 받습니다. 다음을 DM으로 보내주세요:\n"
                "1) 어떤 어려움 (구체적으로 1~2문장)\n"
                "2) 가능한 시간대 (주 1회 30분~1시간)\n"
                "3) 미성년자면 보호자 동의 여부\n\n"
                "받은 정보는 단장(DM)으로만 전달되고, 어디에도 저장되지 않습니다."
            )
        except discord.Forbidden:
            await ctx.send(
                f"{ctx.author.mention} DM이 막혀있습니다. 디스코드 설정에서 DM 허용 후 다시.",
                delete_after=10,
            )
        return

    # DM에서 들어옴 → 단장에게 전달
    if MENTOR_DM_USER_ID == 0:
        await ctx.send("⚠️ 봇 설정 오류 (MENTOR_DM_USER_ID 미설정). 단장에게 직접 연락 부탁.")
        return

    mentor = await bot.fetch_user(MENTOR_DM_USER_ID)
    excerpt = ctx.message.content[:1000]
    await mentor.send(
        f"📩 **새 새끼고양이 신청** (from {ctx.author} / id={ctx.author.id})\n"
        f"```\n{excerpt}\n```\n"
        f"→ SAFETY.md §2 보호자 동의 + PILOT_SELECTION.md §1 기준 확인."
    )
    await ctx.send("✅ 단장에게 전달했습니다. 답변까지 며칠 걸릴 수 있습니다. 냐-옹.")


@bot.command(name="자경단신청")
async def apply_volunteer(ctx: commands.Context) -> None:
    """자원봉사 합류 안내."""
    msg = textwrap.dedent("""
        🐾 **자경단 합류 절차**

        1. https://github.com/catguard-team — 매니페스토·행동강(綱)냥(領) 10조 읽기
        2. 본인이 자경단이라고 선언 — 끝

        **자격 심사·가입비·의무 시간 없습니다.** 그만둘 자유 항상 있습니다.

        합류 후:
        - 본인이 한 일 한 줄 적기 (안 적어도 활동은 활동)
        - 디스코드 #그루밍 채널에서 그루밍(코드 리뷰) 환영

        냐-옹.
    """).strip()
    await ctx.send(msg)


@bot.command(name="꿀잠")
async def search_tips(ctx: commands.Context, *, keyword: str = "") -> None:
    """kkulzam-spot 레포 검색."""
    if not keyword:
        await ctx.send("`!꿀잠 <키워드>` 형식으로. 예: `!꿀잠 vscode 한글`")
        return

    try:
        items = await _gh_search(keyword)
    except Exception as e:
        await ctx.send(f"⚠️ 검색 실패: {e}")
        return

    if not items:
        await ctx.send(
            f"`{keyword}` 관련 꿀잠 스팟이 아직 없네요.\n"
            f"본인이 발견했으면 PR 환영: https://github.com/{KKULZAM_REPO}"
        )
        return

    lines = [f"🍯 **`{keyword}` 꿀잠 스팟 (상위 {len(items)}개)**"]
    for it in items:
        path = it["path"]
        url = it["html_url"]
        lines.append(f"- [{path}]({url})")
    await ctx.send("\n".join(lines))


@bot.command(name="강령")
async def quote_article(ctx: commands.Context, n: str = "") -> None:
    """행동강냥 N조 인용."""
    if not n.isdigit() or not (1 <= int(n) <= 10):
        await ctx.send("`!강령 1`~`!강령 10` 중 하나. 행동강냥은 10조까지.")
        return

    try:
        text = await _fetch_gangnyang()
    except Exception as e:
        await ctx.send(f"⚠️ GANGNYANG.md 가져오기 실패: {e}")
        return

    body = _extract_article(text, int(n))
    if body is None:
        await ctx.send(
            f"제{n}조를 찾지 못했습니다. "
            f"https://github.com/catguard-team/manifesto/blob/main/GANGNYANG.md 직접 확인."
        )
        return

    await ctx.send(f"📜 **행동강(綱)냥(領) 제{n}조**\n>>> {body}")


# ──────────────────────────────────────────────────────────────────────
# 시작
# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
