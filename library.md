---
layout: page
title: Markdown Library
description: Notes and references authored in Markdown, rendered directly on GitHub Pages
---

<!-- markdownlint-disable MD033 -->

Notes and references authored in Markdown — rendered directly from the `md/`
folder on GitHub Pages.

<ul class="md-library">
{% assign notes = site.pages | sort: "path" %}
{% for note in notes %}
  {% if note.path contains "md/" %}
  <li><a href="{{ site.baseurl }}{{ note.url }}">{{ note.path | remove: "md/" | remove: ".md" }}</a></li>
  {% endif %}
{% endfor %}
</ul>
