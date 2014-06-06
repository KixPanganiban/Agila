#!/usr/bin/coffee
# Simple script to compile Jade files (needed for locals)
fs = require 'fs'
path = require 'path'
jade = require 'jade'
wrench = require 'wrench'
argv = require('optimist').argv
crypto = require 'crypto'

config = JSON.parse(fs.readFileSync('config.json', 'utf8'))

inputFname = argv.in
outputFname = argv.out
env = argv.env ? 'dev'

basename = path.basename(inputFname)


getProjectCoffeeFiles = (project) ->
  files = (file.replace(/\.coffee$/, '.js') for file in wrench.readdirSyncRecursive("src/assets/#{project}/js") when file.match(/\.coffee$|\.js$/))

  ("/assets/#{project}/js/#{file}" for file in files)

if basename in ['index.jade', 'typing.jade']
  # Library includes
  if basename == 'index.jade'
    # List all JS files for all the projects
    projects = config.mainProjects
    projectJS = []
    for project in projects
      projectJS.push(getProjectCoffeeFiles(project)...)

    project = 'main'
  else if basename == 'typing.jade'
    project = 'typing'
    projectJS = getProjectCoffeeFiles('typing')


  # Shared includes
  sharedJS = config.js.shared[project]
  if sharedJS == '*'
    # Include everything under shared
    sharedJS = getProjectCoffeeFiles 'shared'
  else
    sharedJS = ("/assets/shared/js/#{file}" for file in sharedJS)

else
  projectJS = []

input = fs.readFileSync inputFname
fn = jade.compile(input,
  filename: 'includes/scripts.jade' # We want the include path to be relative to includes
)

# Cache busting function
cacheBust = (path) -> 
  if /^(?:https?)?\/\//.exec(path)
    return path

  # Find the original path
  if path[0] == '/'
    full_path = "src/#{path[1..]}"
  else
    full_path = "#{path.dirname(inputFname)}/#{path}"

  unless fs.existsSync(full_path)
    if /html$/.exec(full_path)
      full_path = full_path[...-4] + 'jade'
    else if /css$/.exec(full_path)
      full_path = full_path[...-3] + 'scss'
      unless fs.existsSync(full_path)
        full_path = full_path[...-4] + 'less'
    else if /js$/.exec(full_path)
      full_path = full_path[...-2] + 'coffee'
 
  # Get hash
  hash = crypto.createHash 'md5'
  contents = fs.readFileSync(full_path)
  hash.update(contents)
  hashed = hash.digest('hex')

  # Start busting!
  if env == 'dev'
    "#{path}?hash=#{hashed[..7]}"
  else
    [base..., ext] = path.split('.')
    base.concat(["__#{hashed[..7]}_brown_", ext]).join('.') # Hash browns!


fs.writeFileSync(outputFname, fn(
  doctype: 'html'
  config: config
  project: project
  projectJS: projectJS
  sharedJS: sharedJS
  env: env
  cacheBust: cacheBust
))
