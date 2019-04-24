base confd:
  file.managed:
    - name: {{ pillar['dest'] }}
    - source: salt://{{ pillar['template'] }}
    - backup: minion
    - template: jinja
    