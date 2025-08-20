---
layout: default
title: "LLM 논문 다이제스트"
permalink: /LLM/
---

# LLM 논문 다이제스트

LLM(Large Language Model) 관련 논문들의 일별 다이제스트입니다.

## 최근 다이제스트

{% assign llm_files = site.static_files | where_exp: "file", "file.path contains '/LLM/'" | where_exp: "file", "file.name contains '.md'" | where_exp: "file", "file.name != 'index.md'" | sort: "name" | reverse %}

{% for file in llm_files %}
  {% assign date_string = file.name | remove: ".md" %}
  {% assign year = date_string | slice: 0, 4 %}
  {% assign month = date_string | slice: 5, 2 %}
  {% assign day = date_string | slice: 8, 2 %}
- [{{ year }}년 {{ month }}월 {{ day }}일]({{ date_string }}) - {{ file.modified_time | date: "%Y-%m-%d" }}
{% endfor %}

[← 메인으로 돌아가기]({{ site.baseurl }}/)
