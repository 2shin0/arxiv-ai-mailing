import glob, re

for path in glob.glob("ALL/*.md") + glob.glob("LLM/*.md"):
    if path.endswith("index.md"):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "{% raw %}" in content:
        print(f"Skip (already patched): {path}")
        continue
    # front matter가 있는 경우와 없는 경우 모두 처리
    if content.startswith("---"):
        new_content = re.sub(
            r"(^---\n.*?\n---\n)",
            r"\1\n{% raw %}\n",
            content, count=1, flags=re.DOTALL
        )
    else:
        new_content = "{% raw %}\n" + content
    new_content += "\n{% endraw %}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Patched: {path}")