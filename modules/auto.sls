include:
  - modules.basic_software
  - modules.system_initializ

sync modules and collect info:
  cmd.run:
    - name: |
        salt-call saltutil.sync_modules
        salt-call info_collect.process