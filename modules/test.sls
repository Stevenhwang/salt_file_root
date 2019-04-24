include:
  - modules.base_confd
  - modules.service_reload


# salt '*' state.apply modules.test pillar='{'content': 'qazwsxedcrfvrt11', 'dest': '/tmp/ppp', 'template': 'template/base.jinja', 'service': 'nginx'}'
