from openai import OpenAI
from .config import OPENAI_API_KEY, LLM_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)

def rewrite_query_for_search(user_query: str) -> str:
    prompt = f"""
あなたは医学症例検索用の質問変換アシスタントです。
以下の指示に忠実に従い、ユーザーの曖昧な質問を、医学文書検索に最適な症例風の一文に変換してください。

制約:
- 元の入力に含まれていない情報を加えない
- 年齢・性別・症状等は原文から抽出した範囲に限定
- 出力は簡潔で明確な自然文1文のみ

例:
ユーザー:「高校生で肺炎になった人」
出力: 15〜18歳の患者が肺炎と診断された。

変換対象:「{user_query}」
"""
    res = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return res.choices[0].message.content.strip()

def summarize_text(text: str) -> str:
    prompt = f"""
以下は医療診断書/症例報告の一部です。患者の年齢・性別・症状・診断・経過を含め、簡潔に日本語で要約してください。

--- 原文 ---
{text}
"""
    res = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return res.choices[0].message.content.strip()
