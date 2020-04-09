import yaml

def GenerateConfig(context):
  """Generate configuration."""
  container_manifest = yaml.safe_load(context.imports[context.properties['container_manifest']])
  env_variables = yaml.safe_load(context.imports['env_variables'])
  env_variables.extend([
    {
      'name': 'XMPP_SERVER',
      'value': 'jitsi-xmpp.us-central1-a.c.{0}.internal'.format(context.env['project'])
    },
    {
      'name': 'XMPP_BOSH_URL_BASE',
      'value': 'http://jitsi-xmpp.us-central1-a.c.{0}.internal:5280'.format(context.env['project'])
    },
    {
      'name': 'JVB_AUTH_PASSWORD',
      'value': context.properties['jvb_password']
    },
    {
      'name': 'JICOFO_AUTH_PASSWORD',
      'value': context.properties['jicofo_password']
    }
  ])
  container_manifest['spec']['containers'][0]['env'] = env_variables

  resources = []
  resources.append({
    'name': context.env['name'] + '-template',
    'type': 'compute.v1.instanceTemplate',
    'properties': {
      'properties': {
        'zone': 'us-central1-a',
        'machineType': context.properties.get('machineType', 'f1-micro'),
        'metadata': {
          'items': [{
            'key': 'gce-container-declaration',
            'value': yaml.safe_dump(container_manifest)
          }]
        },
        'disks': [{
          'deviceName': 'boot',
          'type': 'PERSISTENT',
          'boot': True,
          'autoDelete': True,
          'initializeParams': {
            'diskSizeGb': '10',
            'sourceImage': 'projects/cos-cloud/global/images/family/cos-stable'
          }
        }],
        'scheduling': {
          'preemptible': True
        },
        'networkInterfaces': [{
          'network': 'global/networks/default',
          'subnetwork': 'regions/us-central1/subnetworks/default',
          'accessConfigs': [{
            'name': 'external-nat',
            'type': 'ONE_TO_ONE_NAT'
          }]
        }],
        'tags': {
          'items': context.properties['tags']
        }
      }
    }
  })
  resources.append({
    'type': 'compute.v1.instanceGroupManagers',
    'name': context.env['name'] + '-group',
    'metadata': {
      'dependsOn': [
        context.env['name'] + '-template'
      ]
    },
    'properties': {
      'instanceTemplate': ''.join(['projects/', context.env['project'], '/global/instanceTemplates/', context.env['name'] + '-template']),
      'name': context.env['name'] + '-group',
      'targetSize': 1,
      'zone': 'us-central1-a'
    }
  })

  return {'resources': resources}
