{
  description = "VATSIM python module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:adisbladis/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = import inputs.systems;

      perSystem =
        { pkgs, lib, ... }:
        let
          workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

          overlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel";
          };

          python = pkgs.python313;

          pythonSet =
            (pkgs.callPackage inputs.pyproject-nix.build.packages {
              inherit python;
            }).overrideScope
              (
                lib.composeManyExtensions [
                  inputs.pyproject-build-systems.overlays.wheel
                  overlay
                  (final: prev: {
                    vatsim = prev.vatsim.overrideAttrs (old: {
                      buildInputs = (old.buildInputs or [ ]) ++ [ final.editables ];
                    });
                  })
                ]
              );
        in
        {
          formatter = pkgs.nixfmt;

          packages = {
            default = pythonSet.mkVirtualEnv "python-vatsim-env" workspace.deps.default;
          };

          devShells = {
            impure = pkgs.mkShell {
              packages = [
                python
                pkgs.uv
              ];
              shellHook = ''
                unset PYTHONPATH
              '';
            };

            default =
              let
                editableOverlay = workspace.mkEditablePyprojectOverlay {
                  root = "$REPO_ROOT";
                };
                editablePythonSet = pythonSet.overrideScope editableOverlay;
                virtualenv = editablePythonSet.mkVirtualEnv "python-vatsim-dev-env" workspace.deps.all;
              in
              pkgs.mkShell {
                packages = [
                  virtualenv
                  pkgs.uv
                  pkgs.nodejs # FIXME: for pyright
                ];
                env = {
                  UV_NO_SYNC = "1";
                  UV_PYTHON = editablePythonSet.python.interpreter;
                  UV_PYTHON_DOWNLOADS = "never";
                };
                shellHook = ''
                  unset PYTHONPATH
                  export REPO_ROOT=$(git rev-parse --show-toplevel)
                '';
              };
          };
        };
    };
}
