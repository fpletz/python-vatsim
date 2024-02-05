{
  description = "VATSIM python module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    poetry2nix = {
      url = "github:fpletz/poetry2nix/ruff-watchfiles-prevent-ifd";
      inputs = {
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs = inputs:
  inputs.flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [
      "x86_64-linux"
      "aarch64-linux"
    ];

    perSystem = { self, pkgs, system, config, lib, ... }: let
      pkgs' = pkgs.extend(inputs.poetry2nix.overlays.default);
      overrides = pkgs'.poetry2nix.overrides.withDefaults(final: prev: {});
      python-vatsim = pkgs'.poetry2nix.mkPoetryApplication {
        inherit overrides;
        python = pkgs'.python311;
        projectDir = pkgs'.poetry2nix.cleanPythonSources { src = ./.; };
      };
      python-vatsim-dev = pkgs'.poetry2nix.mkPoetryEnv {
        inherit overrides;
        python = pkgs'.python311;
        pyproject = ./pyproject.toml;
        poetrylock = ./poetry.lock;
        extraPackages = ps: [ ps.ipython ];
      };
    in {
      packages = {
        default = python-vatsim;
        inherit python-vatsim;
      };

      formatter = pkgs.nixpkgs-fmt;

      devShells.default = python-vatsim-dev.env.overrideAttrs (oldAttrs: {
        nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
          pkgs'.nil
          pkgs'.poetry
          pkgs'.nodejs  # for pyright
        ];
        shellHook = ''
          export POETRY_VIRTUALENVS_IN_PROJECT=true
          export PYTHONPATH=${python-vatsim-dev}/${python-vatsim-dev.sitePackages}
        '';
      });
    };
  };
}
