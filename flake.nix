{
  description = "VATSIM python module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    flake-parts.url = "github:hercules-ci/flake-parts";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem =
        { pkgs, ... }:
        let
          pkgs' = pkgs.extend (inputs.poetry2nix.overlays.default);
          overrides = pkgs'.poetry2nix.overrides.withDefaults (
            final: prev: {
              urllib3 = prev.urllib3.overridePythonAttrs (attrs: {
                nativeBuildInputs = attrs.nativeBuildInputs ++ [ final.hatch-vcs ];
              });
            }
          );
          python-vatsim = pkgs'.poetry2nix.mkPoetryApplication {
            inherit overrides;
            projectDir = pkgs'.poetry2nix.cleanPythonSources { src = ./.; };
          };
          python-vatsim-dev = pkgs'.poetry2nix.mkPoetryEnv {
            inherit overrides;
            pyproject = ./pyproject.toml;
            poetrylock = ./poetry.lock;
          };
        in
        {
          packages = {
            default = python-vatsim;
            inherit python-vatsim;
          };

          formatter = pkgs.nixfmt-rfc-style;

          devShells.default = python-vatsim-dev.env.overrideAttrs (oldAttrs: {
            nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
              pkgs'.poetry
              pkgs'.nodejs # for pyright
            ];
            shellHook = ''
              export POETRY_VIRTUALENVS_IN_PROJECT=true
              export PYTHONPATH=${python-vatsim-dev}/${python-vatsim-dev.sitePackages}
            '';
          });
        };
    };
}
