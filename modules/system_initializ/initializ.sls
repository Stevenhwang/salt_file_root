disable selinux:
  file.replace:
    - name: /etc/selinux/config
    - pattern: SELINUX=[a-z].*
    - repl: SELINUX=disabled
    - count: 1

  cmd.run:
    - name: setenforce 0
    - onlyif: getenforce | grep Enabled

change histsize:
  file.replace:
    - name: /etc/profile
    - pattern: HISTSIZE=[1-9].*
    - repl: HISTSIZE=20000
    - count: 1

stop and disable postfix:
  service.dead:
    - name: postfix
    - enable: False

set timezone:
  timezone.system:
    - name: Asia/Hong_Kong
    - utc: True

enlarge ulimit:
  file.append:
    - name: /etc/security/limits.conf
    - source: salt://modules/system_initializ/ulimit