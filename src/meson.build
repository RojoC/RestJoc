pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'restjoc')
gnome = import('gnome')

gnome.compile_resources('restjoc',
  'restjoc.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'restjoc.in',
  output: 'restjoc',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

restjoc_sources = [
  '__init__.py',
  'gi_composites.py',
  'main.py',
  'window.py',
  'requestItem.py',
  'argumentItem.py',
  'request.py'
]

install_data(restjoc_sources, install_dir: moduledir)
