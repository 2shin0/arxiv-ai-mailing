---
layout: default
title: "전체 AI 논문 다이제스트"
permalink: /ALL/
---

# 전체 AI 논문 다이제스트

arXiv cs.AI 카테고리의 모든 AI 논문들의 일별 다이제스트입니다.

## 최근 다이제스트

{% assign all_files = site.static_files | where_exp: "file", "file.path contains '/ALL/'" | where_exp: "file", "file.name contains '.md'" | where_exp: "file", "file.name != 'index.md'" | sort: "name" | reverse %}

{% for file in all_files %}
  {% assign date_string = file.name | remove: ".md" %}
  {% assign year = date_string | slice: 0, 4 %}
  {% assign month = date_string | slice: 5, 2 %}
  {% assign day = date_string | slice: 8, 2 %}
- [{{ year }}년 {{ month }}월 {{ day }}일]({{ date_string }}) - {{ file.modified_time | date: "%Y-%m-%d" }}
{% endfor %}

[← 메인으로 돌아가기]({{ site.baseurl }}/)