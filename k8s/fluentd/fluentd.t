# Load values
{{ load_module('legion.template_plugins.file_change_monitor', filepath='/opt/config/values.yaml', is_yaml_file=True, var_name='cfg') }}

# Load secrets
{{ load_module('legion.template_plugins.file_change_monitor', filepath='/opt/secrets/aws.yaml', is_yaml_file=True, var_name='aws_secrets') }}

# Receive
<source>
  @type http
  port 80
</source>

# Processing rules
# docs: https://github.com/fluent/fluent-plugin-s3

{% for tag, tagcfg in cfg.specific.iteritems() %}
# Section for tag {{ tag }}
<match *>
  @type s3
  # Connection
  aws_key_id {{ aws_secrets.aws_key_id }}
  aws_sec_key {{ aws_secrets.aws_sec_key }}

  s3_bucket {{ cfg.common.bucket }}
  s3_region {{ cfg.common.region }}

  # Storing
  path {{ tagcfg.path }}
  time_slice_format {{ tagcfg.time_slice_format }}
  time_slice_wait {{ tagcfg.time_slice_wait }}
  s3_object_key_format {{ tagcfg.s3_object_key_format }}
  utc
  store_as {{ tagcfg.store_as }}

  # Buffering
  <buffer tag,time>
    @type file
    path /var/log/fluent/s3
    timekey {{ tagcfg.timekey }}
    timekey_wait {{ tagcfg.timekey_wait }}
    timekey_use_utc true
  </buffer>
  <format>
    @type {{ tagcfg.format_type }}
  </format>
</match>
{% endfor %}

{% if cfg is defined %}
# Default
<match *>
  @type s3
  # Connection
  aws_key_id {{ aws_secrets.aws_key_id }}
  aws_sec_key {{ aws_secrets.aws_sec_key }}

  s3_bucket {{ cfg.common.bucket }}
  s3_region {{ cfg.common.region }}

  # Storing
  path {{ cfg.default.path }}
  time_slice_format {{ cfg.default.time_slice_format }}
  time_slice_wait {{ cfg.default.time_slice_wait }}
  s3_object_key_format {{ cfg.default.s3_object_key_format }}
  utc
  store_as {{ cfg.default.store_as }}

  # Buffering
  <buffer tag,time>
    @type file
    path /var/log/fluent/s3
    timekey {{ cfg.default.timekey }}
    timekey_wait {{ cfg.default.timekey_wait }}
    timekey_use_utc true
  </buffer>
  <format>
    @type {{ cfg.default.format_type }}
  </format>
</match>
{% endif %}