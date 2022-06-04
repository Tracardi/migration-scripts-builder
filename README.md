# Tracardi migration script builder 
#### v0.1.0
This is a simple Python-based console app for constructing Elasticsearch 
migration scripts for Tracardi.

# Setup
In the repo's directory, run ```pip install -r requirements.txt```

In environmental variables, include variable `ELASTIC_HOST`, containing
Elasticsearch instance IP, port and username with password if needed.

# Usage
After setup, run `main.py`. Provide the codenames of both old and new Tracardi
version (just hit Enter if the previous version has no codename, at least one
is required though).
Provide a name for the migration data file, then `<given-name>.json` file
should be created in the `tmp` directory. Move created file to Tracardi and let
Tracardi Migration Engine handle the rest for you. Script has to be specified
though, since it arrives in form:
```
// some commented line of code;\n
// other commented line of code;\n
```
`//` have to be removed wherever you find it reasonable for the line to
be executed (if casting or re-assigning is required).
