{ pkgs ? import <nixpkgs> { }}:

with pkgs;

let
  pythonpkgs = python3.withPackages (ps: with ps; [
    notebook
    pandas
    # pypandoc
  ]);
in
mkShell {
  buildInputs = [ 
    pythonpkgs 
    metabase # PowerBI open-source alternative
    pandoc # notebook to pdf
    texlive.combined.scheme-tetex
  ];
}
