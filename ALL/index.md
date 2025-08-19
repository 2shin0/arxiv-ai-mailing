---
layout: default
title: "전체 AI 논문 다이제스트"
---

# 🔬 전체 AI 논문 다이제스트

AI 전 분야의 최신 연구 동향을 매일 요약해서 제공합니다.

## 📅 최근 다이제스트

{% for post in site.pages %}
  {% if post.path contains 'ALL/' and post.path != 'ALL/index.md' %}
- [{{ post.path | replace: 'ALL/', '' | replace: '.md', '' }}]({{ post.url }})
  {% endif %}
{% endfor %}

---

[← 메인 페이지로 돌아가기](../)
