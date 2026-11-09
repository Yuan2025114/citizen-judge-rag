"""核對網站中的條文原文是否與 data/articles.json 完全相同。

用法（在專案根目錄執行）：
    python tools/check_quotes.py

規則：每個 <article class="law-quote" data-article="N"> 裡的段落，
必須和 data/articles.json 第 N 條的 paragraphs 逐段相同。有差異就回傳錯誤碼 1。
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = {a["no"]: a["paragraphs"] for a in json.loads((ROOT / "data/articles.json").read_text(encoding="utf-8"))["articles"]}


class QuoteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.quotes, self._cur, self._in_body, self._in_p, self._buf = [], None, False, False, ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "article" and "law-quote" in (a.get("class") or "").split():
            self._cur = {"no": int(a["data-article"]), "paragraphs": []}
        elif self._cur is not None and tag == "div" and "art-body" in (a.get("class") or "").split():
            self._in_body = True
        elif self._in_body and tag == "p":
            self._in_p, self._buf = True, ""

    def handle_data(self, data):
        if self._in_p:
            self._buf += data

    def handle_endtag(self, tag):
        if tag == "p" and self._in_p:
            self._cur["paragraphs"].append(self._buf.strip())
            self._in_p = False
        elif tag == "div" and self._in_body:
            self._in_body = False
        elif tag == "article" and self._cur is not None:
            self.quotes.append(self._cur)
            self._cur = None


def main():
    errors, checked = [], 0
    for path in sorted(ROOT.glob("**/*.html")):
        if "templates" in path.parts:
            continue
        parser = QuoteParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for quote in parser.quotes:
            checked += 1
            if quote["no"] not in DATA:
                errors.append(f"{path.relative_to(ROOT)}：第{quote['no']}條不在資料檔中")
            elif quote["paragraphs"] != DATA[quote["no"]]:
                errors.append(f"{path.relative_to(ROOT)}：第{quote['no']}條的條文與資料檔不同")
    print(f"已檢查 {checked} 則條文引用。")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("全部相同。")


if __name__ == "__main__":
    main()
