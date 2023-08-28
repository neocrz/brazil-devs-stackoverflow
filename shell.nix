{ pkgs ? import <nixpkgs> { }}:

with pkgs;

let
  myEnv = python3.withPackages (ps: with ps; [
    flask
    requests
    flask-sqlalchemy
    wtforms
    python-dotenv
    gunicorn
    psycopg2
    flask-wtf
    flask-login
    flask-bcrypt
    email-validator
    bcrypt
  ]);
in
mkShell {
  buildInputs = [ myEnv ];
}
