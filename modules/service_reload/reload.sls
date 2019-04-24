reload service:
  service.running:
    - name: {{ pillar['service'] }}
    - watch:
      - file: {{ pillar['dest'] }}