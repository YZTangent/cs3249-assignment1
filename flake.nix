{
  description = "techjam";

  inputs = { nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable"; };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages."x86_64-linux";

      pythonEnv = pkgs.python3.withPackages (ps:
        with ps; [
          requests
          pydantic
          pydantic
          jsonschema
          python-dateutil
          typing-extensions
          colorama
          tqdm

          fastapi
          uvicorn
          streamlit
        ]);
      commonPackages = with pkgs; [
        # libGL glibc glib 
        pythonEnv
        ollama
      ];

    in {
      apps.x86_64-linux.default = {
        type = "app";
        program = "${
            (pkgs.writeShellApplication {
              name = "run-app";
              runtimeInputs = commonPackages;
              text = ''
                #!/bin/sh
                ollama serve &
                python app/backend.py &
                streamlit run app/frontend.py
              '';
            })
          }/bin/run-app";
      };

      devShells."x86_64-linux".default = pkgs.mkShell {

        packages = commonPackages;

        shellHook = ''
          echo "Starting Ollama..."
          ollama serve &

          sleep 2

          echo "Ollama started successfully."
          echo "Entering Nix shell..."

          cleanup_ollama_on_exit() {
            echo "Exiting Nix shell. Running cleanup..."
            pkill ollama
            echo "Cleanup complete."
          }

          # Trap the EXIT signal to call the cleanup function
          trap cleanup_ollama_on_exit EXIT
        '';

        # env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        #   pkgs.stdenv.cc.cc.lib
        #   pkgs.libz
        #   pkgs.libGL
        #   pkgs.glibc
        #   pkgs.glib
        # ];
      };
    };
}
