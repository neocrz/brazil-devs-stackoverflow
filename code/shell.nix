{ pkgs ? import <nixpkgs> { }}:

with pkgs;

let
  pythonpkgs = python3.withPackages (ps: with ps; [
    notebook
    pandas
    sqlalchemy
  ]);
in
mkShell {
  buildInputs = [
    pythonpkgs 
    metabase # PowerBI open-source alternative
  ];
}
