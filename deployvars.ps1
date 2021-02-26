$envvars = (get-content "${PSScriptRoot}/instance/production.env") -join ' ' -replace '  ', ' '
ssh -t dokku@asdf.simonmartineau.dev config:set projects-api $envvars
